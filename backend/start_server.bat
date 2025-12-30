@echo off
set PYTHONPATH=%~dp0
echo Starting DataClone AI Backend Server...
echo PYTHONPATH set to: %PYTHONPATH%
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
