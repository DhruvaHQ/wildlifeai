import argparse
import json
from wildlifeai.pipeline import run_pipeline


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="WildlifeAI – Camera trap image processing pipeline"
    )

    subparsers = parser.add_subparsers(dest="command")

    process_parser = subparsers.add_parser(
        "process", help="Process images from a folder"
    )

    process_parser.add_argument(
        "--config",
        help="Path to config JSON file",
    )

    process_parser.add_argument(
        "folder",
        nargs="?",
        help="Path to image folder (overrides config)",
    )

    process_parser.add_argument(
        "--json",
        help="Output JSON file (overrides config)",
    )

    process_parser.add_argument(
        "--csv",
        help="Output CSV file (overrides config)",
    )

    args = parser.parse_args()

    if args.command == "process":
        config = {}

        if args.config:
            config = load_config(args.config)

        image_folder = args.folder or config.get("image_folder")
        json_output = args.json or config.get("json_output", "image_metadata.json")
        csv_output = args.csv or config.get("csv_output", "image_metadata.csv")

        if not image_folder:
            raise ValueError("Image folder must be provided via CLI or config")

        run_pipeline(
            image_folder=image_folder,
            json_output=json_output,
            csv_output=csv_output,
        )
    else:
        parser.print_help()
