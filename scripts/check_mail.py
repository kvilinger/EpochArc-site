#!/usr/bin/env python3
"""
Gmail IMAP 邮件检查脚本（用于 Weekly Sweep 发现层）。
使用存储在 macOS 钥匙串中的 App Password，替代依赖短期测试令牌的 gws OAuth。

用法：
  python3 scripts/check_mail.py import-ai         # 最新 Import AI 邮件正文
  python3 scripts/check_mail.py the-batch          # 最新 The Batch 邮件正文
  python3 scripts/check_mail.py import-ai --list   # 仅列出最新一期标题
  python3 scripts/check_mail.py the-batch --list   # 仅列出最新一期标题
  python3 scripts/check_mail.py import-ai --limit 4 --max-chars 0  # 最近 4 期完整正文
  python3 scripts/check_mail.py test               # 测试连接
"""

import argparse
import email
from email.header import decode_header
import imaplib
import subprocess
import sys

EMAIL = "wolfggdtc@gmail.com"

def get_password():
    """从 macOS 钥匙串读取 App Password"""
    try:
        out = subprocess.check_output(
            ["security", "find-generic-password",
             "-a", EMAIL, "-s", "epocharc-gmail-app-password", "-w"],
            stderr=subprocess.DEVNULL
        )
        return out.decode().strip()
    except subprocess.CalledProcessError:
        print("ERROR: App Password not found in keychain. Run:", file=sys.stderr)
        print("  security add-generic-password -a \"wolfggdtc@gmail.com\" -s \"epocharc-gmail-app-password\" -w \"YOUR_PASSWORD\"", file=sys.stderr)
        sys.exit(1)

def decode_mime_header(val):
    """解码 MIME 编码的邮件头"""
    if val is None: return ""
    parts = decode_header(val)
    return " ".join(
        p.decode(c if c else 'utf-8', errors='replace') if isinstance(p, bytes) else p
        for p, c in parts
    )

def get_body(msg):
    """提取邮件正文（优先 plain text）"""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    return payload.decode(charset, errors='replace')
        # fallback: first text part
        for part in msg.walk():
            if part.get_content_type().startswith('text/'):
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    return payload.decode(charset, errors='replace')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or 'utf-8'
            return payload.decode(charset, errors='replace')
    return "[no body found]"

def fetch_messages(source, list_only=False, limit=1, max_chars=15000):
    """按时间倒序获取指定数量的最新邮件。"""
    PASSWORD = get_password()
    
    if source == 'import-ai':
        sender = 'importai@substack.com'
        label = "Import AI"
    elif source == 'the-batch':
        sender = 'thebatch@deeplearning.ai'
        label = "The Batch"
    else:
        print(f"Unknown source: {source}", file=sys.stderr)
        sys.exit(1)
    
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("INBOX")
    
    status, ids = mail.search(None, 'FROM', sender)
    if status != 'OK' or not ids[0]:
        print(f"No {label} emails found.")
        mail.logout()
        return
    
    all_ids = ids[0].split()
    selected_ids = reversed(all_ids[-limit:])

    for message_id in selected_ids:
        status, data = mail.fetch(message_id, '(BODY.PEEK[])')
        if status != 'OK' or not data or not isinstance(data[0], tuple):
            print(f"Failed to fetch {label} email {message_id.decode()}.", file=sys.stderr)
            continue

        msg = email.message_from_bytes(data[0][1])
        subject = decode_mime_header(msg['Subject'])
        date = msg['Date']

        print(f"=== {label} ===")
        print(f"Date: {date}")
        print(f"Subject: {subject}")
        print()

        if not list_only:
            body = get_body(msg)
            if max_chars > 0 and len(body) > max_chars:
                body = body[:max_chars] + "\n\n[... truncated ...]"
            print(body)
        print()

    mail.logout()

def test_connection():
    """测试 IMAP 连接"""
    PASSWORD = get_password()
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("INBOX")
    status, ids = mail.search(None, 'ALL')
    total = len(ids[0].split()) if ids[0] else 0
    
    # Count by sender
    for label, sender in [("Import AI", "importai@substack.com"),
                           ("The Batch", "thebatch@deeplearning.ai")]:
        s, i = mail.search(None, 'FROM', sender)
        cnt = len(i[0].split()) if i[0] else 0
        print(f"  {label}: {cnt} emails")
    
    print(f"Total inbox: {total} emails")
    mail.logout()
    print("Connection: ✅ OK")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check Gmail via IMAP for sweep sources")
    parser.add_argument('source', nargs='?', default='test',
                        choices=['import-ai', 'the-batch', 'test'])
    parser.add_argument('--list', action='store_true', help='仅列出标题不显示正文')
    parser.add_argument('--limit', type=int, default=1, help='读取最近 N 封邮件（默认：1）')
    parser.add_argument(
        '--max-chars',
        type=int,
        default=15000,
        help='每封正文最大字符数；0 表示不截断（默认：15000）',
    )
    args = parser.parse_args()

    if args.limit < 1:
        parser.error('--limit must be at least 1')
    if args.max_chars < 0:
        parser.error('--max-chars cannot be negative')

    if args.source == 'test':
        test_connection()
    else:
        fetch_messages(
            args.source,
            list_only=args.list,
            limit=args.limit,
            max_chars=args.max_chars,
        )
