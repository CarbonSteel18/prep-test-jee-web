from http.server import BaseHTTPRequestHandler
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
FILE_ID_RE = re.compile(r'/file/d/([a-zA-Z0-9_-]+)')

# Kept deliberately small and low-concurrency: a burst of many simultaneous
# requests reads as a scraping attack to MathonGo's link service and gets
# throttled. A few at a time, comfortably inside Vercel's Hobby-plan
# 10-second function limit, is far more reliable even though it's slower.
MAX_LINKS_PER_REQUEST = 6
MAX_CONCURRENCY = 3
PER_LINK_TIMEOUT_SECONDS = 4


def resolve_one(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=PER_LINK_TIMEOUT_SECONDS) as resp:
            final_url = resp.geturl()
            html = resp.read(200000).decode('utf-8', errors='ignore')

        title_match = TITLE_RE.search(html)
        title = title_match.group(1).strip() if title_match else None
        if title and title.endswith(' - Google Drive'):
            title = title[: -len(' - Google Drive')]

        id_match = FILE_ID_RE.search(final_url)
        file_id = id_match.group(1) if id_match else None

        return {
            'hopper': url,
            'resolved': final_url,
            'file_id': file_id,
            'title': title,
            'ok': True,
        }
    except Exception as e:
        return {'hopper': url, 'ok': False, 'error': str(e)}


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)

        try:
            links = json.loads(body).get('links', [])
        except Exception:
            links = []

        links = [u.strip() for u in links if isinstance(u, str) and u.strip()]
        links = links[:MAX_LINKS_PER_REQUEST]

        results = []
        if links:
            workers = min(MAX_CONCURRENCY, len(links))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = {pool.submit(resolve_one, u): u for u in links}
                for future in as_completed(futures):
                    results.append(future.result())
            order = {u: i for i, u in enumerate(links)}
            results.sort(key=lambda r: order.get(r['hopper'], 0))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'results': results}).encode())