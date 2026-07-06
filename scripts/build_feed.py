#!/usr/bin/env python3
"""Build rss.xml from data/events.json for the EpochArc timeline.

Generates an Atom/RSS feed of all events, sorted by date descending.
Call from npm build or standalone.
"""
import json, os, datetime
from html import escape

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
OUTPUT_PATH = os.path.join(ROOT_DIR, 'rss.xml')

SITE_URL = 'https://epoch-arc.com'
FEED_TITLE_EN = 'EpochArc · AI Timeline'
FEED_TITLE_ZH = 'EpochArc · AI 发展史时间线'
FEED_DESC_EN = 'Curated AI milestones from 1950 to the present, with impact analysis and evidence.'
FEED_DESC_ZH = '从 1950 年至今的人工智能里程碑事件时间线，附影响分析和来源证据。'

def build_feed():
    with open(os.path.join(DATA_DIR, 'events.json'), 'r', encoding='utf-8') as f:
        events = json.load(f)

    # Sort by date descending (newest first)
    sorted_events = sorted(events, key=lambda e: e.get('date', ''), reverse=True)

    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    last_event_date = sorted_events[0]['date'] if sorted_events else now

    entries = []
    for e in sorted_events:
        eid = e['id']
        title_en = e.get('title', {}).get('en', eid)
        summary_en = e.get('searchSummary', {}).get('en', e.get('summary', {}).get('en', ''))
        # Truncate summary to 500 chars for feed
        if len(summary_en) > 500:
            summary_en = summary_en[:497] + '...'
        pub_date = e.get('date', '')
        # ISO 8601 format for Atom
        pub_date_iso = pub_date + 'T00:00:00Z' if pub_date else now
        categories = e.get('categories', [])
        cat_tags = ''.join(f'<category term="{escape(c)}" />' for c in categories)

        entries.append(f'''  <entry>
    <id>tag:epoch-arc.com,{pub_date}:events/{eid}</id>
    <published>{pub_date_iso}</published>
    <updated>{pub_date_iso}</updated>
    <title type="html">{escape(title_en)}</title>
    <link href="{SITE_URL}/events/{eid}/" rel="alternate" type="text/html" />
    <summary type="html">{escape(summary_en)}</summary>
    {cat_tags}
  </entry>''')

    feed = f'''<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <id>tag:epoch-arc.com,2026:rss</id>
  <title>{FEED_TITLE_EN}</title>
  <subtitle>{FEED_DESC_EN}</subtitle>
  <link href="{SITE_URL}/" rel="alternate" type="text/html" />
  <link href="{SITE_URL}/rss.xml" rel="self" type="application/atom+xml" />
  <updated>{last_event_date}T00:00:00Z</updated>
  <author>
    <name>EpochArc</name>
    <uri>{SITE_URL}</uri>
  </author>
  <generator uri="https://github.com/kvilinger/EpochArc-site">EpochArc build_feed.py</generator>
  <rights>CC BY 4.0</rights>
{chr(10).join(entries)}
</feed>'''

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(feed)

    print(f"✅ RSS feed generated: {OUTPUT_PATH} ({len(feed)/1024:.1f} KB, {len(sorted_events)} entries)")

if __name__ == '__main__':
    build_feed()
