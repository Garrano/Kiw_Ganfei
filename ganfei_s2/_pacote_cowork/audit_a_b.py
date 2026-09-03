"""(a) A referencia sa aqueceu em 2025?  (b) O dT sobrevive a cobertura constante?"""
import csv, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = list(csv.DictReader(open("audit_termico.csv", encoding="utf-8")))
def f(x, k):
    try: return float(x[k])
    except: return np.nan
for x in R:
    x["ano"] = x["data"][:4]; x["mes"] = int(x["data"][5:7])
    for k in ("saudavel_st","controlo_st","manchaW_st","zona0_st",
              "saudavel_ndvi","controlo_ndvi","manchaW_ndvi","zona0_ndvi","t_ar"):
        x[k] = f(x, k)
print(f"{len(R)} cenas | com t_ar: {sum(1 for x in R if not np.isnan(x['t_ar']))}\n")

# ---------- (a) referencia sa: bruta, menos controlo, e residuo vs t_ar ------
print("=== (a) LST da REFERENCIA SA por ano ===")
print(f"{'ano':5s} {'n':>3s} | {'primavera (Abr-Mai)':>32s} | {'verao (Jun-Set)':>32s}")
print(f"{'':5s} {'':3s} | {'LST':>8s} {'-ctrl':>8s} {'res t_ar':>9s} | {'LST':>8s} {'-ctrl':>8s} {'res t_ar':>9s}")
# modelo LST_sa ~ t_ar sobre a linha de base 2018-2024, para nao deixar 2025 ancorar
base = [x for x in R if "2018" <= x["ano"] <= "2024" and not np.isnan(x["t_ar"])]
A = np.polyfit([x["t_ar"] for x in base], [x["saudavel_st"] for x in base], 1)
print(f"      (modelo de base 2018-2024: LST_sa = {A[0]:.2f}*t_ar + {A[1]:.2f}, n={len(base)})")
tab = {}
for ano in sorted({x["ano"] for x in R}):
    row = [ano, 0]
    for lo, hi in ((4,5),(6,9)):
        s = [x for x in R if x["ano"]==ano and lo<=x["mes"]<=hi]
        if not s: row += [np.nan]*3; continue
        lst = np.nanmean([x["saudavel_st"] for x in s])
        dctrl = np.nanmean([x["saudavel_st"]-x["controlo_st"] for x in s])
        rr = [x["saudavel_st"]-np.polyval(A, x["t_ar"]) for x in s if not np.isnan(x["t_ar"])]
        row += [lst, dctrl, np.nanmean(rr) if rr else np.nan]
        row[1] += len(s)
    tab[ano] = row
    m = "  <<<" if ano == "2025" else ""
    print(f"{row[0]:5s} {row[1]:3d} | {row[2]:8.2f} {row[3]:8.2f} {row[4]:9.2f} | "
          f"{row[5]:8.2f} {row[6]:8.2f} {row[7]:9.2f}{m}")

# ---------- (b) dT a cobertura constante ------------------------------------
print("\n=== (b) dT (manchaW - sa) contra dNDVI (manchaW - sa), MESMA cena ===")
ok = [x for x in R if not np.isnan(x["manchaW_st"]) and not np.isnan(x["manchaW_ndvi"])]
dT = np.array([x["manchaW_st"]-x["saudavel_st"] for x in ok])
dN = np.array([x["manchaW_ndvi"]-x["saudavel_ndvi"] for x in ok])
anos = np.array([x["ano"] for x in ok])
B = np.polyfit(dN, dT, 1); r = np.corrcoef(dN, dT)[0,1]
print(f"n={len(ok)}  dT = {B[0]:.2f}*dNDVI + {B[1]:+.3f}   r = {r:+.3f}")
print(f"  => cada -0,10 de NDVI explica {abs(B[0])*0.10:.2f} C de aquecimento")
res = dT - np.polyval(B, dN)
print(f"\n{'ano':5s} {'n':>3s} {'dNDVI medio':>12s} {'dT medio':>9s} {'dT previsto':>12s} {'RESIDUO':>9s}")
for ano in sorted(set(anos)):
    m = anos == ano
    print(f"{ano:5s} {m.sum():3d} {dN[m].mean():12.3f} {dT[m].mean():9.2f} "
          f"{np.polyval(B, dN[m]).mean():12.2f} {res[m].mean():+9.2f}"
          f"{'  <<<' if ano in ('2025','2026') else ''}")

fig, axs = plt.subplots(1, 2, figsize=(17, 6))
cor = {a: plt.cm.viridis(i/9) for i, a in enumerate(sorted(set(anos)))}
for a in sorted(set(anos)):
    m = anos == a
    axs[0].scatter(dN[m], dT[m], s=32, color=cor[a], label=a, alpha=.85)
xs = np.linspace(dN.min(), dN.max(), 50)
axs[0].plot(xs, np.polyval(B, xs), "k--", lw=2, label=f"ajuste r={r:+.2f}")
axs[0].set_xlabel("NDVI manchaW - referencia sa (mesma cena)")
axs[0].set_ylabel("LST manchaW - referencia sa (C)")
axs[0].set_title("(b) o aquecimento e so perda de copado?"); axs[0].legend(fontsize=8, ncol=2)
axs[0].grid(alpha=.25)
A2 = [tab[a][7] for a in sorted(tab)]; A1 = [tab[a][4] for a in sorted(tab)]
axs[1].plot(sorted(tab), A1, "-o", label="primavera (Abr-Mai)", color="#7fae3a")
axs[1].plot(sorted(tab), A2, "-s", label="verao (Jun-Set)", color="#C2451E")
axs[1].axhline(0, color="k", lw=1)
axs[1].set_ylabel("residuo da LST da referencia sa vs t_ar (C)")
axs[1].set_title("(a) a referencia sa aqueceu em 2025?"); axs[1].legend(); axs[1].grid(alpha=.25)
fig.tight_layout(); fig.savefig("audit_a_b.png", dpi=150)
print("\n-> audit_a_b.png")
