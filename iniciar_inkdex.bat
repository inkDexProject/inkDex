
@echo off
setlocal
cd /d "%~dp0"
title Inkdex - Inicio

echo.
echo ==========================================
echo          INKDEX - INICIADOR
echo ==========================================
echo.

REM Buscar Python
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH.
    echo Instala Python 3 y vuelve a intentarlo.
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
) else (
    echo Entorno virtual existente.
)

REM Instalar dependencias
echo.
echo Instalando o verificando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

REM Comprobar si ya hay una instancia registrada
if exist "inkdex.pid" (
    set /p INKDEX_PID=<inkdex.pid
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
      "$p=Get-CimInstance Win32_Process -Filter \"ProcessId = %INKDEX_PID%\" -ErrorAction SilentlyContinue; if ($p -and $p.CommandLine -like '*run_inkdex.py*') { exit 0 } else { exit 1 }"
    if not errorlevel 1 (
        echo Inkdex ya esta ejecutandose.
        goto mostrar_direcciones
    )
    del "inkdex.pid" 2>nul
)

REM Iniciar Inkdex en segundo plano
echo.
echo Iniciando Inkdex en segundo plano...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$p = Start-Process -FilePath '%CD%\.venv\Scripts\python.exe' -ArgumentList @('run_inkdex.py','--host','0.0.0.0','--port','5000') -WorkingDirectory '%CD%' -WindowStyle Hidden -PassThru; Set-Content -Path '%CD%\inkdex.pid' -Value $p.Id"

if errorlevel 1 (
    echo ERROR: No se pudo iniciar Inkdex.
    pause
    exit /b 1
)

timeout /t 2 /nobreak >nul

:mostrar_direcciones
echo.
echo ==========================================
echo          INKDEX ESTA INICIADO
echo ==========================================
echo.
echo Direcciones de red:

powershell -NoProfile -Command ^
 "$ips = Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null} | ForEach-Object {$_.IPv4Address.IPAddress}; if ($ips) { $ips | ForEach-Object { Write-Host ('  http://' + $_ + ':5000') } } else { Write-Host '  No se pudo detectar la IP.' }"

echo.
echo En esta PC: http://127.0.0.1:5000
echo Registro: %CD%\logs\inkdex.log
echo PID:
if exist "inkdex.pid" type inkdex.pid
echo.
echo Esta ventana se cerrara en 15 segundos.
timeout /t 15 /nobreak >nul
exit /b 0
