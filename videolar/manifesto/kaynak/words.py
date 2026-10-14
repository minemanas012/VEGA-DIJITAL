import json,numpy as np,wave
from faster_whisper import WhisperModel
m=WhisperModel('large-v3',device='cpu',compute_type='int8',cpu_threads=4)
w=wave.open('../ses16k.wav');a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
segs=json.load(open('segs.json'));out=[];off=0
for s0,s1 in segs:
    ss,_=m.transcribe(a[int(s0*16000):int(s1*16000)],language='tr',word_timestamps=True,condition_on_previous_text=False,beam_size=5)
    ws=[{'w':x.word.strip(),'t':round(x.start+off,2),'e':round(x.end+off,2)} for s in ss for x in s.words]
    out.append({'src':[s0,s1],'out':[round(off,3),round(off+s1-s0,3)],'words':ws})
    print(f"{off:6.2f} ",' '.join(f"{x['w']}@{x['t']}" for x in ws))
    off+=s1-s0
json.dump(out,open('timeline.json','w'),ensure_ascii=False,indent=1);print('total',off)
