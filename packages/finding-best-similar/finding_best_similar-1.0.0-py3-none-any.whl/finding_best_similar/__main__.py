# finding_best_similar/__main__.py
import argparse
from . import best_similar, behavior_score

def main():
    p = argparse.ArgumentParser(prog="finding_best_similar")
    sub = p.add_subparsers(dest="cmd", required=True)

    bs = sub.add_parser("best_similar")
    bs.add_argument("file")
    bs.add_argument("--start",  required=True)
    bs.add_argument("--end",    required=True)
    bs.add_argument("--progress", action="store_true")
    bs.add_argument("--plot",     action="store_true")

    bb = sub.add_parser("behavior_score")
    bb.add_argument("file")
    bb.add_argument("--start",    required=True)
    bb.add_argument("--end",      required=True)
    bb.add_argument("--progress", action="store_true")
    bb.add_argument("--plot",     action="store_true")

    args = p.parse_args()
    if args.cmd == "best_similar":
        i1, i2, d = best_similar(
            args.file, start_time=args.start, end_time=args.end,
            show_progress=args.progress, plot=args.plot
        )
        print(i1, i2, d)
    else:
        day, corr = behavior_score(
            args.file, start_time=args.start, end_time=args.end,
            show_progress=args.progress, plot=args.plot
        )
        print(day, corr)

if __name__ == "__main__":
    main()
