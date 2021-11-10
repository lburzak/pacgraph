import subprocess

from pacgraph.models import Package

FIND_PACKAGES_CMD = ["expac", "-S", "%n;%m;%D"]
RECORD_SEPARATOR = "\n"
FIELD_SEPARATOR = ";"
DEPS_SEPARATOR = "  "
NAME_COLUMN = 0
SIZE_COLUMN = 1
DEPS_COLUMN = 2


def parse_package_record(record):
    record = record.split(FIELD_SEPARATOR)

    return Package(
        name=record[NAME_COLUMN],
        size=record[SIZE_COLUMN],
        dependencies=record[DEPS_COLUMN].split(DEPS_SEPARATOR) if len(record[DEPS_COLUMN]) > 0 else []
    )


def get_packages() -> [Package]:
    output = subprocess.check_output(FIND_PACKAGES_CMD, universal_newlines=True)

    normalized_output = output.strip('\n')
    records = normalized_output.split(RECORD_SEPARATOR)

    return [parse_package_record(record) for record in records]
