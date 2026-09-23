import json
from pathlib import Path
from fastapi.templating import Jinja2Templates

from .config import settings

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
BASE_DIR = Path(__file__).resolve().parent.parent
DEV = settings.VITE_DEV_MODE


def load_vite_manifest(dev: bool):
    if not dev:
        manifest_path = manifest_path = BASE_DIR / "static" / "dist" / ".vite" / "manifest.json"
        with manifest_path.open() as file:
            return json.load(file)
    else:
        return {}


vite_manifest = load_vite_manifest(DEV)


def vite_asset(entrypoint: str) -> str:
    if DEV:
        return f"http://localhost:5173/{entrypoint}"
    asset = vite_manifest[entrypoint]
    return f"/static/dist/{asset['file']}"


# We don't really need this, vite_asset should work with css file as well
def vite_css(entrypoint: str) -> list[str]:
    if DEV:
        return f"http://localhost:5173/{entrypoint}"
    asset = vite_manifest[entrypoint]
    return [f"/static/dist/{css}" for css in asset.get('css', [])]



templates.env.globals["vite_asset"] = vite_asset
templates.env.globals["vite_css"] = vite_css
