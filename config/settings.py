import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


@dataclass(frozen=True)
class Account:
    email: str
    password: str
    level: int

    @property
    def configured(self) -> bool:
        return bool(self.email and self.password)


@dataclass(frozen=True)
class InfluxConfig:
    url: str = field(default_factory=lambda: _env("INFLUX_URL"))
    token: str = field(default_factory=lambda: _env("INFLUX_TOKEN"))
    org: str = field(default_factory=lambda: _env("INFLUX_ORG", "deepcheck"))
    bucket: str = field(default_factory=lambda: _env("INFLUX_BUCKET", "test_results"))

    @property
    def enabled(self) -> bool:
        return bool(self.url and self.token)


def _accounts() -> dict[int, Account]:
    # One shared password by default (override per level with TEST_PASSWORD_L<n>).
    shared_pw = _env("TEST_PASSWORD")
    result: dict[int, Account] = {}
    for level in (1, 2, 3, 4):
        email = _env(f"TEST_USER_L{level}")
        password = _env(f"TEST_PASSWORD_L{level}") or shared_pw
        if email:
            result[level] = Account(email=email, password=password, level=level)
    return result


@dataclass(frozen=True)
class Settings:
    base_url: str = field(default_factory=lambda: _env("BASE_URL", "https://dev.deepcheck.deep-medi.com"))
    api_base_url: str = field(default_factory=lambda: _env("API_BASE_URL"))
    env: str = field(default_factory=lambda: _env("TEST_ENV", "dev"))

    accounts: dict[int, Account] = field(default_factory=_accounts)

    git_branch: str = field(
        default_factory=lambda: _env("GIT_BRANCH") or _env("GITHUB_REF_NAME", "local")
    )
    git_commit: str = field(
        default_factory=lambda: _env("GIT_COMMIT") or _env("GITHUB_SHA", "local")
    )

    influx: InfluxConfig = field(default_factory=InfluxConfig)

    def account(self, level: int) -> Account:
        try:
            return self.accounts[level]
        except KeyError:
            raise RuntimeError(
                f"No level-{level} test account configured. "
                f"Set TEST_USER_L{level} (and TEST_PASSWORD)."
            )


settings = Settings()
