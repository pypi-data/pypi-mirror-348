import subprocess
from .args import get_args
from .steps import build, upload, git_tag, update_version, git_commit


def main():
    version = update_version()
    args = get_args()
    if args.build:
        build()
        if args.upload:
            upload(version)

    if args.git_commit:
        git_commit(version)

    if args.git_push:
        subprocess.run(["git", "push"])

    if args.git_tag:
        git_tag(version)

        if args.git_push:
            subprocess.run(["git", "push", "--tags"])


if __name__ == "__main__":
    main()
