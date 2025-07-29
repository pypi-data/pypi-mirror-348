from .nxos import NXOS
from .ios import IOS
from .junos import Junos
from .panos import PANOS

# from .iosxr_netconf import IOSXRNetconf
from .iosxr import IOSXR
from .asa import ASA

PLATFORM_MAP = {
    "ios": IOS,
    "nxos_ssh": NXOS,
    "junos": Junos,
    "panos": PANOS,
    #    "iosxr_netconf": IOSXRNetconf,
    "iosxr": IOSXR,
    "asa": ASA,
}


def get_network_driver(platform: str):
    """
    Returns network driver based on platform string.
    """
    for valid_platform, driver in PLATFORM_MAP.items():
        if valid_platform == platform:
            return driver

    raise NotImplementedError(f"Unsupported platform {platform}")
