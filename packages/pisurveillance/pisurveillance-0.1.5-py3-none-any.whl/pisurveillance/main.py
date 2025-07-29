import argparse
import asyncio
import logging

from pisurveillance.config import env
from pisurveillance.surveillance import start_surveillance

logging.basicConfig(level=logging.INFO)


def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(*args, **kwargs)
    parser.add_argument(
        "-f",
        "--frequency",
        type=int,
        default=env.CAPTURE_FREQUENCY,
        help="Image capture frequency in seconds",
    )

    parser.add_argument(
        "-d",
        "--device",
        type=str,
        default=env.DEVICE_NAME,
        help="Name of your device",
    )

    parser.add_argument(
        "-c",
        "--camera",
        type=int,
        default=env.CAMERA_INDEX,
        help="Camera index",
    )

    return parser.parse_args()


def main():
    args = parse_args(description="Start the surveillance system")
    asyncio.run(start_surveillance(args.frequency, args.device, args.camera))
