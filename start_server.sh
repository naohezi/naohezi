#!/bin/bash

# Wait to make sure we load the server properly.
# Only change this settings if you know what are you doing.
sleep 10

# Navigate to project directory

cd /opt/dashboard || {
  echo "ERROR: cannot cd to /opt/dashboard"
  exit 1
}

# Check packages...
pip || {
  echo "[+] There's no pip package"
  sudo apt install python3-pip
}

# Grab the git clone or gitlab depending for region, check where to update the repo


# Make sure that venv is installed
if [! -f "venv/bin/activate"]; then
  echo "[+] ERROR: Virtual environment not found at /opt/dashboard/venv"
  echo "[+] Creating virtual environment"
  python3 -m venv venv
fi

# Activate  
source venv/bin/activate

if [ -f "requirements.txt"]
  pip install -r requirements.txt
fi

echo "Starting NAS dashboard"
venv/bin/uvicorn dev:app --reload --port 8000 --host 0.0.0.0
