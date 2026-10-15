"""Rebuild ../index.html from the two CSV sheets in this folder.

Usage (from anywhere):  python3 source/build.py
"""
import json, os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, "-I", "build_data.py"], cwd=here, check=True)

data = json.load(open(os.path.join(here, "data.json"), encoding="utf-8"))
tpl = open(os.path.join(here, "template.html"), encoding="utf-8").read()
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
out = tpl.replace("/*__DATA__*/", payload)
open(os.path.join(here, "..", "index.html"), "w", encoding="utf-8").write(out)
print("wrote index.html", len(out), "bytes")
