import argparse, json
from pathlib import Path
try:
    from .manifest import generate_manifest
except ImportError:
    from manifest import generate_manifest

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()
manifest = generate_manifest(json.loads(Path(args.input).read_text(encoding='utf-8')))
Path(args.output).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
