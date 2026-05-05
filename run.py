"""
CLI entry point

python run.py --input data/test_candidates/Sample_FreshGrad_01.json
python run.py --input data/test_candidates/
python run.py --input data/test_candidates --output results.json
"""

import argparse
import json
import pathlib
from cara.classifier import classify


def main():
    parser = argparse.ArgumentParser(description="CARA Classifier")
    parser.add_argument("--input", required=True, help="json file or directory")
    parser.add_argument("--output", default=None, help="output file path")
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)

    if input_path.is_dir():
        json_files = sorted(input_path.glob("*.json"))
        if len(json_files) == 0:
            print("No JSON files found in " + str(input_path))
            return
        profiles = []
        for f in json_files:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                profiles.append(data)
            except json.JSONDecodeError as e:
                print(f"Skipping {f.name}: {e}")
    else:
        if not input_path.exists():
            print(f"File not found: {input_path}")
            return
        profiles = [json.loads(input_path.read_text(encoding="utf-8"))]

    results = []
    for p in profiles:
        results.append(classify(p))

    if len(results) == 1:
        output_str = json.dumps(results[0], indent=2)
    else:
        output_str = json.dumps(results, indent=2)

    if args.output:
        out_path = pathlib.Path(args.output)
        out_path.write_text(output_str, encoding="utf-8")
        print(f"Saved to {out_path}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()
