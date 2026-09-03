"""(c) 2024->25 e ruptura ou continuacao da tendencia 2021-24?
Serie CONTINUA (NDVI medio e dT), nao a serie de area com limiar.
Mais: estabilidade do 'ano do salto' sob limiar +-0,02 e nas duas mascaras."""
import json, csv, glob, os, numpy as np, rasterio
from scipy import ndimage
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]; pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
sau = mk["saudavel"]|mk["saudavel_2"]|mk["saudavel_3"]
Zal = ndimage.binary_dilation(mk["zona0"], np.ones((15,15))) & mk["pomar"]
anuais = [d for d in sorted(os.path.basename(p)[:-4] for p in glob.glob("sentinel/*.tif"))
          if d != "2025-06-17"]                      # uma data por ano
serie = {}
for d in anuais:
    with rasterio.open(f"sentinel/{d}.tif") as ds: nd = ds.read(1)
    ref = float(np.nanmean(nd[sau]))
    serie[d[:4]] = {"ref": ref, "z0": float(np.nanmean(nd[mk["zona0"]])),
                    "z0a": float(np.nanmean(nd[Zal])), "nd": nd,
                    "mw": float(np.nanmean(nd[mk["manchaW"]]))}
anos = sorted(serie)

# --- serie continua: NDVI da zona0 menos referencia --------------------------
y = np.array([serie[a]["z0"] - serie[a]["ref"] for a in anos])
ya = np.array([serie[a]["z0a"] - serie[a]["ref"] for a in anos])
x = np.arange(len(anos))
print("Serie CONTINUA — NDVI(zona0) menos referencia sa\n")
print(f"{'ano':6s} {'z0 - ref':>10s} {'z0alarg - ref':>14s}")
for i, a in enumerate(anos): print(f"{a:6s} {y[i]:10.4f} {ya[i]:14.4f}")

def ruptura(v, nome, base_ini=4, base_fim=7):   # 2021..2024
    b = np.polyfit(x[base_ini:base_fim+1], v[base_ini:base_fim+1], 1)
    resid = v[base_ini:base_fim+1] - np.polyval(b, x[base_ini:base_fim+1])
    sd = resid.std(ddof=1) if resid.size > 2 else np.nan
    print(f"\n{nome}: tendencia 2021-2024 = {b[0]:+.4f}/ano  (dp dos residuos {sd:.4f})")
    for i in (8, 9):
        prev = np.polyval(b, x[i]); obs = v[i]
        z = (obs - prev)/sd if sd and sd > 0 else np.nan
        print(f"   {anos[i]}: previsto {prev:+.4f}  observado {obs:+.4f}  "
              f"desvio {obs-prev:+.4f}  = {z:+.1f} desvios-padrao")
ruptura(y, "zona0 (mascara original)")
ruptura(ya, "zona0 (mascara alargada)")

# --- Pettitt (nao parametrico) ----------------------------------------------
def pettitt(v):
    n = len(v); U = []
    for t in range(1, n):
        s = sum(np.sign(v[i]-v[j]) for i in range(t) for j in range(t, n))
        U.append(abs(s))
    k = int(np.argmax(U))
    return anos[k], max(U)
print(f"\nPettitt (ponto de mudanca mais provavel):")
print(f"   zona0 original : {pettitt(y)[0]}  (K={pettitt(y)[1]})")
print(f"   zona0 alargada : {pettitt(ya)[0]}  (K={pettitt(ya)[1]})")

# --- estabilidade do 'ano do salto' sob limiar -------------------------------
print(f"\nArea em defice da zona0 (ha) sob varios limiares — o 'salto' muda de ano?")
print(f"{'limiar':>8s} " + " ".join(f"{a:>6s}" for a in anos))
for off in (0.03, 0.05, 0.07):
    for nome, reg in (("orig", mk["zona0"]), ("alarg", Zal)):
        linha = []
        for a in anos:
            s = serie[a]; m = (s["nd"] < s["ref"]-off) & reg
            linha.append(ndimage.binary_opening(m, np.ones((2,2))).sum()/100)
        salto = int(np.argmax(np.diff(linha)))+1
        print(f"{off:6.2f}{nome:>5s} " + " ".join(f"{v:6.2f}" for v in linha)
              + f"   maior salto: {anos[salto]}")
fig, ax = plt.subplots(figsize=(11,6))
ax.plot(anos, y, "-o", lw=2, color="#E4A11B", label="zona0 (original)")
ax.plot(anos, ya, "-s", lw=2, color="#b3801a", label="zona0 (alargada)")
ax.plot(anos, [serie[a]["mw"]-serie[a]["ref"] for a in anos], "-^", lw=2,
        color="#C2451E", label="manchaW")
b = np.polyfit(x[4:8], y[4:8], 1)
ax.plot(anos[4:], np.polyval(b, x[4:]), "k:", lw=1.5, label="tendencia 2021-24 extrapolada")
ax.axhline(0, color="#2f6e26", lw=1.5, ls="--", label="referencia sa")
ax.set_ylabel("NDVI menos referencia sa"); ax.grid(alpha=.25); ax.legend(fontsize=9)
ax.set_title("(c) 2025 e ruptura ou continuacao?")
fig.tight_layout(); fig.savefig("audit_c.png", dpi=150)
print("\n-> audit_c.png")
