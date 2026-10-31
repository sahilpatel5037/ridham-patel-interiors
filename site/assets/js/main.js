(function(){
"use strict";
var C=window.SITE_CONFIG||{},d=document,q=function(s,r){return (r||d).querySelector(s)},qa=function(s,r){return [].slice.call((r||d).querySelectorAll(s))};
var reduce=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---- config into the page ---- */
qa("[data-brand]").forEach(function(e){e.textContent=C.BRAND||e.textContent});
qa("[data-person]").forEach(function(e){e.textContent=C.PERSON||e.textContent});
qa("[data-city]").forEach(function(e){e.textContent=C.CITY||e.textContent});
if(C.BRAND&&C.CITY)d.title=C.BRAND+" · "+C.CITY;
var yr=q("#yr");if(yr)yr.textContent=new Date().getFullYear();
function wa(text){var n=String(C.WHATSAPP_NUMBER||"").replace(/\D/g,"");return "https://wa.me/"+(n||"")+"?text="+encodeURIComponent(text||C.WHATSAPP_TEXT||"")}
qa("[data-wa]").forEach(function(a){a.href=wa(a.getAttribute("data-wa-text"));a.target="_blank";a.rel="noopener"});
/* call button: tel: link when CALL_NUMBER is set, otherwise a disabled "coming soon" state */
var callN=String(C.CALL_NUMBER||"").replace(/[^\d+]/g,"");
qa("[data-call]").forEach(function(a){var l=q("[data-call-label]",a)||a;
  if(callN.replace(/\D/g,"").length>=10){a.href="tel:"+(callN.charAt(0)==="+"?callN:"+"+callN);a.classList.remove("is-disabled");a.removeAttribute("aria-disabled");a.removeAttribute("role");l.textContent="Call for Turnkey Project"}
  else{a.removeAttribute("href");a.classList.add("is-disabled");a.setAttribute("aria-disabled","true");l.textContent="Call — number coming soon"}});
qa("[data-ig]").forEach(function(a){if(C.INSTAGRAM_URL)a.href=C.INSTAGRAM_URL;else a.hidden=true});
function media(f){var m=C.MEDIA_URLS||{};return m[f]||((C.MEDIA_BASE||"media/")+f)}

/* ---- cover / countdown ---- */
var root=d.documentElement,cover=q("#cover");
if(root.classList.contains("has-cover")&&cover){
  var mode=String(C.COUNTDOWN_MODE||"auto").toLowerCase(),t=Date.parse(C.LAUNCH_AT||""),cd=q("#cd");if(mode==="auto")mode="countdown";
  var pad=function(n){return (n<10?"0":"")+n};
  var paint=function(){var s=Math.max(0,Math.floor((t-Date.now())/1000));
    q('[data-u="d"]',cd).textContent=pad(Math.floor(s/86400));q('[data-u="h"]',cd).textContent=pad(Math.floor(s%86400/3600));
    q('[data-u="m"]',cd).textContent=pad(Math.floor(s%3600/60));q('[data-u="s"]',cd).textContent=pad(s%60);return s};
  /* "paused" = "Launching soon" with no timer; "countdown" = live timer to LAUNCH_AT, then the site opens by itself */
  if(!isNaN(t)&&mode==="countdown"){cd.hidden=false;paint();
    var iv=setInterval(function(){if(paint()<=0){clearInterval(iv);cover.classList.add("is-gone");root.classList.remove("has-cover");startVideos()}},1000)}
}

/* ---- reveal from the countdown screen: curtains open on the site, then leave ---- */
if(root.classList.contains("rp-reveal")){setTimeout(function(){var r=q("#rv");if(r)r.remove();root.classList.remove("rp-reveal")},reduce?100:2600)}

/* ---- topbar: glass on scroll, active section, full-screen menu ---- */
var nav=q("#nav"),fab=q(".fab"),burger=q(".nav__burger"),menu=q("#menu");
/* simple call links (header pill, "Call for Turnkey", menu): tel: when CALL_NUMBER is set, else they jump to the turnkey section */
qa("[data-tel]").forEach(function(a){if(callN.replace(/\D/g,"").length>=10)a.href="tel:"+(callN.charAt(0)==="+"?callN:"+"+callN)});
var secLinks=qa(".nav__links a[data-sec]"),secs=qa("main section[id]"),ticking=false;
function activeSec(){ticking=false;var mark=window.innerHeight*.35,cur="";
  for(var i=0;i<secs.length;i++){if(secs[i].getBoundingClientRect().top<=mark)cur=secs[i].id}
  if((window.innerHeight+window.scrollY)>=d.documentElement.scrollHeight-4)cur=secs[secs.length-1].id;
  secLinks.forEach(function(a){var on=a.getAttribute("data-sec")===cur;a.classList.toggle("is-active",on);if(on)a.setAttribute("aria-current","true");else a.removeAttribute("aria-current")})}
function onScroll(){var y=window.scrollY;nav.classList.toggle("is-solid",y>12);if(fab)fab.classList.toggle("is-on",y>window.innerHeight*.6);
  if(!ticking){ticking=true;(window.requestAnimationFrame||setTimeout)(activeSec)}}
window.addEventListener("scroll",onScroll,{passive:true});window.addEventListener("resize",onScroll,{passive:true});onScroll();
function setMenu(open,focusBack){
  burger.setAttribute("aria-expanded",String(open));burger.setAttribute("aria-label",open?"Close menu":"Open menu");
  if(open){var sb=window.innerWidth-d.documentElement.clientWidth;if(sb>0)d.body.style.paddingRight=sb+"px";
    root.classList.add("menu-open");menu.removeAttribute("inert");menu.classList.add("is-open");
    var f=q(".menu__links a",menu);if(f)setTimeout(function(){f.focus({preventScroll:true})},reduce?0:120)}
  else{root.classList.remove("menu-open");d.body.style.paddingRight="";menu.classList.remove("is-open");menu.setAttribute("inert","");if(focusBack)burger.focus({preventScroll:true})}
}
burger.addEventListener("click",function(){setMenu(burger.getAttribute("aria-expanded")!=="true",false)});
qa("a",menu).forEach(function(a){a.addEventListener("click",function(){setMenu(false,false)})});
d.addEventListener("keydown",function(e){if((e.key==="Escape"||e.key==="Esc")&&menu.classList.contains("is-open"))setMenu(false,true)});
/* keep Tab key inside the open menu (header buttons + menu) */
d.addEventListener("keydown",function(e){if(e.key!=="Tab"||!menu.classList.contains("is-open"))return;
  var f=[burger].concat(qa("a",menu)),i=f.indexOf(d.activeElement);
  if(e.shiftKey&&(i<=0)){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&i===f.length-1){e.preventDefault();f[0].focus()}else if(i<0){e.preventDefault();f[0].focus()}});
window.matchMedia("(min-width:1024px)").addEventListener&&window.matchMedia("(min-width:1024px)").addEventListener("change",function(m){if(m.matches)setMenu(false,false)});

/* ---- reveal ---- */
if("IntersectionObserver" in window&&!reduce){
  var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("is-in");ro.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px",threshold:.08});
  qa(".reveal").forEach(function(e){ro.observe(e)});
}else qa(".reveal").forEach(function(e){e.classList.add("is-in")});

/* ---- videos: load near the viewport, play only while visible ---- */
var heroV=q(".arch__video");
function attach(v){if(!v.src){v.src=media(v.getAttribute("data-video"));v.load()}}
function play(v){var p=v.play();if(p&&p.catch)p.catch(function(){})}
var cardVids=[];
qa(".card__media[data-video]").forEach(function(b){
  var v=d.createElement("video");v.muted=true;v.defaultMuted=true;v.loop=true;v.playsInline=true;v.setAttribute("playsinline","");v.setAttribute("muted","");v.preload="none";
  v.setAttribute("aria-hidden","true");v.setAttribute("data-video",b.getAttribute("data-video"));
  v.addEventListener("playing",function(){v.classList.add("is-ready")});
  b.insertBefore(v,b.querySelector(".card__play"));cardVids.push(v);
});
function startVideos(){
  if(reduce){return}
  if(heroV){attach(heroV);play(heroV)}
  if(!("IntersectionObserver" in window))return;
  var near=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){attach(e.target);near.unobserve(e.target)}})},{rootMargin:"300px 0px"});
  var vis=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting&&!d.hidden&&lb.hidden){attach(v);play(v)}else v.pause()})},{threshold:.35});
  cardVids.concat(heroV?[heroV]:[]).forEach(function(v){near.observe(v);vis.observe(v)});
}
if(!root.classList.contains("has-cover"))startVideos();
d.addEventListener("visibilitychange",function(){if(d.hidden)qa("video").forEach(function(v){v.pause()})});

