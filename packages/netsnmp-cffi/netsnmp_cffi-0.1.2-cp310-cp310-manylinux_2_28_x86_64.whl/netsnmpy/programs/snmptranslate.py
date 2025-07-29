import argparse
from enum import Enum

from netsnmpy import netsnmp
from netsnmpy.constants import NETSNMP_DS_LIB_OID_OUTPUT_FORMAT, NETSNMP_DS_LIBRARY_ID
from netsnmpy.netsnmp import oid_to_symbol
from netsnmpy.oids import OID

# constants

NETSNMP_OID_OUTPUT_SUFFIX = 1
NETSNMP_OID_OUTPUT_MODULE = 2
NETSNMP_OID_OUTPUT_FULL = 3
NETSNMP_OID_OUTPUT_NUMERIC = 4
NETSNMP_OID_OUTPUT_UCD = 5
NETSNMP_OID_OUTPUT_NONE = 6


class OIDOutputOption(Enum):
    SUFFIX = NETSNMP_OID_OUTPUT_SUFFIX
    MODULE = NETSNMP_OID_OUTPUT_MODULE
    FULL = NETSNMP_OID_OUTPUT_FULL
    NUMERIC = NETSNMP_OID_OUTPUT_NUMERIC
    UCD = NETSNMP_OID_OUTPUT_UCD
    NONE = NETSNMP_OID_OUTPUT_NONE


def main():
    args = parse_args()
    netsnmp.load_mibs()
    netsnmp._lib.netsnmp_ds_set_int(
        NETSNMP_DS_LIBRARY_ID,
        NETSNMP_DS_LIB_OID_OUTPUT_FORMAT,
        args.output_format.value,
    )
    print(f"setting oid output option to {args.output_format.name}")
    for oid in args.oid:
        symbol = oid_to_symbol(oid)
        print(f"{oid}: {symbol}")


def parse_args():
    parser = argparse.ArgumentParser(description="Translate OIDs to symbolic names")
    parser.add_argument("oid", nargs="+", help="OID", type=OID)
    parser.add_argument(
        "--output-format",
        "-o",
        type=oid_output_option,
        default=OIDOutputOption.FULL,
        help="Net-SNMP OID Output option",
    )
    return parser.parse_args()


def oid_output_option(value):
    try:
        return OIDOutputOption(int(value))
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid OID output option: {value}")


if __name__ == "__main__":
    main()
