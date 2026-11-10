# python3 mix.py silent.mp4 final.mp4 31.5 tts_dir a0:0.3 a1:5.9 a2:12.4 ...
# Lays each voice clip at its start time, ducks the music under the voice, normalizes to -14 LUFS.
import subprocess, sys, os
silent,out,dur,tdir=sys.argv[1],sys.argv[2],float(sys.argv[3]),sys.argv[4]
segs=[(s.split(':')[0],float(s.split(':')[1])) for s in sys.argv[5:]]
music=os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets','music.mp3')
cmd=['ffmpeg','-v','error','-y','-i',silent,'-stream_loop','-1','-i',music]
for s,_ in segs: cmd+=['-i',f'{tdir}/{s}.wav']
fc=[f'[{k+2}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={int(st*1000)}|{int(st*1000)}[s{k}]' for k,(s,st) in enumerate(segs)]
fc.append(''.join(f'[s{k}]' for k in range(len(segs)))+f'amix=inputs={len(segs)}:normalize=0,volume=1.6[vo]')
fc.append('[vo]asplit=2[vo1][vo2]')
fc.append(f'[1:a]atrim=0:{dur},volume=0.3,afade=t=out:st={dur-2}:d=2[mu]')
fc.append('[mu][vo1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck]')
fc.append(f'[duck][vo2]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:{dur}[a]')
cmd+=['-filter_complex',';'.join(fc),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',out]
subprocess.check_call(cmd);print('ok',out)
