#!/usr/bin/env python3
"""Download up to 3 Wikimedia Commons thumbnails per landmark (CC-licensed)."""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images", "places")
API = "https://commons.wikimedia.org/w/api.php"
UA = "YunnanItinerary/1.0 (educational; local mirror)"

# slug, search query, max images
SPOTS = [
    ("cuihu", "Cuihu Park Kunming", 3),
    ("daguan", "Daguan Park Kunming", 3),
    ("dianchi", "Dianchi Lake Kunming", 3),
    ("yuantong", "Yuantong Temple Kunming", 3),
    ("shaxi", "Shaxi ancient town Yunnan", 3),
    ("yujin-bridge", "Yujin Bridge Shaxi", 3),
    ("yulong", "Jade Dragon Snow Mountain", 3),
    ("blue-moon", "Blue Moon Valley Yunnan", 3),
    ("lijiang-old", "Old Town of Lijiang UNESCO", 3),
    ("shuhe", "Shuhe ancient town Lijiang", 3),
    ("baisha", "Baisha Old Town Lijiang", 3),
    ("golden-horse", "Jinma Biji Arch Kunming", 3),
]


def api(params):
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(API + "?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def search_files(query, limit):
    data = api(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,
            "srlimit": limit,
            "format": "json",
        }
    )
    hits = data.get("query", {}).get("search", [])
    return [h["title"] for h in hits]


def image_thumbs(titles, width=720):
    if not titles:
        return []
    data = api(
        {
            "action": "query",
            "titles": "|".join(titles),
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": str(width),
            "format": "json",
        }
    )
    pages = data.get("query", {}).get("pages", {})
    out = []
    for _pid, page in pages.items():
        if "imageinfo" not in page:
            continue
        ii = page["imageinfo"][0]
        url = ii.get("thumburl") or ii.get("url")
        if url:
            out.append(url)
    return out


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for slug, query, n in SPOTS:
        titles = search_files(query, n)
        thumbs = image_thumbs(titles[:n])
        manifest[slug] = []
        for i, url in enumerate(thumbs[:n], start=1):
            ext = ".jpg"
            if ".png" in url.lower():
                ext = ".png"
            dest = os.path.join(OUT, slug, f"{i}{ext}")
            try:
                sz = download(url, dest)
                rel = os.path.relpath(dest, ROOT).replace("\\", "/")
                manifest[slug].append(rel)
                print(f"OK {slug} {i} {sz} bytes -> {rel}")
            except Exception as e:
                print(f"FAIL {slug} {i} {url[:80]}... {e}", file=sys.stderr)
            time.sleep(0.4)
        time.sleep(0.5)

    man_path = os.path.join(OUT, "manifest.json")
    with open(man_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("Wrote", man_path)


if __name__ == "__main__":
    main()
