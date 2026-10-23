import json
from pathlib import Path
from urllib.parse import urlparse

FIELDS = ('platform', 'arch', 'version', 'minimumSupportedVersion', 'downloadUrl', 'size', 'sha256', 'signature', 'releaseNotes')


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or not isinstance(manifest.get('releases'), list):
        raise ValueError('manifest must contain a releases list')
    seen = set()
    for item in manifest['releases']:
        missing = [field for field in FIELDS if field not in item]
        if missing:
            raise ValueError(f'missing field: {missing[0]}')
        key = (item['platform'], item['arch'])
        if key in seen:
            raise ValueError(f'duplicate platform/arch: {key[0]}/{key[1]}')
        seen.add(key)
        if urlparse(item['downloadUrl']).scheme != 'https':
            raise ValueError('downloadUrl must use HTTPS')
        if not isinstance(item['size'], int) or item['size'] < 0:
            raise ValueError('size must be a non-negative integer')
        if not isinstance(item['sha256'], str) or len(item['sha256']) != 64 or any(c not in '0123456789abcdef' for c in item['sha256'].lower()):
            raise ValueError('sha256 must be a 64-character hexadecimal string')
    return manifest


def generate_manifest(manifest):
    validate_manifest(manifest)
    return {'releases': sorted(manifest['releases'], key=lambda item: (item['platform'], item['arch']))}


def load_manifest(path):
    return generate_manifest(json.loads(Path(path).read_text(encoding='utf-8')))
