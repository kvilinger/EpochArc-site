#!/usr/bin/env python3
"""Validate Vite output for unresolved stylesheet imports."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
IMPORT_RE = re.compile(r"@import\s+(?:url\(\s*)?[\"']?[^;\"')]+", re.IGNORECASE)


def main() -> None:
    if not DIST.is_dir():
        raise SystemExit("dist/ does not exist; run Vite build first")

    css_files = sorted((DIST / "assets").glob("*.css"))
    if not css_files:
        raise SystemExit("No generated CSS assets found in dist/assets")

    errors: list[str] = []
    for path in css_files:
        content = path.read_text(encoding="utf-8")
        imports = IMPORT_RE.findall(content)
        if imports:
            errors.append(
                f"{path.relative_to(ROOT)}: unresolved CSS import(s): "
                + ", ".join(imports)
            )

    if errors:
        raise SystemExit("Build asset validation failed:\n" + "\n".join(errors))

    print(f"✅ Validated {len(css_files)} generated CSS asset(s); no unresolved imports")


if __name__ == "__main__":
    main()
