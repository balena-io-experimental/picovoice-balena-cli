import argparse


def parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--access_key",
        help="AccessKey obtained from Picovoice Console (https://picovoice.ai/console/)",
        required=False,
    )

    parser.add_argument(
        "--audio_device_index",
        help="Index of input audio device.",
        type=int,
        default=-1,
    )

    return parser.parse_args()
