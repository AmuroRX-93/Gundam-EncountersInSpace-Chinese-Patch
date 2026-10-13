from pathlib import Path
import sys, subprocess, os, json
ROOT=Path(__file__).resolve().parent
print("Encounter in Space ALLPLATFORM 1.0.1")
print("1. 从日版原盘生成中文 ISO\n2. 校验已生成 ISO\n3. 查看输出位置说明")
if len(sys.argv)>1:
    args=sys.argv[1:]
else:
    choice=input("请输入 1/2/3，然后回车：").strip()
    if choice=="1": args=[]
    elif choice=="2":
        value=input("将中文 ISO 拖入窗口或输入完整路径：").strip()
        # Use the same standard-library path handling as the installer, without importing via PYTHONPATH.
        if os.name=="posix":
            import shlex
            try:
                parsed=shlex.split(value)
                if len(parsed)==1: value=parsed[0]
            except ValueError: pass
        args=["--verify-result",value.strip('"')]
    elif choice=="3":
        print("默认输出在您选择的日文原版 ISO 旁边，名为 Encounter_in_Space_ALLPLATFORM_1.0.1.iso。")
        print("脚本成功后会显示绝对路径；不是模拟器 dev_hdd0，也不会自动移动到模拟器目录。")
        sys.exit(0)
    else:
        print("未选择有效操作，未修改任何文件。")
        sys.exit(1)
sys.exit(subprocess.call([sys.executable,"-I","-B","-X","utf8",str(ROOT/"install.py"),*args]))
