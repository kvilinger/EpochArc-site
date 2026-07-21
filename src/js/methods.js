function sitePath(path) {
  return typeof window.localizedSitePath === 'function' ? window.localizedSitePath(path) : path;
}

// Detect browser language for initial default
function detectBrowserLang() {
  const langs = navigator.languages || [navigator.language || ''];
  for (const l of langs) {
    if (l.startsWith('zh')) return 'zh-Hans';
  }
  return 'en';
}

const state = {
  lang: normalizeLang(localStorage.getItem('epocharc-lang') || detectBrowserLang()),
  theme: localStorage.getItem('epocharc-theme') || 'light'
};

const langSelect = document.getElementById('langSelect');
const themeText = document.getElementById('themeText');
const themeIcon = document.getElementById('themeIcon');

function normalizeLang(lang) {
  return lang === 'zh' || lang === 'zh-CN' || lang === 'zh-Hant' || lang === 'zh-Hans' ? 'zh-Hans' : 'en';
}

function isChinese() {
  return state.lang === 'zh-Hans';
}

function updateLocale() {
  const isZh = isChinese();
  document.documentElement.lang = isZh ? 'zh-Hans' : 'en';
  if (langSelect) langSelect.value = state.lang;
  
  // 动态更新页面 Title
  document.title = isZh ? '方法与来源 · EpochArc' : 'Methodology & Sources · EpochArc';
  
  // 动态更新 Meta Description
  const metaDesc = document.querySelector('meta[name="description"]');
  if (metaDesc) {
    metaDesc.setAttribute('content', isZh 
      ? '了解 EpochArc 如何筛选 AI 里程碑、评估来源证据、计算影响指数并复核可能方向。'
      : 'How EpochArc curates AI milestones, evaluates evidence, scores impact, and reviews possible directions.'
    );
  }

  document.querySelectorAll('[data-zh]').forEach((el) => {
    el.innerText = isZh ? el.getAttribute('data-zh') : el.getAttribute('data-en');
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
      ? '<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"></path>'
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

// 统一方法页侧栏高亮逻辑
const sections = document.querySelectorAll('.panel[id]');
const navLinks = document.querySelectorAll('.methods-nav a');

window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.clientHeight;
    if (window.scrollY >= (sectionTop - 150)) {
      current = section.getAttribute('id');
    }
  });

  navLinks.forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
  });
});

// 全局顶导路由自适应分流，完美规避 http 线上各级 URL 部署 404
document.addEventListener('click', function(e) {
  const logo = e.target.closest('.logo');
  const arcsBtn = e.target.closest('.nav-arcs-btn');
  
  if (logo) {
    e.preventDefault();
    if (window.location.protocol === 'file:') {
      const isSubDir = window.location.pathname.includes('/events/') || window.location.pathname.includes('/arcs/');
      window.location.href = isSubDir ? '../../index.html' : 'index.html';
    } else {
      window.location.href = sitePath('/');
    }
  }
  
  if (arcsBtn) {
    e.preventDefault();
    if (window.location.protocol === 'file:') {
      const isSubDir = window.location.pathname.includes('/events/') || window.location.pathname.includes('/arcs/');
      window.location.href = isSubDir ? '../../arcs.html' : 'arcs.html';
    } else {
      window.location.href = sitePath('/arcs');
    }
  }
});

updateTheme();
