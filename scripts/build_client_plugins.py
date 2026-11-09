"""Genera la variante Git de Imagina desde la configuración común."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    target = ROOT / "clients" / "imagina"
    target.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "plugin.json").read_text())
    manifest["name"] = "mobysuite-reports-imagina"
    interface = manifest["extensions"]["com.openai"]["interface"]
    interface["displayName"] = "Mobysuite Reports · Imagina"
    interface["shortDescription"] = "Reportes de ventas · Imagina"
    (target / "plugin.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    mcp = json.loads((ROOT / "mcp.json").read_text())
    server = mcp["mcpServers"].pop("mobysuite-reports")
    server["url"] = "https://mcp.mobysuite.com/imagina/reports"
    mcp["mcpServers"]["mobysuite-reports-imagina"] = server
    (target / "mcp.json").write_text(json.dumps(mcp, indent=2) + "\n")
    (target / "assets").mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "assets/icon.png", target / "assets/icon.png")
    (target / "skills/setup").mkdir(parents=True, exist_ok=True)
    skill = (ROOT / "skills/setup/SKILL.md").read_text()
    skill = skill.replace("Copérnico", "__OTHER__").replace("Imagina", "Copérnico").replace("__OTHER__", "Imagina")
    skill = skill.replace("/copernico/reports", "/imagina/reports")
    (target / "skills/setup/SKILL.md").write_text(skill)
    print(f"Variante generada: {target}")


if __name__ == "__main__":
    main()
