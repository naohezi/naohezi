import os
import json
import subprocess

CONFIG_DIR = os.getenv('DASHBOARD_CONFIG_PATH', '/opt/dashboard/config')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'settings.json')

def initial_wizard():
  if os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
      settings = json.load(f)
      return settings
  else:
    run_wizard()

def run_wizard():
  
