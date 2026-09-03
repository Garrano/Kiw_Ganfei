"""Pos-processamento D3/D6 — nao toca no process_sentinel.py.

Metrica principal (D3.1): NDVI medio e mediano por mascara por data.
Metrica de apoio (D3.2): area abaixo de media(saudavel_data) - 0.05 (defice
moderado) e - 0.10 (defice severo). Offsets ABSOLUTOS sobre a referencia sa da
propria data: normaliza entre datas e nao depende do DP.
A regra media - 2 DP foi abandonada (D3.3) e nao e calculada.
"""
import csv, json, glob, os, numpy as np, rasterio
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = "sentinel"
FLAG = {"2019-09-02": "canopia em inicio de senescencia (2 set); "
                      "pode inflacionar area de defice"}
PX_HA = 0.01

masks_px = json.load(open(f"{SRC}/masks.json"))
datas = sorted(os.path.basename(p)[:-4] for p in glob.glob(f"{SRC}/*.tif"))
with rasterio.open(f"{SRC}/{datas[0]}.tif") as ds:
    H, W = ds.height, ds.width
yy, xx = np.mgrid[0:H, 0:W]
pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(H, W) for k, v in masks_px.items()}
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]     # referencia unida
ALVOS = ("pomar", "manchaW", "zona0")

linhas, defice_maps = [], {}
for d in datas:
    with rasterio.open(f"{SRC}/{d}.tif") as ds:
        nd = ds.read(1)
    ref = float(np.nanmean(nd[sau]))
    ref_sd = float(np.nanstd(nd[sau]))
    row = {"data": d, "flag_fenologia": FLAG.get(d, ""),
           "ref_saudavel_media": round(ref, 4), "ref_saudavel_dp": round(ref_sd, 4)}
    for a in ALVOS + ("saudavel_uniao",):
        m = sau if a == "saudavel_uniao" else mk[a]
        v = nd[m]; v = v[~np.isnan(v)]
        row[f"{a}_ndvi_medio"] = round(float(v.mean()), 4)
        row[f"{a}_ndvi_mediana"] = round(float(np.median(v)), 4)
        row[f"{a}_px_validos"] = int(v.size)
    for a in ALVOS:
        v = nd[mk[a]]
        for nome, off in (("moderado", 0.05), ("severo", 0.10)):
            n = int(np.nansum(v < ref - off))
            row[f"{a}_defice_{nome}_ha"] = round(n * PX_HA, 2)
            row[f"{a}_defice_{nome}_pct"] = round(100 * n / mk[a].sum(), 1)
    linhas.append(row)
    defice_maps[d] = nd - ref
    print(f"{d}  ref={ref:.3f}  pomar medio={row['pomar_ndvi_medio']:.3f}  "
          f"manchaW={row['manchaW_ndvi_medio']:.3f}  zona0={row['zona0_ndvi_medio']:.3f}")

with open("expansao.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
    w.writeheader(); w.writerows(linhas)

# ---- D4: degrau de baseline 2021->2022 na referencia sa ---------------------
anual = {r["data"][:4]: r["ref_saudavel_media"] for r in linhas if r["data"][:4] != "2025"}
degrau = None
if "2021" in anual and "2022" in anual:
    degrau = round(anual["2022"] - anual["2021"], 4)
    print(f"\nD4 — referencia sa 2021={anual['2021']:.4f} 2022={anual['2022']:.4f} "
          f"delta={degrau:+.4f}")
prov = json.load(open(f"{SRC}/proveniencia.json"))
prov["baseline_l2a"] = {
    "verificado": "earthsearch:boa_offset_applied por cena",
    "resultado": "True em todas as cenas de baseline >=04.00; 2017-07-02 e "
                 "baseline 00.01, anterior ao offset BOA — nada a aplicar",
    "conclusao": "coleccao harmonizada; nao ha degrau radiometrico esperado em 2022",
    "delta_referencia_sa_2021_2022": degrau,
    "nota": "a metrica de defice usa a referencia sa da propria data (D3.2), "
            "logo absorve qualquer residuo de baseline"}
prov["mascaras"] = {k: {"vertices": len(v)} for k, v in masks_px.items()}
prov["metrica"] = {"principal": "NDVI medio/mediano por mascara (D3.1)",
                   "apoio": "area < ref-0.05 (moderado) e < ref-0.10 (severo) (D3.2)",
                   "abandonado": "media - 2 DP (D3.3): colapsa com referencia uniforme"}
json.dump(prov, open(f"{SRC}/proveniencia.json", "w"), indent=2, ensure_ascii=False)

# ---- expansao.png -----------------------------------------------------------
xs = [r["data"] for r in linhas]
fig, axs = plt.subplots(2, 1, figsize=(11, 9), sharex=True)
for a, c in (("saudavel_uniao", "#2f6e26"), ("pomar", "#5B6152"),
             ("manchaW", "#C2451E"), ("zona0", "#E4A11B")):
    axs[0].plot(xs, [r[f"{a}_ndvi_medio"] for r in linhas], "-o", ms=5, lw=2, color=c, label=a)
axs[0].set_ylabel("NDVI medio"); axs[0].legend(frameon=False, ncol=4, fontsize=9)
axs[0].set_title("Ganfei — NDVI medio por mascara (metrica principal)")
axs[0].grid(alpha=.25)
for a, c in (("pomar", "#5B6152"), ("manchaW", "#C2451E"), ("zona0", "#E4A11B")):
    axs[1].plot(xs, [r[f"{a}_defice_moderado_pct"] for r in linhas], "-o", ms=5, lw=2,
                color=c, label=f"{a} moderado")
    axs[1].plot(xs, [r[f"{a}_defice_severo_pct"] for r in linhas], "--s", ms=4, lw=1.5,
                color=c, alpha=.7, label=f"{a} severo")
axs[1].set_ylabel("% da mascara abaixo do limiar"); axs[1].grid(alpha=.25)
axs[1].legend(frameon=False, ncol=3, fontsize=8)
axs[1].set_title("Areas de defice (apoio) — offsets absolutos sobre a referencia sa")
for ax in axs:
    for i, d in enumerate(xs):
        if d in FLAG: ax.axvline(i, color="k", ls=":", lw=1, alpha=.5)
plt.xticks(rotation=45, ha="right"); fig.tight_layout(); fig.savefig("expansao.png", dpi=150)

# ---- D5: grelha de miniaturas do mapa de defice ------------------------------
n = len(datas); cols = 4; rows = (n + cols - 1) // cols
fig, axs = plt.subplots(rows, cols, figsize=(4*cols, 2.3*rows))
for ax, d in zip(axs.ravel(), datas):
    im = ax.imshow(defice_maps[d], cmap="RdBu", vmin=-0.35, vmax=0.35, interpolation="nearest")
    ax.set_title(f"{d}{'  *' if d in FLAG else ''}", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    for k, c in (("pomar", "k"), ("manchaW", "#C2451E"), ("zona0", "#E4A11B")):
        p = np.array(masks_px[k] + [masks_px[k][0]])
        ax.plot(p[:, 0], p[:, 1], color=c, lw=.9)
for ax in axs.ravel()[n:]: ax.axis("off")
fig.suptitle("Defice = NDVI - media(saudavel) da propria data  (azul = abaixo da referencia)",
             fontsize=11)
fig.colorbar(im, ax=axs, shrink=.6, label="delta NDVI")
fig.savefig("defice_miniaturas.png", dpi=140, bbox_inches="tight")
print("\n-> expansao.csv, expansao.png, defice_miniaturas.png, proveniencia.json")
