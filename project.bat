@echo off

set PYTHONPATH=%~dp0
set PYCACHE_DIR=%PYTHONPATH%__pycache__
set PYTHONPYCACHEPREFIX=%PYCACHE_DIR%

python -m main