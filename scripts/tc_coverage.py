"""TC coverage mapper.

Reads the web TC master sheet from deepcheck_TC.xlsx, extracts every TC_ID with
its category/scenario/priority, then scans tests/ for TC_IDs already referenced
(in param ids or comments) to classify each TC as:
  - automated : a test references the TC_ID and is not skipped
  - skipped   : referenced only by a @pytest.mark.skip test
  - missing   : no reference anywhere

Writes a full mapping to artifacts/tc_coverage.csv and prints a summary.

The workbook has a malformed custom-properties part that breaks openpyxl, so we
load from a sanitized in-memory copy.
"""
import csv
import io
import pathlib
import re
import sys
import zipfile

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
XLSX = ROOT / "deepcheck_TC.xlsx"
SHEET = "Deep check 2.0(웹) v1.0.0"
TESTS_DIR = ROOT / "tests"
OUT = ROOT / "artifacts"
OUT.mkdir(exist_ok=True)

TC_RE = re.compile(r"TC_\d{3}_\d{3}")


def _sanitized_workbook(path: pathlib.Path):
    """openpyxl trips on docProps/custom.xml (empty property name); drop it."""
    buf = io.BytesIO()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in zin.namelist():
            if n == "docProps/custom.xml":
                continue
            data = zin.read(n)
            if n == "[Content_Types].xml":
                data = re.sub(rb"<Override PartName=\"/docProps/custom\.xml\"[^>]*/>", b"", data)
            zout.writestr(n, data)
    buf.seek(0)
    return openpyxl.load_workbook(buf, data_only=True)


def extract_tcs():
    wb = _sanitized_workbook(XLSX)
    ws = wb[SHEET]
    rows = list(ws.iter_rows(min_row=6, values_only=True))
    tcs = []
    cat_a = cat_b = cat_c = ""
    for r in rows:
        a, b, c, tc_id = (r[0], r[1], r[2], r[3])
        if a:
            cat_a = str(a).strip()
        if b:
            cat_b = str(b).strip()
        if c:
            cat_c = str(c).strip()
        if not tc_id or not TC_RE.fullmatch(str(tc_id).strip()):
            continue
        scenario = str(r[5]).strip() if r[5] else ""
        priority = str(r[8]).strip() if len(r) > 8 and r[8] else ""
        tcs.append(
            {
                "tc_id": str(tc_id).strip(),
                "screen": cat_a,
                "group": cat_b,
                "detail": cat_c,
                "scenario": scenario,
                "priority": priority,
            }
        )
    return tcs


def scan_referenced():
    """Map TC_ID -> set of statuses ('test' or 'skip') found in test files."""
    refs: dict[str, set[str]] = {}
    for py in TESTS_DIR.rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        # crude per-test split so we can tell skipped TCs apart
        blocks = re.split(r"(?=^@|^def test_)", text, flags=re.MULTILINE)
        for blk in blocks:
            ids = set(TC_RE.findall(blk))
            if not ids:
                continue
            status = "skip" if ".skip" in blk or ".xfail" in blk else "test"
            for i in ids:
                refs.setdefault(i, set()).add(status)
    return refs


def main():
    tcs = extract_tcs()
    refs = scan_referenced()

    def status_of(tc_id):
        s = refs.get(tc_id)
        if not s:
            return "missing"
        return "automated" if "test" in s else "skipped"

    for tc in tcs:
        tc["status"] = status_of(tc["tc_id"])

    csv_path = OUT / "tc_coverage.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(
            f, fieldnames=["tc_id", "screen", "group", "detail", "priority", "status", "scenario"]
        )
        w.writeheader()
        for tc in tcs:
            w.writerow(tc)

    total = len(tcs)
    by_status = {}
    by_screen = {}
    for tc in tcs:
        by_status[tc["status"]] = by_status.get(tc["status"], 0) + 1
        sc = by_screen.setdefault(tc["screen"], {"automated": 0, "skipped": 0, "missing": 0})
        sc[tc["status"]] += 1

    print(f"\n=== 웹 TC 총 {total}건 | 상태별 ===")
    for k in ("automated", "skipped", "missing"):
        print(f"  {k:9}: {by_status.get(k, 0)}")
    print("\n=== 화면(분류 A)별 ===")
    print(f"  {'screen':22} auto skip miss")
    for sc, d in by_screen.items():
        print(f"  {sc[:22]:22} {d['automated']:4} {d['skipped']:4} {d['missing']:4}")

    # referenced but not in sheet (typos / stale ids)
    sheet_ids = {tc["tc_id"] for tc in tcs}
    orphan = sorted(set(refs) - sheet_ids)
    if orphan:
        print("\n=== 코드에는 있으나 시트에 없는 TC_ID ===")
        print(" ", ", ".join(orphan))

    print(f"\n상세 매핑: {csv_path}")


if __name__ == "__main__":
    sys.exit(main())
