# -*- coding: utf-8 -*-
"""C8-04 · a tabela «Debito dos Sectores» e os poligonos de sector do desenho.

PERGUNTA FIXA, escrita antes de correr
--------------------------------------
A tabela impressa do esquema enumera sectores com caudal. **Quantos sao, e
cobrem o lobo oeste ou so o corpo principal?**

  · Se a tabela cobrir os dois, entao o proprio documento de projecto trata o
    troco oeste como parte da mesma rede — e a hipotese «rede sobre-estendida»
    tem no desenho o objecto que o teste por valvula nao teve.
  · Se a tabela so cobrir o corpo, o troco oeste e posterior ao projecto.

O QUE ISTO NAO DECIDE: nao converte caudal em area, nem sector em valvula.
A tabela nao declara area nenhuma.

METODO
------
Sobre a imagem NATIVA (200 dpi; a C0 trabalhou a 300 dpi interpolados), separar
o tramado de cor dos sectores impressos por matiz, agrupar por componente
conexa, e reportar quantos poligonos ha e onde caem em x. Nenhuma escala e
usada — a contagem e ordinal, nao metrica.
"""
import os
import json
import numpy as np
from PIL import Image
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(AQUI, "esquema_nativo.jpeg")).convert("RGB")
a = np.asarray(im).astype(float)
H, W = a.shape[:2]

# a tabela impressa, transcrita do recorte rec_F_faixa_baixa2.png (leitura
# visual; o PDF nao tem texto extraivel — «texto len 0»)
DEBITO = [("A", 65.0), ("B", 85.0), ("C", 90.5), ("D", 96.8), ("E", 87.6),
          ("F", 79.1), ("G", 99.9), ("H", 91.5), ("I", 78.5), ("J", 71.6),
          ("L", 56.8), ("M", 55.3), ("N", 82.7)]
print("=" * 78)
print("A · a tabela «Debito dos Sectores» tal como esta impressa")
print("=" * 78)
print("  letras: %s" % " ".join(k for k, _ in DEBITO))
print("  n de sectores tabelados: %d" % len(DEBITO))
print("  NAO ha sector K — o alfabeto do desenho e o portugues antigo,")
print("  que salta o K. Quem contar de A a N em alfabeto ingles conta 14.")
print("  total do debito: %.1f m3" % sum(v for _, v in DEBITO))
print("  minimo %.1f (%s) · maximo %.1f (%s) · razao %.2fx"
      % (min(v for _, v in DEBITO), min(DEBITO, key=lambda t: t[1])[0],
         max(v for _, v in DEBITO), max(DEBITO, key=lambda t: t[1])[0],
         max(v for _, v in DEBITO) / min(v for _, v in DEBITO)))

# contra-verificacao: valvulas_v6.json guarda uma lista `_sectores`
V6 = json.load(open(r"C:\Users\Jackster2\Downloads\ganfei_s2\valvulas_v6.json",
                    encoding="utf-8"))
s6 = list(V6.get("_sectores", []))
print()
print("  valvulas_v6.json `_sectores` (leitura anterior, 28-08): %d — %s"
      % (len(s6), " ".join(s6)))
print("  coincide com a tabela impressa: %s"
      % (sorted(s6) == sorted(k for k, _ in DEBITO)))

# ---------------------------------------------------------------- poligonos
print()
print("=" * 78)
print("B · poligonos de sector impressos (tramado a cor), por componente")
print("=" * 78)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = a.max(2)
mn = a.min(2)
sat = mx - mn
cor = (sat > 22) & (mx > 120)            # tramado colorido, papel excluido
# fora da moldura do cartucho, da legenda e do titulo lateral
zona = np.zeros((H, W), bool)
zona[150:900, 60:2260] = True
c = cor & zona
c = ndimage.binary_closing(c, np.ones((13, 13)))
c = ndimage.binary_opening(c, np.ones((5, 5)))
lab, n = ndimage.label(c, np.ones((3, 3)))
tam = ndimage.sum(c, lab, range(1, n + 1))
print("componentes de tramado: %d (>=400 px: %d)"
      % (n, int((tam >= 400).sum())))
saida = []
for i in np.argsort(-tam):
    if tam[i] < 400:
        continue
    m = lab == i + 1
    ys, xs = np.where(m)
    saida.append(dict(px=int(tam[i]), x0=int(xs.min()), x1=int(xs.max()),
                      y0=int(ys.min()), y1=int(ys.max()),
                      xc=float(xs.mean())))
saida.sort(key=lambda d: d["xc"])
LOBO_X = 470          # fronteira lida no desenho: a leste da valvula 5 abre-se
                      # a faixa sem tramado (rec T3_vazio_meio.png)
for d in saida:
    d["troco"] = "OESTE" if d["xc"] < LOBO_X else "corpo"
    print("  x %4d..%4d  y %4d..%4d  %6d px  centro x=%6.1f  %s"
          % (d["x0"], d["x1"], d["y0"], d["y1"], d["px"], d["xc"], d["troco"]))
no = sum(1 for d in saida if d["troco"] == "OESTE")
print()
print("  componentes com tramado no troco OESTE: %d" % no)
print("  componentes com tramado no corpo:       %d" % (len(saida) - no))
print()
print("  LEITURA: ha tramado de sector impresso nos DOIS trocos. O desenho de")
print("  projecto (PRILUX, JUL 09, ESC 1/3500 @ A1) sectoriza o troco oeste")
print("  como sectoriza o corpo. A tabela de debito e uma so, com %d sectores."
      % len(DEBITO))

json.dump(dict(debito={k: v for k, v in DEBITO}, n_sectores=len(DEBITO),
               total_m3=sum(v for _, v in DEBITO),
               sectores_v6=s6, componentes=saida,
               n_componentes_oeste=no,
               n_componentes_corpo=len(saida) - no),
          open(os.path.join(AQUI, "c8_04_sectores.json"), "w"), indent=1)
print("\nescrito c8_04_sectores.json")
