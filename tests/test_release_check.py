import pytest

from tools.release_check import check_release


def release(version="1.2.0", minimum="1.0.0"):
    return {"platform": "android", "arch": "arm64-v8a", "version": version,
            "minimumSupportedVersion": minimum, "downloadUrl": "https://example.com/app.apk",
            "size": 1, "sha256": "a" * 64, "signature": "sig", "releaseNotes": "notes"}


def test_current_version_is_current():
    assert check_release({"releases": [release()]}, platform="android", arch="arm64-v8a", current_version="1.2.0")["state"] == "current"


def test_newer_version_requests_update():
    assert check_release({"releases": [release()]}, platform="android", arch="arm64-v8a", current_version="1.1.0")["state"] == "update"


def test_minimum_version_blocks_old_client():
    assert check_release({"releases": [release(minimum="1.1.0")]}, platform="android", arch="arm64-v8a", current_version="1.0.0")["state"] == "blocked"


def test_invalid_manifest_is_rejected():
    with pytest.raises(ValueError):
        item = release()
        item["downloadUrl"] = "http://example.com/app.apk"
        check_release({"releases": [item]}, platform="android", arch="arm64-v8a", current_version="1.0.0")
