"""Proxy de drenagem interna: taxa de secagem do solo depois da chuva, vista
pelo Sentinel-1. Solo que drena mal mantem retrodifusao alta mais tempo."""
import csv, requests, numpy as np, datetime as dt
r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
    "latitude": 42.047, "longitude": -8.626,
    "start_date": "2022-10-01", "end_date": "2025-04-30",
    "daily": "precipitation_sum", "timezone": "UTC"}, timeout=180).json()
chuva = {dt.date.fromisoformat(d): (p or 0.0)
         for d, p in zip(r["daily"]["time"], r["daily"]["precipitation_sum"])}
def dias_desde(d, lim=5.0):
    for k in range(0, 30):
        if chuva.get(d - dt.timedelta(days=k), 0) >= lim: return k
    return 30
sar = list(csv.DictReader(open("sar_invernos.csv", encoding="utf-8")))
for x in sar:
    for k in x:
        if k.endswith("_db"): x[k] = float(x[k])
    x["_d"] = dt.date.fromisoformat(x["data"])
    x["_dias"] = dias_desde(x["_d"])
print(f"{len(sar)} cenas S1 com dias-desde-chuva(>=5 mm)\n")
print(f"{'mascara':10s} {'orb':>4s} {'n':>3s} {'declive dB/dia':>15s} {'r':>7s} "
      f"{'VV a 0-1 dia':>13s} {'VV a >=7 dias':>14s}")
for nm in ("saudavel", "manchaW", "zona0"):
    for orb in ("125", "147"):
        sub = [x for x in sar if x["orbita"] == orb]
        d = np.array([x["_dias"] for x in sub], float)
        v = np.array([x[f"{nm}_vv_db"] for x in sub])
        m = d <= 14
        if m.sum() < 6: continue
        A = np.polyfit(d[m], v[m], 1)
        rr = np.corrcoef(d[m], v[m])[0, 1]
        h = v[d <= 1]; s = v[d >= 7]
        print(f"{nm:10s} {orb:>4s} {m.sum():3d} {A[0]:+15.4f} {rr:+7.3f} "
              f"{(h.mean() if h.size else np.nan):13.2f} {(s.mean() if s.size else np.nan):14.2f}")
print("\nDiferenca manchaW - saudavel por classe de dias-desde-chuva (VV dB):")
print(f"{'dias':>6s} {'n':>4s} {'dVV':>8s}")
for lo, hi, lab in ((0,1,"0-1"), (2,3,"2-3"), (4,6,"4-6"), (7,30,">=7")):
    sub = [x for x in sar if lo <= x["_dias"] <= hi]
    if not sub: continue
    dv = np.mean([x["manchaW_vv_db"] - x["saudavel_vv_db"] for x in sub])
    print(f"{lab:>6s} {len(sub):4d} {dv:+8.3f}")
