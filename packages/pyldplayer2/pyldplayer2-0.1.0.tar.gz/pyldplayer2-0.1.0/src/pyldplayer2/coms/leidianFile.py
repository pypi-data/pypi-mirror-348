import typing
import json
from pyldplayer2.base.models.leidian_config import LeidianConfig
from pyldplayer2.base.models.leidians_config import LeidiansConfig
from pyldplayer2.base.objects.appattr import UseAppAttr
import os
from pyldplayer2.base.objects.pathcache import MtimeProp, PathCache
from pyldplayer2.coms.instanceQuery import ALL_QUERY_TYPES, Query


class LeidianFile(UseAppAttr):
    @staticmethod
    @PathCache.register("leidians")
    def loadLeidians(path: str):
        with open(path, "r") as f:
            return LeidiansConfig.from_dict(json.load(f))

    @staticmethod
    @PathCache.register("leidian")
    def loadLeidian(path: str):
        with open(path, "r") as f:
            return LeidianConfig.from_dict(json.load(f))

    @MtimeProp("attr.config")
    def listLeidianConfigs(self):
        return [
            os.path.join(self.attr.config, file)
            for file in os.listdir(self.attr.config)
            if file.endswith(".config")
            and file.startswith("leidian")
            and file != "leidians.config"
        ]

    def getConfig(
        self, query: ALL_QUERY_TYPES | None = None
    ) -> typing.Union[LeidiansConfig, typing.Dict[int, LeidianConfig]]:
        is_string = isinstance(query, str)
        is_int = isinstance(query, int)
        if query is None or (is_string and query.startswith("leidians")):
            return PathCache.getContents(
                os.path.join(self.attr.config, "leidians.config"), "leidians"
            )

        if is_int or (is_string and query.isdigit()):
            return {
                int(query): PathCache.getContents(
                    os.path.join(self.attr.config, f"leidian{query}.config"), "leidian"
                )
            }

        if is_string and query.startswith("leidian"):
            return {
                int(query[7:]): PathCache.getContents(
                    os.path.join(self.attr.config, f"{query}.config"), "leidian"
                )
            }

        q = Query(self.attr)
        metas = q.queryInts(query)
        return {
            meta: PathCache.getContents(
                os.path.join(self.attr.config, f"leidian{meta}.config"), "leidian"
            )
            for meta in metas
        }

    def dumpLeidians(self, config: LeidiansConfig):
        with open(os.path.join(self.attr.config, "leidians.config"), "w") as f:
            json.dump(config.to_dict(), f, indent=4)

    def dumpLeidian(self, config: LeidianConfig):
        with open(
            os.path.join(self.attr.config, f"leidian{config.id}.config"), "w"
        ) as f:
            json.dump(config.to_dict(), f, indent=4)
