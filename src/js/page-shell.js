export function normalizePageLang(value) {
  return /^zh/i.test(value || '') ? 'zh-Hans' : 'en';
}

export function localizedPageText(record, lang) {
  if (record == null) return '';
  if (typeof record === 'string') return record;
  return lang === 'zh-Hans'
    ? (record.zhHans || record.zh || record.en || '')
    : (record.en || record.zhHans || record.zh || '');
}

export function setupPageShell() {
  const savedLang = localStorage.getItem('epocharc-lang');
  const browserLang = navigator.language || navigator.languages?.[0] || 'en';
  const state = {
    lang: normalizePageLang(savedLang || browserLang),
    theme: localStorage.getItem('epocharc-theme') || 'light'
  };

  const applyLocale = () => {
    const useChinese = state.lang === 'zh-Hans';
    document.documentElement.lang = useChinese ? 'zh-Hans' : 'en';
    document.querySelectorAll('[data-zh]').forEach((element) => {
      const value = useChinese ? element.dataset.zh : element.dataset.en;
      if (value !== undefined) element.textContent = value;
    });
    const select = document.getElementById('langSelect');
    if (select) select.value = state.lang;
    document.dispatchEvent(new CustomEvent('epocharc:localechange', { detail: { lang: state.lang } }));
  };

  const applyTheme = () => {
    document.body.dataset.theme = state.theme;
    const icon = document.getElementById('themeIcon');
    if (icon) {
      icon.innerHTML = state.theme === 'dark'
        ? '<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"></path>'
        : '<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"></path>';
    }
  };

  document.getElementById('langSelect')?.addEventListener('change', (event) => {
    state.lang = normalizePageLang(event.target.value);
    localStorage.setItem('epocharc-lang', state.lang);
    applyLocale();
  });

  document.getElementById('themeToggle')?.addEventListener('click', () => {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('epocharc-theme', state.theme);
    applyTheme();
    document.dispatchEvent(new CustomEvent('epocharc:themechange', { detail: { theme: state.theme } }));
  });

  applyTheme();
  applyLocale();

  return {
    get lang() { return state.lang; },
    get theme() { return state.theme; },
    isChinese: () => state.lang === 'zh-Hans',
    localized: (record) => localizedPageText(record, state.lang)
  };
}
