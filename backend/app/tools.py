# IMPORTANT
# This is entire file is holding older and unused code, utilities.py is the correct one.
# IMPORTANT



import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def load_vite_manifest():
    manifest_path = BASE_DIR / "static" / "dist" / ".vite" / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError(f"Vite manifest was not found: {manifest_path}, Run `npm run build` first")
    with manifest_path.open() as f:
        return json.load(f)


vite_manifest = load_vite_manifest()

DEV = False

if not DEV:
    manifest_path = (BASE_DIR / "static" / "dist" / ".vite" / "manifest.json")
    with manifest_path.open() as f:
        vite_manifest = json.load(f)
else:
    vite_manifest = {}


# This is not used, it's the older version of vite_asset
def vite_asset(entrypoint: str) -> str:
    try:
        asset = vite_manifest[entrypoint]
    except KeyError:
        raise KeyError(f"Vite entry point was not found in manifest: {entrypoint}")
    return f"/static/dist/{asset['file']}"