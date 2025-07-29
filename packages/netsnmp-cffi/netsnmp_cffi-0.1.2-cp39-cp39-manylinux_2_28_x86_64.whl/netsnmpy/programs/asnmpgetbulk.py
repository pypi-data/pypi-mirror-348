import argparse
import asyncio
import logging
from typing import List

from netsnmpy import netsnmp, session
from netsnmpy.netsnmp import SNMPVariable


def main():
    args = parse_args()

    logging.basicConfig(level=logging.INFO)
    netsnmp.load_mibs()
    netsnmp.register_log_callback()

    asyncio.run(run(args))


async def run(args):
    sess = session.SNMPSession(host=args.host, port=args.port, version=args.version)
    sess.open()
    objids = [netsnmp.symbol_to_oid(obj) for obj in args.oid]

    try:
        result: List[SNMPVariable] = await sess.agetbulk(
            *objids,
            non_repeaters=args.non_repeaters,
            max_repetitions=args.max_repetitions,
        )
    except TimeoutError:
        print("Request timed out")
    else:
        for var in result:
            print(var)
            # print(f"{var.symbolic_name} = {var.value}")
        #     print(f"{varoid} = {var.val}")
        # res = [(netsnmp.oid_to_symbol(oid), val) for oid, val in result]
        # for oid, val in res:
        #     print(f"{oid} = {val}")


def parse_args():
    parser = argparse.ArgumentParser(description="SNMP GET-BULK request")
    parser.add_argument("host", help="SNMP agent host")
    parser.add_argument("--port", "-p", type=int, default=161, help="SNMP agent port")
    parser.add_argument(
        "--version", "-v", type=str, default="2c", help="SNMP agent version"
    )
    parser.add_argument(
        "--community", "-c", default="public", help="SNMP community string"
    )
    parser.add_argument(
        "--non-repeaters", "-n", type=int, default=0, help="Number of non repeaters"
    )
    parser.add_argument(
        "--max-repetitions", "-m", type=int, default=10, help="Maximum repetitions"
    )
    parser.add_argument("oid", nargs="+", help="MIB objects to query for")
    return parser.parse_args()


if __name__ == "__main__":
    main()
