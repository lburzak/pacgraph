import subprocess

from pacgraph.models import Package

FIND_INSTALLED_PACKAGES_CMD = ["expac", "%n;%m;%D"]
FIND_EXPLICITLY_INSTALLED_PACKAGES_CMD = "pacman -Qet | awk '{print $1}'"
RECORD_SEPARATOR = "\n"
FIELD_SEPARATOR = ";"
DEPS_SEPARATOR = "  "
NAME_COLUMN = 0
SIZE_COLUMN = 1
DEPS_COLUMN = 2


def get_installed_packages() -> [Package]:
    output = subprocess.check_output(FIND_INSTALLED_PACKAGES_CMD, universal_newlines=True)
    records = normalize_output(output).split(RECORD_SEPARATOR)

    parser = PackageRecordParser()

    return [parser.parse(record) for record in records]


def get_explicitly_installed_packages_names() -> [str]:
    output = subprocess.check_output(FIND_EXPLICITLY_INSTALLED_PACKAGES_CMD, shell=True, universal_newlines=True)
    names = normalize_output(output).split(RECORD_SEPARATOR)

    return names


def normalize_output(output):
    return output.strip('\n')


class PackageRecordParser:
    explicitly_installed_packages: [str]

    def __init__(self) -> None:
        self.explicitly_installed_packages = get_explicitly_installed_packages_names()

    def parse(self, record: [str]) -> Package:
        record = record.split(FIELD_SEPARATOR)

        return Package(
            name=record[NAME_COLUMN],
            size=int(record[SIZE_COLUMN]),
            dependencies=record[DEPS_COLUMN].split(DEPS_SEPARATOR) if len(record[DEPS_COLUMN]) > 0 else [],
            is_explicitly_installed=record[NAME_COLUMN] in self.explicitly_installed_packages
        )
