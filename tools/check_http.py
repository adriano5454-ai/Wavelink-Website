#!/usr/bin/env python3
"""Serve the local site and compare every response body to the source bytes.

Uses only a temporary loopback server and Python's standard library. Does not
contact the public website, GitHub, the demo, or any external service.
"""
from __future__ import annotations
import argparse
import functools
import hashlib
import http.client
import http.server
import json
import threading
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--json', type=Path, help='Optional JSON output file')
    args = ap.parse_args()
    handler = functools.partial(QuietHandler, directory=str(SITE))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    results, errors = [], []
    connection = http.client.HTTPConnection('127.0.0.1', server.server_port, timeout=10)
    try:
        for path in sorted(p for p in SITE.rglob('*') if p.is_file()):
            relative = path.relative_to(SITE).as_posix()
            expected = path.read_bytes()
            connection.request('GET', '/' + quote(relative))
            response = connection.getresponse()
            actual = response.read()
            okay = response.status == 200 and actual == expected
            results.append({'path': relative, 'status': response.status, 'bytes': len(actual),
                            'sha256': hashlib.sha256(actual).hexdigest(), 'byte_match': okay})
            if not okay:
                errors.append(f'HTTP/source mismatch: {relative}')
    except (OSError, http.client.HTTPException) as exc:
        errors.append(f'{type(exc).__name__}: {exc}')
    finally:
        connection.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    report = {'release': 'website-3.1.0', 'passed': not errors,
              'scope': 'local loopback only; byte-for-byte responses',
              'external_network_requests': False, 'results': results, 'errors': errors}
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1

if __name__ == '__main__':
    raise SystemExit(main())
