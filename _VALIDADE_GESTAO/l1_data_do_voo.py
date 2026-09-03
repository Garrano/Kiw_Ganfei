# -*- coding: utf-8 -*-
"""L1 — a data do voo LiDAR, calculada a partir do tempo GPS dos pontos.

Porque este ficheiro tinha de existir
-------------------------------------
`ADVERSARIO_2026-08-29.md`, veredicto:

  «**Não passa nada que dependa de L1 enquanto L1 não tiver o cálculo em
  disco.** São duas linhas de `laspy`. Enquanto não existirem, o facto fundador
  desta adenda tem o mesmo estatuto epistémico que a pasta `sentinel_b1\\` tinha
  em 27 de Agosto: provavelmente certo, e sem prova.»

Uma varredura por `laspy`, `gps_time` ou `adjusted standard` em todos os `.py`
do projecto devolve **zero ficheiros**. A data «06-07-2025, 14h35 UTC» esteve
em circulação três dias, entrou na P02 e ancora a partição pérgola/chão de que
dependem a P02, a P03, a P04 e a P05 — sem o cálculo em disco.

Isto não é análise nova: é a prova de um facto já em uso, que uma paragem de
linha em vigor exige. Correcção, não reabertura.

O cálculo, e as três armadilhas
-------------------------------
1. **Qual das duas convenções.** O bit 0 de `global_encoding` diz se os tempos
   são *Adjusted Standard GPS Time* (padrão menos 1e9) ou *GPS Week Time*
   (segundos desde o início da semana, que sozinho não data nada). Lê-se o bit
   em vez de se assumir.
2. **A época.** GPS conta desde 1980-01-06 00:00:00 UTC.
3. **Os saltos.** O tempo GPS não tem segundos intercalares; o UTC tem. Em 2025
   a diferença é de **18 s**, constante desde 2017-01-01. Subtrai-se.

E reporta-se a DISPERSÃO, não só o instante: uma folha voada em duas passagens
separadas por horas ou dias não se pode descrever por uma data única, e é isso
que decide se a frase «6 de Julho às 14h35» é dizível.
"""
import datetime as dt
import glob
import json
import os

import numpy as np

try:
    import laspy
except ImportError:  # pragma: no cover
    raise SystemExit("laspy não está instalado — o cálculo não pode correr")

LAZ = r"C:\Users\Jackster2\Downloads\ganfei_s2\lidar\laz"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"

EPOCA_GPS = dt.datetime(1980, 1, 6, 0, 0, 0)
SALTOS = 18            # segundos intercalares GPS−UTC, constantes desde 2017-01-01

saida = {"epoca_gps": "1980-01-06T00:00:00Z", "saltos_s": SALTOS, "folhas": {}}

print("=" * 84)
print("L1 — DATA DO VOO A PARTIR DO TEMPO GPS DOS PONTOS")
print("=" * 84)

for f in sorted(glob.glob(os.path.join(LAZ, "*.laz"))):
    nome = os.path.basename(f)
    with laspy.open(f) as fh:
        cab = fh.header
        n = cab.point_count
        ajustado = bool(cab.global_encoding.gps_time_type)
        pts = fh.read()
        t = np.asarray(pts.gps_time, dtype="float64")

    print()
    print("### %s" % nome)
    print("  pontos                    : %d" % n)
    print("  global_encoding bit 0     : %d  (%s)"
          % (int(ajustado),
             "Adjusted Standard GPS Time" if ajustado else "GPS Week Time"))

    if not ajustado:
        print("  *** os tempos são de SEMANA GPS: não datam sozinhos. NÃO DATÁVEL.")
        saida["folhas"][nome] = dict(pontos=int(n), ajustado=False,
                                     datavel=False)
        continue

    seg = t + 1e9                       # de ajustado para GPS padrão
    q = np.percentile(seg, [0, 1, 50, 99, 100])
    inst = [EPOCA_GPS + dt.timedelta(seconds=float(s) - SALTOS) for s in q]
    span_h = (q[-1] - q[0]) / 3600.0

    print("  intervalo GPS (s)         : %.1f a %.1f" % (q[0], q[-1]))
    print("  UTC mínimo                : %s" % inst[0].strftime("%Y-%m-%d %H:%M:%S"))
    print("  UTC mediana               : %s" % inst[2].strftime("%Y-%m-%d %H:%M:%S"))
    print("  UTC máximo                : %s" % inst[-1].strftime("%Y-%m-%d %H:%M:%S"))
    print("  amplitude                 : %.2f h" % span_h)
    dias = sorted({i.date().isoformat() for i in inst})
    print("  dias abrangidos           : %s" % ", ".join(dias))
    saida["folhas"][nome] = dict(
        pontos=int(n), ajustado=True, datavel=True,
        utc_min=inst[0].isoformat(), utc_mediana=inst[2].isoformat(),
        utc_max=inst[-1].isoformat(), amplitude_h=float(span_h),
        dias=dias)

print()
print("=" * 84)
print("VEREDICTO SOBRE A FRASE EM USO")
print("=" * 84)
print()
ok = [v for v in saida["folhas"].values() if v.get("datavel")]
if not ok:
    print("NENHUMA folha é datável pelo tempo GPS. A frase «06-07-2025, 14h35»")
    print("não tem suporte e sai de todas as peças.")
else:
    todos = sorted({d for v in ok for d in v["dias"]})
    amp = max(v["amplitude_h"] for v in ok)
    print("dias abrangidos por todas as folhas : %s" % ", ".join(todos))
    print("maior amplitude numa folha          : %.2f h" % amp)
    print()
    if len(todos) == 1 and amp < 1.0:
        print("A data única e a hora são dizíveis. A frase da P02 fica como está.")
    elif len(todos) == 1:
        print("O DIA é dizível; a HORA única não — a folha abrange %.1f h." % amp)
        print("A frase tem de passar a nomear o dia, e a hora sai ou vira intervalo.")
    else:
        print("O voo abrange mais de um dia. «06-07-2025» sozinho não descreve")
        print("o levantamento, e a frase tem de nomear o intervalo.")
saida["dias_todos"] = sorted({d for v in ok for d in v["dias"]}) if ok else []

json.dump(saida, open(os.path.join(VG, "l1_data_do_voo.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito l1_data_do_voo.json")
