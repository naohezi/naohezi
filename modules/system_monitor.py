import json
import subprocess

def show_drives():
  result = subprocess.run(["lsblk","-J","-o", "NAME,SIZE"],
        capture_output=True, text=True, check=True
    )
  print(type(json.loads(result.stdout)))
  return json.loads(result.stdout)

def format_disk(selected_disk: str, filesystem: str):
  device = f"/dev/{selected_disk}"  
  if "ext4" == filesystem:
    subprocess.run(["mkfs.ext4", "-F", device], check=True)
  elif "xfs" == filesystem:
    subprocess.run(["mkfs.xfs", "-f", device], check=True)
  #elif "mkfs.ext4" == filesystem:
  #  subprocess.run(["mkfs.ext4", "-F", device], check=True)
  #elif "mkfs.ext4" == filesystem:
  #  subprocess.run(["mkfs.ext4", "-F", device], check=True)
