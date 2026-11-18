import subprocess, numpy as np, cv2
src='v8.mp4'; W,H=720,1280
X0,Y0,X1,Y1=260,560,700,1100
dec=subprocess.Popen(['ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-i',src,'-map','0:v','-map','1:a?','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-shortest','v8_clean.mp4'],stdin=subprocess.PIPE)
k=np.ones((3,3),np.uint8)
while True:
    b=dec.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3).copy()
    hsv=cv2.cvtColor(f[Y0:Y1,X0:X1],cv2.COLOR_RGB2HSV)
    txt=((hsv[...,2]>185)&(hsv[...,1]<70))|((hsv[...,1]>110)&(hsv[...,2]>90))
    m=cv2.dilate(txt.astype(np.uint8)*255,k,iterations=3)
    M=np.zeros((H,W),np.uint8); M[Y0:Y1,X0:X1]=m
    f=cv2.inpaint(f,M,5,cv2.INPAINT_NS)
    enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait()
