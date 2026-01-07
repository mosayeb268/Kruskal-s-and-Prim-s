@echo off
title Algorithm Project Runner
echo Starting local server...
start "" http://localhost:8000/index.html
python -m http.server 8000
pause
