#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
HOST=$(uname -s)
ARCH=$(uname -m)
case "$HOST:$ARCH" in
 Darwin:arm64) RUNTIME=macos-arm64 ;;
 Darwin:x86_64) RUNTIME=macos-x64 ;;
 Linux:x86_64|Linux:amd64) RUNTIME=linux-x64 ;;
 Linux:aarch64|Linux:arm64) RUNTIME=linux-arm64 ;;
 *) echo "Unsupported host/architecture: $HOST / $ARCH" >&2; exit 1 ;;
esac
PYTHON="$SCRIPT_DIR/runtime/$RUNTIME/python/bin/python3"
if [ ! -f "$PYTHON" ]; then
 echo "Bundled Python is missing. Extract the complete Encounter in Space ALLPLATFORM 1.0.1 package." >&2
 exit 1
fi
if [ ! -x "$PYTHON" ]; then chmod u+x "$PYTHON"; fi
set +e
"$PYTHON" -I -B -X utf8 "$SCRIPT_DIR/launch.py" "$@"
RESULT=$?
printf "\nPress Enter to close..."
read -r UNUSED
exit "$RESULT"
