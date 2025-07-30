import re

from lxml import html, etree
from ..md_2_html.markdown_2_html import render_article


def test_remove_section():
    # html = importlib.resources.read_text("robot_basic", "html.py")
    with open("in.html", "r", encoding="utf-8") as f:
        content = f.read()
    root = html.fromstring(content)
    container = root.xpath("//section/*")[0]
    div_html_content = html.tostring(container, encoding="unicode", pretty_print=True)
    div_html_content = div_html_content.replace("测试", "{{}}")
    pattern_str_list = [
        r'data-.*?=".*?"',
        r'class=".*?"',
        r'id=".*?"',
        r'data-mpa-.*?=".*?"',
        r'mpa-from-tpl=".*?"',
        r'data-mpa-powered-by=".*?"',
        r'powered-by=".*?"',
        r'data-cropselx\d=".*?"',
        r'data-cropsely\d=".*?"',
        r'data-md5=".*?"',
        r'mpa-is-content=".*?"',
        r'<mpchecktext contenteditable="false"/>',
    ]
    result = re.sub("|".join(pattern_str_list), "", div_html_content)
    result = etree.tostring(
        html.fromstring(result), encoding="unicode", pretty_print=True
    )
    print(result)


def test_md_2_html():
    with open(
        r"D:\work\rpa_doc\RPA文章\GithubTrend.md",
        "r",
        encoding="utf-8",
    ) as f:
        content = f.read()
    result = render_article(content, "默认")
    print(result)
    with open("out.html", "w", encoding="utf-8") as f:
        f.write(result)
