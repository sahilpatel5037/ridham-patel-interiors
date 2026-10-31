// Ridham site media host: serves /pNN.mp4 with byte-range support (iPhone Safari needs 206 answers).
const H={"X-Robots-Tag":"noindex, nofollow, noarchive","Access-Control-Allow-Origin":"*","Cache-Control":"public, max-age=604800","Accept-Ranges":"bytes","X-Content-Type-Options":"nosniff"};
export default {async fetch(req,env){
  const u=new URL(req.url),p=u.pathname;
  if(p==="/robots.txt")return new Response("User-agent: *\nDisallow: /\n",{headers:{...H,"content-type":"text/plain"}});
  const m=p.match(/^\/(p\d\d)\.mp4$/);
  if(!m){ if(p==="/"||p==="/index.html")return new Response('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>.</title>',{headers:{...H,"content-type":"text/html; charset=utf-8"}});
    return new Response("Not found",{status:404,headers:H}); }
  const a=await env.ASSETS.fetch(new Request(u.origin+"/_v/"+m[1]+".mp4"));
  if(!a.ok)return new Response("Not found",{status:404,headers:H});
  const buf=await a.arrayBuffer(),n=buf.byteLength,head=req.method==="HEAD";
  const base={...H,"content-type":"video/mp4"};const et=a.headers.get("etag");if(et)base.ETag=et;
  const r=req.headers.get("range");
  if(r){const mm=/bytes=(\d*)-(\d*)/.exec(r)||["","0",""];let s,e;
    if(mm[1]===""){s=Math.max(0,n-Number(mm[2]||0));e=n-1}else{s=Number(mm[1]);e=mm[2]===""?n-1:Math.min(Number(mm[2]),n-1)}
    if(s>=n||s>e)return new Response(null,{status:416,headers:{...base,"Content-Range":`bytes */${n}`}});
    return new Response(head?null:buf.slice(s,e+1),{status:206,headers:{...base,"Content-Range":`bytes ${s}-${e}/${n}`,"Content-Length":String(e-s+1)}});}
  return new Response(head?null:buf,{headers:{...base,"Content-Length":String(n)}});
}};
