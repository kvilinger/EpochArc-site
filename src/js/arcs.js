/* ─── Arc Pages: Language, Theme, Navigation ─── */

function sitePath(path) {
  return typeof window.localizedSitePath === 'function' ? window.localizedSitePath(path) : path;
}

window.navigateToEvent = function(id) {
  if (window.location.protocol === 'file:') {
    window.location.href = `../../events/${id}/index.html`;
  } else {
    window.location.href = sitePath(`/events/${id}/`);
  }
};

// 渐进式增强：用全局事件代理拦截所有 .arc-anchor-event 事件卡片的点击，自动兼容各种协议与 URL 斜杠路径
document.addEventListener('click', function(e) {
  const anchor = e.target.closest('.arc-anchor-event');
  const logo = e.target.closest('.logo');
  const arcsBtn = e.target.closest('.nav-arcs-btn');

  if (anchor) {
    e.preventDefault();
    const slug = anchor.getAttribute('data-event-slug') || anchor.getAttribute('data-event-id');
    if (slug) {
      window.navigateToEvent(slug);
    }
  }

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

(function() {
  const state = {
    lang: 'en',
    theme: localStorage.getItem('epocharc-theme') || 'light'
  };

  // Language detection
  const browserLang = navigator.language || navigator.languages?.[0] || 'en';
  if (/^zh/i.test(browserLang)) {
    state.lang = 'zh-Hans';
  }
  const saved = localStorage.getItem('epocharc-lang');
  if (saved) state.lang = saved;

  function updateLocale() {
    document.querySelectorAll('[data-zh]').forEach(el => {
      const val = state.lang === 'zh-Hans' ? el.dataset.zh : el.dataset.en;
      if (val !== undefined) el.textContent = val;
    });
    const sel = document.getElementById('langSelect');
    if (sel) sel.value = state.lang === 'zh-Hans' ? 'zh-Hans' : 'en';
  }

  function updateTheme() {
    document.body.dataset.theme = state.theme;
    const icon = document.getElementById('themeIcon');
    const text = document.getElementById('themeText');
    if (icon) {
      icon.innerHTML = state.theme === 'dark'
        ? '<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"></path>'
        : '<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"></path>';
    }
    if (text) {
      text.textContent = state.theme === 'dark'
        ? (state.lang === 'zh-Hans' ? '浅色模式' : 'Light Mode')
        : (state.lang === 'zh-Hans' ? '深色模式' : 'Dark Mode');
    }
  }

  // Init
  updateLocale();
  updateTheme();

  // Language switch
  const langSelect = document.getElementById('langSelect');
  if (langSelect) {
    langSelect.addEventListener('change', function() {
      state.lang = this.value;
      localStorage.setItem('epocharc-lang', state.lang);
      updateLocale();
      updateTheme();
    });
  }

  // Theme toggle
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      localStorage.setItem('epocharc-theme', state.theme);
      updateTheme();
    });
  }

  // TOC scroll spy (detail page only)
  const tocLinks = document.querySelectorAll('.arc-toc a');
  if (tocLinks.length > 0) {
    const chapters = [];
    tocLinks.forEach(link => {
      const id = link.getAttribute('href')?.replace('#', '');
      if (id) {
        const el = document.getElementById(id);
        if (el) chapters.push({ link, el });
      }
    });

    function updateActiveToc() {
      let current = null;
      for (const ch of chapters) {
        const rect = ch.el.getBoundingClientRect();
        if (rect.top <= 160) current = ch;
      }
      tocLinks.forEach(l => l.classList.remove('active'));
      if (current) current.link.classList.add('active');
    }

    window.addEventListener('scroll', updateActiveToc, { passive: true });
    updateActiveToc();
  }
})();
