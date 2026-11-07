"""Show how a script change moves the stored example output, and save the new output.

    python3 tests/update_expected.py           show the diff, then write the new files
    python3 tests/update_expected.py --check   show the diff only, and exit 1 if anything changed

Review the diff before you commit. It is the before-and-after record of your change.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from support import EXPECTED, all_snapshots, diff, read  # noqa: E402


def main():
    check_only = "--check" in sys.argv[1:]
    snaps = all_snapshots()
    changed = 0
    for path, actual in sorted(snaps.items()):
        stored = read(path) if os.path.exists(path) else ""
        if stored != actual:
            changed += 1
            print(diff(stored, actual, path) or f"new file: {path}")
            if not check_only:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(actual)
    for name in sorted(set(os.listdir(EXPECTED)) - {os.path.basename(p) for p in snaps}):
        changed += 1
        print(f"stale file with no fixture: tests/expected/{name}")
        if not check_only:
            os.remove(os.path.join(EXPECTED, name))
    if not changed:
        print("No changes. The stored output matches the script.")
    elif check_only:
        print(f"{changed} stored file(s) differ. Run python3 tests/update_expected.py to save them.")
        sys.exit(1)
    else:
        print(f"Updated {changed} file(s) in tests/expected.")


if __name__ == "__main__":
    main()
