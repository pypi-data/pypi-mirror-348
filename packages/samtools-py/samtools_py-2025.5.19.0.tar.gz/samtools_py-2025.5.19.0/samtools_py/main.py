from samtools_py.exec_real_time import exec_real_time
import sys
from pathlib import Path


def main():
    args = sys.argv[1:]

    cwd = Path(__file__).resolve().parent
    samtools = cwd.parent / "samtools/data/ucrt64/bin/samtools.exe"
    args.insert(0, samtools)
    exec_real_time(args)


if __name__ == "__main__":
    main()
