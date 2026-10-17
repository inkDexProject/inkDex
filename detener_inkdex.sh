
#!/usr/bin/env bash

set -u
cd "$(dirname "$0")"

PID_FILE="$PWD/inkdex.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "No se encontró inkdex.pid."
    echo "Inkdex podría no estar iniciado."
    exit 1
fi

PID=$(cat "$PID_FILE")

if ! [[ "$PID" =~ ^[0-9]+$ ]]; then
    echo "El archivo PID no contiene un identificador válido."
    exit 1
fi

if ! kill -0 "$PID" 2>/dev/null; then
    echo "El proceso ya no está activo."
    rm -f "$PID_FILE"
    exit 0
fi

if ! ps -p "$PID" -o args= | grep -Fq "run_inkdex.py"; then
    echo "El PID no parece corresponder a Inkdex."
    echo "No se detuvo ningún proceso."
    exit 1
fi

echo "Deteniendo Inkdex (PID $PID)..."
kill "$PID"

for _ in {1..10}; do
    if ! kill -0 "$PID" 2>/dev/null; then
        rm -f "$PID_FILE"
        echo "Inkdex se ha detenido."
        exit 0
    fi
    sleep 1
done

echo "Inkdex no se detuvo a tiempo."
echo "El proceso sigue activo; revisa su estado manualmente."
exit 1
