import argparse
from pathlib import Path
from report_of_monaco_2018.racing import RaceData


def race_report() -> None:
    DEFAULT_DATA_PATH = Path(__file__).parent / "data"

    parser = argparse.ArgumentParser(
        description="Monaco 2018 Q1 lap‐time report"
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        required=True,
        help="the way to file (start.log, end.log, abbreviations.txt)"
    )
    parser.add_argument(
        "--driver", "-d",
        type=str,
        help="if True  print by driver"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--asc", action="store_true", help="sorting asc")
    group.add_argument("--desc", action="store_true", help="sorting desc")

    args = parser.parse_args()
    sort_order = "desc" if args.desc else "asc"
    if args.file is None:
        folder_path = DEFAULT_DATA_PATH
    else:
        folder_path = Path(args.file)
    try:
        RaceData().print_report(
            folder=folder_path,
            driver=args.driver,
            sort_order=sort_order
        )
    except FileNotFoundError as e:
        raise FileNotFoundError(f"[ERROR] {e}")
    except ValueError as e:
        raise ValueError(f"[ERROR] {e}")


if __name__ == "__main__":
   race_report()
