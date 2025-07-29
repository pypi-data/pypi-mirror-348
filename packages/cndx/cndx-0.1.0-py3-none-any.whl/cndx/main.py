import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(
        prog="cndx",
        description="Run commands in Conda project environment (wrapper for 'conda project run')"
    )
    parser.add_argument(
        'command',
        nargs=argparse.REMAINDER,
        help='Command and arguments to run'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd = ["conda", "project", "run"] + args.command

    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("Error: 'conda' not found in PATH", file=sys.stderr)
        sys.exit(127)