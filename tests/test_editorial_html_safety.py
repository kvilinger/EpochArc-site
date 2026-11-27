"""Security regressions for citation URLs and JSON embedded into HTML script elements."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from html_safety import http_url, script_json, claim_source_link
from build_localized_pages import rewrite_json_ld


class EmbeddedDataSafety(unittest.TestCase):
    def test_script_end_tag_is_escaped_and_data_round_trips(self):
        data = {'title': '</script><img src=x onerror=alert(1)> & quoted "text"', 'zh': '中文'}
        encoded = script_json(data, ensure_ascii=False)
        self.assertNotIn('</script', encoded.lower())
        self.assertEqual(data, json.loads(encoded))

    def test_claim_source_external_fallback_checks_scheme(self):
        link = claim_source_link({'title': '<img>', 'url': 'javascript:alert(1)'}, 'x')
        self.assertNotIn('href=', link)
        self.assertIn('&lt;img&gt;', link)
        self.assertIn('href="https://example.com/"', claim_source_link({'url': 'https://example.com/'}, 'x'))
        self.assertIn('href="#source-x"', claim_source_link({'url': 'javascript:alert(1)'}, 'x', 1))

    def test_zh_jsonld_never_marks_english_body_as_chinese(self):
        payload = {'@type': 'Article', 'headline': 'English', 'description': 'English description',
                   'articleBody': 'English body', 'articleSection': 'Safety', 'url': 'https://epoch-arc.com/events/x/'}
        markup = '<script type="application/ld+json">' + json.dumps(payload) + '</script>'
        result = rewrite_json_ld(markup, 'zh-Hans', '中文标题 · EpochArc', '中文描述')
        body = result.split('>', 1)[1].rsplit('</script>', 1)[0]
        decoded = json.loads(body)
        self.assertEqual('zh-Hans', decoded['inLanguage'])
        self.assertEqual('中文标题', decoded['headline'])
        self.assertNotIn('articleBody', decoded)
        self.assertNotIn('articleSection', decoded)
        self.assertEqual('https://epoch-arc.com/zh-hans/events/x/', decoded['url'])

    def test_non_http_urls_are_rejected(self):
        for value in ['javascript:alert(1)', 'data:text/html,a', '//example.com', 'https://example.com\nattack', None]:
            self.assertIsNone(http_url(value))
        self.assertEqual('https://example.com/a?b=1', http_url('https://example.com/a?b=1'))


if __name__ == '__main__':
    unittest.main()
