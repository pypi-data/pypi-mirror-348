from pathlib import Path


def get_version(project_toml: Path) -> list[int]:
    content = project_toml.read_text(encoding="utf8")
    import re

    versions = re.findall(r'version = "([0-9\.]+)"', content)
    if len(versions) == 0:
        print("cannot find version")
        exit(-1)

    if versions[0].count(".") != 3:  # year, month, day, rev
        print("incorrect version format")
        exit(-1)

    year, month, day, rev = versions[0].split(".")
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        rev = int(rev)
    except ValueError:
        print("incorrect version format")
        exit(-1)

    return [year, month, day, rev]


def next_version(version: list[int]) -> str:
    year, month, day, rev = version
    new_version = [year, month, day, rev]
    import datetime

    now = datetime.datetime.now()
    if year == now.year and month == now.month and day == now.day:
        new_version[3] += 1
    else:
        new_version = [now.year, now.month, now.day, 0]

    return new_version


def str_version(version: list[int]) -> str:
    if isinstance(version, str):
        return version
    return ".".join(map(str, version))


def update_version() -> str:
    from .toml import get_project_toml

    project_toml = get_project_toml()
    version = get_version()
    nextv = next_version(version)

    nextv = str_version(nextv)

    project_toml.write_text(
        encoding="utf8",
        data=project_toml.read_text(encoding="utf8").replace(
            str_version(version), str_version(nextv)
        ),
    )

    return nextv
