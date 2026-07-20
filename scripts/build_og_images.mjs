#!/usr/bin/env node
/** Generate event-specific Open Graph images as 1200x630 PNG files. */

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.dirname(scriptDir);
const eventsPath = path.join(rootDir, 'data', 'events.json');
const outputDir = path.join(rootDir, 'assets', 'og', 'events');
const logoPath = path.join(rootDir, 'assets', 'logo-icon.svg');
const logoDataUri = `data:image/svg+xml;base64,${(await fs.readFile(logoPath)).toString('base64')}`;

function clean(value) {
  return String(value ?? '').replace(/\s*[—–‑]+\s*/g, ' - ').trim();
}

function xml(value) {
  return clean(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;');
}

function visualUnits(text) {
  return [...text].reduce((total, character) => total + (/[^\u0000-\u00ff]/.test(character) ? 1 : 0.55), 0);
}

function wrapTitle(value, maxUnits = 16, maxLines = 4) {
  const text = clean(value).trim();
  const tokens = /[\u3400-\u9fff]/.test(text) ? [...text] : text.split(/\s+/).map((word) => `${word} `);
  const lines = [];
  let line = '';
  for (const token of tokens) {
    const candidate = `${line}${token}`.trimEnd();
    if (line && visualUnits(candidate) > maxUnits) {
      lines.push(line.trim());
      line = token.trimStart();
      if (lines.length === maxLines - 1) break;
    } else {
      line = `${line}${token}`;
    }
  }
  if (line.trim() && lines.length < maxLines) lines.push(line.trim());
  const consumed = lines.join(/[\u3400-\u9fff]/.test(text) ? '' : ' ');
  if (consumed.length < text.length - 2) {
    lines[lines.length - 1] = `${lines[lines.length - 1].replace(/[ .]+$/, '')}...`;
  }
  return lines;
}

function categoryLabel(category) {
  const labels = {
    capability: 'CAPABILITY',
    product: 'PRODUCT',
    commerce: 'COMMERCE',
    governance: 'GOVERNANCE',
    safety: 'SAFETY',
    society: 'SOCIETY',
    research: 'RESEARCH',
    policy: 'POLICY'
  };
  return labels[category] || clean(category).toUpperCase();
}

function eventSvg(event) {
  const title = event.title?.en || event.id;
  const lines = wrapTitle(title);
  const fontSize = lines.length >= 4 ? 54 : lines.length === 3 ? 60 : 66;
  const lineHeight = Math.round(fontSize * 1.08);
  const titleLines = lines.map((line, index) => (
    `<text x="84" y="${190 + (index * lineHeight)}" class="title">${xml(line)}</text>`
  )).join('');
  const primaryCategory = categoryLabel(event.categories?.[0] || 'milestone');
  const categoryWidth = Math.max(106, 32 + (primaryCategory.length * 8));
  const categoryY = 190 + ((lines.length - 1) * lineHeight) + 30;
  const date = clean(event.displayDate?.en || event.date);

  return `
  <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
    <rect width="1200" height="630" fill="#f7f8fb"/>
    <rect width="18" height="630" fill="#2677ff"/>
    <path d="M830 0 C970 120 984 274 1200 300" fill="none" stroke="#dce8ff" stroke-width="2"/>
    <path d="M910 0 C1010 105 1038 205 1200 218" fill="none" stroke="#e7eef9" stroke-width="1"/>
    <circle cx="1100" cy="82" r="148" fill="#edf3ff"/>
    <circle cx="1100" cy="82" r="7" fill="#2677ff"/>
    <style>
      .brand { font: 700 28px -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif; fill: #121826; letter-spacing: -0.7px; }
      .label { font: 700 14px Menlo, Monaco, monospace; fill: #5f6b7a; letter-spacing: 1.8px; }
      .title { font: 720 ${fontSize}px -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif; fill: #121826; letter-spacing: -1.8px; }
      .meta { font: 650 22px -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif; fill: #121826; }
      .small { font: 700 14px Menlo, Monaco, monospace; fill: #2677ff; letter-spacing: 1px; }
      .domain { font: 650 13px Menlo, Monaco, monospace; fill: #5f6b7a; letter-spacing: 1px; }
    </style>
    <image href="${logoDataUri}" x="84" y="43" width="34" height="34" preserveAspectRatio="xMidYMid meet"/>
    <text x="130" y="72" class="brand">EpochArc</text>
    <text x="1116" y="73" class="label" text-anchor="end">AI MILESTONE</text>
    ${titleLines}
    <rect x="84" y="${categoryY}" width="${categoryWidth}" height="36" rx="8" fill="#e7efff" stroke="#c9dbff"/>
    <text x="${84 + (categoryWidth / 2)}" y="${categoryY + 24}" class="small" text-anchor="middle">${xml(primaryCategory)}</text>
    <line x1="84" y1="515" x2="1116" y2="515" stroke="#dfe4eb" stroke-width="1"/>
    <text x="84" y="565" class="meta">${xml(date)}</text>
    <text x="84" y="604" class="label">L${xml(event.significance)} · IMPACT ${xml(event.impactIndex)}/10</text>
    <text x="1116" y="604" class="domain" text-anchor="end">epoch-arc.com</text>
  </svg>`;
}

const events = JSON.parse(await fs.readFile(eventsPath, 'utf8'));
const requestedSlug = process.argv[2];
const selectedEvents = requestedSlug ? events.filter((event) => event.slug === requestedSlug) : events;
if (requestedSlug && selectedEvents.length !== 1) {
  throw new Error(`Unknown event slug: ${requestedSlug}`);
}
if (!requestedSlug) await fs.rm(outputDir, { recursive: true, force: true });
await fs.mkdir(outputDir, { recursive: true });

await Promise.all(selectedEvents.map(async (event) => {
  const filename = path.join(outputDir, `${event.slug}.png`);
  await sharp(Buffer.from(eventSvg(event)))
    .png({ compressionLevel: 9, palette: true })
    .toFile(filename);
}));

const distDir = path.join(rootDir, 'dist', 'assets', 'og', 'events');
try {
  await fs.access(path.join(rootDir, 'dist'));
  if (!requestedSlug) await fs.rm(distDir, { recursive: true, force: true });
  await fs.mkdir(distDir, { recursive: true });
  if (requestedSlug) {
    await fs.copyFile(
      path.join(outputDir, `${requestedSlug}.png`),
      path.join(distDir, `${requestedSlug}.png`)
    );
  } else {
    await fs.cp(outputDir, distDir, { recursive: true });
  }
} catch {
  // A standalone pre-build run may not have a dist directory yet.
}

console.log(`✅ Generated and synced ${selectedEvents.length} event Open Graph PNG image(s)`);
