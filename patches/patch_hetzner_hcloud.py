"""Patch nullable resource handling in the bundled Hetzner collection."""

from __future__ import annotations

from pathlib import Path


def find_module() -> Path:
    """Find the installed Hetzner server_info module."""
    candidates = [
        path
        for root in (Path("/usr/local/lib"), Path("/usr/share/ansible"))
        for path in root.glob(
            "**/ansible_collections/hetzner/hcloud/plugins/modules/server_info.py"
        )
    ]
    if not candidates:
        raise FileNotFoundError("Hetzner server_info module was not found")
    return candidates[0]

REPLACEMENTS = {
    '"created": server.created.isoformat(),':
        '"created": server.created.isoformat() if server.created is not None else None,',
    '"ipv4_address": server.public_net.ipv4.ip if server.public_net.ipv4 is not None else None,':
        '"ipv4_address": (server.public_net.ipv4.ip\n'
        '                        if server.public_net is not None and server.public_net.ipv4 is not None\n'
        '                        else None),',
    '"ipv6": server.public_net.ipv6.ip if server.public_net.ipv6 is not None else None,':
        '"ipv6": (server.public_net.ipv6.ip\n'
        '                        if server.public_net is not None and server.public_net.ipv6 is not None\n'
        '                        else None),',
    '"private_networks": [net.network.name for net in server.private_net],':
        '"private_networks": [\n'
        '                        net.network.name\n'
        '                        for net in (server.private_net or [])\n'
        '                        if net.network is not None\n'
        '                    ],',
    '"private_networks_info": [{"name": net.network.name, "ip": net.ip} for net in server.private_net],':
        '"private_networks_info": [\n'
        '                        {"name": net.network.name, "ip": net.ip}\n'
        '                        for net in (server.private_net or [])\n'
        '                        if net.network is not None\n'
        '                    ],',
    '"server_type": server.server_type.name,':
        '"server_type": server.server_type.name if server.server_type is not None else None,',
    '"datacenter": server.datacenter.name,':
        '"datacenter": server.datacenter.name if server.datacenter is not None else None,',
    '"datacenter": server.datacenter and server.datacenter.name,':
        '"datacenter": server.datacenter.name if server.datacenter is not None else None,',
    '"location": server.datacenter.location.name,':
        '"location": (server.datacenter.location.name\n'
        '                        if server.datacenter is not None and server.datacenter.location is not None\n'
        '                        else None),',
    '"location": server.location.name,':
        '"location": server.location.name if server.location is not None else None,',
    '"delete_protection": server.protection["delete"],':
        '"delete_protection": (server.protection or {}).get("delete"),',
    '"rebuild_protection": server.protection["rebuild"],':
        '"rebuild_protection": (server.protection or {}).get("rebuild"),',
}


def patch_source(source: str) -> str:
    """Make nullable fields in the module result safe to serialize."""
    for old, new in REPLACEMENTS.items():
        source = source.replace(old, new)
    return source


def main() -> None:
    try:
        module = find_module()
    except FileNotFoundError:
        # Older Ansible distributions do not ship the hetzner.hcloud
        # collection. They still need to build successfully.
        print("Hetzner server_info module not present; nothing to patch")
        return

    original = module.read_text()
    patched = patch_source(original)
    if patched == original:
        print(f"Hetzner server_info module already handles nullable fields: {module}")
        return
    module.write_text(patched)
    print(f"Patched {module}")


if __name__ == "__main__":
    main()
