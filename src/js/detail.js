// Detect browser language
function detectBrowserLang() {
  const langs = navigator.languages || [navigator.language || ''];
  for (const l of langs) {
    if (l.startsWith('zh')) return 'zh-Hans';
  }
  return 'en';
}

const state = {
  lang: localStorage.getItem('epocharc-lang') || detectBrowserLang(),
  theme: localStorage.getItem('epocharc-theme') || 'light'
};

function normalizeLang(lang) {
  return lang === 'zh' || lang === 'zh-CN' || lang === 'zh-Hant' || lang === 'zh-Hans' ? 'zh-Hans' : 'en';
}

state.lang = normalizeLang(state.lang);

const langSelect = document.getElementById('langSelect');
const themeText = document.getElementById('themeText');
const themeIcon = document.getElementById('themeIcon');

function isChineseContent() {
  return state.lang === 'zh-Hans';
}

function updateLocale() {
  const isZh = isChineseContent();
  document.documentElement.lang = isZh ? 'zh-Hans' : 'en';
  if (langSelect) langSelect.value = state.lang;

  // 动态翻译标有 data-zh/data-en 属性的静态节点
  document.querySelectorAll('[data-zh]').forEach((el) => {
    const zhText = el.getAttribute('data-zh');
    const enText = el.getAttribute('data-en');
    if (zhText && enText) {
      if (el.children.length === 0) {
        el.innerText = isZh ? zhText : enText;
      } else {
        // 如果有子节点，可以通过选择性深层文本节点遍历来实现更完美的递归翻译，这里由于都是简单节点，先这样处理
      }
    }
  });

  if (themeText) {
    themeText.innerText = isZh
      ? (state.theme === 'light' ? '深色模式' : '浅色模式')
      : (state.theme === 'light' ? 'Dark Mode' : 'Light Mode');
  }
}

function updateTheme() {
  document.body.setAttribute('data-theme', state.theme);
  if (themeIcon) {
    themeIcon.innerHTML = state.theme === 'dark'
      ? '<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707M6.343 6.343l-.707-.707m12.728 6.364A9 9 0 115.636 5.636m12.728 12.728A9 9 0 015.636 5.636"></path>'
      : '<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"></path>';
  }
  updateLocale();
}

if (langSelect) {
  langSelect.addEventListener('change', (event) => {
    state.lang = normalizeLang(event.target.value);
    localStorage.setItem('epocharc-lang', state.lang);
    updateLocale();
  });
}

const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('epocharc-theme', state.theme);
    updateTheme();
  });
}

// 关联事件跳转（智能兼容本地 file:// 相对定位与线上 http 绝对根路径定位）
window.navigateToEvent = function(id) {
  if (window.location.protocol === 'file:') {
    window.location.href = `../${id}/index.html`;
  } else {
    window.location.href = `/events/${id}/index.html`;
  }
};

// SVG 拓扑图 Hover 连线高亮
window.highlightLink = function(linkId, doHighlight) {
  const link = document.getElementById(linkId);
  if (link) {
    if (doHighlight) {
      link.classList.add('highlighted');
      link.setAttribute('marker-end', 'url(#arrow-highlighted)');
    } else {
      link.classList.remove('highlighted');
      link.setAttribute('marker-end', 'url(#arrow)');
    }
  }
};

// SVG 拓扑图的 Tooltip 动态加载
window.showEventTooltip = function(event, id) {
  const data = window.relatedEventsData ? window.relatedEventsData[id] : null;
  if (!data) return;

  const tooltip = document.getElementById('global-tooltip');
  if (!tooltip) return;

  const isZh = isChineseContent();
  const titleText = isZh ? data.title.zh : data.title.en;
  const summaryText = isZh ? data.summary.zh : data.summary.en;
  const catName = isZh ? data.category.zh : data.category.en;

  const content = `
    <div style="font-family: var(--font-body); text-align: left; display: flex; flex-direction: column; gap: 6px;">
      <div style="display: flex; align-items: center; justify-content: space-between; font-family: var(--font-mono); font-size: 10px; color: var(--muted); border-bottom: 1px solid var(--border); padding-bottom: 4px; margin-bottom: 2px;">
        <span>${data.date}</span>
        <span style="color: var(--accent); font-weight: 700;">L${data.significance} · ${catName}</span>
      </div>
      <strong style="font-size: 12.5px; color: var(--fg); line-height: 1.4; display: block;">${titleText}</strong>
      <p style="font-size: 11.5px; color: var(--muted); line-height: 1.45; margin: 0;">${summaryText}</p>
    </div>
  `;

  tooltip.innerHTML = content;
  tooltip.classList.add('show');

  const rect = event.currentTarget.getBoundingClientRect();
  let left = rect.left + (rect.width / 2) - 145;
  let top = rect.top - tooltip.offsetHeight - 8;

  if (left < 10) left = 10;
  if (left + 290 > window.innerWidth - 10) {
    left = window.innerWidth - 300;
  }
  if (top < 10) {
    top = rect.bottom + 8;
  }

  tooltip.style.left = `${left + window.scrollX}px`;
  tooltip.style.top = `${top + window.scrollY}px`;
};

window.hideEventTooltip = function() {
  const tooltip = document.getElementById('global-tooltip');
  if (tooltip) {
    tooltip.classList.remove('show');
  }
};

updateTheme();
