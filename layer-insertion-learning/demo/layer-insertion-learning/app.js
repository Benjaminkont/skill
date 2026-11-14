const stages = [
  ['起点 / 直接认识', '一个事物 a 亮起来', '在漆黑的知识空间中，先遇到 a。给出它的定义，让这个陌生事物获得一个最初的轮廓。', '我知道了 a 的直接含义，但它与周围的关系还未显现。', 'a · 直接定义'],
  ['横向 / 所在层', '照亮 a 所在的 A 层', '让 A 层的其他事物进入视野。通过共同点与差异，反过来辨认 a 的角色、作用和边界。', '周围事物帮助我理解 a；它们的出现服务于当前目标。', 'A · 同层展开'],
  ['跨项目 / 找到邻居', '另一个项目的 x 亮起来', '在独立的项目中，找到与 a 有可比之处的 x。两个事物建立一条较弱的对照关系。', '一个熟悉或更容易理解的邻居，可以来自另一个项目。', 'x · 跨项目邻居'],
  ['横向 / 弱对照', 'X 层也进入视野', '从 x 展开它所在的 X 层，让 a 与这片邻近空间形成弱对照。借相似之处理解，再用差异守住边界。', '两个项目不必完全对应。只取能帮助理解 a 的联系。', 'X · 跨项目展开'],
  ['跨项目 / 再找一个邻居', '项目 03 的 p 亮起来', '把注意力移到第三个独立项目，找到与 a 有可比之处的 p。之前的空间暗下来，当前邻居成为新的观察中心。', '帮助理解 a 的邻居，可以来自多个独立项目。', 'p · 第三个项目'],
  ['横向 / 再次弱对照', '展开 p 所在的 P 层', '让 P 层的其他事物进入视野，与 a 建立弱对照。当前 P 层亮起，之前的 A、X 层保持暗淡。', '注意力转到新的局部空间，用它反过来理解 a。', 'P · 第三项目展开'],
  ['换层 / 上层接口', '沿着关系，点亮 b', 'A 层的上层接口 b 进入视野。带着刚才对 A 层的认识，理解 b 做什么，以及它与 A 层如何连接。', '下层的具体认识，让上层接口的作用变得可理解。', 'b · 进入上层'],
  ['递归 / 新的起点', '以 b 为中心，展开 B 层', '现在 b 成为新的理解目标。让 B 层的其他事物亮起来，再通过同层对照，理解 b 本身。', '在 a 上发生的过程，开始在 b 上重复。', 'B · 重复展开'],
  ['递归 / 再次换层', '继续进入接口 c', '如果理解需要继续向上，沿 B 层的关系进入接口 c。刚才的局部空间，成为理解下一层的依据。', '从事物到所在层，再到下一层的接口，过程可以继续。', 'c · 再次换层'],
  ['递归 / 继续展开', 'C 层亮起，过程继续', '以 c 为新的目标，展开 C 层。递归的形式已经出现：点亮一个事物，照亮其周围，沿接口换层，然后重复。', '每次展开都回到当前目标，让它的含义更清晰。', 'C · 递归展开']
];
const ns = 'http://www.w3.org/2000/svg';
function el(tag, attrs, parent, text) { const n = document.createElementNS(ns, tag); for (const [k,v] of Object.entries(attrs)) n.setAttribute(k,v); if(text)n.textContent=text; parent.appendChild(n); return n; }
const projectRoot = document.querySelector('#projects');
const layers = [], nodes = {}, lines = [];
const points = [[.2,.25],[.45,.25],[.7,.25],[.9,.25],[.2,.65],[.5,.65],[.8,.65]];
const activeLayers = [null, 'A', null, 'X', null, 'P', null, 'B', null, 'C'];
const activeNodes = ['a', null, 'x', null, 'p', null, 'b', null, 'c', null];
function project(x, y, name, color, labels, nodeIds) {
  el('text', {x:x+130,y:y+195,class:'project-label'}, projectRoot, name);
  labels.forEach((label,i)=>{
    const sy=y-i*115, group=el('g',{'data-layer':label},projectRoot);
    const poly=el('polygon',{points:`${x},${sy} ${x+290},${sy-78} ${x+420},${sy+5} ${x+130},${sy+83}`,fill:'#101923',stroke:'#293545','stroke-width':1,class:'slab'},group);
    el('path',{d:`M${x} ${sy}v18l130 83 290-78V${sy+5} M${x+130} ${sy+83}v18`,fill:'none',stroke:'#23303e'},group);
    const title=el('text',{x:x-22,y:sy+6,fill:'#455669',class:'layer-label'},group,label);
    const entries=[];
    points.forEach(([u,v],j)=>{
      const px=x+290*u+130*v, py=sy-78*u+83*v;
      const id = j===2 ? nodeIds[i] : null;
      const g=el('g',{class:'node',...(id?{'data-node':id}:{})},group);
      const halo=el('circle',{cx:px,cy:py,r:16,fill:color,filter:'url(#glow)',opacity:0},g);
      const circle=el('circle',{cx:px,cy:py,r:id?7:4,fill:'#344454'},g);
      const text=el('text',{x:px+13,y:py+5,fill:'#516171',opacity:id?1:0},g,id||'');
      const item={id,px,py,circle,halo,text,color};entries.push(item);if(id)nodes[id]=item;
    });layers.push({label,poly,title,entries,color});
  });
}
project(50,405,'项目 01','#67e5d5',['A','B','C'],['a','b','c']);
project(550,420,'项目 02','#b79aff',['X','Y','Z'],['x',null,null]);
project(1050,435,'项目 03','#f2bb75',['P','Q','R'],['p',null,null]);
const relRoot=document.querySelector('#relations');
function line(from,to,type,steps) {const a=nodes[from],b=nodes[to];const p=el('path',{d:type==='weak'?`M${a.px} ${a.py} C${a.px+170} ${a.py+110},${b.px-100} ${b.py+110},${b.px} ${b.py}`:`M${a.px} ${a.py-10} L${b.px} ${b.py+12}`,stroke:b.color,'stroke-dasharray':type==='weak'?'4 8':'0',opacity:0,class:'relation'},relRoot);lines.push({p,steps,type});}
line('a','x','weak',[2,3]);line('a','p','weak',[4,5]);line('a','b','up',[6,7]);line('b','c','up',[8,9]);
// 弱对照指向当前展开的层；换步后旧层和旧关系都暗下来。
[['X',3,'x'],['P',5,'p']].forEach(([label,step,id])=>{
  layers.find(l=>l.label===label).entries.filter(n=>n.id!==id).forEach(n=>{const a=nodes.a;const p=el('path',{d:`M${a.px} ${a.py} Q${(a.px+n.px)/2} 550 ${n.px} ${n.py}`,stroke:n.color,'stroke-dasharray':'2 10',opacity:0,class:'relation'},document.querySelector('#connections'));lines.push({p,steps:[step],type:'context'});});
});
let current=0,timer=null;
const nav=document.querySelector('#steps');
stages.forEach((s,i)=>{const b=document.createElement('button');b.className='step';b.innerHTML=`<span>${String(i+1).padStart(2,'0')}</span><span>${s[4]}</span>`;b.onclick=()=>{pause();render(i)};nav.appendChild(b);});
function render(i){
  current=i;const s=stages[i];
  document.querySelector('#stage-count').textContent=`${String(i+1).padStart(2,'0')} / ${String(stages.length).padStart(2,'0')}`;
  ['step-kicker','step-title','step-description','step-insight'].forEach((id,j)=>document.getElementById(id).textContent=s[j]);
  document.querySelector('#svg-desc').textContent=`当前步骤 ${i+1}：${s[1]}。${s[2]}`;
  layers.forEach(l=>{
    const full=activeLayers[i]===l.label;
    l.poly.setAttribute('fill',full?l.color+'16':'#101923');l.poly.setAttribute('stroke',full?l.color+'90':'#293545');l.title.setAttribute('fill',full?l.color:'#455669');
    l.entries.forEach(n=>{const lit=full||(n.id&&activeNodes[i]===n.id);n.circle.setAttribute('fill',lit?n.color:'#344454');n.halo.setAttribute('opacity',lit?(n.id?.8:.3):0);n.text.setAttribute('fill',lit?n.color:'#516171');});
  });
  lines.forEach(l=>l.p.setAttribute('opacity',l.steps.includes(i)?(l.type==='context'?.16:l.type==='weak'?.45:.8):0));
  [...nav.children].forEach((b,j)=>{b.className='step'+(j===i?' active':j<i?' done':'');if(j===i)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});
  document.querySelector('#prev').disabled=i===0;document.querySelector('#next').disabled=i===stages.length-1;
  if(!timer)document.querySelector('#play').textContent=i===stages.length-1?'重新播放':'自动播放';
}
function pause(){clearInterval(timer);timer=null;document.querySelector('#play').textContent=current===stages.length-1?'重新播放':'自动播放';}
function toggle(){if(timer){pause();return;}if(current===stages.length-1)render(0);document.querySelector('#play').textContent='暂停播放';timer=setInterval(()=>{render(current+1);if(current===stages.length-1)pause();},4200);}
document.querySelector('#play').onclick=toggle;
document.querySelector('#prev').onclick=()=>{pause();render(Math.max(0,current-1));};
document.querySelector('#next').onclick=()=>{pause();render(Math.min(stages.length-1,current+1));};
document.querySelector('#reset').onclick=()=>{pause();render(0);};
document.addEventListener('keydown',e=>{if(e.target.closest('button,a,input,textarea,select'))return;if(e.code==='Space'){e.preventDefault();toggle();}if(e.key==='ArrowRight'){pause();render(Math.min(stages.length-1,current+1));}if(e.key==='ArrowLeft'){pause();render(Math.max(0,current-1));}});
render(0);
