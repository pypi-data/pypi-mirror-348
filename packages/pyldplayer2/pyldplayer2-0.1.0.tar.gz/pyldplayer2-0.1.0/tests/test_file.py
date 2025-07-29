import dotenv
import os
from pyldplayer2.base.models.leidians_config import LeidiansConfig
from pyldplayer2.base.objects.appattr import AppAttr

dotenv.load_dotenv()
appattr = AppAttr(os.getenv("LDPATH"))


def test_smp():
    from pyldplayer2.coms.smpFile import SMPFile

    smp = SMPFile()
    results = smp.customizeList
    assert results is not None
    assert isinstance(results, list)


def test_leidian():
    from pyldplayer2.coms.leidianFile import LeidianFile

    leidian = LeidianFile()
    assert isinstance(leidian.getConfig(), LeidiansConfig)
    assert isinstance(leidian.listLeidianConfigs, list)


def test_record():
    from pyldplayer2.coms.recordFile import RecordFile
    from pyldplayer2.base.models.record import Record

    record = RecordFile()
    assert isinstance(record.getRecord(record.recordList[0]), Record)
    assert isinstance(record.recordList, list)


def test_kmp():
    from pyldplayer2.coms.kmpFile import KMPFile
    from pyldplayer2.base.models.kmp import KeyboardMapping

    kmp = KMPFile()
    assert isinstance(kmp.getCustomize(kmp.customizeList[0]), KeyboardMapping)
    assert isinstance(kmp.customizeList, list)
