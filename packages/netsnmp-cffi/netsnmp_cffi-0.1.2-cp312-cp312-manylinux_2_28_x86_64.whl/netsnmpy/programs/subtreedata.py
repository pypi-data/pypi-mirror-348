import argparse

from netsnmpy import netsnmp
from netsnmpy.oids import OID


def main():
    args = parse_args()
    netsnmp.load_mibs()

    for oid in args.oid:
        print_subtree_info(oid)


def print_subtree_info(oid: OID):
    ffi = netsnmp._ffi
    symbol = netsnmp.oid_to_symbol(oid)
    print(f"{oid}: {symbol}")
    subtree = netsnmp.get_subtree_for_object(oid)
    print("label:: {}".format(ffi.string(subtree.label).decode()))

    print(netsnmp.get_loaded_mibs())


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get MIB subtree information for an OID from Net-SNMP"
    )
    parser.add_argument(
        "oid",
        nargs="*",
        help="OID",
        type=OID,
        default=[OID(".1.3.6.1.4.1.9.9.187.1.2.5.1.4.1.4.10.0.0.1")],
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
