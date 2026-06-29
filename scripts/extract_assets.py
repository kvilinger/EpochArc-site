#!/usr/bin/env python3
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, 'index.html')
CSS_DIR = os.path.join(ROOT_DIR, 'src', 'css')
JS_DIR = os.path.join(ROOT_DIR, 'src', 'js')

os.makedirs(CSS_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 提取 CSS
# 寻找最后一处 <style>...</style> (通常就是主 CSS)
style_blocks = list(re.finditer(r'<style>(.*?)</style>', content, re.DOTALL))
if style_blocks:
    main_style = style_blocks[-1].group(1)
    
    # 抽离全局基础变量和重置样式作为 global.css
    # 我们找 :root 到 curator-commentary 或者其他地方的界限
    # 简单起见，我们将前 380 行（包含主题变量、font、topnav、reset等基础样式）提取为 global.css，其余为 main.css
    lines = main_style.split('\n')
    
    # 我们可以根据常见的 .topnav 或 .global-tooltip 划分
    # 让 Python 来定位具体的通用重置样式边界
    boundary = 0
    for idx, line in enumerate(lines):
        if ' Curated Category ' in line or '/* ─── Timeline Structure' in line:
            boundary = idx
            break
            
    if boundary == 0:
        boundary = 400 # 兜底行数
        
    global_css = '\n'.join(lines[:boundary])
    main_css = '\n'.join(lines[boundary:])
    
    with open(os.path.join(CSS_DIR, 'global.css'), 'w', encoding='utf-8') as sf:
        sf.write(global_css.strip() + '\n')
        
    with open(os.path.join(CSS_DIR, 'main.css'), 'w', encoding='utf-8') as mf:
        # 在 main.css 第一行导入 global.css
        mf.write('@import "./global.css";\n\n' + main_css.strip() + '\n')
        
    print("✅ Extracted CSS to src/css/global.css and src/css/main.css")
else:
    print("❌ No style block found!")

# 2. 提取 JS
# 寻找最后一处 <script>...</script> (通常就是主逻辑)
script_blocks = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
if script_blocks:
    main_script = script_blocks[-1].group(1)
    
    with open(os.path.join(JS_DIR, 'main.js'), 'w', encoding='utf-8') as jf:
        jf.write(main_script.strip() + '\n')
        
    print("✅ Extracted JS to src/js/main.js")
else:
    print("❌ No script block found!")

# 3. 更新 index.html
# 清空 <style>...</style> 和 <script>...</script> 替换为模块化外部链接
new_content = content
# 替换 CSS (保留 <style> 块所在的 <head>，只替换 style 标签及其内容)
# 为了精确起见，我们把原来的 <style>...</style> 整体替换为 link 标签
# 注意这里如果有多个 style 块，正则需要精确匹配最后一个
new_content = re.sub(
    r'<style>.*?</style>', 
    '<link rel="stylesheet" href="./src/css/main.css">', 
    new_content, 
    flags=re.DOTALL
)

# 替换最后一个 script 块（主 JS 逻辑）
# 在最后一个 </script> 之前，主 script 大约有 1800 行
# 我们将其替换为引入 main.js
# 我们通过先匹配最后一个 script 的特征来确保替换正确
# 我们知道 main.js 中包含 window.openDetails 等函数，所以用正则来只替换主 script 标签
main_script_pattern = r'<script>\s*\(function\(\)\s*\{.*?window\.openDetails.*?\s*\}\)\(\);\s*</script>'
if re.search(main_script_pattern, new_content, re.DOTALL):
    new_content = re.sub(
        main_script_pattern,
        '<script type="module" src="./src/js/main.js"></script>',
        new_content,
        flags=re.DOTALL
    )
else:
    # 兜底：如果上面的复杂正则匹配失败，我们替换最后一个没有任何属性的 <script> 标签
    # 最后一个 <script> 标签在 2506 行
    parts = re.split(r'<script>', new_content)
    if len(parts) > 1:
        # 最后一部分有 </script>
        last_part = parts[-1]
        subparts = re.split(r'</script>', last_part, 1)
        if len(subparts) > 1:
            parts[-1] = '<script type="module" src="./src/js/main.js"></script>' + subparts[1]
            new_content = '<script>'.join(parts)

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("✅ Updated index.html with modular external references")
