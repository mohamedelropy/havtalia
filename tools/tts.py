# python3 tts.py lines.json outdir   ; lines.json = {"a0":"text", "a1":"text", ...}
# Needs kokoro-onnx + models: see PLAYBOOK.md (Setup). Prints each clip's duration in seconds.
import json, sys, os, soundfile as sf
from kokoro_onnx import Kokoro
M=os.environ.get("KOKORO_DIR",os.path.expanduser("~/kokoro"))
k=Kokoro(f"{M}/kokoro-v1.0.onnx",f"{M}/voices-v1.0.bin")
lines=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True)
for key,txt in lines.items():
    a,sr=k.create(txt,voice="am_michael",speed=1.08,lang="en-us");sf.write(f"{out}/{key}.wav",a,sr);print(key,round(len(a)/sr,2))
