import logging

import importlib.resources as pkg_resources

from .driver_3_version import RecordData


def main():
    logging.basicConfig(level=logging.INFO)

    try:
        cli_args = RecordData.cli()

        data_path = pkg_resources.files("monaco_qualifying.data")

        abbreviations = cli_args["abbreviations"] or data_path.joinpath("abbreviations.txt")
        start_log = cli_args["start_log"] or data_path.joinpath("start.log")
        stop_log = cli_args["stop_log"] or data_path.joinpath("end.log")

        record = RecordData()

        good_records, bad_records = record.build_report(
            file=abbreviations,
            start_file=start_log,
            stop_file=stop_log,
            asc=cli_args["asc"],
            driver=cli_args["driver"],
        )

        RecordData.print_report(good_records, bad_records)

    except FileNotFoundError as e:
        logging.error(f"Critical error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
