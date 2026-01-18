@echo off
chcp 65001 >nul
echo Starting Polymarket Price Monitor Service...
python price_monitor_service.py
pause
