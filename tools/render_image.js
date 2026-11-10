// node render_image.js templates/my-post.html out/post.jpg 1080 1350   (story: 1080 1920)
const {chromium}=require('playwright');const path=require('path');const [,,html,out,w,h]=process.argv;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w||1080,height:+h||1350}});
await p.goto('file://'+path.resolve(html));await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:out,type:out.endsWith('.png')?'png':'jpeg',quality:out.endsWith('.png')?undefined:92});await b.close()})();
