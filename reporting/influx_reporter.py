from __future__ import annotations

from datetime import datetime, timezone

from config.settings import settings

try:
    from influxdb_client import InfluxDBClient, Point
    from influxdb_client.client.write_api import SYNCHRONOUS
except ImportError:  # influxdb-client not installed
    InfluxDBClient = None
    Point = None
    SYNCHRONOUS = None


class InfluxReporter:
    """Streams one point per test outcome to InfluxDB for Grafana dashboards.

    Disabled silently when InfluxDB is not configured, so local runs and
    debugging never depend on a reachable database.
    """

    MEASUREMENT = "test_result"

    def __init__(self) -> None:
        cfg = settings.influx
        self._client = None
        self._write_api = None
        if cfg.enabled and InfluxDBClient is not None:
            self._client = InfluxDBClient(url=cfg.url, token=cfg.token, org=cfg.org)
            self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self._bucket = cfg.bucket

    @property
    def active(self) -> bool:
        return self._write_api is not None

    def record(self, *, nodeid: str, outcome: str, duration: float, suite: str, tc_id: str = "") -> None:
        if not self.active:
            return
        point = (
            Point(self.MEASUREMENT)
            .tag("test", nodeid)
            .tag("suite", suite)
            .tag("outcome", outcome)
            .tag("tc_id", tc_id or "(untagged)")
            .tag("env", settings.env)
            .tag("branch", settings.git_branch)
            .tag("commit", settings.git_commit)
            .field("duration", float(duration))
            .field("passed", 1 if outcome == "passed" else 0)
            .time(datetime.now(timezone.utc))
        )
        try:
            self._write_api.write(bucket=self._bucket, record=point)
        except Exception as exc:
            # Telemetry must never break the test run: disable after first failure.
            print(f"[influx-reporter] disabled (InfluxDB unreachable): {exc}")
            self.close()
            self._write_api = None

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
