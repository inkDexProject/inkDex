
@echo off
setlocal
cd /d "%~dp0"
title Inkdex - Detener

if not exist "inkdex.pid" (
    echo No se encontro el archivo inkdex.pid.
    echo Inkdex podria no estar iniciado.
    pause
    exit /b 1
)

set /p INKDEX_PID=<inkdex.pid

echo Deteniendo Inkdex (PID %INKDEX_PID%)...
taskkill /PID %INKDEX_PID% /T /F >nul 2>&1

if errorlevel 1 (
    echo No se pudo detener el proceso.
    echo Comprueba si sigue ejecutandose.
    pause
    exit /b 1
)

del inkdex.pid
echo Inkdex se ha detenido.
pause
