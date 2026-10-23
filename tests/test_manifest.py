import pytest
from tools.manifest import validate_manifest, generate_manifest

def entry(**overrides):
    value = {"platform": "android", "arch": "arm64-v8a", "version": "0.1.0", "minimumSupportedVersion": "0.1.0", "downloadUrl": "https://example.com/app.apk", "size": 3, "sha256": "a" * 64, "signature": "sig", "releaseNotes": "Initial release"}
    value.update(overrides)
    return value

def test_rejects_missing_field():
    item = entry(); del item["sha256"]
    with pytest.raises(ValueError, match="sha256"): validate_manifest({"releases": [item]})

def test_rejects_duplicate_platform_arch():
    with pytest.raises(ValueError, match="duplicate"): validate_manifest({"releases": [entry(), entry(version="0.1.1")]})

def test_rejects_non_https_download_url():
    with pytest.raises(ValueError, match="HTTPS"): validate_manifest({"releases": [entry(downloadUrl="http://example.com/app.apk")]})

def test_rejects_invalid_hash():
    with pytest.raises(ValueError, match="sha256"): validate_manifest({"releases": [entry(sha256="xyz")]})

def test_generation_is_deterministic_and_sorted():
    manifest = {"releases": [entry(platform="windows", arch="x64"), entry()]}
    first = generate_manifest(manifest)
    second = generate_manifest({"releases": list(reversed(manifest["releases"]))})
    assert first == second
    assert [item["platform"] for item in first["releases"]] == ["android", "windows"]
