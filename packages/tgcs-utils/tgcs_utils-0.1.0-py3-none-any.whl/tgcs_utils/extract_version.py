import json
import sys

from cappa import command
from dataclasses import dataclass


@command(name="extract-version")
@dataclass
class TGCSExtractVersion:
    def __call__(self):
        data = json.loads(sys.stdin.read())
        print(data["release"]["version"])
