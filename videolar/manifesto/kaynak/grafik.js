const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs=require('fs');
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file:///home/user/ham/build/grafik.html'); await p.evaluate(()=>document.fonts.ready);
  const W=await p.evaluate(()=>W);
  const arg=process.argv.slice(2);
  if(arg[0]==='stills'){ for(const t of arg.slice(1)){await p.evaluate(t=>render(+t),t);await p.screenshot({path:`st_${t}.png`,omitBackground:true});} }
  else { fs.mkdirSync('gf',{recursive:true}); const fps=30, N=Math.ceil(48.81*fps); let n=0;
    for(let i=0;i<N;i++){const t=i/fps; if(!Object.values(W).some(([a,c])=>t>=a&&t<=c))continue;
      await p.evaluate(t=>render(t),t); await p.screenshot({path:`gf/${String(i).padStart(5,'0')}.png`,omitBackground:true}); n++;}
    console.log('frames',n); }
  await b.close();
})();
