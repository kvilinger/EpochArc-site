const LANGUAGES = {
      en: { html: 'en', content: 'en' },
      'zh-Hans': { html: 'zh-Hans', content: 'zh' }
    };

    function sitePath(path) {
      return typeof window.localizedSitePath === 'function' ? window.localizedSitePath(path) : path;
    }

    const UI_TEXT = {
      darkMode: { en: 'Dark Mode', es: 'Modo oscuro', ja: 'ダーク', 'zh-Hans': '深色模式', 'zh-Hant': '深色模式', fr: 'Mode sombre' },
      lightMode: { en: 'Light Mode', es: 'Modo claro', ja: 'ライト', 'zh-Hans': '浅色模式', 'zh-Hant': '淺色模式', fr: 'Mode clair' },
      loadingPredictions: { en: 'Loading possible directions', 'zh-Hans': '正在加载可能方向' },
      loadingPredictionsBody: { en: 'The page is loading structured content files.', 'zh-Hans': '页面正在读取独立数据文件。' },
      predictionsError: { en: 'Possible directions unavailable', 'zh-Hans': '可能方向加载失败' },
      predictionsErrorBody: { en: 'Serve the site over HTTP and verify that data/forecasts.json is reachable.', 'zh-Hans': '请通过静态服务器访问站点，或检查 data/forecasts.json 是否可用。' },
      loadingTimeline: { en: 'Loading timeline', es: 'Cargando cronología', ja: 'タイムラインを読み込み中', 'zh-Hans': '正在加载时间轴', 'zh-Hant': '正在載入時間軸', fr: 'Chargement de la chronologie' },
      loadingTimelineBody: { en: 'The site is loading timeline data from JSON.', es: 'El sitio está cargando la cronología desde JSON.', ja: 'JSON からタイムラインを読み込んでいます。', 'zh-Hans': '站点正在加载独立事件数据。', 'zh-Hant': '網站正在載入獨立事件資料。', fr: 'Le site charge les données de chronologie depuis JSON.' },
      timelineError: { en: 'Timeline unavailable', es: 'Cronología no disponible', ja: 'タイムラインを利用できません', 'zh-Hans': '时间轴数据加载失败', 'zh-Hant': '時間軸資料載入失敗', fr: 'Chronologie indisponible' },
      timelineErrorBody: { en: 'This build depends on static JSON files. Make sure data/events.json is deployed.', es: 'Esta versión depende de archivos JSON estáticos. Asegúrate de publicar data/events.json.', ja: 'このビルドは静的 JSON に依存します。data/events.json が公開されているか確認してください。', 'zh-Hans': '当前版本依赖静态 JSON 文件，请确认部署时包含 data/events.json。', 'zh-Hant': '目前版本依賴靜態 JSON 檔案，請確認部署時包含 data/events.json。', fr: 'Cette version dépend de fichiers JSON statiques. Vérifiez que data/events.json est déployé.' },
      openMethodology: { en: 'Open methodology', es: 'Ver metodología', ja: '方法を見る', 'zh-Hans': '查看方法页', 'zh-Hant': '查看方法頁', fr: 'Voir la méthodologie' },
      reviewDirection: { en: 'Open direction', 'zh-Hans': '打开方向' },
      fullDirection: { en: 'Read full direction', 'zh-Hans': '查看完整方向' },
      closeDetails: { en: 'Collapse', 'zh-Hans': '收起' },
      chooseDirection: { en: 'Pick this', 'zh-Hans': '选这个' },
      selectedDirection: { en: 'My pick', 'zh-Hans': '我的选择' },
      otherDirections: { en: 'Other directions', 'zh-Hans': '其他方向' },
      showAllDirections: { en: 'Show all', 'zh-Hans': '查看全部' },
      hideAllDirections: { en: 'Hide', 'zh-Hans': '收起' },
      changeDirection: { en: 'Open', 'zh-Hans': '打开' },
      clearSelection: { en: 'Clear pick', 'zh-Hans': '取消选择' },
      votePick: { en: 'Select', 'zh-Hans': '选择' },
      voteSelected: { en: 'Selected', 'zh-Hans': '已选' },
      activeStatus: { en: 'Monitoring', 'zh-Hans': '观察中' },
      availableDirections: { en: 'directions available', 'zh-Hans': '个可切换方向' },
      linkedSignals: { en: 'linked signals', 'zh-Hans': '个关联信号' },
      signalBasis: { en: 'Supporting signals', 'zh-Hans': '支持信息' },
      relatedEventsTitle: { en: 'Related events', 'zh-Hans': '关联事件' },
      sourceLinksTitle: { en: 'Sources', 'zh-Hans': '来源链接' },
      peopleTracking: { en: 'selected', 'zh-Hans': '人已选' },
      currentBaseline: { en: 'Current baseline', 'zh-Hans': '当前基线' },
      whyThisDirection: { en: 'Why this direction', 'zh-Hans': '为何值得看' },
      counterSignal: { en: 'Current constraints', 'zh-Hans': '当前限制' },
      openQuestions: { en: 'Open questions', 'zh-Hans': '开放问题' },
      linkedEvents: { en: 'Linked events', 'zh-Hans': '关联事件' },
      noResults: { en: 'No matching node records found', es: 'No hay eventos coincidentes', ja: '一致する記録はありません', 'zh-Hans': '暂无匹配的节点数据', 'zh-Hant': '暫無符合的節點資料', fr: 'Aucun événement correspondant' },
      impactScore: { en: 'Impact', es: 'Impacto', ja: '影響', 'zh-Hans': '影响分', 'zh-Hant': '影響分', fr: 'Impact' },
      affected: { en: 'Affected', es: 'Afectados', ja: '影響対象', 'zh-Hans': '影响对象', 'zh-Hant': '影響對象', fr: 'Affectés' }
    };

    function normalizeLang(lang) {
      if (lang === 'zh') return 'zh-Hans';
      if (lang === 'zh-CN') return 'zh-Hans';
      if (lang === 'zh-TW' || lang === 'zh-HK' || lang === 'zh-Hant') return 'zh-Hans';
      return LANGUAGES[lang] ? lang : 'en';
    }

    function contentLang() {
      return LANGUAGES[state.lang]?.content || 'en';
    }

    function isChineseContent() {
      return contentLang() === 'zh';
    }

    function text(key) {
      const entry = UI_TEXT[key] || {};
      return entry[state.lang] || entry[contentLang()] || entry.en || key;
    }

    function localizedText(entry) {
      if (!entry) return '';
      if (typeof entry === 'string') return entry;
      return entry[state.lang] || entry[state.lang.replace('-', '')] || entry[contentLang()] || entry.zhHans || entry.zhHant || entry.zh || entry.en || '';
    }

    function labelFor(entry) {
      return localizedText(entry);
    }

    function renderTimelineWithTransition(afterRender) {
      const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (!reduceMotion && document.startViewTransition) {
        const transition = document.startViewTransition(() => renderTimeline());
        if (typeof afterRender === 'function') {
          transition.updateCallbackDone.then(afterRender);
        }
        return;
      }
      renderTimeline();
      if (typeof afterRender === 'function') {
        afterRender();
      }
    }

    function localizedRecord(record) {
      return {
        title: localizedText(record?.title),
        summary: localizedText(record?.summary || record?.thesis),
        desc: localizedText(record?.description || record?.thesis || record?.summary),
        category: localizedText(record?.categoryLabel),
        source: localizedText(record?.sourceLabel),
        description: localizedText(record?.narrative || record?.description || record?.summary || record?.thesis)
      };
    }

    function eventIdFromLocation() {
      const hashParams = new URLSearchParams(window.location.hash.replace(/^#/, ''));
      return hashParams.get('event') || new URLSearchParams(window.location.search).get('event');
    }

    function eventStateUrl(id) {
      return `${window.location.pathname}#event=${encodeURIComponent(id)}`;
    }

    /* ─── State Management ──────────────────────────────────────────── */
    const READER_PULSE_API = '/api/reader-pulse';
    const SELECTED_FORECAST_STORAGE_KEY = 'ea-selected-forecast-v1';
    const SELECTION_COUNTS_STORAGE_KEY = 'ea-forecast-selection-counts-v1';

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
      theme: localStorage.getItem('epocharc-theme') || 'light', // 'light' or 'dark'
      filters: {
        significance: 'all',
        category: 'all',
        impactDimension: 'all',
        consensusLevel: 'all',
        year: 'all'
      },
      searchQuery: '',
      openEventIds: new Set(),
      previewForecastId: '',
      selectedForecastId: localStorage.getItem(SELECTED_FORECAST_STORAGE_KEY) || '',
      selectedForecastExpanded: false,
      forecastSelectionCounts: readSelectionCounts(),
      readerPulseSource: 'local',
      directionsPanelOpen: false,
      dataStatus: 'loading',
      dataError: ''
    };

    /* ─── Content Data ──────────────────────────────────────────────── */
    let forecasts = [];
    let aiEvents = [];
    let sourcesById = new Map();
    let categoryLabels = {};
    let impactLabels = {};
    let timeframeLabels = {};
    let consensusLabels = {};

    const sourceTypeLabels = {
      primary: { zhHans: '原始资料', zhHant: '原始資料', en: 'Primary' },
      official: { zhHans: '官方资料', zhHant: '官方資料', en: 'Official' },
      news: { zhHans: '新闻报道', zhHant: '新聞報導', en: 'News' },
      analysis: { zhHans: '分析资料', zhHant: '分析資料', en: 'Analysis' },
      encyclopedia: { zhHans: '百科资料', zhHant: '百科資料', en: 'Reference' },
      unknown: { zhHans: '来源资料', zhHant: '來源資料', en: 'Source' }
    };


    async function loadJson(url) {
      const requestUrl = window.location.protocol === 'file:'
        ? url
        : `/${url.replace(/^\/+/, '')}`;
      const response = await fetch(requestUrl, { cache: 'no-store' });
      if (!response.ok) {
        throw new Error(`${requestUrl}: ${response.status}`);
      }
      return response.json();
    }

    function readFallbackJson(id) {
      const node = document.getElementById(id);
      if (!node) return null;
      return JSON.parse(node.textContent);
    }

    function loadFallbackData(error) {
      const predictionData = readFallbackJson('fallback-forecasts-data');
      const eventData = readFallbackJson('fallback-events-data');
      const sourceData = readFallbackJson('fallback-sources-data');
      if (!predictionData || !eventData || !sourceData) {
        throw error;
      }
      forecasts = predictionData;
      aiEvents = eventData;
      sourcesById = new Map(sourceData.map((source) => [source.id, source]));
      state.dataStatus = 'ready';
      state.dataError = '';
    }

    // 获取除了 excludeFilterKey 外，应用了其它所有条件的过滤事件子集
    function getFilteredEventsExcept(excludeFilterKey) {
      return aiEvents.filter(e => {
        // 1. Significance
        if (excludeFilterKey !== 'significance') {
          if (state.filters.significance !== 'all' && e.significance !== parseInt(state.filters.significance)) {
            return false;
          }
        }
        // 2. Category
        if (excludeFilterKey !== 'category') {
          if (state.filters.category !== 'all' && !e.categories.includes(state.filters.category)) {
            return false;
          }
        }
        // 3. Impact Dimension
        if (excludeFilterKey !== 'impactDimension') {
          if (state.filters.impactDimension !== 'all' && !e.impacts.some(impact => impact.dimension === state.filters.impactDimension)) {
            return false;
          }
        }
        // 4. Consensus Level
        if (excludeFilterKey !== 'consensusLevel') {
          if (state.filters.consensusLevel !== 'all' && e.consensusLevel !== state.filters.consensusLevel) {
            return false;
          }
        }
        // 5. Year
        if (excludeFilterKey !== 'year') {
          if (state.filters.year !== 'all') {
            const eventYear = String(e.date || '').split('-')[0];
            if (eventYear !== state.filters.year) {
              return false;
            }
          }
        }
        // 6. Search Query
        if (state.searchQuery) {
          const query = state.searchQuery.toLowerCase();
          const copy = localizedRecord(e);
          const matchesTitle = copy.title.toLowerCase().includes(query);
          const matchesCategory = e.categories.some(c => labelFor(categoryLabels[c]).toLowerCase().includes(query));
          const matchesSummary = copy.summary.toLowerCase().includes(query);
          const matchesTags = Array.isArray(e.tags) && e.tags.some(tag => tag.toLowerCase().includes(query));
          if (!(matchesTitle || matchesCategory || matchesSummary || matchesTags)) {
            return false;
          }
        }
        return true;
      });
    }

    function initFilterOptionsWithCounts() {
      const yearSelect = document.getElementById('yearFilter');
      
      // 如果年份下拉框尚未初始化，则提取全部事件中的年份做一次性 DOM 生成
      if (yearSelect && yearSelect.options.length <= 1) {
        const years = new Set();
        aiEvents.forEach(e => {
          const year = String(e.date || '').split('-')[0];
          if (year) years.add(year);
        });
        const sortedYears = Array.from(years).sort((a, b) => b - a);
        yearSelect.innerHTML = '';
        
        const allOption = document.createElement('option');
        allOption.value = 'all';
        allOption.setAttribute('data-zh', '全部年份');
        allOption.setAttribute('data-en', 'All Years');
        allOption.innerText = '全部年份';
        yearSelect.appendChild(allOption);
        
        sortedYears.forEach(y => {
          const option = document.createElement('option');
          option.value = y;
          option.setAttribute('data-zh', `${y}年`);
          option.setAttribute('data-en', y);
          option.innerText = y;
          yearSelect.appendChild(option);
        });
      }

      const updateOptions = (selector, counts) => {
        document.querySelectorAll(selector).forEach(opt => {
          const val = opt.value;
          const count = counts[val] || 0;
          let baseZh = opt.getAttribute('data-zh') || opt.innerText;
          let baseEn = opt.getAttribute('data-en') || opt.innerText;
          
          baseZh = baseZh.replace(/（\d+）$/, '');
          baseEn = baseEn.replace(/\s*\(\d+\)$/, '');
          
          opt.setAttribute('data-zh', `${baseZh}（${count}）`);
          opt.setAttribute('data-en', `${baseEn} (${count})`);
        });
      };

      // 1. Significance
      const sigEvents = getFilteredEventsExcept('significance');
      const sigCounts = {
        all: sigEvents.length,
        3: sigEvents.filter(e => e.significance === 3).length,
        2: sigEvents.filter(e => e.significance === 2).length,
        1: sigEvents.filter(e => e.significance === 1).length
      };
      updateOptions('#significanceFilter option', sigCounts);

      // 2. Event Category
      const catEvents = getFilteredEventsExcept('category');
      const catCounts = { all: catEvents.length };
      catEvents.forEach(e => {
        if (e.categories) {
          e.categories.forEach(c => {
            catCounts[c] = (catCounts[c] || 0) + 1;
          });
        }
      });
      updateOptions('#categoryFilter option', catCounts);

      // 3. Impact Dimension
      const dimEvents = getFilteredEventsExcept('impactDimension');
      const dimCounts = { all: dimEvents.length };
      dimEvents.forEach(e => {
        if (e.impacts) {
          e.impacts.forEach(imp => {
            dimCounts[imp.dimension] = (dimCounts[imp.dimension] || 0) + 1;
          });
        }
      });
      updateOptions('#impactFilter option', dimCounts);

      // 4. Consensus
      const conEvents = getFilteredEventsExcept('consensusLevel');
      const conCounts = {
        all: conEvents.length,
        broad: conEvents.filter(e => e.consensusLevel === 'broad').length,
        debated: conEvents.filter(e => e.consensusLevel === 'debated').length,
        emerging: conEvents.filter(e => e.consensusLevel === 'emerging').length
      };
      updateOptions('#consensusFilter option', conCounts);

      // 5. Dynamic Year Filter
      const yearEvents = getFilteredEventsExcept('year');
      const yearCounts = { all: yearEvents.length };
      yearEvents.forEach(e => {
        const year = String(e.date || '').split('-')[0];
        if (year) {
          yearCounts[year] = (yearCounts[year] || 0) + 1;
        }
      });
      updateOptions('#yearFilter option', yearCounts);
      
      updateLocale();
      updateResetButtonState();
    }

    function updateResetButtonState() {
      const isFiltered = state.searchQuery !== '' ||
                         state.filters.significance !== 'all' ||
                         state.filters.category !== 'all' ||
                         state.filters.impactDimension !== 'all' ||
                         state.filters.consensusLevel !== 'all' ||
                         state.filters.year !== 'all';

      const filterControls = [
        elements.significanceFilter,
        elements.categoryFilter,
        elements.impactFilter,
        elements.consensusFilter,
        elements.yearFilter
      ];
      filterControls.forEach((control) => {
        const isActive = control.value !== 'all';
        control.classList.toggle('is-active', isActive);
        control.closest('.filter-field')?.classList.toggle('is-active', isActive);
      });

      elements.filterResetBtn.disabled = !isFiltered;
    }

    let fullEventDataLoaded = false;
    let fullEventDataPromise = null;
    let fullEventDataError = false;

    async function ensureFullEventData() {
      if (fullEventDataLoaded) return Promise.resolve();
      if (!fullEventDataPromise) {
        fullEventDataError = false;
        fullEventDataPromise = loadJson('data/events.json').then(data => {
          const summaryMap = new Map(aiEvents.map(e => [e.id, e]));
          data.forEach(full => {
            const existing = summaryMap.get(full.id);
            if (existing) {
              Object.assign(existing, full);
            }
          });
          fullEventDataLoaded = true;
          renderTimeline();
        }).catch(err => {
          fullEventDataPromise = null;
          fullEventDataError = true;
          renderTimeline();
          throw err;
        });
      }
      return fullEventDataPromise;
    }

    async function loadSiteData() {
      state.dataStatus = 'loading';
      state.dataError = '';
      renderPredictions();
      renderTimeline();

      try {
        const [labelsData, forecastData, eventData, sourceData] = await Promise.all([
          loadJson('data/labels.json'),
          loadJson('data/forecasts.json'),
          loadJson('data/events_summary.json'),
          loadJson('data/sources.json')
        ]);
        categoryLabels = labelsData.category || {};
        impactLabels = labelsData.impactDimension || {};
        timeframeLabels = labelsData.timeframe || {};
        consensusLabels = labelsData.consensus || {};
        forecasts = forecastData;
        aiEvents = eventData;
        sourcesById = new Map(sourceData.map((source) => [source.id, source]));
        state.dataStatus = 'ready';
      } catch (error) {
        try {
          loadFallbackData(error);
        } catch (fallbackError) {
          state.dataStatus = 'error';
          state.dataError = String(fallbackError.message || fallbackError);
        }
      }

      initFilterOptionsWithCounts();
      updateLocale();

      renderPredictions();
      renderTimeline();
    }

    const elements = {
      langSelect: document.getElementById('langSelect'),
      themeToggle: document.getElementById('themeToggle'),
      themeIcon: document.getElementById('themeIcon'),
      themeText: document.getElementById('themeText'),
      predictionsContainer: document.getElementById('predictionsContainer'),
      timelineContainer: document.getElementById('timelineContainer'),
      searchInput: document.getElementById('searchInput'),
      significanceFilter: document.getElementById('significanceFilter'),
      categoryFilter: document.getElementById('categoryFilter'),
      impactFilter: document.getElementById('impactFilter'),
      consensusFilter: document.getElementById('consensusFilter'),
      yearFilter: document.getElementById('yearFilter'),
      filterResetField: document.getElementById('filterResetField'),
      filterResetBtn: document.getElementById('filterResetBtn'),
      backToTopBtn: document.getElementById('backToTopBtn'),
    };

    /* ─── Language Switcher Logic ───────────────────────────────────── */
    function updateLocale() {
      document.documentElement.lang = LANGUAGES[state.lang]?.html || 'en';
      if (elements.langSelect) {
        elements.langSelect.value = state.lang;
      }
      
      // Update page title
      const isZh = isChineseContent();
      document.title = isZh
        ? 'EpochArc · AI 时间轴：1950 至今的重要里程碑'
        : 'EpochArc · AI Timeline: Key Milestones from 1950 to Today';
      
      // Update meta description
      const metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc) {
        metaDesc.setAttribute('content', isZh
          ? '浏览 93 个经过策展的 AI 里程碑，以及对应来源、影响分析、专题叙事与可能方向。'
          : 'Explore 93 curated AI milestones with evidence, impact analysis, narrative arcs, and possible directions.'
        );
      }
      
      // Update OG tags
      const ogTitle = document.querySelector('meta[property="og:title"]');
      if (ogTitle) ogTitle.setAttribute('content', document.title);
      
      const ogDesc = document.querySelector('meta[property="og:description"]');
      if (ogDesc) {
        ogDesc.setAttribute('content', isZh
          ? '浏览 93 个经过策展的 AI 里程碑，以及对应来源、影响分析、专题叙事与可能方向。'
          : 'Explore 93 curated AI milestones with evidence, impact analysis, narrative arcs, and possible directions.'
        );
      }
      
      const ogLocale = document.querySelector('meta[property="og:locale"]');
      if (ogLocale) {
        ogLocale.setAttribute('content', isZh ? 'zh_CN' : 'en_US');
      }
      
      // Update Twitter tags
      const twTitle = document.querySelector('meta[name="twitter:title"]');
      if (twTitle) twTitle.setAttribute('content', document.title);
      
      const twDesc = document.querySelector('meta[name="twitter:description"]');
      if (twDesc) {
        twDesc.setAttribute('content', isZh
          ? '浏览 93 个经过策展的 AI 里程碑，以及对应来源、影响分析、专题叙事与可能方向。'
          : 'Explore 93 curated AI milestones with evidence, impact analysis, narrative arcs, and possible directions.'
        );
      }
      
      // Update all elements with data-zh / data-en
      document.querySelectorAll('[data-zh]').forEach(el => {
        const translated = el.getAttribute(`data-${state.lang}`);
        el.innerText = translated || (isChineseContent() ? el.getAttribute('data-zh') : el.getAttribute('data-en'));
      });

      // Update placeholders
      document.querySelectorAll('[data-zh-placeholder]').forEach(el => {
        const translated = el.getAttribute(`data-${state.lang}-placeholder`);
        el.setAttribute('placeholder', translated || (isChineseContent() ? el.getAttribute('data-zh-placeholder') : el.getAttribute('data-en-placeholder')));
      });

      // Update titles
      document.querySelectorAll('[data-zh-title]').forEach(el => {
        const translated = el.getAttribute(`data-${state.lang}-title`);
        el.setAttribute('title', translated || (isChineseContent() ? el.getAttribute('data-zh-title') : el.getAttribute('data-en-title')));
      });

      renderPredictions();
      renderTimeline();
      updateThemeLabels();
    }

    elements.langSelect.addEventListener('change', (event) => {
      state.lang = normalizeLang(event.target.value);
      localStorage.setItem('epocharc-lang', state.lang);
      updateLocale();
    });

    /* ─── Theme Switcher Logic ──────────────────────────────────────── */
    function updateTheme() {
      document.body.setAttribute('data-theme', state.theme);
      updateThemeLabels();
      
      // Update icon dynamically
      if (state.theme === 'dark') {
        elements.themeIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"></path>`;
      } else {
        elements.themeIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"></path>`;
      }
    }

    elements.themeToggle.addEventListener('click', () => {
      state.theme = state.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem('epocharc-theme', state.theme);
      updateTheme();
    });

    function updateThemeLabels() {
      if (elements.themeText) {
        elements.themeText.innerText = state.theme === 'light' ? text('darkMode') : text('lightMode');
      }
    }

    function renderStatus(container, title, body, linkText) {
      container.innerHTML = `
        <div class="status-panel">
          <strong>${title}</strong>
          <span>${body}</span>
          ${linkText ? `<div style="margin-top: 8px;"><a class="status-link" href="/methods">${linkText}</a></div>` : ''}
        </div>
      `;
    }

    function escapeHtml(value) {
      return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
    }

    function readSelectionCounts() {
      try {
        const raw = localStorage.getItem(SELECTION_COUNTS_STORAGE_KEY);
        if (!raw) return {};
        return sanitizeSelectionCounts(JSON.parse(raw));
      } catch (error) {
        return {};
      }
    }

    function persistSelectionCounts() {
      localStorage.setItem(SELECTION_COUNTS_STORAGE_KEY, JSON.stringify(state.forecastSelectionCounts));
    }

    function persistSelectedForecastId() {
      if (state.selectedForecastId) {
        localStorage.setItem(SELECTED_FORECAST_STORAGE_KEY, state.selectedForecastId);
      } else {
        localStorage.removeItem(SELECTED_FORECAST_STORAGE_KEY);
      }
    }

    function sanitizeSelectionCounts(value) {
      if (!value || typeof value !== 'object') return {};
      return Object.fromEntries(
        Object.entries(value).flatMap(([forecastId, count]) => {
          const parsed = Math.max(0, Math.floor(Number(count) || 0));
          return parsed ? [[forecastId, parsed]] : [];
        })
      );
    }

    function applyReaderPulseState({ selectedForecastId = '', counts = {}, source = 'local', persistCounts = true }) {
      state.selectedForecastId = selectedForecastId || '';
      if (!state.selectedForecastId) {
        state.selectedForecastExpanded = false;
      }
      state.forecastSelectionCounts = sanitizeSelectionCounts(counts);
      state.readerPulseSource = source;
      persistSelectedForecastId();
      if (persistCounts) {
        persistSelectionCounts();
      }
    }

    function syncLocalReaderPulseState(selectedForecastId = state.selectedForecastId) {
      applyReaderPulseState({
        selectedForecastId,
        counts: selectedForecastId ? { [selectedForecastId]: 1 } : {},
        source: 'local'
      });
    }

    function applyRemoteReaderPulsePayload(payload) {
      applyReaderPulseState({
        selectedForecastId: typeof payload?.selectedForecastId === 'string' ? payload.selectedForecastId : '',
        counts: payload?.counts || {},
        source: 'remote',
        persistCounts: false
      });
    }

    async function loadReaderPulseStateFromApi() {
      try {
        const response = await fetch(READER_PULSE_API, {
          cache: 'no-store',
          headers: {
            'Accept': 'application/json'
          }
        });
        if (!response.ok) return false;
        applyRemoteReaderPulsePayload(await response.json());
        return true;
      } catch (error) {
        return false;
      }
    }

    async function submitReaderPulseSelection(forecastId) {
      try {
        const response = await fetch(READER_PULSE_API, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            forecastId: forecastId || ''
          })
        });
        if (!response.ok) return false;
        applyRemoteReaderPulsePayload(await response.json());
        return true;
      } catch (error) {
        return false;
      }
    }

    function getForecastSelectionCount(forecastId) {
      const stored = Number(state.forecastSelectionCounts?.[forecastId] || 0);
      if (state.selectedForecastId === forecastId) {
        return Math.max(stored, 1);
      }
      return stored;
    }

    function formatSelectionCount(forecastId) {
      const count = getForecastSelectionCount(forecastId);
      return {
        count,
        label: `${count} ${text('peopleTracking')}`
      };
    }

    function signalSummary(forecast) {
      const list = Array.isArray(forecast?.signals) ? forecast.signals.filter(item => item.status === 'observed') : [];
      return { observed: list.length, total: list.length };
    }

    function truncateText(value, maxLength = 24) {
      const text = String(value ?? '');
      if (text.length <= maxLength) return text;
      return `${text.slice(0, maxLength - 1).trimEnd()}…`;
    }

    function signalEventChips(signal) {
      const eventIds = Array.isArray(signal?.eventIds) ? signal.eventIds : [];
      const linkedEvents = eventIds
        .map((eventId) => aiEvents.find((event) => event.id === eventId))
        .filter(Boolean);

      if (!linkedEvents.length) return '';

      const visibleEvents = linkedEvents.slice(0, 2);
      const hiddenCount = linkedEvents.length - visibleEvents.length;

      return `${visibleEvents.map((event) => {
        const copy = localizedRecord(event);
        const year = String(event.date || '').split('-')[0];
        const label = truncateText(copy.title || event.id, 22);
        const chip = year ? `${year} · ${label}` : label;
        return `<button class="signal-event-link" type="button" onclick="jumpToEvent('${event.id}')">${escapeHtml(chip)}</button>`;
      }).join('')}${hiddenCount > 0 ? `<span class="signal-event-more">+${hiddenCount}</span>` : ''}`;
    }

    function signalEventLinks(signal) {
      const chips = signalEventChips(signal);
      if (!chips) return '';
      return `<div class="signal-event-links" aria-label="${escapeHtml(text('linkedEvents'))}">${chips}</div>`;
    }

    function signalSourceChips(signal) {
      const sourceIds = Array.isArray(signal?.sourceIds) ? signal.sourceIds : [];
      const linkedSources = sourceIds
        .map((sourceId) => sourcesById.get(sourceId))
        .filter((source) => source && source.url);

      if (!linkedSources.length) return '';

      return `${linkedSources.slice(0, 3).map((source) => {
        const label = truncateText(source.title || source.id, 26);
        return `<a class="signal-event-link signal-source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(label)}</a>`;
      }).join('')}${linkedSources.length > 3 ? `<span class="signal-event-more">+${linkedSources.length - 3}</span>` : ''}`;
    }

    function signalSourceLinks(signal) {
      const chips = signalSourceChips(signal);
      if (!chips) return '';
      return `<div class="signal-event-links" aria-label="${escapeHtml(text('sourceLinksTitle'))}">${chips}</div>`;
    }

    function signalSupportRows(forecast) {
      const list = Array.isArray(forecast?.signals) ? forecast.signals.filter(item => item.status === 'observed') : [];
      if (!list.length) return '';
      return `
        <section class="support-matrix">
          <div class="support-row-list">
            ${list.map(item => {
              const eventChips = signalEventChips(item);
              const sourceChips = signalSourceChips(item);
              return `
                <article class="support-row">
                  <div class="support-card">
                    <p class="support-card-copy">${escapeHtml(localizedText(item.summary))}</p>
                  </div>
                  <div class="support-links-cell">
                    <div class="signal-links-stack">
                      ${eventChips}
                      ${sourceChips}
                    </div>
                  </div>
                </article>
              `;
            }).join('')}
          </div>
        </section>
      `;
    }

    function predictionDetails(forecast) {
      return signalSupportRows(forecast);
    }

    function chevronIcon(direction = 'down') {
      const directionClass = direction === 'up' ? 'forecast-chevron up' : 'forecast-chevron';
      return `
        <svg class="${directionClass}" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path d="M3.5 6.25 8 10.75l4.5-4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
      `;
    }

    function compactCardAction(forecast) {
      return `<button class="forecast-toggle" type="button" aria-label="${escapeHtml(text('reviewDirection'))}" onclick="event.stopPropagation(); previewForecast('${forecast.id}')">${chevronIcon('down')}</button>`;
    }

    function expandedPrimaryAction(forecast, mode) {
      if (mode === 'selected') {
        return `<button class="forecast-choice-button secondary" type="button" onclick="event.stopPropagation(); clearSelectedForecast()">${escapeHtml(text('clearSelection'))}</button>`;
      }
      return `<button class="forecast-choice-button" type="button" onclick="event.stopPropagation(); chooseForecast('${forecast.id}')">${escapeHtml(text('chooseDirection'))}</button>`;
    }

    function expandedCollapseAction(mode) {
      const handler = mode === 'selected' ? 'collapseSelectedForecast()' : 'clearPreview()';
      return `<button class="predict-collapse-button" type="button" onclick="event.stopPropagation(); ${handler}">${escapeHtml(text('closeDetails'))}${chevronIcon('up')}</button>`;
    }

    function fullDirectionLink(forecast) {
      return `<a class="forecast-full-link" href="/directions/${encodeURIComponent(forecast.slug || forecast.id)}/" onclick="event.stopPropagation()">${escapeHtml(text('fullDirection'))}<span aria-hidden="true">→</span></a>`;
    }

    function renderForecastCard(forecast, mode = 'compact') {
      const copy = localizedRecord(forecast);
      const signals = signalSummary(forecast);
      const isExpanded = mode === 'expanded' || mode === 'selected';
      const isSelected = state.selectedForecastId === forecast.id;
      const selection = formatSelectionCount(forecast.id);
      const cardClass = ['predict-card', mode, isExpanded ? 'is-expanded' : '', isSelected ? 'selected' : ''].filter(Boolean).join(' ');
      const signalText = signals.total ? `${signals.observed} ${text('linkedSignals')}` : text('activeStatus');
      return `
        <article class="${cardClass}" onclick="${mode === 'compact' ? `previewForecast('${forecast.id}')` : ''}">
          <div class="predict-main">
            <div class="predict-header">
              ${isExpanded ? `
                <div class="predict-expanded-topline">
                  <div class="predict-expanded-title">
                    <h3>${escapeHtml(copy.title)}</h3>
                  </div>
                  <div class="predict-expanded-controls">
                    ${expandedPrimaryAction(forecast, mode)}
                    <div class="forecast-selection-badge" aria-label="${escapeHtml(selection.label)}">
                      <span class="forecast-selection-count">${escapeHtml(selection.count)}</span>
                      <span class="forecast-selection-label">${escapeHtml(text('peopleTracking'))}</span>
                    </div>
                  </div>
                </div>
                <p class="predict-intro">${escapeHtml(copy.desc)}</p>
              ` : `
                <h3>${escapeHtml(copy.title)}</h3>
                <p>${escapeHtml(copy.desc)}</p>
                <div class="predict-meta-signals">
                  <span class="signal-count">${escapeHtml(signalText)}</span>
                </div>
              `}
            </div>
            ${!isExpanded ? `
              <div class="predict-action-row">
                <div class="predict-footer-left">
                  <button class="forecast-mini-vote-btn" type="button" onclick="event.stopPropagation(); ${isSelected ? 'clearSelectedForecast()' : `chooseForecast('${forecast.id}')`}">
                    ${isSelected ? escapeHtml(text('voteSelected')) : escapeHtml(text('votePick'))}
                  </button>
                  <div class="forecast-selection-badge" aria-label="${escapeHtml(selection.label)}">
                    <span class="forecast-selection-count">${escapeHtml(selection.count)}</span>
                    <span class="forecast-selection-label">${escapeHtml(text('peopleTracking'))}</span>
                  </div>
                </div>
                <div class="predict-footer-right">
                  ${compactCardAction(forecast)}
                </div>
              </div>
            ` : ''}
          </div>
          ${isExpanded ? `
            <div class="predict-expanded-content">
              <div class="prediction-details">
                ${predictionDetails(forecast)}
              </div>
              <div class="predict-expanded-toolbar">
                ${fullDirectionLink(forecast)}
                ${expandedCollapseAction(mode)}
              </div>
            </div>
          ` : ''}
        </article>
      `;
    }

    function renderDirectionEntry(activeId, isConfirmed = false) {
      const others = forecasts.filter(f => f.id !== activeId);
      return `
        <div class="direction-entry ${state.directionsPanelOpen ? 'open' : ''}">
          <div class="direction-entry-head">
            <div>
              <div class="direction-entry-title">${escapeHtml(text('otherDirections'))}</div>
              <div class="direction-entry-sub">${escapeHtml(others.length)} ${escapeHtml(text('availableDirections'))}</div>
            </div>
            <button class="forecast-action" onclick="toggleDirectionsPanel()">${escapeHtml(text(state.directionsPanelOpen ? 'hideAllDirections' : 'showAllDirections'))}</button>
          </div>
          <div class="direction-list">
            ${others.map(forecast => {
              const copy = localizedRecord(forecast);
              const signals = signalSummary(forecast);
              return `
                <div class="direction-row">
                  <div>
                    <div class="direction-row-title">${escapeHtml(copy.title)}</div>
                    <div class="direction-row-meta">${escapeHtml(signals.observed)} ${escapeHtml(text('linkedSignals'))} · ${escapeHtml(text('activeStatus'))}</div>
                  </div>
                  <button class="forecast-action" onclick="previewForecast('${forecast.id}')">${escapeHtml(text('changeDirection'))}</button>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }

    /* ─── Future Signals Selection Logic ────────────────────────────── */
    function renderPredictions() {
      if (state.dataStatus === 'loading') {
        elements.predictionsContainer.innerHTML = '';
        return;
      }

      if (state.dataStatus === 'error') {
        elements.predictionsContainer.classList.remove('compact-mode');
        renderStatus(
          elements.predictionsContainer,
          text('predictionsError'),
          text('predictionsErrorBody'),
          text('openMethodology')
        );
        return;
      }

      elements.predictionsContainer.innerHTML = '';

      const selected = forecasts.find(f => f.id === state.selectedForecastId);
      if (selected && state.selectedForecastExpanded) {
        elements.predictionsContainer.classList.remove('compact-mode');
        elements.predictionsContainer.innerHTML = renderForecastCard(selected, 'selected') + renderDirectionEntry(selected.id, true);
        return;
      }

      const preview = forecasts.find(f => f.id === state.previewForecastId);
      if (preview) {
        elements.predictionsContainer.classList.remove('compact-mode');
        elements.predictionsContainer.innerHTML = renderForecastCard(preview, 'expanded') + renderDirectionEntry(preview.id, false);
        return;
      }

      elements.predictionsContainer.classList.add('compact-mode');
      elements.predictionsContainer.innerHTML = forecasts.map(forecast => {
        return renderForecastCard(forecast, 'compact');
      }).join('');
    }

    window.previewForecast = async function(id) {
      if (state.selectedForecastId === id) {
        state.selectedForecastExpanded = true;
        state.previewForecastId = '';
        state.directionsPanelOpen = false;
        renderPredictions();
        return;
      }

      state.previewForecastId = state.previewForecastId === id ? '' : id;
      state.selectedForecastExpanded = false;
      state.directionsPanelOpen = false;
      renderPredictions();
    };

    window.clearPreview = function() {
      state.previewForecastId = '';
      state.directionsPanelOpen = false;
      renderPredictions();
    };

    window.chooseForecast = async function(id) {
      if (state.selectedForecastId !== id) {
        const syncedRemotely = await submitReaderPulseSelection(id);
        if (!syncedRemotely) {
          syncLocalReaderPulseState(id);
        }
      }
      persistSelectedForecastId();
      state.previewForecastId = '';
      state.directionsPanelOpen = false;
      renderPredictions();
    };

    window.collapseSelectedForecast = function() {
      state.selectedForecastExpanded = false;
      state.previewForecastId = '';
      state.directionsPanelOpen = false;
      renderPredictions();
    };

    window.clearSelectedForecast = async function(shouldRender = true) {
      const clearedRemotely = await submitReaderPulseSelection('');
      if (!clearedRemotely) {
        syncLocalReaderPulseState('');
      }
      state.previewForecastId = '';
      state.directionsPanelOpen = false;
      if (shouldRender) {
        renderPredictions();
      }
    };

    window.toggleDirectionsPanel = function() {
      state.directionsPanelOpen = !state.directionsPanelOpen;
      renderPredictions();
    };

    window.jumpToEvent = function(id) {
      if (!id) return;
      state.openEventIds.add(id);
      renderTimeline();
      requestAnimationFrame(() => {
        const node = document.getElementById(`item-${id}`);
        if (node) {
          if (typeof window.hideEventTooltip === 'function') window.hideEventTooltip();
          if (typeof window.hideGlobalTooltip === 'function') window.hideGlobalTooltip();
          node.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    };

    /* ─── Curated Timeline Rendering ────────────────────────────────── */
    function renderTimeline() {
      try {
      if (state.dataStatus === 'loading') {
        renderStatus(
          elements.timelineContainer,
          text('loadingTimeline'),
          text('loadingTimelineBody')
        );
        return;
      }

      if (state.dataStatus === 'error') {
        renderStatus(
          elements.timelineContainer,
          text('timelineError'),
          text('timelineErrorBody'),
          text('openMethodology')
        );
        return;
      }

      elements.timelineContainer.innerHTML = '';
      
      const filteredEvents = aiEvents
        .slice()
        .sort((a, b) => b.date.localeCompare(a.date))
        .filter(e => {
        if (state.filters.significance !== 'all' && e.significance !== parseInt(state.filters.significance)) {
          return false;
        }
        if (state.filters.category !== 'all' && !e.categories.includes(state.filters.category)) {
          return false;
        }
        if (state.filters.impactDimension !== 'all' && !e.impacts.some(impact => impact.dimension === state.filters.impactDimension)) {
          return false;
        }
        if (state.filters.consensusLevel !== 'all' && e.consensusLevel !== state.filters.consensusLevel) {
          return false;
        }
        if (state.filters.year !== 'all') {
          const eventYear = String(e.date || '').split('-')[0];
          if (eventYear !== state.filters.year) {
            return false;
          }
        }
        if (state.searchQuery) {
          const query = state.searchQuery.toLowerCase();
          const copy = localizedRecord(e);
          const matchesTitle = copy.title.toLowerCase().includes(query);
          const matchesCategory = e.categories.some(c => labelFor(categoryLabels[c]).toLowerCase().includes(query));
          const matchesSummary = copy.summary.toLowerCase().includes(query);
          const matchesTags = Array.isArray(e.tags) && e.tags.some(tag => tag.toLowerCase().includes(query));
          return matchesTitle || matchesCategory || matchesSummary || matchesTags;
        }
        return true;
      });

      filteredEvents.forEach(e => {
        const item = document.createElement('div');
        item.className = `timeline-item sig-${e.significance}`;
        item.setAttribute('data-category', e.categories[0]);
        item.id = `item-${e.id}`;
        
        let nodeHTML = '';
        const copy = localizedRecord(e);
        const catClass = e.categories[0] || 'capability';
        const categoryName = labelFor(categoryLabels[e.categories[0]]);
        const secondaryCatHTML = e.categories.length > 1
          ? `<span class="category-badge secondary ${e.categories[1]}">${labelFor(categoryLabels[e.categories[1]])}</span>`
          : '';
        const consensusName = labelFor(consensusLabels[e.consensusLevel]);
        const dateHTML = renderTimelineDate(e);
        const isExpanded = state.openEventIds.has(e.id);
        const detailsId = `details-${e.id}`;
        const detailsHTML = isExpanded ? renderEventDetails(e, detailsId) : '';
        const expandedClass = isExpanded ? ' expanded' : '';
        const metricsHTML = renderNodeMetrics(e, consensusName);

        if (e.significance === 3) {
          // Critical Node Layout
          nodeHTML = `
            <div class="timeline-date-col">
              ${dateHTML}
            </div>
            <div class="timeline-dot level-3"></div>
            <div class="timeline-entry">
              <article class="timeline-card-l3${expandedClass}" tabindex="0" aria-expanded="${isExpanded}" aria-controls="${detailsId}" onclick="toggleDetails('${e.id}')" onkeydown="handleCardKeydown(event, '${e.id}')">
                <div class="timeline-node-head">
                  <div class="timeline-node-main">
                    <div class="card-meta">
                      <span class="category-badge ${catClass}">${categoryName}</span>
                      ${secondaryCatHTML}
                    </div>
                    <div class="card-content">
                      <h3>${copy.title}</h3>
                      <p class="summary">${copy.summary}</p>
                      <div class="timeline-card-action">
                        <a class="source-title-link card-view-link" href="/events/${e.slug || e.id}/" style="font-size: 13px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; color: var(--accent);" onclick="event.stopPropagation()">
                          <span>${isChineseContent() ? '在页面内查看' : 'View in Page'}</span>
                          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="transform: translateY(-0.5px);"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        </a>
                        <span class="timeline-card-indicator" aria-hidden="true"></span>
                      </div>
                    </div>
                  </div>
                  ${metricsHTML}
                </div>
                ${detailsHTML}
              </article>
            </div>
          `;
        } else if (e.significance === 2) {
          // Major Node Layout
          nodeHTML = `
            <div class="timeline-date-col">
              ${dateHTML}
            </div>
            <div class="timeline-dot level-2"></div>
            <div class="timeline-entry">
              <article class="timeline-card-l2${expandedClass}" tabindex="0" aria-expanded="${isExpanded}" aria-controls="${detailsId}" onclick="toggleDetails('${e.id}')" onkeydown="handleCardKeydown(event, '${e.id}')">
                <div class="timeline-node-head">
                  <div class="timeline-node-main">
                    <div class="card-meta">
                      <span class="category-badge ${catClass}">${categoryName}</span>
                      ${secondaryCatHTML}
                    </div>
                    <div class="card-content">
                      <h3>${copy.title}</h3>
                      <p class="summary">${copy.summary}</p>
                      <div class="timeline-card-action">
                        <a class="source-title-link card-view-link" href="/events/${e.slug || e.id}/" style="font-size: 13px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; color: var(--accent);" onclick="event.stopPropagation()">
                          <span>${isChineseContent() ? '在页面内查看' : 'View in Page'}</span>
                          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="transform: translateY(-0.5px);"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        </a>
                        <span class="timeline-card-indicator" aria-hidden="true"></span>
                      </div>
                    </div>
                  </div>
                  ${metricsHTML}
                </div>
                ${detailsHTML}
              </article>
            </div>
          `;
        } else {
          // Minor Record Layout
          nodeHTML = `
            <div class="timeline-date-col">
              ${dateHTML}
            </div>
            <div class="timeline-dot level-1"></div>
            <div class="timeline-entry">
              <article class="timeline-card-l1${expandedClass}" tabindex="0" aria-expanded="${isExpanded}" aria-controls="${detailsId}" onclick="toggleDetails('${e.id}')" onkeydown="handleCardKeydown(event, '${e.id}')">
                <div class="timeline-node-head">
                  <div class="timeline-node-main">
                    <div class="card-meta">
                      <span class="category-badge ${catClass}">${categoryName}</span>
                      ${secondaryCatHTML}
                    </div>
                    <div class="card-content">
                      <h3>${copy.title}</h3>
                      <div class="timeline-card-action">
                        <a class="source-title-link card-view-link" href="/events/${e.slug || e.id}/" style="font-size: 13px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; color: var(--accent);" onclick="event.stopPropagation()">
                          <span>${isChineseContent() ? '在页面内查看' : 'View in Page'}</span>
                          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="transform: translateY(-0.5px);"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        </a>
                        <span class="timeline-card-indicator" aria-hidden="true"></span>
                      </div>
                    </div>
                  </div>
                  ${metricsHTML}
                </div>
                ${detailsHTML}
              </article>
            </div>
          `;
        }
        
        item.innerHTML = nodeHTML;
        elements.timelineContainer.appendChild(item);
      });

      if (filteredEvents.length === 0) {
        const noResult = document.createElement('div');
        noResult.style.padding = '40px 0';
        noResult.style.textAlign = 'center';
        noResult.style.color = 'var(--muted)';
        noResult.innerText = text('noResults');
        elements.timelineContainer.appendChild(noResult);
      }
      } catch (renderErr) {
        console.error('Timeline render crashed:', renderErr);
        elements.timelineContainer.innerHTML = '<p style="padding:40px;color:var(--c-text-secondary)">Render error - check console.</p>';
      }
    }

    function renderTimelineDate(e) {
      const raw = String(e.date || '');
      const parts = raw.split('-');
      const year = parts[0] || raw;
      let subdate = '';

      if (e.datePrecision === 'day' && parts.length >= 3) {
        subdate = isChineseContent()
          ? `${Number(parts[1])}月${Number(parts[2])}日`
          : new Date(`${parts[0]}-${parts[1]}-${parts[2]}T00:00:00`).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      } else if (e.datePrecision === 'month' && parts.length >= 2) {
        subdate = isChineseContent()
          ? `${Number(parts[1])}月`
          : new Date(`${parts[0]}-${parts[1]}-01T00:00:00`).toLocaleDateString('en-US', { month: 'short' });
      }

      return `
        <span class="timeline-year">${year}</span>
        ${subdate ? `<span class="timeline-subdate">${subdate}</span>` : ''}
      `;
    }

    function renderNodeMetrics(e, consensusName) {
      const impactLabel = isChineseContent() ? '影响' : 'Impact';
      return `
        <div class="timeline-node-side">
          <span class="timeline-node-meta">L${e.significance} · ${impactLabel} ${e.impactIndex}/10 · ${consensusName}</span>
        </div>
      `;
    }

    function renderEventDetails(e, detailsId) {
      const copy = localizedRecord(e);
      
      const isPartial = !e.narrative && !e.impacts;
      if (isPartial) {
        const detailStatus = fullEventDataError
          ? (isChineseContent() ? '详情加载失败，请重试或打开完整事件页面。' : 'Details failed to load. Retry or open the full event page.')
          : (isChineseContent() ? '加载详情中…' : 'Loading details…');
        return `
          <div class="timeline-details" id="${detailsId}" onclick="event.stopPropagation()" onkeydown="event.stopPropagation()">
            <div class="timeline-details-inner">
              <div class="detail-section" style="text-align: center; padding: var(--gap-lg) 0;">
                <p style="color: var(--muted); font-size: 14px; margin-bottom: 16px;">
                  ${detailStatus}
                </p>
                <a href="/events/${e.slug || e.id}/" class="source-title-link" style="font-weight: 700; font-size: 14px; display: inline-flex; align-items: center; gap: 4px;" onclick="event.stopPropagation()">
                  <span>${isChineseContent() ? '直接查看完整事件页面 →' : 'View full event page →'}</span>
                </a>
              </div>
            </div>
          </div>
        `;
      }
      const eventSources = (e.sources || []).map((sourceRef) => ({
        ref: sourceRef,
        source: sourcesById.get(sourceRef.sourceId) || { id: sourceRef.sourceId, title: sourceRef.sourceId, type: 'unknown', url: '' }
      }));

      const sourceItems = eventSources.map(({ ref, source }, index) => {
        const sourceKind = labelFor(sourceTypeLabels[source.type]) || source.type || labelFor(sourceTypeLabels.unknown);
        const sourceTitle = source.url
          ? `<a class="source-title source-title-link" href="${source.url}" target="_blank" rel="noopener noreferrer">${source.title}</a>`
          : `<span class="source-title">${source.title}</span>`;
        return `
          <li class="source-card">
            <span class="source-index">${index + 1}</span>
            <div class="source-body">
              <div class="source-row">
                ${sourceTitle}
              </div>
              <p class="source-meta">${source.url || (isChineseContent() ? '当前记录的是来源指向。推荐后续补 DOI、原始页面链接、存档链接和抓取时间。' : 'This currently stores the citation pointer. Next step: add DOI, canonical URL, archive URL, and capture timestamp.')}</p>
              ${ref.quote ? `<div class="source-quote">${ref.quote}</div>` : ''}
              <div class="source-status">
                <span class="source-chip">${sourceKind}</span>
                <span class="source-chip">${isChineseContent() ? '引用已记录' : 'Citation logged'}</span>
                <span class="source-chip">${source.url ? (isChineseContent() ? '原文可访问' : 'Live source') : (isChineseContent() ? '待补原文链接' : 'URL pending')}</span>
              </div>
            </div>
          </li>
        `;
      }).join('');

      const impactItems = e.impacts.map(impact => `
        <li class="impact-item">
          <div class="impact-head">
            <span class="impact-name">${labelFor(impactLabels[impact.dimension])}</span>
            <span class="impact-score">${impact.severity > 0 ? '+' : ''}${impact.severity} · ${labelFor(timeframeLabels[impact.timeframe])}</span>
          </div>
          <p class="impact-description">${localizedText(impact.description)}</p>
          <p class="impact-description">${text('affected')}: ${impact.affectedGroups.join(isChineseContent() ? '、' : ', ')}</p>
        </li>
      `).join('');

      // 计算关联关系
      const currentId = e.id;
      const relatedIds = new Set(e.relatedEvents || []);
      aiEvents.forEach(evt => {
        if (evt.relatedEvents && evt.relatedEvents.includes(currentId)) {
          relatedIds.add(evt.id);
        }
      });
      relatedIds.delete(currentId);

      const relatedEventsList = Array.from(relatedIds)
        .map(rid => aiEvents.find(evt => evt.id === rid))
        .filter(Boolean)
        .sort((a, b) => a.date.localeCompare(b.date));

      const precursors = relatedEventsList.filter(evt => evt.date < e.date);
      const successors = relatedEventsList.filter(evt => evt.date > e.date);

      // 渲染前驱卡片带
      let precursorsHTML = '';
      if (precursors.length > 0) {
        const cards = precursors.map(p => {
          const pCopy = localizedRecord(p);
          return `
            <div class="related-card" onclick="navigateToEvent('${p.id}')">
              <div class="related-card-meta">
                <span>${p.date}</span>
                <span class="sig-badge">L${p.significance}</span>
              </div>
              <h4 class="related-card-title">${pCopy.title}</h4>
              <p class="related-card-summary">${pCopy.summary}</p>
            </div>
          `;
        }).join('');
        precursorsHTML = `
          <div class="related-row">
            <div class="related-row-title">
              <span>← ${isChineseContent() ? '前驱事件 (Origins)' : 'Origins'}</span>
            </div>
            <div class="related-cards-container">
              ${cards}
            </div>
          </div>
        `;
      }

      // 渲染后继卡片带
      let successorsHTML = '';
      if (successors.length > 0) {
        const cards = successors.map(s => {
          const sCopy = localizedRecord(s);
          return `
            <div class="related-card" onclick="navigateToEvent('${s.id}')">
              <div class="related-card-meta">
                <span>${s.date}</span>
                <span class="sig-badge">L${s.significance}</span>
              </div>
              <h4 class="related-card-title">${sCopy.title}</h4>
              <p class="related-card-summary">${sCopy.summary}</p>
            </div>
          `;
        }).join('');
        successorsHTML = `
          <div class="related-row">
            <div class="related-row-title">
              <span>→ ${isChineseContent() ? '后继事件 (Successors)' : 'Successors'}</span>
            </div>
            <div class="related-cards-container">
              ${cards}
            </div>
          </div>
        `;
      }

      // 绘制 SVG 拓扑图
      let topologyHTML = '';
      if (relatedEventsList.length > 0) {
        const viewWidth = 700;
        const viewHeight = 280;
        const centerNodeX = 350;
        const centerNodeY = 140;
        const precursorX = 110;
        const successorX = 590;

        const visiblePrecursors = precursors.slice(-4); // 选最接近的 4 个
        const visibleSuccessors = successors.slice(0, 4); // 选最接近的 4 个

        let nodesMarkup = '';
        let linksMarkup = '';

        let defsMarkup = `
          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 2 L 10 5 L 0 8 z" fill="var(--border)" />
            </marker>
            <marker id="arrow-highlighted" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 2 L 10 5 L 0 8 z" fill="var(--accent)" />
            </marker>
          </defs>
        `;

        // 渲染中心节点
        const centerTitle = copy.title.length > 22 ? copy.title.substring(0, 20) + '...' : copy.title;
        nodesMarkup += `
          <g class="svg-node" onclick="event.stopPropagation()" onmouseenter="showEventTooltip(event, '${e.id}')" onmouseleave="hideEventTooltip()">
            <rect class="svg-node-rect center-node breathing-aura" x="${centerNodeX - 95}" y="${centerNodeY - 26}" width="190" height="52" />
            <text class="svg-node-title" x="${centerNodeX}" y="${centerNodeY - 2}" text-anchor="middle" title="${copy.title}">${centerTitle}</text>
            <text class="svg-node-date" x="${centerNodeX}" y="${centerNodeY + 16}" text-anchor="middle">${e.date} · L${e.significance}</text>
          </g>
        `;

        // 渲染前驱节点与连线
        if (visiblePrecursors.length > 0) {
          const gapY = viewHeight / (visiblePrecursors.length + 1);
          visiblePrecursors.forEach((p, idx) => {
            const nodeY = gapY * (idx + 1);
            const pCopy = localizedRecord(p);
            const pTitle = pCopy.title.length > 20 ? pCopy.title.substring(0, 18) + '...' : pCopy.title;

            const startX = precursorX + 85;
            const startY = nodeY;
            const endX = centerNodeX - 95;
            const endY = centerNodeY;
            const ctrlX1 = startX + 40;
            const ctrlY1 = startY;
            const ctrlX2 = endX - 40;
            const ctrlY2 = endY;

            linksMarkup += `
              <path class="svg-link-path" id="link-${p.id}-${e.id}" d="M ${startX} ${startY} C ${ctrlX1} ${ctrlY1}, ${ctrlX2} ${ctrlY2}, ${endX} ${endY}" marker-end="url(#arrow)" />
            `;

            nodesMarkup += `
              <g class="svg-node" onclick="navigateToEvent('${p.id}')" onmouseenter="highlightLink('link-${p.id}-${e.id}', true); showEventTooltip(event, '${p.id}')" onmouseleave="highlightLink('link-${p.id}-${e.id}', false); hideEventTooltip()">
                <rect class="svg-node-rect" x="${precursorX - 85}" y="${nodeY - 22}" width="170" height="44" />
                <text class="svg-node-title" x="${precursorX}" y="${nodeY - 2}" text-anchor="middle">${pTitle}</text>
                <text class="svg-node-date" x="${precursorX}" y="${nodeY + 12}" text-anchor="middle">${p.date} · L${p.significance}</text>
              </g>
            `;
          });
        }

        // 渲染后继节点与连线
        if (visibleSuccessors.length > 0) {
          const gapY = viewHeight / (visibleSuccessors.length + 1);
          visibleSuccessors.forEach((s, idx) => {
            const nodeY = gapY * (idx + 1);
            const sCopy = localizedRecord(s);
            const sTitle = sCopy.title.length > 20 ? sCopy.title.substring(0, 18) + '...' : sCopy.title;

            const startX = centerNodeX + 95;
            const startY = centerNodeY;
            const endX = successorX - 85;
            const endY = nodeY;
            const ctrlX1 = startX + 40;
            const ctrlY1 = startY;
            const ctrlX2 = endX - 40;
            const ctrlY2 = endY;

            linksMarkup += `
              <path class="svg-link-path" id="link-${e.id}-${s.id}" d="M ${startX} ${startY} C ${ctrlX1} ${ctrlY1}, ${ctrlX2} ${ctrlY2}, ${endX} ${endY}" marker-end="url(#arrow)" />
            `;

            nodesMarkup += `
              <g class="svg-node" onclick="navigateToEvent('${s.id}')" onmouseenter="highlightLink('link-${e.id}-${s.id}', true); showEventTooltip(event, '${s.id}')" onmouseleave="highlightLink('link-${e.id}-${s.id}', false); hideEventTooltip()">
                <rect class="svg-node-rect" x="${successorX - 85}" y="${nodeY - 22}" width="170" height="44" />
                <text class="svg-node-title" x="${successorX}" y="${nodeY - 2}" text-anchor="middle">${sTitle}</text>
                <text class="svg-node-date" x="${successorX}" y="${nodeY + 12}" text-anchor="middle">${s.date} · L${s.significance}</text>
              </g>
            `;
          });
        }

        topologyHTML = `
          <div class="related-topology-container">
            <span class="related-topology-title">${isChineseContent() ? '局部演进图谱 (Local Lineage)' : 'Local Lineage'}</span>
            <svg class="related-svg" viewBox="0 0 ${viewWidth} ${viewHeight}">
              ${defsMarkup}
              ${linksMarkup}
              ${nodesMarkup}
            </svg>
          </div>
        `;
      }

      let relatedSectionHTML = '';
      if (relatedEventsList.length > 0) {
        relatedSectionHTML = `
          <div class="detail-section related-section">
            <span class="detail-title">${isChineseContent() ? '关联事件' : 'Related Events'}</span>
            ${precursorsHTML}
            ${successorsHTML}
            ${topologyHTML}
          </div>
        `;
      }

      return `
        <div class="timeline-details" id="${detailsId}" onclick="event.stopPropagation()" onkeydown="event.stopPropagation()">
          <div class="timeline-details-inner">
            <div class="detail-section">
              <span class="detail-title">${isChineseContent() ? '事件摘要' : 'Event Summary'}</span>
              <p class="commentary-text">${copy.description}</p>
            </div>
            <div class="detail-section">
              <span class="detail-title">${isChineseContent() ? '影响评估' : 'Impact Assessment'}</span>
              <ul class="impact-list">${impactItems}</ul>
            </div>
            <div class="detail-section">
              <span class="detail-title">${isChineseContent() ? '共识度与来源' : 'Consensus &amp; Sources'}</span>
              <div class="evidence-summary">
                <div class="evidence-item">
                  <span class="label">
                    ${isChineseContent() ? '重要度' : 'Significance'}
                    <span class="info-trigger" onmouseover="showGlobalTooltip(event, 'significance')" onmouseout="hideGlobalTooltip()">
                      <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.6;"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                    </span>
                  </span>
                  <span class="val">L${e.significance}</span>
                </div>
                <div class="evidence-item">
                  <span class="label">
                    ${isChineseContent() ? '分类' : 'Category'}
                    <span class="info-trigger" onmouseover="showGlobalTooltip(event, 'category')" onmouseout="hideGlobalTooltip()">
                      <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.6;"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                    </span>
                  </span>
                  <span class="val">${e.categories.map(c => labelFor(categoryLabels[c])).join(' / ')}</span>
                </div>
                <div class="evidence-item">
                  <span class="label">
                    ${isChineseContent() ? '共识度' : 'Consensus'}
                    <span class="info-trigger" onmouseover="showGlobalTooltip(event, 'consensus')" onmouseout="hideGlobalTooltip()">
                      <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.6;"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                    </span>
                  </span>
                  <span class="val">${labelFor(consensusLabels[e.consensusLevel])}</span>
                </div>
                <div class="evidence-item">
                  <span class="label">
                    ${isChineseContent() ? '影响指数' : 'Impact Index'}
                    <span class="info-trigger" onmouseover="showGlobalTooltip(event, 'impactIndex')" onmouseout="hideGlobalTooltip()">
                      <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.6;"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                    </span>
                  </span>
                  <span class="val">${e.impactIndex}/10</span>
                </div>
              </div>
              <ul class="source-list">${sourceItems}</ul>
            </div>
            ${relatedSectionHTML}
            <div style="display: flex; align-items: center; justify-content: space-between; gap: var(--gap-md); margin-top: var(--gap-lg); border-top: 1px solid color-mix(in oklch, var(--border) 82%, transparent); padding-top: 12px; padding-bottom: 2px;">
              <a class="source-title-link" href="/events/${e.slug || e.id}/" style="font-size: 13px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; color: var(--accent);" onclick="event.stopPropagation()">
                <span>${isChineseContent() ? '在页面内查看' : 'View in Page'}</span>
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="transform: translateY(-0.5px);"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
              <button class="details-collapse" type="button" onclick="collapseDetailsFromFooter(event, '${e.id}')" style="margin-top: 0; border-top: 0; padding: 0; width: auto; font-weight: 700; display: inline-flex; align-items: center; gap: 2px; margin-right: 8px;">${isChineseContent() ? '收起' : 'Collapse'}</button>
            </div>
          </div>
        </div>
      `;
    }

    /* ─── Related Events Navigation & SVG Highlight ─────────────────── */
    window.navigateToEvent = function(id) {
      if (typeof window.hideEventTooltip === 'function') window.hideEventTooltip();
      if (typeof window.hideGlobalTooltip === 'function') window.hideGlobalTooltip();
      state.openEventIds.clear();
      state.openEventIds.add(id);
      renderTimeline();

      setTimeout(() => {
        const targetItem = document.getElementById(`item-${id}`);
        if (targetItem) {
          targetItem.scrollIntoView({ behavior: 'smooth', block: 'start' });
          const card = targetItem.querySelector('.timeline-card-l3, .timeline-card-l2, .timeline-card-l1');
          if (card) {
            card.classList.add('flash-highlight-active');
            setTimeout(() => {
              card.classList.remove('flash-highlight-active');
            }, 2000);
          }
        }
      }, 120);

      history.pushState(null, '', eventStateUrl(id));
    };

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

    window.showEventTooltip = function(event, id) {
      const e = aiEvents.find(evt => evt.id === id);
      if (!e) return;
      
      const tooltip = document.getElementById('global-tooltip');
      if (!tooltip) return;

      const copy = localizedRecord(e);
      const catName = labelFor(categoryLabels[e.categories[0]]) || e.categories[0];
      
      const content = `
        <div style="font-family: var(--font-body); text-align: left; display: flex; flex-direction: column; gap: 6px;">
          <div style="display: flex; align-items: center; justify-content: space-between; font-family: var(--font-mono); font-size: 10px; color: var(--muted); border-bottom: 1px solid var(--border); padding-bottom: 4px; margin-bottom: 2px;">
            <span>${e.date}</span>
            <span style="color: var(--accent); font-weight: 700;">L${e.significance} · ${catName}</span>
          </div>
          <strong style="font-size: 12.5px; color: var(--fg); line-height: 1.4; display: block;">${copy.title}</strong>
          <p style="font-size: 11.5px; color: var(--muted); line-height: 1.45; margin: 0;">${copy.summary}</p>
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

    /* ─── Interactive Inline Details ────────────────────────────────── */
     window.openDetails = function(id, shouldPushState = true) {
      const e = aiEvents.find(item => item.id === id);
      if (!e) return;

      ensureFullEventData().catch(() => {});

      state.openEventIds.add(id);
      renderTimelineWithTransition();
      
      if (shouldPushState) {
        history.pushState(null, '', eventStateUrl(e.id));
      }
    };

    window.toggleDetails = function(id, shouldPushState = true) {
      const e = aiEvents.find(item => item.id === id);
      if (!e) return;

      ensureFullEventData().catch(() => {});

      if (state.openEventIds.has(id)) {
        state.openEventIds.delete(id);
      } else {
        state.openEventIds.add(id);
      }
      renderTimelineWithTransition();

      if (shouldPushState) {
        history.pushState(null, '', state.openEventIds.has(id) ? eventStateUrl(e.id) : window.location.pathname);
      }
    };

    window.collapseDetailsFromFooter = function(event, id) {
      event.stopPropagation();
      const e = aiEvents.find(item => item.id === id);
      const item = document.getElementById(`item-${id}`);
      if (!e || !item || !state.openEventIds.has(id)) return;

      const anchor = item.nextElementSibling || item;
      const anchorId = anchor.id;
      const previousTop = anchor.getBoundingClientRect().top;
      const previousScrollBehavior = document.documentElement.style.scrollBehavior;
      const previousHtmlOverflowAnchor = document.documentElement.style.overflowAnchor;
      const previousBodyOverflowAnchor = document.body.style.overflowAnchor;

      state.openEventIds.delete(id);
      document.documentElement.style.scrollBehavior = 'auto';
      document.documentElement.style.overflowAnchor = 'none';
      document.body.style.overflowAnchor = 'none';
      renderTimeline();

      const updatedAnchor = document.getElementById(anchorId);
      if (updatedAnchor) {
        const nextTop = updatedAnchor.getBoundingClientRect().top;
        window.scrollTo(window.scrollX, window.scrollY + nextTop - previousTop);
      }
      requestAnimationFrame(() => {
        document.documentElement.style.scrollBehavior = previousScrollBehavior;
        document.documentElement.style.overflowAnchor = previousHtmlOverflowAnchor;
        document.body.style.overflowAnchor = previousBodyOverflowAnchor;
      });

      history.pushState(null, '', window.location.pathname);
    };

    window.handleCardKeydown = function(event, id) {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      if (event.target !== event.currentTarget) return;
      event.preventDefault();
      toggleDetails(id);
    };

    window.closeDetails = function(shouldPushState = true) {
      state.openEventIds.clear();
      renderTimelineWithTransition();
      if (shouldPushState) {
        history.pushState(null, '', window.location.pathname);
      }
    };

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeDetails(true);
    });

    /* ─── Browser Back-button (History) Integration ─────────────────── */
    window.addEventListener('popstate', () => {
      const eventId = eventIdFromLocation();
      state.openEventIds.clear();
      if (eventId) state.openEventIds.add(eventId);
      renderTimelineWithTransition();

      if (eventId) {
        setTimeout(() => {
          const targetItem = document.getElementById(`item-${eventId}`);
          if (targetItem) {
            targetItem.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 150);
      }
    });

    /* ─── Search and Filtering ──────────────────────────────────────── */
    const searchField = elements.searchInput.closest('.filter-field');
    function updateSearchExpansion() {
      if (document.activeElement === elements.searchInput || elements.searchInput.value.trim() !== '') {
        searchField.classList.add('is-expanded');
      } else {
        searchField.classList.remove('is-expanded');
      }
    }
    
    elements.searchInput.addEventListener('focus', updateSearchExpansion);
    elements.searchInput.addEventListener('blur', updateSearchExpansion);
    
    elements.searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value;
      updateSearchExpansion();
      initFilterOptionsWithCounts();
      renderTimeline();
    });

    elements.significanceFilter.addEventListener('change', (e) => {
      state.filters.significance = e.target.value;
      initFilterOptionsWithCounts();
      renderTimeline();
    });
    elements.categoryFilter.addEventListener('change', (e) => {
      state.filters.category = e.target.value;
      initFilterOptionsWithCounts();
      renderTimeline();
    });
    elements.impactFilter.addEventListener('change', (e) => {
      state.filters.impactDimension = e.target.value;
      initFilterOptionsWithCounts();
      renderTimeline();
    });
    elements.consensusFilter.addEventListener('change', (e) => {
      state.filters.consensusLevel = e.target.value;
      initFilterOptionsWithCounts();
      renderTimeline();
    });
    elements.yearFilter.addEventListener('change', (e) => {
      state.filters.year = e.target.value;
      initFilterOptionsWithCounts();
      renderTimeline();
    });

    elements.filterResetBtn.addEventListener('click', () => {
      state.searchQuery = '';
      state.filters.significance = 'all';
      state.filters.category = 'all';
      state.filters.impactDimension = 'all';
      state.filters.consensusLevel = 'all';
      state.filters.year = 'all';
      
      elements.searchInput.value = '';
      elements.significanceFilter.value = 'all';
      elements.categoryFilter.value = 'all';
      elements.impactFilter.value = 'all';
      elements.consensusFilter.value = 'all';
      elements.yearFilter.value = 'all';
      
      updateSearchExpansion();
      initFilterOptionsWithCounts();
      renderTimeline();
    });
    
    // 初始化执行一次，防止浏览器缓存的输入文本与搜索框展开样式发生错位
    updateSearchExpansion();

    /* ─── Back to Top Button Interaction ────────────────────────────── */
    let toggleBackToTop = () => {};
    if (elements.backToTopBtn) {
      const timelineTitle = document.getElementById('timelineTitle');
      toggleBackToTop = () => {
        // 双重安全判定：只有当用户滚过了 Hero 区域（scrollY > 200）且时间轴标题已进入或越过屏幕底边时才显示
        if (window.scrollY > 200 && timelineTitle && timelineTitle.getBoundingClientRect().top <= window.innerHeight) {
          elements.backToTopBtn.classList.add('is-visible');
        } else {
          elements.backToTopBtn.classList.remove('is-visible');
        }
      };

      window.addEventListener('scroll', toggleBackToTop);
      
      elements.backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }

    /* ─── Initialization ────────────────────────────────────────────── */
    async function init() {
      // Prefer fragment-based UI state so event deep links do not create
      // separate crawlable query URLs. Keep legacy ?event= links working.
      const eventId = eventIdFromLocation();
      const legacyEventId = new URLSearchParams(window.location.search).get('event');
      if (legacyEventId) {
        history.replaceState(null, '', eventStateUrl(legacyEventId));
      }
      const readerPulseLoaded = await loadReaderPulseStateFromApi();
      if (!readerPulseLoaded) {
        syncLocalReaderPulseState(state.selectedForecastId);
      }
      
      // Update UI languages & themes
      updateLocale();
      updateTheme();
      await loadSiteData();
      
      // 此时数据已完全加载并完成初次渲染，页面高度已撑开，可以准确执行初始滚动判定
      toggleBackToTop();
      
      if (eventId && state.dataStatus === 'ready') {
        setTimeout(() => {
          openDetails(eventId, false);
          setTimeout(() => {
            const targetItem = document.getElementById(`item-${eventId}`);
            if (targetItem) {
              targetItem.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
          }, 150);
        }, 300);
      }

      // 全局顶导路由自适应分流，完美规避 http 线上各级 URL 部署 404
      document.addEventListener('click', function(e) {
        const logo = e.target.closest('.logo');
        const arcsBtn = e.target.closest('.nav-arcs-btn');
        const detailLink = e.target.closest('.source-title-link');
        
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

        if (detailLink) {
          const href = detailLink.getAttribute('href');
          const eventMatch = href?.match(/^\/?events\/([^/]+)\/?$/);
          if (eventMatch) {
            e.preventDefault();
            const id = eventMatch[1];
            if (id) {
              if (window.location.protocol === 'file:') {
                window.location.href = `events/${id}/index.html`;
              } else {
                window.location.href = sitePath(`/events/${id}/`);
              }
            }
          }
        }
      });
    }

    init();

    // Tooltip definitions and handlers
    const TOOLTIP_TEXTS = {
      significance: {
        zh: '<strong>重要度分级 (L1-L3)：</strong>编辑评定的历史重要度。<br>· <strong>L1 (Important)</strong>：长期脉络有记录价值，影响范围明确但有限。<br>· <strong>L2 (Key)</strong>：显著推动研究范式、产品、商业、政策或认知中至少一项。<br>· <strong>L3 (Turning Point)</strong>：改变主流技术路线、公众认知或社会行为，影响跨领域且可持续。',
        en: '<strong>Significance (L1-L3):</strong> Editorial historical evaluation.<br>· <strong>L1 (Important)</strong>: Worthy of long-term record; clear but limited impact.<br>· <strong>L2 (Key)</strong>: Key driver of paradigms, adoption, business models, or policy.<br>· <strong>L3 (Turning Point)</strong>: Reshapes tech trajectories, public perception, or regulation.'
      },
      category: {
        zh: '<strong>事件分类 (Category)：</strong>事件的主导属性类型。<br>· <strong>模型发布</strong>：具体 AI 模型、模型族或能力包的正式发布。<br>· <strong>能力突破</strong>：AI 首次或显著完成了此前不可行的任务。<br>· <strong>研究范式</strong>：论文、算法、架构或评测改变了研究路线。<br>· <strong>产品化</strong>：AI 能力进入了用户实际可用的产品、平台与商业服务。<br>· <strong>开源事件</strong>：开源权重、代码、数据集或生态改变了访问门槛。<br>· <strong>政策法规</strong>：法律、监管、政策或重大判决成为事件主体。<br>· <strong>安全伦理</strong>：对齐、伦理风险、治理框架、重大事故或暂停倡议。<br>· <strong>社会影响</strong>：就业、版权、舆论、劳动市场等社会外溢后果。',
        en: '<strong>Event Category:</strong> Primary attribute of the recorded event.<br>· <strong>Model</strong>: Release of models, model families, or capabilities.<br>· <strong>Capability</strong>: AI demonstrating previously impossible tasks.<br>· <strong>Research</strong>: Papers, architectures, or paradigms shifting research paths.<br>· <strong>Product</strong>: AI entering shipping products, workflows, or platforms.<br>· <strong>Open Source</strong>: Open weights, codes, or datasets changing access.<br>· <strong>Regulation</strong>: Laws, policies, regulatory acts, or court rulings.<br>· <strong>Safety</strong>: Alignment research, governance, ethical incidents, or safety actions.<br>· <strong>Social</strong>: Market, copyright, education, or macroeconomic impacts.'
      },
      consensus: {
        zh: '<strong>共识度</strong> — 反映事件的事实确定性及影响解释的认同程度。<br>请区分：共识度衡量的是<em>对事件的解读</em>到了什么层面，而非事件真实与否。<br>· <strong>广泛共识</strong>：事实清晰，影响解释被广泛接受。<br>· <strong>仍在讨论</strong>：事实清晰，但对影响规模、归因或后果存在分歧。<br>· <strong>共识形成中</strong>：事实和影响的判断都仍在积累中。',
        en: '<strong>Consensus</strong> — Reflects how settled the facts are and how widely the impact interpretation is accepted.<br>Note: This is about <em>interpretation status</em>, not whether the event is real.<br>· <strong>Broad Consensus</strong>: Facts are clear; the impact interpretation is widely agreed upon.<br>· <strong>Actively Debated</strong>: Facts are clear, but the scale, attribution, or consequences remain contested.<br>· <strong>Emerging Consensus</strong>: Both factual understanding and impact judgment are still developing.'
      },
      impactIndex: {
        zh: '<strong>影响指数算法 (0-10)：</strong>定量评估事件的影响强弱。<br>· <strong>维度得分</strong>：基于能力、经济、普惠、风险、认知等 5 维度影响严重度绝对值求和 (除以3，上限 4 分)。<br>· <strong>证据加分</strong>：支撑材料证据可信度 (最低A级+1.5分，D级-1分)。<br>· <strong>持续性加分</strong>：长期影响+1.5分，中期+1分，短期+0.5分。<br>· <strong>受众广度加分</strong>：影响群体数量 (≥4类+2分)。<br>· <strong>争议调整</strong>：高争议但证据不足时扣减 0.5 分。',
        en: '<strong>Impact Index Algorithm (0-10):</strong> Quantifies overall event impact.<br>· <strong>Dimension</strong>: Sum of severity absolute values of 5 key areas (cap/econ/access/risk/paradigm, max 4.0).<br>· <strong>Evidence</strong>: Lowest source evidence grade bonus (A:+1.5, D:-1.0).<br>· <strong>Durability</strong>: Higher timeframe bonus (long:+1.5, med:+1.0, short:+0.5).<br>· <strong>Scope</strong>: Number of affected groups (>=4 groups:+2.0).<br>· <strong>Controversy</strong>: Deducts 0.5 if high debate with low evidence.'
      }
    };

    window.showGlobalTooltip = function(event, key) {
      const tooltip = document.getElementById('global-tooltip');
      if (!tooltip) return;
      
      const lang = isChineseContent() ? 'zh' : 'en';
      tooltip.innerHTML = TOOLTIP_TEXTS[key][lang];
      
      tooltip.classList.add('show');
      
      // Calculate positioning dynamically
      const rect = event.currentTarget.getBoundingClientRect();
      
      let left = rect.left + (rect.width / 2) - 145; // 145 is half of tooltip width (290px)
      let top = rect.top - tooltip.offsetHeight - 8;
      
      // Guard boundaries (screen margins)
      if (left < 10) left = 10;
      if (left + 290 > window.innerWidth - 10) {
        left = window.innerWidth - 300;
      }
      
      // Flip below if not enough room on top
      if (top < 10) {
        top = rect.bottom + 8;
      }
      
      tooltip.style.left = `${left + window.scrollX}px`;
      tooltip.style.top = `${top + window.scrollY}px`;
    };

    window.hideGlobalTooltip = function() {
      const tooltip = document.getElementById('global-tooltip');
      if (tooltip) {
        tooltip.classList.remove('show');
      }
    };

    /* ─── Cookie Notice ──────────────────────────────────────────── */
    (function() {
      if (localStorage.getItem('ea-cookie-notice-dismissed')) return;
      const banner = document.getElementById('cookie-notice');
      if (banner) {
        banner.classList.add('show');
        banner.querySelector('.cookie-notice-close').onclick = function() {
          banner.classList.remove('show');
          localStorage.setItem('ea-cookie-notice-dismissed', '1');
        };
      }
    })();
