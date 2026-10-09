#!/bin/bash
cd -- "$(dirname -- "$0")" || exit 1
case "$(uname -m)" in
 arm64) PY="$PWD/runtime/macos-arm64/python/bin/python3" ;;
 x86_64) PY="$PWD/runtime/macos-x64/python/bin/python3" ;;
 *) echo '暂不支持该Mac架构'; exit 1 ;;
esac
if [ ! -x "$PY" ]; then echo '包内Python不可执行，请按说明恢复本文件和Python的执行权限。'; exit 1; fi
"$PY" -I "$PWD/install.py" "$@"
result=$?
echo
read -r -p '按回车关闭窗口…'
exit "$result"
