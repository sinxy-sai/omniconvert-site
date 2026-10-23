import argparse, hashlib, json
from pathlib import Path
from .manifest import load_manifest

parser = argparse.ArgumentParser()
parser.add_argument('manifest')
parser.add_argument('--artifacts', default='.')
args = parser.parse_args()
manifest = load_manifest(args.manifest)
root = Path(args.artifacts)
for item in manifest['releases']:
    path = root / item['downloadUrl'].split('/')[-1]
    if item['size'] == 0 and item['platform'] == 'web':
        continue
    if not path.is_file(): raise SystemExit(f'missing artifact: {path}')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if path.stat().st_size != item['size'] or digest != item['sha256']:
        raise SystemExit(f'artifact mismatch: {path}')
print('all declared artifacts verified')
