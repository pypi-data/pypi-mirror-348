import json
import pathlib
import os
import sys

from cappa import command
from dataclasses import dataclass


@command(name="create-build-env")
@dataclass
class TGCSCreateBuildEnv:
    bundle_metadata: pathlib.Path
    eas_json: pathlib.Path

    def __call__(self):
        direct_export_keys = (
            "TGCS_EXPO_OWNER",
            "TGCS_APP_NAME",
            "TGCS_APP_SLUG",
            "TGCS_APP_BASE_URL",
            "TGCS_APP_URL_SCHEME",
            "TGCS_EXPO_PROJECT_ID",
            "TGCS_ANDROID_PACKAGE",
            "TGCS_ANDROID_MAPS_API_KEY",
            "TGCS_IOS_BUNDLE_IDENTIFIER",
        )

        with open(self.bundle_metadata) as bf:
            data = json.load(bf)

        version = data["release"]["version"]
        version_pattern = os.environ.get("TGCS_VERSION_PATTERN", "{}")
        package_version = version_pattern.format(version)

        android_version_code_offset = int(
            os.environ.get("TGCS_ANDROID_VERSION_CODE_OFFSET", "0")
        )

        with open(self.eas_json, "r") as ef:
            eas_data = json.load(ef)

        build_env = {}
        if len(sys.argv) == 2:
            with open(sys.argv[-1], "r") as fh:
                for line in map(str.strip, fh.readlines()):
                    k, v = line.split("=")
                    build_env[k] = v
        else:
            build_env = os.environ  # l o l

        for env in ("development", "preview", "production"):
            eas_data["build"][env]["env"] = {
                **eas_data["build"][env]["env"],
                **({k: build_env.get(k) for k in direct_export_keys}),
                "TGCS_APP_VERSION": package_version,
                "TGCS_ANDROID_VERSION_CODE": str(version + android_version_code_offset),
            }

        with open(self.eas_json, "w") as ef:
            json.dump(eas_data, ef, indent=2)
