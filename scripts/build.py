#!/usr/bin/env python3
"""从 SKILL.md 生成 index.html（静态站点）。

用法：
    python3 scripts/build.py
"""
import json
import pathlib
import sys

try:
    import markdown
except ImportError:
    sys.exit("缺少依赖：pip install markdown")

ROOT = pathlib.Path(__file__).resolve().parent.parent


def strip_front_matter(text: str) -> str:
    """去掉 YAML front-matter，只保留正文。"""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip("\n")
    return text


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>👟 跑步姿态训练指南</title>
<meta name="description" content="运动与健身：分析并纠正跑步姿态——着地方式、步频步幅、身体前倾角度的优化。">
<style>
:root {
  --bg: #0e1117; --panel: #161b22; --text: #e6edf3; --muted: #8b949e;
  --accent: #3fb950; --line: #30363d;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font: 16px/1.75 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
        "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
}
.wrap { max-width: 860px; margin: 0 auto; padding: 48px 24px 96px; }
header {
  border-bottom: 1px solid var(--line); padding-bottom: 24px; margin-bottom: 32px;
}
header .badge {
  display: inline-block; font-size: 12px; letter-spacing: .08em; text-transform: uppercase;
  color: var(--accent); border: 1px solid var(--accent); border-radius: 999px;
  padding: 2px 10px; margin-bottom: 12px;
}
header h1 { font-size: 2em; margin: .2em 0 .3em; }
header p { color: var(--muted); margin: 0; }
h2 { font-size: 1.35em; margin-top: 2em; padding-bottom: .3em; border-bottom: 1px solid var(--line); }
h3 { font-size: 1.1em; margin-top: 1.6em; color: var(--accent); }
a { color: #58a6ff; }
table { width: 100%; border-collapse: collapse; margin: 1.2em 0; font-size: .95em; }
th, td { border: 1px solid var(--line); padding: 10px 12px; text-align: left; }
th { background: var(--panel); }
tr:nth-child(even) td { background: rgba(255,255,255,.02); }
blockquote {
  margin: 1.2em 0; padding: .6em 1em; border-left: 3px solid var(--accent);
  background: var(--panel); color: var(--muted);
}
code { background: var(--panel); padding: .15em .4em; border-radius: 4px; font-size: .9em; }
pre { background: var(--panel); padding: 16px; border-radius: 8px; overflow-x: auto; }
pre code { background: none; padding: 0; }
ul, ol { padding-left: 1.4em; }
nav.toc { background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
          padding: 16px 20px; margin-bottom: 32px; font-size: .92em; }
nav.toc .toc-title { color: var(--muted); font-size: .85em; letter-spacing: .06em;
                     text-transform: uppercase; margin-bottom: 8px; }
nav.toc ul { list-style: none; padding-left: 0; margin: 0; }
nav.toc ul ul { padding-left: 1.2em; }
nav.toc li { margin: .25em 0; }
footer { margin-top: 64px; padding-top: 24px; border-top: 1px solid var(--line);
         color: var(--muted); font-size: .85em; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <span class="badge">运动与健身 · v{{VERSION}}</span>
    <h1>👟 跑步姿态训练指南</h1>
    <p>着地方式 · 步频步幅 · 身体前倾角度 —— 科学分析与纠正</p>
  </header>
  <nav class="toc">
    <div class="toc-title">目录</div>
    <div class="toc" id="toc"></div>
  </nav>
  <main id="content">
{{BODY}}
  </main>
  <footer>
    跑步姿态训练指南 · 内容版本 {{VERSION}} · 由 GitHub Pages 自动部署
  </footer>
</div>
<script>
// 从正文 h2 生成目录
(function () {
  var toc = document.getElementById('toc');
  var heads = document.querySelectorAll('#content h2');
  if (!heads.length) { document.querySelector('nav.toc').style.display = 'none'; return; }
  var ul = document.createElement('ul');
  heads.forEach(function (h, i) {
    if (!h.id) h.id = 'sec-' + i;
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#' + h.id; a.textContent = h.textContent;
    li.appendChild(a); ul.appendChild(li);
  });
  toc.appendChild(ul);
})();
</script>
</body>
</html>
"""


def main() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    meta = json.loads((ROOT / "_meta.json").read_text(encoding="utf-8"))

    body_html = markdown.markdown(
        strip_front_matter(skill),
        extensions=["tables", "fenced_code", "sane_lists"],
    )

    version = meta.get("version", "")
    page = TEMPLATE.replace("{{VERSION}}", version).replace("{{BODY}}", body_html)

    out = ROOT / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"已生成 {out.relative_to(ROOT)}（{len(body_html)} 字节正文）")


if __name__ == "__main__":
    main()
