from datetime import timedelta, datetime
from pathlib import Path
import re

class RaceData:
    RecordDict = dict[str, "RaceData"]
    def __init__(
        self,
        driver=None,
        team=None,
        abbreviation=None,
        start=None,
        end=None,
    ) -> None:
        self.driver: str = driver
        self.team: str = team
        self.abbreviation: str = abbreviation
        self.start: datetime = start
        self.end: datetime = end
        self.recordErrors: list[str] = []
        self._duration = None

    @property
    def duration(self) -> timedelta | None:
        """Return duration"""
        return self._duration

    @duration.setter
    def duration(self, value: timedelta | None) -> None:
        if value is not None and value.total_seconds() < 0:
            self.recordErrors.append(f"{self.abbreviation}: duration is negative")
            self._duration = None
        else:
            self._duration = value

    def __str__(self) -> str:
        return f"{self.driver} {self.team} {self.duration}"

    @classmethod
    def read_file(cls, filename: str, folder: Path | None) -> str:
        """
        Read `filename` either from a user-provided folder or
        from the package‐bundled `data/` directory.

        :param filename: one of "start.log", "end.log", "abbreviations.txt"
        :param folder:  optional Path to user’s own data folder
        :return: file contents as string
        """
        full_folder = folder / filename
        try:
            return full_folder.read_text()
        except ModuleNotFoundError:
            raise FileNotFoundError(f"{filename!r} not found in the specified folder or package data")

    @classmethod
    def create_race_list(cls, folder: Path) -> RecordDict:
        """
        Create a dictionary with races
        :param folder: path to folder
        :return dict with abbreviation and RaceData object
        """
        fmt = "%Y-%m-%d_%H:%M:%S.%f"
        record_dict = {}
        starts = RaceData.read_file("start.log", folder).strip().split("\n")
        ends = RaceData.read_file("end.log", folder).strip().split("\n")

        for start in starts:
            abb_start = start[0:3]
            start_date = datetime.strptime(start[3:].strip(), fmt)
            race = RaceData()
            race.abbreviation = abb_start
            race.start = start_date
            record_dict[abb_start] = race

        for end in ends:
            abb_end = end[0:3]
            end_date = datetime.strptime(end[3:].strip(), fmt)
            if abb_end in record_dict:
                record = record_dict[abb_end]
                record.end = end_date
                record.duration = record.end - record.start
                record_dict[abb_end] = record

            else:
                race = RaceData()
                race.abbreviation = abb_end
                race.end = end_date
                race._duration = None
                record_dict[abb_end] = race
        return record_dict

    @classmethod
    def sorted_asc_desc(
        cls, dict_to_sort: RecordDict, sort_flag: str = "asc"
    ) -> RecordDict:
        """
        Sort passing dictionary
        :param dict_to_sort: the dictionary to sort -> dict type
        :param sort_flag: sort parameter -> boolean type
        :return: sorting dict by duration time
        """
        if sort_flag == "asc":
            return dict(
                sorted(sorted(dict_to_sort.items()), key=lambda item: item[1].duration)
            )
        else:
            return dict(
                sorted(
                    dict_to_sort.items(),
                    key=lambda item: item[1].duration,
                    reverse=True,
                )
            )

    def read_abbreviation(self, folder: Path) -> RecordDict:
        """
        Read abbreviations file and add it to dictionary
        :param folder: way to folder -> Path type
        :return: dictionary with abbreviation and RaceData object
        """
        abb_file = RaceData.read_file( "abbreviations.txt",folder)
        abbreviations_list = [line.split("_") for line in abb_file.strip().split("\n")]
        record_dict = self.create_race_list(folder)
        for abb_item in abbreviations_list:
            if len(abb_item) >= 3:
                driver, team = abb_item[1], abb_item[2]
                if abb_item[0] in record_dict.keys():
                    record_dict[abb_item[0]].driver = driver
                    record_dict[abb_item[0]].team = team

        return record_dict

    def build_report(
        self, folder: Path | None, driver: str | None, sort_order: str = None
    ) -> RecordDict | tuple[RecordDict, RecordDict]:
        """
        Create, filter and sort all records list
        :return: dictionary only with good races:  type RecordDict
        """
        record = self.read_abbreviation(folder)
        if driver is not None:
            result = dict(
                filter(lambda value: value[1].driver == driver.strip(), record.items())
            )
            return result
        else:
            filtered = dict(
                filter(lambda value: value[1].duration is not None, record.items())
            )
            filtered_duration_error = dict(
                filter(lambda value: value[1].duration is None, record.items())
            )
            result_dict = self.sorted_asc_desc(filtered, sort_order)

            return result_dict, filtered_duration_error


    def print_report(
        self,
        folder: Path | None = None,
        driver: str = None,
        sort_order: str | None = None,
        underline: int = 14,
    ) -> None:
        """
        Print result dict to stdout
        :param folder:
        :param driver:
        :param sort_order:
        :param underline: print line and repeat it: type int
        :return:
        """
        line_limit = 60


        if driver is None:
            good_report, error_report = self.build_report(folder, driver, sort_order)
            for i, record in enumerate(good_report.values()):
                formatted_time = re.sub(r"^0:|(?<=:)0", "", str(record.duration))
                print(
                    f"{i + 1}. {record.driver} | {record.team} | {formatted_time[:-3]}"
                )
                if i == underline:
                    print("-" * line_limit + "\n")

            print("This is lines with some error:")
            for i, (abb, race) in enumerate(error_report.items()):
                print(
                    f"{i+1}. [ERROR] The driver {race.driver} has some issues: {race.recordErrors}"
                )

        else:
            driver_report = self.build_report(folder, driver, sort_order)
            print("\n")
            print("The driver has next statistic about  race:")
            for race in driver_report.values():
                formatted_time = re.sub(r"^0:|(?<=:)0", "", str(race.duration))
                if len(race.recordErrors) == 0:
                    print(f"{race.driver} | {race.team} | {formatted_time[:-3]}")
                else:
                    print(
                        f"The driver {race.driver} has wrong duration time: {race.recordErrors}"
                    )
            print("-" * line_limit)
