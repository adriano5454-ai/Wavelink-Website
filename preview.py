#!/usr/bin/env python3
"""Optional local preview. Binds loopback only; does not publish to a network."""
from __future__ import annotations

import functools
import http.server
from pathlib import Path
import threading
import webbrowser


def main() -> int:
    site = Path(__file__).resolve().parents[1] / 'site'
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
    server = None
    for port in range(8000, 8010):
        try:
            server = http.server.ThreadingHTTPServer(('127.0.0.1', port), handler)
            break
        except OSError:
            continue
    if server is None:
        print('Ports 8000–8009 are unavailable. Open site/index.html directly in your browser.')
        return 1
    url = f'http://127.0.0.1:{server.server_port}/'
    print(f'Wavelink website preview: {url}\nPress Ctrl+C to stop. No site files are changed.')
    opener = threading.Timer(0.6, lambda: webbrowser.open(url))
    opener.daemon = True
    opener.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nPreview stopped.')
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
