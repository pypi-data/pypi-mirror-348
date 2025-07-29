import json
from pyldplayer2.base.models.smp import SMP
from pyldplayer2.base.objects.appattr import AppAttr, UseAppAttr
import os
from pyldplayer2.base.objects.pathcache import MtimeProp, PathCache


class SMPFile(UseAppAttr):
    def __init__(self, path: str | AppAttr | None = None):
        super().__init__(path)

    @MtimeProp("attr.customizeConfigs")
    def customizeList(self) -> list[str]:
        return [
            os.path.basename(file)
            for file in os.listdir(self.attr.customizeConfigs)
            if os.path.isfile(os.path.join(self.attr.customizeConfigs, file))
            and file.endswith(".smp")
        ]

    def getCustomize(self, name: str) -> SMP:
        if not name.endswith(".smp"):
            name += ".smp"
        return PathCache.getContents(
            os.path.join(self.attr.customizeConfigs, name), "smp"
        )

    def getRecommended(self, name: str) -> str:
        if not name.endswith(".smp"):
            name += ".smp"
        return PathCache.getContents(
            os.path.join(self.attr.recommendedConfigs, name), "smp"
        )

    @staticmethod
    @PathCache.register("smp")
    def load(path: str):
        with open(path, "r") as f:
            return json.load(f)

    def dump(self, path: str, smp: SMP):
        # check file relative to appattr
        if not os.path.isabs(path):
            path = os.path.join(self.attr.customizeConfigs, path)

        with open(path, "w") as f:
            json.dump(smp, f, indent=4)
