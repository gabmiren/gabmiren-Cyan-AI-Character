import subprocess, numpy as np, sys, json
def segs(path, thr_db=-38, min_sil=0.18, min_speech=0.08):
    raw = subprocess.run(['ffmpeg','-v','error','-i',path,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    x = np.frombuffer(raw,np.int16).astype(np.float32)/32768
    hop=320  # 20ms
    n=len(x)//hop
    rms=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2))+1e-9 for i in range(n)])
    db=20*np.log10(rms)
    v=db>thr_db
    out=[];start=None;last=None
    for i,f in enumerate(v):
        t=i*0.02
        if f:
            if start is None: start=t
            last=t+0.02
        elif start is not None and t-last>=min_sil:
            if last-start>=min_speech: out.append((round(start,2),round(last,2)))
            start=None
    if start is not None: out.append((round(start,2),round(last,2)))
    return out, len(x)/16000
if __name__=='__main__':
    for p in sys.argv[1:]:
        s,d=segs(p); print(p, round(d,2), s)
