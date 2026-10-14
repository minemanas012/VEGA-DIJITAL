import numpy as np, wave
SR=48000; rng=np.random.default_rng(7)
def save(n,x):
    x=(np.clip(x,-1,1)*32767).astype(np.int16); w=wave.open(n,'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes())
def whoosh(d=0.5):
    n=int(SR*d); t=np.linspace(0,1,n); env=np.sin(np.pi*t)**2*(t<1)
    x=rng.standard_normal(n); y=np.zeros(n); a=0.0; lp=0
    cut=200+3500*np.sin(np.pi*t)**1.5
    for i in range(n):
        k=1-np.exp(-2*np.pi*cut[i]/SR); lp+=k*(x[i]-lp); y[i]=lp
    y=y-np.convolve(y,np.ones(40)/40,'same')*0.6
    return 0.9*y/np.abs(y).max()*env
def pop():
    n=int(SR*0.12); t=np.arange(n)/SR; f=520*np.exp(-t*18)+260
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*38)*0.8
def shutter():
    n=int(SR*0.16); x=np.zeros(n)
    for s,a in((0,1.0),(int(SR*0.055),0.7)):
        m=int(SR*0.03); c=rng.standard_normal(m)*np.exp(-np.arange(m)/SR*160)*a; x[s:s+m]+=c
    return 0.8*x/np.abs(x).max()
save('whoosh.wav',whoosh()); save('pop.wav',pop()); save('shutter.wav',shutter()); print('ok')
