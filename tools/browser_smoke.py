#!/usr/bin/env python3
"""Compatibility entry point for the current optional Node/Chromium QA script."""
import os,subprocess,sys
from pathlib import Path
if __name__=='__main__':
 node=os.environ.get('CODEX_PRIMARY_RUNTIME_NODE','node')
 raise SystemExit(subprocess.call([node,str(Path(__file__).with_suffix('.cjs'))]+sys.argv[1:]))
