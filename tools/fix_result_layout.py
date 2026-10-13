#!/usr/bin/env python3
"""Patch EIS Chinese 1.0 result-label geometry only (stdlib, no game assets)."""
import argparse,hashlib,json,os,shutil,struct,tempfile
from pathlib import Path
SOURCE_SHA256='69c2250dd91cdfd55cd44921419196a4d8fae379009adfd550143149c5e9c6e0'
TARGET_SHA256='1095f8579499c5e53a4576247c90938a403a62ee2b9b07bedcdf723c6db44878'
ISO_SIZE=4643094528
GAME_OFFSET=1567647744
GROUPS=((72064,207),(72644,207),(73340,208),(74732,208))
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(16<<20),b''):h.update(block)
    return h.hexdigest()
def edits(path):
    with path.open('rb') as stream:
        stream.seek(GAME_OFFSET);header=stream.read(24);count,end,bank=struct.unpack_from('<III',header,8)
        if not 511<count<100000:raise ValueError('Unexpected GAME container')
        stream.seek(GAME_OFFSET+24+510*44);member=stream.read(44)
        if member[:32].rstrip(b'\0')!=b'indicator.drm':raise ValueError('Unexpected UI member')
        sector,size,flags=struct.unpack_from('<III',member,32);offset=GAME_OFFSET+bank+sector*2048
        stream.seek(offset);data=stream.read(size)
    if len(data)!=204604:raise ValueError('Unexpected result layout size')
    commands,command_offset,command_stride=struct.unpack_from('<III',data,88)
    uv_count,uv_offset,uv_stride=struct.unpack_from('<III',data,104)
    if (command_stride,uv_count,uv_stride)!=(18,341,8):raise ValueError('Unexpected layout format')
    changes=[]
    for name_offset,uv in GROUPS:
        if struct.unpack_from('<I',data,name_offset+76)[0]!=2 or struct.unpack_from('<I',data,name_offset+88)[0]!=uv:
            raise ValueError('Unexpected result-label reference')
        x,y,width,height=struct.unpack_from('<4H',data,uv_offset+uv*8)
        if (width,height)!=(216,22):raise ValueError('Unexpected Chinese label dimensions')
        start,length=struct.unpack_from('<II',data,name_offset+100)
        if length!=4 or start+length>commands:raise ValueError('Unexpected animation')
        for index in range(start,start+length):
            p=command_offset+index*command_stride+8;old_width,old_height=struct.unpack_from('<hh',data,p)
            if old_width!=14 or old_height not in (0,18):raise ValueError('Layout is not the supported 1.0 baseline')
            changes.append((offset+p,struct.pack('<h',width)))
            if old_height:changes.append((offset+p+2,struct.pack('<h',height)))
    return changes

def main():
    parser=argparse.ArgumentParser(description='Upgrade EIS Chinese 1.0 result-label layout to 1.0.1.')
    parser.add_argument('source',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
    source=args.source.resolve();output=args.output.resolve()
    if source==output or output.exists():raise ValueError('Choose a new output path; input and existing outputs are never overwritten')
    if source.stat().st_size!=ISO_SIZE or digest(source)!=SOURCE_SHA256:raise ValueError('This updater requires the exact Chinese 1.0 ISO; use the cumulative release for an original Japanese disc')
    changes=edits(source);output.parent.mkdir(parents=True,exist_ok=True)
    handle,tmp_name=tempfile.mkstemp(prefix=output.name+'.',suffix='.partial',dir=output.parent);os.close(handle);tmp=Path(tmp_name)
    try:
        shutil.copyfile(source,tmp)
        with tmp.open('r+b')as stream:
            for offset,data in changes:stream.seek(offset);stream.write(data)
            stream.flush();os.fsync(stream.fileno())
        if digest(tmp)!=TARGET_SHA256:raise ValueError('Target verification failed')
        if output.exists():raise FileExistsError(output)
        os.rename(tmp,output)
        print(json.dumps({'version':'1.0.1','iso':str(output),'sha256':TARGET_SHA256,'frame_field_edits':len(changes)},ensure_ascii=False))
    finally:
        if tmp.exists():tmp.unlink()
if __name__=='__main__':main()