/* ---- filters ---- */
qa(".chip").forEach(function(c){c.addEventListener("click",function(){
  var f=c.getAttribute("data-f");qa(".chip").forEach(function(x){var on=x===c;x.classList.toggle("is-on",on);x.setAttribute("aria-selected",String(on))});
  qa("#grid .card:not(.card--more)").forEach(function(card){var cats=(card.getAttribute("data-cat")||"").split(" ");card.classList.toggle("is-hidden",!(f==="all"||cats.indexOf(f)>-1))});
  fillGap();
})});
/* filter views end even: the "See all projects" tile takes whatever cells the last row leaves empty */
var moreCard=q("#moreCard"),gridEl=q("#grid");
function fillGap(){
  if(!moreCard||!gridEl)return;
  var on=q(".chip.is-on"),f=on?on.getAttribute("data-f"):"all";
  var cols=getComputedStyle(gridEl).gridTemplateColumns.split(" ").filter(Boolean).length||1,cells=0;
  qa("#grid .card:not(.card--more)").forEach(function(c){if(!c.classList.contains("is-hidden"))cells+=c.classList.contains("card--wide")?Math.min(2,cols):1});
  var rem=(cols-cells%cols)%cols;
  if(f!=="all"&&rem>0){moreCard.style.gridColumn="span "+rem;moreCard.hidden=false}else{moreCard.hidden=true;moreCard.style.gridColumn=""}
}
if(moreCard){
  var tot=q("[data-total]",moreCard);if(tot)tot.textContent=String(qa("#grid .card:not(.card--more)").length);
  var sa=q("[data-showall]",moreCard);if(sa)sa.addEventListener("click",function(){var all=q('.chip[data-f="all"]');if(all){all.click();all.focus({preventScroll:true})}});
  var rt;addEventListener("resize",function(){clearTimeout(rt);rt=setTimeout(fillGap,120)});
}

