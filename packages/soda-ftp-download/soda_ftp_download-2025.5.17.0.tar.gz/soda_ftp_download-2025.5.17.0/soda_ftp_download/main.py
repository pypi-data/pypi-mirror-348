from soda_ftp_download import download_file
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", "-i", type=str, help="ftp url to download", required=True
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="local file name (auto-detect if empty)",
        default="",
    )
    args = parser.parse_args()
    download_file(args.input, args.output)


if __name__ == "__main__":
    main()
