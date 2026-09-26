@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
  py -3 tools\preview.py
  goto :finish
)
where python >nul 2>&1
if not errorlevel 1 (
  python tools\preview.py
  goto :finish
)
echo Python is optional and is not required to publish this website.
echo Opening site\index.html directly instead.
start "" "%~dp0site\index.html"
goto :eof
:finish
if errorlevel 1 pause
