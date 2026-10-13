#!/usr/bin/env python3
"""Gundam Encounters in Space 1.0 original ISO installer. Python 3.8+, standard library only."""
import argparse, hashlib, json, os, shutil, sys, tempfile, errno
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BLOCK=8*1024*1024

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(BLOCK),b''): h.update(b)
    return h.hexdigest()

def manifest(root):
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if m.get('format')!='gundam-eis-original-fixed-spans-1': raise ValueError('不支持的补丁格式')
    for key in ['source','target','payload']:
        q=m[key]
        if type(q['size']) is not int or q['size']<0: raise ValueError('非法文件大小')
        if len(q['sha256'])!=64 or any(c not in '0123456789abcdef' for c in q['sha256']): raise ValueError('非法SHA256')
    if m['source']['size']!=m['target']['size']: raise ValueError('镜像长度不一致')
    if m['payload']['name']!='update.bin' or m['target']['name']!='Encounter_in_Space_ALLPLATFORM_1.0.iso': raise ValueError('非法文件名')
    cursor=payload_cursor=0
    for r in m['spans']:
        if len(r)!=3 or any(type(v) is not int for v in r): raise ValueError('非法差分记录')
        off,n,p=r
        if off<cursor or n<=0 or off+n>m['target']['size'] or p!=payload_cursor: raise ValueError('差分重叠、越界或数据顺序错误')
        cursor=off+n;payload_cursor+=n
    if payload_cursor!=m['payload']['size']: raise ValueError('差分大小不符')
    return m

def check(path,record,label):
    if path.stat().st_size!=record['size']: raise ValueError(label+'大小不匹配，请选正确版本的完整ISO。')
    if sha(path)!=record['sha256']: raise ValueError(label+'SHA256不匹配。禁止强制跳过校验；旧汉化/其他地区/CHD不能作为本包输入。')

def fat32(path):
    if os.name!='nt': return False
    import ctypes
    buf=ctypes.create_unicode_buffer(1024);fs=ctypes.create_unicode_buffer(128)
    k=ctypes.windll.kernel32
    if not k.GetVolumePathNameW(str(path.resolve()),buf,len(buf)): raise OSError('无法识别目标磁盘')
    if not k.GetVolumeInformationW(buf.value,None,0,None,None,None,fs,len(fs)): raise OSError('无法识别目标文件系统')
    return fs.value.upper() in ('FAT','FAT32')

def apply(source,target,root=ROOT):
    m=manifest(root);source=Path(source).expanduser().resolve();target=Path(target).expanduser().absolute()
    if not source.is_file(): raise ValueError('输入ISO不存在')
    if target.exists() or target.is_symlink(): raise FileExistsError('输出已经存在，请换文件名；不会覆盖。')
    if not target.parent.is_dir(): raise ValueError('输出文件夹不存在')
    if source==target.resolve(): raise ValueError('输入和输出不能是同一文件')
    if fat32(target.parent): raise ValueError('ISO超过4GiB，不能写入FAT32。请使用支持大文件的磁盘。')
    if shutil.disk_usage(target.parent).free < m['target']['size']+64*1024*1024: raise OSError('空间不足，目标磁盘至少还需约4.8GB空闲空间。')
    print('1/4 校验日文原版ISO（约4.64GB，请等待）…',flush=True)
    check(source,m['source'],'输入ISO')
    payload=root/m['payload']['name'];check(payload,m['payload'],'补丁数据')
    tmp=None;lock=target.with_name(target.name+'.install.lock');lock_owned=False;reserved=False
    try:
        with lock.open('x',encoding='utf-8') as f: f.write(str(os.getpid()))
        lock_owned=True
        if target.exists() or target.is_symlink(): raise FileExistsError('输出已存在')
        fd,name=tempfile.mkstemp(prefix='.'+target.name+'.',suffix='.partial',dir=target.parent);tmp=Path(name)
        print('2/4 合成新版ISO，原版保持不变…',flush=True)
        with os.fdopen(fd,'w+b') as out,source.open('rb') as src,payload.open('rb') as patch:
            source_hash=hashlib.sha256()
            for b in iter(lambda:src.read(BLOCK),b''): out.write(b);source_hash.update(b)
            if source_hash.hexdigest()!=m['source']['sha256']: raise ValueError('合成期间输入文件发生变化')
            for off,n,pos in m['spans']:
                out.seek(off);patch.seek(pos)
                while n:
                    data=patch.read(min(n,BLOCK))
                    if not data: raise ValueError('补丁意外截断')
                    out.write(data);n-=len(data)
            out.flush();os.fsync(out.fileno())
        print('3/4 完整读回并校验新版ISO…',flush=True);check(tmp,m['target'],'输出ISO')
        if target.exists() or target.is_symlink(): raise FileExistsError('校验期间出现同名输出，停止提交')
        try:
            os.link(tmp,target)
        except OSError as e:
            if e.errno not in (errno.EPERM,errno.EOPNOTSUPP,errno.ENOTSUP,errno.EXDEV,errno.ENOSYS): raise
            # Filesystems without hard links: reserve the output exclusively first.
            with target.open('xb'): pass
            reserved=True
            os.replace(tmp,target);tmp=None;reserved=False
        if tmp is not None: tmp.unlink();tmp=None
        print('4/4 安装成功：'+str(target),flush=True)
        print('SHA256：'+m['target']['sha256']);return target
    finally:
        if tmp is not None: tmp.unlink(missing_ok=True)
        if reserved: target.unlink(missing_ok=True)
        if lock_owned: lock.unlink(missing_ok=True)

def clean_path(s):
    s=s.strip()
    if os.name=='posix':
        import shlex
        try:
            vals=shlex.split(s)
            if len(vals)==1: return vals[0]
        except ValueError: pass
    return s.strip('"')

def main():
    p=argparse.ArgumentParser(description='高达 相逢在宇宙 日版1.03 → 中文1.0')
    p.add_argument('source',nargs='?',help='完整日文原版ISO')
    p.add_argument('--output',help='新ISO完整路径，不覆盖已有文件')
    p.add_argument('--check-only',action='store_true',help='只检查输入与补丁，不生成ISO')
    p.add_argument('--verify-result',metavar='ISO',help='只校验已生成的1.0 ISO')
    a=p.parse_args();m=manifest(ROOT)
    if a.verify_result:
        check(Path(a.verify_result),m['target'],'1.0 ISO');print('1.0完整校验通过');return
    source=a.source or clean_path(input('将日文原版ISO拖到此窗口后按回车：\n'))
    if not source: raise ValueError('未选择输入')
    if a.check_only:
        check(Path(source),m['source'],'输入ISO');check(ROOT/'update.bin',m['payload'],'补丁');print('输入和补丁校验通过，未修改文件');return
    output=a.output or str(Path(source).expanduser().resolve().parent/m['target']['name'])
    apply(source,output)
if __name__=='__main__':
    try: main()
    except (Exception,KeyboardInterrupt) as e:
        print('\n未完成：'+str(e),file=sys.stderr);sys.exit(1)
