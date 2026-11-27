"""Safe helpers for untrusted citation text and JSON embedded in script elements."""
import html
import json
from urllib.parse import urlsplit


def http_url(value):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        return None
    try:
        parts = urlsplit(value)
        return value if parts.scheme.lower() in {'http', 'https'} and parts.netloc else None
    except ValueError:
        return None


SOURCE_TYPE_LABELS = {
    'primary': {'en': 'Primary', 'zhHans': '原始资料'},
    'official': {'en': 'Official', 'zhHans': '官方资料'},
    'news': {'en': 'News', 'zhHans': '新闻报道'},
    'analysis': {'en': 'Analysis', 'zhHans': '分析资料'},
    'encyclopedia': {'en': 'Reference', 'zhHans': '百科资料'},
    'paper': {'en': 'Academic paper', 'zhHans': '学术论文'},
    'blog': {'en': 'Official blog', 'zhHans': '官方博文'},
    'code': {'en': 'Code repository', 'zhHans': '代码仓库'},
    'tweet': {'en': 'Social post', 'zhHans': '社交媒体帖子'},
    'governance': {'en': 'Official document', 'zhHans': '政策官方文档'},
    'report': {'en': 'Report', 'zhHans': '报告'},
    'model_card': {'en': 'Model card', 'zhHans': '模型卡'},
    'benchmark': {'en': 'Benchmark', 'zhHans': '基准测试'},
    'unknown': {'en': 'Source', 'zhHans': '来源资料'},
}


def claim_source_link(source, source_id, source_number=None):
    title = html.escape(str(source.get('title', source_id)), quote=True)
    if source_number:
        return f'<a href="#source-{html.escape(str(source_id), quote=True)}" title="{title}">[{source_number}]</a>'
    url = http_url(source.get('url'))
    if url:
        return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer" title="{title}">[↗]</a>'
    return f'<span title="{title}">[—]</span>'


def script_json(value, **kwargs):
    # Escaping '<' prevents HTML's script end-tag parser seeing </script>.
    return json.dumps(value, **kwargs).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
