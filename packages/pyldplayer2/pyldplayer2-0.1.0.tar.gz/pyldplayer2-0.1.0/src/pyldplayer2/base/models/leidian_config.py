from dataclasses import asdict, dataclass
from typing import TypedDict, Optional
import typing
from pyldplayer2.base.utils.dotDict import parse_dotted_dict, flatten_nested_dict


class HotkeySettings(TypedDict):
    backKey: dict
    homeKey: dict
    appSwitchKey: dict
    menuKey: dict
    zoomInKey: dict
    zoomOutKey: dict
    bossKey: dict
    shakeKey: dict
    operationRecordKey: dict
    fullScreenKey: dict
    showMappingKey: dict
    videoRecordKey: dict
    mappingRecordKey: dict
    keyboardModelKey: dict


class KeyConfig(TypedDict):
    modifiers: int
    key: int


class ResolutionSettings(TypedDict):
    width: int
    height: int


class AdvancedSettings(TypedDict):
    resolution: ResolutionSettings
    resolutionDpi: int
    cpuCount: int
    memorySize: int
    micphoneName: Optional[str]
    speakerName: Optional[str]


class BasicSettings(TypedDict):
    left: int
    top: int
    width: int
    height: int
    realHeigh: int
    realWidth: int
    isForstStart: bool
    mulFsAddSize: int
    mulFsAutoSize: int
    verticalSync: bool
    fsAutoSize: int
    noiceHypeVOpen: bool
    autoRun: bool
    rootMode: bool
    heightFrameRate: bool
    adbDebug: int
    autoRotate: bool
    isForceLandscape: bool
    standaloneSysVmdk: bool
    lockWindow: bool
    disableMouseFastOpt: bool
    cjztdisableMouseFastOpt_new: int
    HDRQuality: int
    qjcjdisableMouseFast: int
    fps: int
    astc: bool
    rightToolBar: bool


class NetworkSettings(TypedDict):
    networkEnable: bool
    networkSwitching: bool
    networkStatic: bool
    networkAddress: str
    networkGateway: str
    networkSubnetMask: str
    networkDNS1: str
    networkDNS2: str
    networkInterface: Optional[str]


class PropertySettings(TypedDict):
    phoneIMEI: str
    phoneIMSI: str
    phoneSimSerial: str
    phoneAndroidId: str
    phoneModel: str
    phoneManufacturer: str
    macAddress: str
    phoneNumber: Optional[str]


class StatusSettings(TypedDict):
    sharedApplications: str
    sharedPictures: str
    sharedMisc: str
    closeOption: int
    playerName: str


@dataclass
class LeidianConfig:
    propertySettings: PropertySettings
    statusSettings: StatusSettings
    basicSettings: BasicSettings
    networkSettings: NetworkSettings
    advancedSettings: typing.Optional[AdvancedSettings] = None
    hotkeySettings: typing.Optional[HotkeySettings] = None

    @classmethod
    def from_dict(cls, data: dict) -> "LeidianConfig":
        data = parse_dotted_dict(data)
        return cls(**data)

    def to_dict(self) -> dict:
        data = asdict(self)
        data = flatten_nested_dict(data)
        return data
