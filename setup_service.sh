#!/bin/bash

echo "Setting up NAS Dashboard service..."

sudo cp nas-dashboard.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/nas-dashboard.service

chmod +x start_server.sh

sudo systemctl daemon-reload
sudo systemctl start nas-dashboard.service
sudo systemctl enable nas-dashboard.service

echo "To check status: sudo systemctl status nas-dashboard.service"
