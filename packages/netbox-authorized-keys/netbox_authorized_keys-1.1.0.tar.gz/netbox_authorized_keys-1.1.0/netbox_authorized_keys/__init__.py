"""Top-level package for NetBox cesnet_services Plugin."""

__author__ = """Jan Krupa"""
__email__ = "jan.krupa@cesnet.cz"
__version__ = "1.1.0"


from netbox.plugins import PluginConfig


class NetBoxAuthorizeKeysConfig(PluginConfig):
    name = "netbox_authorized_keys"
    verbose_name = "NetBox Authorized key Plugin"
    description = ""
    version = __version__
    base_url = "authorized-keys"


config = NetBoxAuthorizeKeysConfig
