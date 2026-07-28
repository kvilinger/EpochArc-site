import"./modulepreload-polyfill-B5Qt9EMX.js";import{s as B}from"./page-shell-CYs8BIEM.js";const S=B(),b=document.getElementById("trendStart"),M=document.getElementById("trendCategories"),T=document.getElementById("trendResult"),C=document.getElementById("trendStatus"),m=["capability","product","commerce","governance","safety","society"];let u=new Set(["capability","product","governance"]),f=[],x={};function A(t){return String(t??"").replace(/\s*[—–‑]+\s*/g," - ").trim()}function s(t){return A(t).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;")}function i(t,r){return S.isChinese()?r:t}function w(t){var r;return A(S.localized((r=x==null?void 0:x.category)==null?void 0:r[t]))||t}function P(){const t=new URLSearchParams(window.location.search),r=t.get("from");["1950","1990","2010","2020"].includes(r)&&(b.value=r);const e=(t.get("categories")||"").split(",").filter(a=>m.includes(a));e.length&&(u=new Set(e))}function I(){const t=new URL(window.location.href);t.searchParams.set("from",b.value),t.searchParams.set("categories",m.filter(r=>u.has(r)).join(",")),history.replaceState({},"",t)}function E(){M.innerHTML=m.map(t=>{const r=u.has(t);return`<button type="button" class="trend-category-button category-${s(t)} ${r?"is-active":""}" data-category="${s(t)}" aria-pressed="${r}">${s(w(t))}</button>`}).join("")}function q(t,r){const e=Array.from({length:r-t+1},(c,d)=>t+d),a=Object.fromEntries(m.map(c=>[c,Object.fromEntries(e.map(d=>[d,0]))])),g=Object.fromEntries(e.map(c=>[c,[]]));for(const c of f){const d=Number(String(c.date).slice(0,4));if(!(d<t||d>r)){g[d].push(c);for(const $ of c.categories||[])a[$]&&(a[$][d]+=1)}}return{years:e,counts:a,eventsByYear:g}}function O(t,r){return t.map((e,a)=>{const g=r.left+a/Math.max(t.length-1,1)*r.width,c=r.top+r.height-e/r.max*r.height;return`${a?"L":"M"}${g.toFixed(2)},${c.toFixed(2)}`}).join(" ")}function U(t,r){const e={left:54,top:22,width:806,height:304,max:1},a=m.filter(o=>u.has(o));e.max=Math.max(1,...a.flatMap(o=>t.map(n=>r[o][n])));const g=Array.from({length:Math.min(e.max,4)+1},(o,n)=>Math.round(e.max/Math.min(e.max,4)*n)),d=[...new Set(g)].map(o=>{const n=e.top+e.height-o/e.max*e.height;return`<g><line x1="${e.left}" y1="${n}" x2="${e.left+e.width}" y2="${n}" class="trend-grid-line"/><text x="${e.left-12}" y="${n+4}" text-anchor="end" class="trend-axis-label">${o}</text></g>`}).join(""),$=t.length>40?10:t.length>20?5:t.length>10?2:1,y=t.map((o,n)=>n%$!==0&&n!==t.length-1?"":`<text x="${e.left+n/Math.max(t.length-1,1)*e.width}" y="${e.top+e.height+28}" text-anchor="middle" class="trend-axis-label">${o}</text>`).join(""),v=a.map(o=>{const n=t.map(h=>r[o][h]),l=n.map((h,p)=>{const L=e.left+p/Math.max(n.length-1,1)*e.width,k=e.top+e.height-h/e.max*e.height;return`<circle cx="${L}" cy="${k}" r="3.2"><title>${s(`${w(o)} ${t[p]}: ${h}`)}</title></circle>`}).join("");return`<g class="trend-series category-${s(o)}"><path d="${O(n,e)}"/>${l}</g>`}).join("");return`
    <svg class="trend-chart" viewBox="0 0 900 370" role="img" aria-labelledby="trendChartTitle trendChartDesc">
      <title id="trendChartTitle">${s(i("Annual AI milestone density by category","按类别统计的年度 AI 里程碑密度"))}</title>
      <desc id="trendChartDesc">${s(i("Line chart showing curated event counts for the selected categories and period.","折线图展示所选类别和时间范围内的策展事件数量。"))}</desc>
      ${d}${y}${v}
    </svg>`}function F(t,r){const e=m.filter(a=>u.has(a));return`
    <details class="trend-data-details">
      <summary>${s(i("View underlying annual counts","查看年度计数明细"))}</summary>
      <div class="trend-table-wrap">
        <table>
          <thead><tr><th>${s(i("Year","年份"))}</th>${e.map(a=>`<th>${s(w(a))}</th>`).join("")}</tr></thead>
          <tbody>${t.map(a=>`<tr><th>${a}</th>${e.map(g=>`<td>${r[g][a]}</td>`).join("")}</tr>`).join("")}</tbody>
        </table>
      </div>
    </details>`}function j(){if(!f.length)return;const t=Number(b.value),r=Math.max(...f.map(n=>Number(String(n.date).slice(0,4)))),{years:e,counts:a,eventsByYear:g}=q(t,r),c=m.filter(n=>u.has(n)),d=f.filter(n=>{var h;return Number(String(n.date).slice(0,4))>=t&&((h=n.categories)==null?void 0:h.some(p=>u.has(p)))}),y=e.map(n=>({year:n,count:g[n].filter(l=>{var h;return(h=l.categories)==null?void 0:h.some(p=>u.has(p))}).length})).reduce((n,l)=>l.count>n.count?l:n,{year:t,count:0}),v=c.map(n=>({category:n,count:e.reduce((l,h)=>l+a[n][h],0)})),o=v.reduce((n,l)=>l.count>n.count?l:n,v[0]);I(),T.innerHTML=`
    <section class="trend-stat-strip" aria-label="${s(i("Trend summary","趋势摘要"))}">
      <div><span>${s(i("Matching events","匹配事件"))}</span><strong>${d.length}</strong></div>
      <div><span>${s(i("Peak year","峰值年份"))}</span><strong>${y.year}</strong><small>${y.count} ${s(i("events","个事件"))}</small></div>
      <div><span>${s(i("Most active category","最活跃类别"))}</span><strong>${s(w(o.category))}</strong><small>${o.count} ${s(i("category records","条类别记录"))}</small></div>
    </section>
    <section class="trend-figure" aria-labelledby="trendFigureTitle">
      <div class="trend-figure-heading">
        <h2 id="trendFigureTitle">${s(i("Event density over time","事件密度随时间变化"))}</h2>
        <p>${s(i("One event can appear in two series when it has two published categories.","当一个事件有两个已发布类别时，它会同时计入两条序列。"))}</p>
      </div>
      <div class="trend-chart-scroll">
        ${U(e,a)}
      </div>
    </section>
    ${F(e,a)}
    <aside class="trend-method-note">
      <strong>${s(i("How to read this","如何理解"))}</strong>
      <p>${s(i("A rise can reflect more real-world activity, broader source coverage, or EpochArc editorial expansion. Treat the chart as a map of this collection, not a universal market index.","曲线上升可能来自现实活动增加、来源覆盖扩大，或 EpochArc 策展范围扩展。请把它视为本站资料集的地图，而不是全行业指数。"))}</p>
    </aside>`,C.hidden=!0,T.hidden=!1}M.addEventListener("click",t=>{const r=t.target.closest("[data-category]");if(!r)return;const e=r.dataset.category;if(u.has(e)){if(u.size===1)return;u.delete(e)}else u.add(e);E(),j()});b.addEventListener("change",j);document.addEventListener("epocharc:localechange",()=>{f.length&&(E(),j())});async function H(){try{[f,x]=await Promise.all([fetch("/data/events.json").then(t=>{if(!t.ok)throw new Error("events");return t.json()}),fetch("/data/labels.json").then(t=>{if(!t.ok)throw new Error("labels");return t.json()})]),P(),E(),j()}catch{C.textContent=i("Unable to load trend data.","无法加载趋势数据。"),C.classList.add("is-error")}}H();
