"""Valida lo básico y genera un ZIP de borrador sin credenciales."""

import json
import struct
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "plugin.json").read_text())
    mcp = json.loads((ROOT / "mcp.json").read_text())
    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert mcp["$schema"] == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    extension = manifest["extensions"]["com.openai"]
    interface = extension["interface"]
    assert 0 < len(interface["displayName"]) <= 30
    assert 0 < len(interface["shortDescription"]) <= 30
    assert interface["category"] == "Data & Analytics"
    assert extension["publication"]["countries"] == ["CL"]
    assert extension["review"]["commerce"] is False
    assert "apps" not in manifest and "apps" not in extension
    assert not (ROOT / ".app.json").exists()

    files = {"plugin.json", "mcp.json"}
    for field in ("logo", "composerIcon"):
        path = (ROOT / interface[field]).resolve()
        assert path.is_relative_to(ROOT), "El icono debe estar dentro del paquete"
        data = path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", data[16:24])
        assert 256 <= width == height <= 4096
        assert len(data) <= 5 * 1024 * 1024
        files.add(path.relative_to(ROOT).as_posix())

    server = mcp["mcpServers"]["mobysuite-reports"]
    template = "https://mcp.mobysuite.com/{cliente}/reports"
    assert server["url"] == template
    assert server["extensions"]["com.openai"]["urlTemplates"] == [template]
    for client in ("copernico", "imagina"):
        assert template.format(cliente=client) == f"https://mcp.mobysuite.com/{client}/reports"
    auth = server["extensions"]["com.openai"]["auth"]
    assert auth["type"] == "oauth" and auth["client"]["mode"] == "dcr"
    assert auth["baseScopes"] == ["mcp:tools"]
    assert "clientSecret" not in auth

    destination = ROOT / "dist" / "mobysuite-reports-DRAFT.zip"
    destination.parent.mkdir(exist_ok=True)
    prefix = manifest["name"] + "/"
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(files):
            archive.write(ROOT / relative, prefix + relative)
    with zipfile.ZipFile(destination) as archive:
        assert set(archive.namelist()) == {prefix + name for name in files}
        assert archive.testzip() is None
        for name in ("plugin.json", "mcp.json"):
            json.loads(archive.read(prefix + name))
    print(f"Paquete de borrador generado e inspeccionado: {destination}")
    print("Pendiente de URLs legales, pruebas MCP, casos, demo y revisión del portal.")


if __name__ == "__main__":
    main()