/* ---- lightbox ---- */
var lb=q("#lb"),lbV=q("#lbVideo"),items=qa("#grid .card[data-index]"),cur=0,lastFocus=null;
function visibleItems(){return items.filter(function(c){return !c.classList.contains("is-hidden")})}
function show(card){
  var b=q(".card__media",card);cur=visibleItems().indexOf(card);
  q("#lbTitle").textContent=q(".card__title",card).textContent;
  q("#lbMeta").innerHTML=q(".card__meta",card).innerHTML;
  q("#lbInfo").innerHTML="";q("#lbInfo").appendChild(q("template",card).content.cloneNode(true));
  lbV.poster=q("img",b).getAttribute("src");lbV.src=media(b.getAttribute("data-video"));playLb();
}
/* sound: grid previews stay muted; the lightbox starts muted with a "Tap for sound" button (Sahil OK'd 31 Oct); once turned on it stays on for the next clips */
var lbSnd=q("#lbSnd"),wantSound=false;
function sndUI(){lbSnd.setAttribute("aria-pressed",String(!lbV.muted));lbSnd.setAttribute("aria-label",lbV.muted?"Turn sound on":"Mute");}
function playLb(){lbV.muted=!wantSound;var p=lbV.play();
  if(p&&p.catch)p.catch(function(){if(!lbV.muted){lbV.muted=true;var p2=lbV.play();if(p2&&p2.catch)p2.catch(function(){})}sndUI()});sndUI()}
lbSnd.addEventListener("click",function(e){e.stopPropagation();wantSound=lbV.muted;lbV.muted=!wantSound;if(lbV.paused)play(lbV);sndUI()});
lbV.addEventListener("volumechange",sndUI);
function open(card){lastFocus=d.activeElement;qa("video").forEach(function(v){if(v!==lbV)v.pause()});lb.hidden=false;d.body.style.overflow="hidden";show(card);q(".lb__x",lb).focus()}
function close(){lb.hidden=true;lbV.pause();lbV.muted=true;lbV.removeAttribute("src");lbV.load();d.body.style.overflow="";if(lastFocus)lastFocus.focus();
  cardVids.concat(heroV?[heroV]:[]).forEach(function(v){var r=v.getBoundingClientRect();if(v.src&&r.bottom>0&&r.top<innerHeight)play(v)})}
