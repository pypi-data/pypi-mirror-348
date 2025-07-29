from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Literal
import os

from dataclass_wizard import YAMLWizard


@dataclass(unsafe_hash=True)
class CopyPair:
    src: str
    dest: str


@dataclass(unsafe_hash=True)
class AppSpecBase:
    pass


@dataclass(unsafe_hash=True)
class AppExecSpec(AppSpecBase):
    commands: list[str] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class AppInstallHelmSpec(AppSpecBase):
    values: list[str] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class AppInstallYamlSpec(AppSpecBase):
    files: list[str] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class AppInstallKustomizeSpec(AppSpecBase):
    kustomize_path: str


@dataclass(unsafe_hash=True)
class AppCopySpec(AppSpecBase):
    paths: list[CopyPair] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class AppPullHelmSpec(AppSpecBase):
    repo: str
    chart: str
    dest: str
    chart_version: Optional[str] = None
    app_version: Optional[str] = None
    removes: list[str] = field(default_factory=list)
    overrides: list[str] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class AppPullHelmOciSpec(AppSpecBase):
    repo: str
    chart: str
    dest: str
    chart_version: Optional[str] = None
    app_version: Optional[str] = None
    removes: list[str] = field(default_factory=list)
    overrides: list[str] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class AppPullGitSpec(AppSpecBase):
    repo: str
    paths: list[CopyPair] = field(default_factory=list)

    def __init__(self, **kwargs):
        self.repo = kwargs['repo']
        self.paths = [CopyPair(**path) for path in kwargs['paths']]


@dataclass(unsafe_hash=True, kw_only=True)
class AppPullHttpSpec(AppSpecBase):
    name: str = 'pull-http'
    url: str
    paths: list[CopyPair] = field(default_factory=list)

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.paths = [CopyPair(**path) for path in kwargs['paths']]


@dataclass(unsafe_hash=True, kw_only=True)
class AppInfoScheme(YAMLWizard):
    name: str
    type: Literal[
        'exec',
        'copy-repo', 'copy-chart', 'copy-root', 'copy-app',
        'install-helm', 'install-yaml', 'install-kustomize',
        'pull-helm', 'pull-helm-oci', 'pull-git', 'pull-http'
    ]
    path: Optional[str] = None
    enabled: bool = field(init=False, default=False)
    namespace: Optional[str] = None
    specs: dict = field(default_factory=dict)


@dataclass(unsafe_hash=True)
class AppGroupScheme(YAMLWizard):
    namespace: str
    deps: list[str] = field(default_factory=list)
    apps: list[AppInfoScheme] = field(default_factory=list)


def load_apps(group_name: str) -> AppGroupScheme:
    curr_file_path = Path(__file__).parent.resolve()
    yaml_path = Path(os.path.expanduser(str(curr_file_path / group_name / "config.yaml")))
    return AppGroupScheme.from_yaml_file(yaml_path)


if __name__ == '__main__':
    group_scheme = load_apps("a000_infra")
    for app in group_scheme.apps:
        print(app)
        if app.type == 'install-helm':
            helm_spec = AppInstallHelmSpec(**app.specs)
            print(helm_spec)
        elif app.type == 'pull-git':
            git_spec = AppPullGitSpec(**app.specs)
            print(git_spec)
