#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

def synthesize(text, out_path):
    # Using espeak-ng directly for reliability in this environment
    cmd = ["espeak-ng", "-s", "160", "-p", "50", text, "-w", str(out_path)]
    subprocess.run(cmd, check=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script-json", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    data = json.loads(Path(args.script_json).read_text())
    text = data.get("script", "")
    synthesize(text, Path(args.output))

if __name__ == "__main__":
    main()
