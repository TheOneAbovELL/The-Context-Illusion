@echo off
rem Double-click to start The Context Illusion (checks, then the local interface in your browser).
rem Extra options are passed through, e.g.  start.bat --full   or   start.bat --check
cd /d "%~dp0"
where py >nul 2>nul && (py -3 start.py %*) || (python start.py %*)
if errorlevel 1 pause
