@echo off
TITLE AegisVault (SentinEL-4626) Launcher
COLOR 0B
echo ===================================================================
echo           AEGISVAULT: AUTONOMOUS MULTI-AGENT VAULT PROTOCOL
echo                     Production Full-Stack Runner
echo ===================================================================
echo.

cd /d "%~dp0"

echo [1/3] Syncing Blockchain Contracts & Strategy Bindings...
python contracts\scripts\deploy_live.py
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Deployment sync had warnings, continuing...
)

echo.
echo [2/3] Launching Autonomous Multi-Agent Co-Processor (Port 8000)...
start "Aegis Agent Server" cmd /k "cd agents && python server.py"

echo.
echo [3/3] Launching React 19 Institutional Terminal (Port 5173)...
start "Aegis Frontend" cmd /k "cd frontend && npm run dev -- --host"

timeout /t 3 /nobreak >nul
echo.
echo ===================================================================
echo [SUCCESS] All AegisVault services are online!
echo  - Frontend Dashboard: http://localhost:5173/
echo  - Agent Co-Processor: http://localhost:8000/
echo  - Developer CLI:      python cli.py status
echo ===================================================================
echo.
start http://localhost:5173/
