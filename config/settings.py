import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


@dataclass(frozen=True)
class InfluxConfig:
    url: str = field(default_factory=lambda: _env("INFLUX_URL"))
    token: str = field(default_factory=lambda: _env("INFLUX_TOKEN"))
    org: str = field(default_factory=lambda: _env("INFLUX_ORG", "deepcheck"))
    bucket: str = field(default_factory=lambda: _env("INFLUX_BUCKET", "test_results"))

    @property
    def enabled(self) -> bool:
        return bool(self.url and self.token)


@dataclass(frozen=True)
class Settings:
    base_url: str = field(default_factory=lambda: _env("BASE_URL"))
    api_base_url: str = field(default_factory=lambda: _env("API_BASE_URL"))
    env: str = field(default_factory=lambda: _env("TEST_ENV", "local"))

    test_user: str = field(default_factory=lambda: _env("TEST_USER"))
    test_password: str = field(default_factory=lambda: _env("TEST_PASSWORD"))

    git_branch: str = field(
        default_factory=lambda: _env("GIT_BRANCH") or _env("GITHUB_REF_NAME", "local")
    )
    git_commit: str = field(
        default_factory=lambda: _env("GIT_COMMIT") or _env("GITHUB_SHA", "local")
    )

    influx: InfluxConfig = field(default_factory=InfluxConfig)


settings = Settings()
