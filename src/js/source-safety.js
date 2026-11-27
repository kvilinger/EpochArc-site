// Source records are untrusted even when authored in the repository.
export const SOURCE_TYPE_LABELS = {
  primary: { en: 'Primary', zhHans: '原始资料' },
  official: { en: 'Official', zhHans: '官方资料' },
  news: { en: 'News', zhHans: '新闻报道' },
  analysis: { en: 'Analysis', zhHans: '分析资料' },
  encyclopedia: { en: 'Reference', zhHans: '百科资料' },
  paper: { en: 'Academic paper', zhHans: '学术论文' },
  blog: { en: 'Official blog', zhHans: '官方博文' },
  code: { en: 'Code repository', zhHans: '代码仓库' },
  tweet: { en: 'Social post', zhHans: '社交媒体帖子' },
  governance: { en: 'Official document', zhHans: '政策官方文档' },
  report: { en: 'Report', zhHans: '报告' },
  model_card: { en: 'Model card', zhHans: '模型卡' },
  benchmark: { en: 'Benchmark', zhHans: '基准测试' },
  unknown: { en: 'Source', zhHans: '来源资料' },
};
export function escapeSourceText(value) {
  return String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
}

export function safeSourceUrl(value) {
  if (typeof value !== 'string' || !value || /[\x00-\x1f]/.test(value)) return null;
  try {
    const parsed = new URL(value);
    return (parsed.protocol === 'http:' || parsed.protocol === 'https:') && parsed.hostname ? value : null;
  } catch {
    return null;
  }
}
