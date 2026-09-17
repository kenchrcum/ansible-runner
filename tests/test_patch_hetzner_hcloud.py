from pathlib import Path

import importlib.util


PATCHER_PATH = Path(__file__).parents[1] / "patches/patch_hetzner_hcloud.py"
SPEC = importlib.util.spec_from_file_location("patch_hetzner_hcloud", PATCHER_PATH)
assert SPEC is not None and SPEC.loader is not None
PATCHER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PATCHER)


def test_server_info_nullable_fields_are_guarded() -> None:
    source = """
                    "created": server.created.isoformat(),
                    "ipv4_address": server.public_net.ipv4.ip if server.public_net.ipv4 is not None else None,
                    "ipv6": server.public_net.ipv6.ip if server.public_net.ipv6 is not None else None,
                    "private_networks": [net.network.name for net in server.private_net],
                    "private_networks_info": [{"name": net.network.name, "ip": net.ip} for net in server.private_net],
                    "server_type": server.server_type.name,
                    "datacenter": server.datacenter and server.datacenter.name,
                    "location": server.location.name,
                    "delete_protection": server.protection["delete"],
                    "rebuild_protection": server.protection["rebuild"],
    """

    patched = PATCHER.patch_source(source)

    assert "server.server_type.name if server.server_type is not None else None" in patched
    assert "server.location.name if server.location is not None else None" in patched
    assert "for net in (server.private_net or [])" in patched
    assert '(server.protection or {}).get("delete")' in patched
