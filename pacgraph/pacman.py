import subprocess

from pacgraph.models import Package

FIND_INSTALLED_PACKAGES_CMD = ["expac", "-Q", "%n;%m;%D;%w"]
RECORD_SEPARATOR = "\n"
FIELD_SEPARATOR = ";"
DEPS_SEPARATOR = "  "
NAME_COLUMN = 0
SIZE_COLUMN = 1
DEPS_COLUMN = 2
REASON_COLUMN = 3


def get_installed_packages() -> [Package]:
    output = subprocess.check_output(FIND_INSTALLED_PACKAGES_CMD, universal_newlines=True)
    records = normalize_output(output).split(RECORD_SEPARATOR)

    return [parse_package_record(record) for record in records]


def parse_package_record(record: [str]) -> Package:
    record = record.split(FIELD_SEPARATOR)

    return Package(
        name=record[NAME_COLUMN],
        size=int(record[SIZE_COLUMN]),
        dependencies=record[DEPS_COLUMN].split(DEPS_SEPARATOR) if len(record[DEPS_COLUMN]) > 0 else [],
        is_explicitly_installed=record[REASON_COLUMN] == 'explicit'
    )


def normalize_output(output):
    return output.strip('\n')
