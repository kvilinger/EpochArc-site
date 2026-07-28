import"./modulepreload-polyfill-B5Qt9EMX.js";import{s as M}from"./page-shell-CYs8BIEM.js";const I=M(),p=document.getElementById("eventA"),u=document.getElementById("eventB"),B=document.getElementById("comparisonResult"),b=document.getElementById("compareStatus"),y=document.getElementById("copyCompareUrl");let i=[],d={};function E(e){return String(e??"").replace(/\s*[—–‑]+\s*/g," - ").trim()}function n(e){return E(e).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;")}function s(e,t){return I.isChinese()?t:e}function c(e){return E(I.localized(e))}function w(e,t){var a;return c((a=d==null?void 0:d[e])==null?void 0:a[t])||E(t).replaceAll("_"," ")}function T(e){return c(e.displayDate)||e.date}function D(e){return`${T(e)} | ${c(e.title)}`}function x(e){const t={};for(const a of e.impacts||[]){const r=t[a.dimension];(r==null||Math.abs(a.severity)>Math.abs(r))&&(t[a.dimension]=a.severity)}return t}function A(e){if(e==null)return'<span class="compare-empty">0</span>';const t=e>0?"is-positive":e<0?"is-negative":"",a=e>0?"+":"";return`<strong class="impact-value ${t}">${a}${e}</strong>`}function H(e){return(e.categories||[]).map(t=>`<span class="compare-category category-${n(t)}">${n(w("category",t))}</span>`).join("")}function S(e){return`
    <article class="compare-event-header">
      <div class="compare-event-date">${n(T(e))}</div>
      <h2>${n(c(e.title))}</h2>
      <div class="compare-category-list">${H(e)}</div>
    </article>`}function m(e,t,a,r=""){return`
    <div class="compare-row ${r}">
      <div class="compare-row-label">${n(e)}</div>
      <div>${t}</div>
      <div>${a}</div>
    </div>`}function k(e,t){const a=new URL(window.location.href);a.searchParams.set("a",e.slug),a.searchParams.set("b",t.slug),history.replaceState({},"",a)}function g(){var o,f,C,L;if(!i.length)return;const e=i.find(l=>l.slug===p.value),t=i.find(l=>l.slug===u.value);if(!e||!t)return;k(e,t);const a=x(e),r=x(t),v=Object.keys(d.impactDimension||{}),h=e.slug===t.slug,$=v.map(l=>m(w("impactDimension",l),A(a[l]),A(r[l]),"compare-impact-row")).join("");B.innerHTML=`
    ${h?`<div class="compare-notice">${n(s("Choose two different events for a meaningful comparison.","请选择两个不同事件以获得有意义的对比。"))}</div>`:""}
    <section class="compare-event-grid" aria-label="${n(s("Selected events","已选事件"))}">
      <div aria-hidden="true"></div>
      ${S(e)}
      ${S(t)}
    </section>

    <section class="compare-table" aria-labelledby="compareMetricsTitle">
      <h2 id="compareMetricsTitle">${n(s("Structural comparison","结构对比"))}</h2>
      ${m(s("Metric","指标"),'<span class="compare-column-name">A</span>','<span class="compare-column-name">B</span>',"compare-column-head")}
      ${m(s("Significance","历史重要度"),`<strong class="compare-large-value">L${e.significance}</strong>`,`<strong class="compare-large-value">L${t.significance}</strong>`)}
      ${m(s("Impact index","影响指数"),`<strong class="compare-large-value">${e.impactIndex}<small>/10</small></strong>`,`<strong class="compare-large-value">${t.impactIndex}<small>/10</small></strong>`)}
      ${m(s("Consensus","解读共识"),`<strong>${n(w("consensus",e.consensusLevel))}</strong>`,`<strong>${n(w("consensus",t.consensusLevel))}</strong>`)}
      ${m(s("Evidence sources","来源数量"),`<strong>${((o=e.sources)==null?void 0:o.length)||0}</strong>`,`<strong>${((f=t.sources)==null?void 0:f.length)||0}</strong>`)}
      ${m(s("Claims","主张数量"),`<strong>${((C=e.claims)==null?void 0:C.length)||0}</strong>`,`<strong>${((L=t.claims)==null?void 0:L.length)||0}</strong>`)}
    </section>

    <section class="compare-table compare-impacts" aria-labelledby="compareImpactTitle">
      <h2 id="compareImpactTitle">${n(s("Impact dimensions","影响维度"))}</h2>
      <p>${n(s("Signed severity from -3 to +3. Zero means the event has no published assessment in that dimension.","带方向的严重度范围为 -3 到 +3。0 表示该事件在该维度没有已发布评估。"))}</p>
      ${$}
    </section>

    <section class="compare-reading" aria-labelledby="compareContextTitle">
      <h2 id="compareContextTitle">${n(s("Historical context","历史语境"))}</h2>
      <div class="compare-reading-grid">
        <article>
          <h3>${n(c(e.title))}</h3>
          <p>${n(c(e.searchSummary||e.summary))}</p>
          <a href="/events/${n(e.slug)}/">${n(s("Open event detail","查看事件详情"))} →</a>
        </article>
        <article>
          <h3>${n(c(t.title))}</h3>
          <p>${n(c(t.searchSummary||t.summary))}</p>
          <a href="/events/${n(t.slug)}/">${n(s("Open event detail","查看事件详情"))} →</a>
        </article>
      </div>
    </section>`,b.hidden=!0,B.hidden=!1}function j(){const e=[...i].sort((o,f)=>f.date.localeCompare(o.date)),t=e.map(o=>`<option value="${n(o.slug)}">${n(D(o))}</option>`).join(""),a=p.value,r=u.value;p.innerHTML=t,u.innerHTML=t;const v=new URLSearchParams(window.location.search),h=a||v.get("a")||"deep-blue",$=r||v.get("b")||"alphago";p.value=i.some(o=>o.slug===h)?h:e[0].slug,u.value=i.some(o=>o.slug===$)?$:e[1].slug}async function P(){try{[i,d]=await Promise.all([fetch("/data/events.json").then(e=>{if(!e.ok)throw new Error("events");return e.json()}),fetch("/data/labels.json").then(e=>{if(!e.ok)throw new Error("labels");return e.json()})]),j(),g()}catch{b.textContent=s("Unable to load comparison data.","无法加载对比数据。"),b.classList.add("is-error")}}p.addEventListener("change",g);u.addEventListener("change",g);document.getElementById("swapEvents").addEventListener("click",()=>{const e=p.value;p.value=u.value,u.value=e,g()});y.addEventListener("click",async()=>{try{await navigator.clipboard.writeText(window.location.href),y.textContent=s("Copied","已复制")}catch{y.textContent=s("Copy failed","复制失败")}window.setTimeout(()=>{y.textContent=s("Copy comparison link","复制对比链接")},1600)});document.addEventListener("epocharc:localechange",()=>{i.length&&(j(),g())});P();
