import subprocess


def get_staged_diff() -> str:
    diff = subprocess.run(
        ["git", "diff", "--staged", "--unified=0"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return diff


def commit_staged(message: str, edit: bool = False):
    args = ["git", "commit", "--cleanup=strip", f"--message={message}"]
    if edit:
        args += ["--edit"]
    subprocess.run(args, check=True)
