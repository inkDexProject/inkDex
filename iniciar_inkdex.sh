#!/usr/bin/env bash

set -Eeuo pipefail
cd "$(dirname "$0")"

PROJECT_DIR="$PWD"
VENV="$PROJECT_DIR/.venv"
PYTHON="$VENV/bin/python"
PID_FILE="$PROJECT_DIR/inkdex.pid"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/inkdex.log"

mkdir -p "$LOG_DIR"

echo
echo "=========================================="
echo "          INKDEX - INICIADOR"
echo "=========================================="
echo

# 1. Comprobar Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 no está instalado."

    if command -v apt-get >/dev/null 2>&1; then
        echo "Se intentará instalar Python 3 y venv."
        sudo apt-get update
        sudo apt-get install -y python3 python3-venv
    else
        echo "Instala Python 3 mediante el gestor de paquetes de tu distribución."
        exit 1
    fi
fi

# 2. Comprobar si se puede crear un entorno virtual
if [ ! -x "$PYTHON" ]; then
    echo "Creando entorno virtual..."

    if ! python3 -m venv "$VENV"; then
        echo
        echo "No se pudo crear el entorno virtual."

        if command -v apt-get >/dev/null 2>&1; then
            echo "Instalando el paquete venv..."
            sudo apt-get update
            sudo apt-get install -y python3-venv

            # Reintentar la creación
            python3 -m venv "$VENV"
        else
            echo "Instala el paquete venv correspondiente a tu distribución."
            exit 1
        fi
    fi
fi

# 3. Instalar dependencias

echo
echo "Comprobando pip..."

if ! "$PYTHON" -m pip --version >/dev/null 2>&1; then
    echo "pip no está disponible. Intentando instalarlo..."

    if "$PYTHON" -m ensurepip --upgrade; then
        echo "pip instalado correctamente."
    else
        echo "No se pudo instalar pip automáticamente."
        echo "En Ubuntu/Debian se intentará instalar el paquete necesario."

        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-venv

            echo "Recreando el entorno virtual..."
            rm -rf "$VENV"
            python3 -m venv "$VENV"
        else
            echo "Instala pip y vuelve a ejecutar el lanzador."
            exit 1
        fi
    fi
fi

echo "Instalando o verificando dependencias..."
"$PYTHON" -m pip install -r "$PROJECT_DIR/requirements.txt"


# 4. Comprobar si Inkdex ya está ejecutándose
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")

    if [[ "$OLD_PID" =~ ^[0-9]+$ ]] &&
       kill -0 "$OLD_PID" 2>/dev/null &&
       ps -p "$OLD_PID" -o args= | grep -Fq "run_inkdex.py"; then
        echo
        echo "Inkdex ya está ejecutándose (PID $OLD_PID)."
    else
        rm -f "$PID_FILE"
    fi
fi

# 5. Iniciar si no hay una instancia activa
if [ ! -f "$PID_FILE" ]; then
    echo
    echo "Iniciando Inkdex en segundo plano..."

    nohup "$PYTHON" "$PROJECT_DIR/run_inkdex.py" \
        --host 0.0.0.0 --port 5000 \
        >> "$LOG_FILE" 2>&1 < /dev/null &

    NEW_PID=$!
    echo "$NEW_PID" > "$PID_FILE"

    sleep 2

    if ! kill -0 "$NEW_PID" 2>/dev/null; then
        rm -f "$PID_FILE"
        echo "ERROR: Inkdex no pudo iniciarse."
        echo "Consulta: $LOG_FILE"
        exit 1
    fi
fi

# 6. Mostrar direcciones
echo
echo "=========================================="
echo "          INKDEX ESTÁ INICIADO"
echo "=========================================="
echo
echo "Direcciones detectadas:"

IPS=$(hostname -I 2>/dev/null || true)

if [ -n "$IPS" ]; then
    for IP in $IPS; do
        echo "  http://$IP:5000"
    done
else
    echo "No se detectaron direcciones IP."
fi

echo
echo "En esta PC: http://127.0.0.1:5000"
echo "Registro: $LOG_FILE"

if [ -f "$PID_FILE" ]; then
    echo "PID: $(cat "$PID_FILE")"
fi

echo
echo "La terminal se cerrará en 15 segundos."
sleep 15

