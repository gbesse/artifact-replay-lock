import hashlib,json,os,platform,re,stat
from pathlib import Path
from .common import integer,unique_ids

def run(data):
    root=Path(data['root']).absolute();files=data['files'];maximum=integer(data.get('maximum_total_bytes',100_000_000),1,100_000_000)
    if not root.is_dir() or len(files)>1000:raise ValueError('root_or_size')
    unique_ids(files,'path');rows=[];total=0
    for item in files:
        raw=item['path']
        if not isinstance(raw,str):raise ValueError('path')
        rel=Path(raw)
        if rel.is_absolute() or '..' in rel.parts or not rel.parts:raise ValueError('path')
        expected=item.get('expected_sha256')
        if expected is not None and (not isinstance(expected,str) or not re.fullmatch('[0-9a-f]{64}',expected)):raise ValueError('sha256')
        cursor=root;symlink=False
        for part in rel.parts:
            cursor=cursor/part
            if cursor.is_symlink():symlink=True;break
        if symlink:rows.append({'path':raw,'state':'symlink_rejected'});continue
        path=root/rel
        try:
            flags=os.O_RDONLY|getattr(os,'O_NOFOLLOW',0);fd=os.open(path,flags)
            with os.fdopen(fd,'rb') as stream:
                before=os.fstat(stream.fileno())
                if not stat.S_ISREG(before.st_mode):rows.append({'path':raw,'state':'not_regular_file'});continue
                if before.st_size>maximum-total:rows.append({'path':raw,'state':'byte_budget_exceeded'});continue
                h=hashlib.sha256();read=0
                while True:
                    chunk=stream.read(min(65536,maximum-total-read+1))
                    if not chunk:break
                    read+=len(chunk)
                    if read>maximum-total:break
                    h.update(chunk)
                after=os.fstat(stream.fileno());current=os.stat(path,follow_symlinks=False)
            total+=min(read,maximum-total)
            if read>before.st_size or (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns) or (current.st_dev,current.st_ino)!=(before.st_dev,before.st_ino):rows.append({'path':raw,'state':'changed_during_read'});continue
            actual=h.hexdigest();rows.append({'path':raw,'state':'recorded_without_expected_hash' if expected is None else 'match' if actual==expected else 'mismatch','sha256':actual,'expected_sha256':expected,'bytes':read})
        except FileNotFoundError:rows.append({'path':raw,'state':'missing'})
        except OSError:rows.append({'path':raw,'state':'unreadable'})
    environment={'python_version':platform.python_version(),'python_implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine()};expected_env=data.get('expected_environment',{})
    if not isinstance(expected_env,dict) or not set(expected_env)<=set(environment) or any(not isinstance(v,str) for v in expected_env.values()):raise ValueError('environment')
    mismatches=[k for k,v in expected_env.items() if environment[k]!=v];manifest={'files':sorted(rows,key=lambda r:r['path']),'observed_environment':environment};digest=hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {**manifest,'manifest_sha256':digest,'all_expected_hashes_match':bool(rows) and all(r['state']=='match' for r in rows),'environment_mismatches':mismatches,'declared_environment_matches':not mismatches,'bytes_read':total,'scope':'local file-content and selected runtime metadata check, not signature, SLSA certification, dependency resolution or adversarial filesystem sandbox'}
