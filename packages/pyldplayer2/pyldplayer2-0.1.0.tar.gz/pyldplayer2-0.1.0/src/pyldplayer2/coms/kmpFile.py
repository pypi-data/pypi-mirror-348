import json
from pyldplayer2.base.models.kmp import KeyboardMapping
from pyldplayer2.base.objects.appattr import AppAttr, UseAppAttr
import os
from pyldplayer2.base.objects.pathcache import MtimeProp, PathCache


class KMPFile(UseAppAttr):
    def __init__(self, path: str | AppAttr | None = None):
        super().__init__(path)

    @MtimeProp("attr.customizeConfigs")
    def customizeList(self) -> list[str]:
        return [
            os.path.basename(file)
            for file in os.listdir(self.attr.customizeConfigs)
            if os.path.isfile(os.path.join(self.attr.customizeConfigs, file))
            and file.endswith(".kmp")
        ]

    def getCustomize(self, name: str) -> KeyboardMapping:
        if not name.endswith(".kmp"):
            name += ".kmp"
        return PathCache.getContents(
            os.path.join(self.attr.customizeConfigs, name), "kmp"
        )

    def getRecommended(self, name: str) -> KeyboardMapping:
        if not name.endswith(".kmp"):
            name += ".kmp"
        return PathCache.getContents(
            os.path.join(self.attr.recommendedConfigs, name), "kmp"
        )

    @staticmethod
    @PathCache.register("kmp")
    def load(path: str) -> KeyboardMapping:
        with open(path, "r") as f:
            return KeyboardMapping.from_dict(json.load(f))

    def dump(self, path: str, mapping: KeyboardMapping):
        # check file relative to appattr
        if not os.path.isabs(path):
            path = os.path.join(self.attr.customizeConfigs, path)

        with open(path, "w") as f:
            json.dump(mapping.to_dict(), f, indent=4)
