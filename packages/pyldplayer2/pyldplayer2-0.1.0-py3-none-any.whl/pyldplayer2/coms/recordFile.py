from dataclasses import asdict
import json
from pyldplayer2.base.models.record import Record, RecordInfo, Operation
from pyldplayer2.base.objects.appattr import AppAttr, UseAppAttr
import os
from pyldplayer2.base.objects.pathcache import MtimeProp, PathCache


class RecordFile(UseAppAttr):
    def __init__(self, path: str | AppAttr | None = None):
        super().__init__(path)

    @MtimeProp("attr.operationRecords")
    def recordList(self) -> list[str]:
        return [
            os.path.basename(file)
            for file in os.listdir(self.attr.operationRecords)
            if os.path.isfile(os.path.join(self.attr.operationRecords, file))
            and file.endswith(".record")
        ]

    def getRecord(self, name: str) -> Record:
        if not name.endswith(".record"):
            name += ".record"
        return PathCache.getContents(
            os.path.join(self.attr.operationRecords, name), "record"
        )

    @staticmethod
    @PathCache.register("record")
    def load(path: str):
        with open(path, "r") as f:
            data = json.load(f)
            return Record(
                recordInfo=RecordInfo(**data["recordInfo"]),
                operations=[Operation(**operation) for operation in data["operations"]],
            )

    def dump(self, path: str, record: Record):
        # check file relative to appattr
        if not os.path.isabs(path):
            path = os.path.join(self.attr.operationRecords, path)

        with open(path, "w") as f:
            json.dump(asdict(record), f, indent=4)
