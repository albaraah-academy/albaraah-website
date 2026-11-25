"""Builds the news from news.json (newest first):
- news/<slug>.html: one page per item, with its own share picture and share buttons;
- news/index.html: «كل الأخبار», every item;
- the home page's news block (between <!-- news:start --> and <!-- news:end -->): the three newest.

Each item: slug, when, title, summary, image (/assets/…), share_image (/assets/… 1200×630, optional), image_alt, body (paragraphs; <strong> allowed).
Run:  python tools/build_news.py   (then preview, commit and push)."""
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://albaraah.org'
NAME = 'أكاديمية البراءة التعليمية'
esc = html.escape


def rel(path):
    """/assets/… whether news.json holds it relative or absolute."""
    return path[len(SITE):] if path.startswith(SITE) else path


def url(item):
    return f"{SITE}/news/{item['slug']}"


def share(item, pad):
    wa = 'https://wa.me/?text=' + quote(f"{item['title']} — {NAME}\n{url(item)}")
    fb = 'https://www.facebook.com/sharer/sharer.php?u=' + quote(url(item), safe='')
    p = ' ' * pad
    return (f'{p}<div class="share">\n{p}  <span>شاركوا الخبر:</span>\n'
            f'{p}  <a class="share-btn share-wa" href="{esc(wa)}" target="_blank" rel="noopener">واتساب</a>\n'
            f'{p}  <a class="share-btn share-fb" href="{esc(fb)}" target="_blank" rel="noopener">فيسبوك</a>\n'
            f'{p}  <button type="button" class="share-btn share-copy" data-copy="{url(item)}">نسخ الرابط</button>\n{p}</div>')


def head(title, description, canonical, image, kind='website', w=1200, h=630):
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} | {NAME}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="{kind}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="{NAME}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{SITE}{image}">
  <meta property="og:image:width" content="{w}">
  <meta property="og:image:height" content="{h}">
  <meta property="og:locale" content="ar_SY">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#a9612c">
  <link rel="icon" href="/assets/favicon.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v=2026-11-26-news">
</head>
<body>
  <header class="site-header">
    <div class="wrap header-row">
      <a class="brand" href="/">
        <img src="/assets/academy.jpg" alt="شعار {NAME}" width="52" height="52">
        <span><strong>{NAME}</strong><small>سوريا · حلب · الباب</small></span>
      </a>
      <a class="btn btn-outline" href="/news/">كل الأخبار</a>
    </div>
  </header>
'''


FOOT = f'''  <footer class="site-footer">
    <div class="wrap footer-row">
      <p>© 2026 {NAME}</p>
      <p><a href="/">الصفحة الرئيسية</a> · <a href="https://portal.albaraah.org/" target="_blank" rel="noopener">بوابة المدرسة</a></p>
    </div>
  </footer>
  <script src="/share.js"></script>
</body>
</html>
'''


def card(item, pad, heading='h3'):
    p = ' ' * pad
    return (f'{p}<article class="news-item">\n'
            f'{p}  <a href="/news/{item["slug"]}"><img src="{item["image"]}" alt="{esc(item.get("image_alt", ""))}" loading="lazy"></a>\n'
            f'{p}  <div class="news-body">\n'
            f'{p}    <p class="news-date">{esc(item["when"])}</p>\n'
            f'{p}    <{heading}><a href="/news/{item["slug"]}">{esc(item["title"])}</a></{heading}>\n'
            f'{p}    <p>{esc(item["summary"])}</p>\n'
            f'{p}    <p><a class="news-more" href="/news/{item["slug"]}">اقرأ الخبر ←</a></p>\n'
            f'{share(item, pad + 4)}\n'
            f'{p}  </div>\n{p}</article>')


def main():
    data = json.loads((ROOT / 'news.json').read_text(encoding='utf-8'))
    items = data['items']
    for item in items:
        item['image'] = rel(item['image'])
        if item.get('share_image'):
            item['share_image'] = rel(item['share_image'])
    (ROOT / 'news').mkdir(exist_ok=True)
    for item in items:
        img = item.get('share_image') or item['image']
        body = '\n'.join(f'      <p>{p}</p>' for p in item.get('body') or [item['summary']])
        page = (head(item['title'], item['summary'], url(item), img, 'article') +
                f'''  <main class="section">
    <article class="wrap news-page">
      <p class="eyebrow">أخبارنا</p>
      <p class="news-date">{esc(item["when"])}</p>
      <h1>{esc(item["title"])}</h1>
      <img class="news-hero" src="{item["image"]}" alt="{esc(item.get("image_alt", ""))}">
{body}
{share(item, 6)}
    </article>
  </main>
''' + FOOT)
        (ROOT / 'news' / f'{item["slug"]}.html').write_text(page, encoding='utf-8')
    archive = (head('كل الأخبار', f'أخبار {NAME} وأنشطة طلابها.', f'{SITE}/news/', '/assets/share.jpg') +
               '  <main class="section">\n    <div class="wrap">\n      <p class="eyebrow">أخبارنا</p>\n      <h1>كل الأخبار</h1>\n      <div class="news-list">\n' +
               '\n'.join(card(i, 8, 'h2') for i in items) + '\n      </div>\n    </div>\n  </main>\n' + FOOT)
    (ROOT / 'news' / 'index.html').write_text(archive, encoding='utf-8')
    home = ROOT / 'index.html'
    s = home.read_text(encoding='utf-8')
    a, b = s.index('<!-- news:start -->'), s.index('<!-- news:end -->')
    more = '\n          <p class="center"><a class="btn btn-outline" href="/news/">كل الأخبار</a></p>'
    block = '<!-- news:start -->\n        <div class="news-list">\n' + '\n'.join(card(i, 10) for i in items[:3]) + '\n        </div>' + more + '\n        '
    home.write_text(s[:a] + block + s[b:], encoding='utf-8')
    # news.json keeps an absolute link and picture for the portal's card.
    for item in items:
        item['link'] = url(item)
        item['image'] = SITE + item['image']          # the portal shows pictures of the site only, by full address
    (ROOT / 'news.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(len(items), 'news items built')


if __name__ == '__main__':
    main()
