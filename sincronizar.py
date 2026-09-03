# -*- coding: utf-8 -*-
"""Sincroniza este repositório com a árvore de trabalho em Downloads.

PORQUE ISTO É UM SCRIPT E NÃO UM COMANDO
-----------------------------------------
Este repositório é uma **cópia filtrada** de três pastas que vivem fora dele
(`_VALIDACAO_CAMADAS`, `_VALIDADE_GESTAO`, `ganfei_s2`). Se a cópia se fizer à
mão, o filtro muda de vez em quando sem ninguém dar por isso — e o que fica de
fora deixa de ser uma decisão e passa a ser um acidente.

O filtro é a decisão editorial deste repositório, e está aqui, legível:

  · entram  `.py .md .json .csv .txt` e as peças `P0*.png` / `P0*.svg`
  · ficam de fora as caches de imagem (regeneráveis pelo próprio código) e os
    produtos da DGT — folhas LiDAR e ortofotos, que **não são nossas para
    redistribuir**

O `.gitignore` diz o mesmo em rede de segurança: mesmo que este script deixe
entrar alguma coisa por engano, o git recusa-a. As duas camadas são de propósito.

    python sincronizar.py            mostra o que mudaria
    python sincronizar.py --aplicar  copia
"""
import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ORIGEM = os.path.dirname(RAIZ)
PASTAS = ("_VALIDACAO_CAMADAS", "_VALIDADE_GESTAO", "ganfei_s2")
EXT = (".py", ".md", ".json", ".csv", ".txt")
EXCLUI = ("_reg01_landsat_cache", "_reg01_cache", "_densa_ganfei",
          "_orto297313", "sentinel_b1", os.sep + "orto" + os.sep,
          os.sep + "lidar" + os.sep, "__pycache__")
APLICAR = "--aplicar" in sys.argv


def entra(rel):
    if any(x in rel for x in EXCLUI):
        return False
    b = os.path.basename(rel)
    if b.startswith("P0") and b.lower().endswith((".png", ".svg")):
        return True
    return rel.lower().endswith(EXT)


novos, mudados, iguais = [], [], 0
for pasta in PASTAS:
    base = os.path.join(ORIGEM, pasta)
    if not os.path.isdir(base):
        print("AVISO: %s nao existe" % base)
        continue
    for dirpath, _, ficheiros in os.walk(base):
        for f in ficheiros:
            src = os.path.join(dirpath, f)
            rel = os.path.relpath(src, ORIGEM)
            if not entra(rel):
                continue
            dst = os.path.join(RAIZ, rel)
            if not os.path.exists(dst):
                novos.append(rel)
            elif os.path.getsize(src) != os.path.getsize(dst) or \
                    os.path.getmtime(src) > os.path.getmtime(dst) + 1:
                mudados.append(rel)
            else:
                iguais += 1
                continue
            if APLICAR:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)

# a cópia de topo do documento obrigatório
mo = os.path.join(ORIGEM, "_VALIDACAO_CAMADAS", "ANTES_DE_COMECAR.md")
if os.path.exists(mo) and APLICAR:
    shutil.copy2(mo, os.path.join(RAIZ, "ANTES_DE_COMECAR.md"))

print("iguais %d  ·  novos %d  ·  mudados %d" % (iguais, len(novos), len(mudados)))
for t, L in (("NOVO", novos), ("MUDADO", mudados)):
    for r in sorted(L)[:40]:
        print("  %-7s %s" % (t, r))
    if len(L) > 40:
        print("  ... e mais %d" % (len(L) - 40))
if not APLICAR and (novos or mudados):
    print()
    print("nada foi copiado. `python sincronizar.py --aplicar` para o fazer.")
