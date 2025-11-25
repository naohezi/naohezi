import json
import os
import subprocess
from typing import Dict, List, Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

CONFIG_DIR = os.getenv("DASHBOARD_CONFIG_PATH", "/opt/dashboard/config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")

templates = Jinja2Templates(directory="templates")

FORMAT_COMMANDS = {
    "ext4": ["mkfs.ext4", "-F"],
    "btrfs": ["mkfs.btrfs", "-f"],
    "zfs": ["mkfs.zfs", "-f"],
}


def _ensure_config_dir() -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load_settings() -> Dict:
    _ensure_config_dir()
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_settings(settings: Dict) -> None:
    _ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2)


def list_disks() -> List[Dict]:
    result = subprocess.run(
        ["lsblk", "-J", "-o", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT"],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    return payload.get("blockdevices", [])


def format_disk(device: str, filesystem: str) -> None:
    command = FORMAT_COMMANDS.get(filesystem)
    if not command:
        raise ValueError(f"Unsupported filesystem: {filesystem}")

    subprocess.run([*command, device], check=True)


def mount_disk(device: str, mount_point: str) -> None:
    os.makedirs(mount_point, exist_ok=True)
    subprocess.run(["mount", device, mount_point], check=True)


def prepare_data_directory(mount_point: str, folder_name: Optional[str]) -> Optional[str]:
    if not folder_name:
        return None

    target_path = os.path.join(mount_point, folder_name.strip("/"))
    os.makedirs(target_path, exist_ok=True)
    return target_path


def initial_wizard(request: Request):
    settings = load_settings()

    if settings.get("wizard_complete"):
        return RedirectResponse("/storage", status_code=303)

    return templates.TemplateResponse(
        "wizard-setup.html",
        {
            "request": request,
            "disks": list_disks(),
            "filesystems": list(FORMAT_COMMANDS.keys()),
            "message": None,
        },
    )


def handle_wizard_submission(
    request: Request,
    selected_disk: str,
    filesystem: str,
    mount_path: str,
    data_folder: Optional[str] = None,
):
    device = f"/dev/{selected_disk}"

    format_disk(device, filesystem)
    mount_disk(device, mount_path)
    data_directory = prepare_data_directory(mount_path, data_folder)

    settings = load_settings()
    settings.update(
        {
            "wizard_complete": True,
            "storage": {
                "device": device,
                "filesystem": filesystem,
                "mount_point": mount_path,
                "data_directory": data_directory,
            },
        }
    )
    save_settings(settings)

    return templates.TemplateResponse(
        "wizard-setup.html",
        {
            "request": request,
            "disks": list_disks(),
            "filesystems": list(FORMAT_COMMANDS.keys()),
            "message": "Drive formatted and mounted successfully.",
        },
    )