function step(n){var v=visibleItems();if(!v.length)return;cur=(cur+n+v.length)%v.length;show(v[cur])}
items.forEach(function(card){q(".card__media",card).addEventListener("click",function(){open(card)})});
qa("[data-close]",lb).forEach(function(e){e.addEventListener("click",close)});
q("#lbPrev").addEventListener("click",function(){step(-1)});q("#lbNext").addEventListener("click",function(){step(1)});
d.addEventListener("keydown",function(e){if(lb.hidden)return;if(e.key==="Escape")close();if(e.key==="ArrowRight")step(1);if(e.key==="ArrowLeft")step(-1)});
var sx=null;lb.addEventListener("touchstart",function(e){sx=e.touches[0].clientX},{passive:true});
lb.addEventListener("touchend",function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50)step(dx<0?1:-1);sx=null});

/* ---- consultation form -> WhatsApp ---- */
var form=q("#form"),err=q("#formErr");
form.addEventListener("submit",function(e){e.preventDefault();var f=form.elements,name=f.name.value.trim(),area=f.area.value,space=f.space.value;
  if(!name||!area||!space){err.hidden=false;(!name?f.name:!area?f.area:f.space).focus();return}err.hidden=true;
  var lines=["Hi Ridham, I would like a free consultation.","Name: "+name,"Area: "+area,"Space: "+space];
  if(f.size.value.trim())lines.push("Home type / size: "+f.size.value.trim());
  if(f.msg.value.trim())lines.push("Message: "+f.msg.value.trim());
  window.open(wa(lines.join("\n")),"_blank","noopener");
});
})();

/* live background: slow gold dust (canvas). Pauses when the tab is hidden; off for reduced motion and the minimal theme. */
(function(){
var cv=document.querySelector(".bgfx .dust"),root=document.documentElement;
if(!cv||!cv.getContext)return;
var tc={dark:"#11100E",minimal:"#FFFFFF",earthy:"#F2E9DA"}[root.getAttribute("data-theme")]||"#11100E",mt=document.querySelector('meta[name="theme-color"]');if(mt)mt.setAttribute("content",tc);
if(root.getAttribute("data-theme")==="minimal"||(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches))return;
var x=cv.getContext("2d"),W=0,H=0,dpr=Math.min(window.devicePixelRatio||1,2),P=[],raf=0,last=0;
var rgb=(getComputedStyle(root).getPropertyValue("--dust")||"226,196,140").trim();
function size(){W=innerWidth;H=innerHeight;cv.width=W*dpr;cv.height=H*dpr;x.setTransform(dpr,0,0,dpr,0,0);
  var n=Math.round(Math.min(W<700?38:70,W*H/16000));while(P.length<n)P.push(mk(true));P.length=n}
function mk(any){return{x:Math.random()*W,y:any?Math.random()*H:H+10,r:Math.random()*1.5+.4,vy:-(Math.random()*.18+.05),vx:(Math.random()-.5)*.12,a:Math.random()*.5+.15,t:Math.random()*6.28,s:Math.random()*.02+.006}}
function draw(ts){raf=requestAnimationFrame(draw);var dt=Math.min(3,(ts-last)/16.7||1);last=ts;x.clearRect(0,0,W,H);
  for(var i=0;i<P.length;i++){var p=P[i];p.y+=p.vy*dt;p.x+=p.vx*dt+Math.sin(p.t)*.08;p.t+=p.s*dt;if(p.y<-10||p.x<-10||p.x>W+10){P[i]=mk(false);continue}
    var al=p.a*(.55+.45*Math.sin(p.t*2));x.beginPath();x.fillStyle="rgba("+rgb+","+al.toFixed(3)+")";x.arc(p.x,p.y,p.r,0,6.283);x.fill();
    if(p.r>1.4){x.beginPath();x.fillStyle="rgba("+rgb+","+(al*.18).toFixed(3)+")";x.arc(p.x,p.y,p.r*3.2,0,6.283);x.fill()}}}
size();addEventListener("resize",size);raf=requestAnimationFrame(draw);
document.addEventListener("visibilitychange",function(){if(document.hidden){cancelAnimationFrame(raf);raf=0}else if(!raf){last=0;raf=requestAnimationFrame(draw)}});
})();
