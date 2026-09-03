# -*- coding: utf-8 -*-
"""Descarrega as 21 folhas do MDS-50cm que cobrem a AOI de Ganfei.

As folhas sao exactamente as do MDT que ja estao em ganfei_s2\lidar — mesma
grelha, mesmo voo, mesma versao. MDS - MDT = altura de copado.

Autorizado pelo utilizador em 29-08-2026.
"""
import glob
import os
import re
import sys
import requests

B = "https://cdd.dgterritorio.gov.pt/dgt-be/v1"
LID = r"C:\Users\Jackster2\Downloads\ganfei_s2\lidar"
folhas = sorted({re.search(r"MDT-50cm-(\d+)-07-2025", os.path.basename(p)).group(1)
                 for p in glob.glob(os.path.join(LID, "MDT-50cm-*.tif"))})
print("folhas a obter: %d -> %s" % (len(folhas), ", ".join(folhas)))
tot = 0
for i, t in enumerate(folhas, 1):
    iid = "MDS-50cm-%s-07-2025" % t
    dest = os.path.join(LID, iid + "_v02.tif")
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print("  %2d/%d  ja existe %s" % (i, len(folhas), os.path.basename(dest)))
        tot += os.path.getsize(dest); continue
    try:
        m = requests.get("%s/collections/MDS-50cm/items/%s" % (B, iid),
                         params={"f": "json"}, timeout=90).json()
        f = m.get("data", m)
        href = f["assets"]["data"]["href"]
        esp = f["properties"].get("file:size")
        r = requests.get(href, timeout=600, stream=True)
        r.raise_for_status()
        n = 0
        with open(dest, "wb") as fh:
            for ch in r.iter_content(1 << 20):
                fh.write(ch); n += len(ch)
        tot += n
        print("  %2d/%d  %s  %.1f MB%s" % (i, len(folhas), iid, n / 1e6,
              "" if esp in (None, n) else "  (esperado %.1f MB)" % (esp / 1e6)))
    except Exception as e:
        print("  %2d/%d  FALHOU %s: %s" % (i, len(folhas), iid, str(e)[:120]))
print("total %.0f MB" % (tot / 1e6))
