// node render_video.js templates/my-short.html out/silent.mp4 31.5
// The HTML must define a global render(t) that draws the frame at t seconds (see templates/short-example.html).
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
const [,,html,out,durS]=process.argv;const DUR=parseFloat(durS),FPS=30;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(html));await p.evaluate(()=>document.fonts.ready);
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r',String(FPS),out]);
const n=Math.round(DUR*FPS);for(let f=0;f<n;f++){await p.evaluate(t=>render(t),f/FPS);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('frames',n)})();
