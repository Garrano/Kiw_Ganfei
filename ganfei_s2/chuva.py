"""Precipitacao e humidade do solo em Ganfei, ERA5-Land via Open-Meteo (sem chave).
Compara o Inverno/Primavera 2024-25 com os anos homologos."""
import requests, numpy as np, datetime as dt
LAT, LON = 42.047, -8.626
r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
    "latitude": LAT, "longitude": LON,
    "start_date": "2016-09-01", "end_date": "2026-08-20",
    "daily": "precipitation_sum",
    "hourly": "soil_moisture_7_to_28cm",
    "timezone": "UTC"}, timeout=180).json()
d = np.array(r["daily"]["time"], dtype="datetime64[D]")
p = np.array([x if x is not None else np.nan for x in r["daily"]["precipitation_sum"]], float)
ht = np.array(r["hourly"]["time"], dtype="datetime64[h]")
sm = np.array([x if x is not None else np.nan for x in r["hourly"]["soil_moisture_7_to_28cm"]], float)
smd = {}
for t, v in zip(ht.astype("datetime64[D]"), sm):
    smd.setdefault(t, []).append(v)
smd = {k: np.nanmean(v) for k, v in smd.items()}
sol = np.array([smd.get(x, np.nan) for x in d])

def janela(ini, fim):
    m = (d >= np.datetime64(ini)) & (d <= np.datetime64(fim))
    pp = p[m]; ss = sol[m]
    # maior sequencia de dias com solo acima do percentil 90 de toda a serie
    lim = np.nanpercentile(sol, 90)
    run = best = 0
    for v in ss:
        run = run + 1 if v >= lim else 0
        best = max(best, run)
    return (np.nansum(pp), int(np.nansum(pp >= 20)), np.nanmean(ss), best, lim)

print("Ano hidrologico Out-Mar + Abr-Jun, em Ganfei (ERA5-Land)\n")
print(f"{'periodo':17s} {'P Out-Mar':>10s} {'d>=20mm':>8s} {'solo med':>9s} {'dias solo>P90':>14s}")
for a in range(2016, 2026):
    tot, big, sm_, run, lim = janela(f"{a}-10-01", f"{a+1}-03-31")
    marca = "  <<<" if a == 2024 else ""
    print(f"{a}-10 a {a+1}-03 {tot:10.0f} {big:8d} {sm_:9.3f} {run:14d}{marca}")
print(f"\n(limiar solo P90 da serie completa = {lim:.3f} m3/m3)\n")
print(f"{'periodo':17s} {'P Abr-15Jun':>12s} {'d>=20mm':>8s} {'solo med':>9s}")
for a in range(2017, 2027):
    tot, big, sm_, run, _ = janela(f"{a}-04-01", f"{a}-06-15")
    marca = "  <<<" if a == 2025 else ""
    print(f"{a}-04 a {a}-06   {tot:12.0f} {big:8d} {sm_:9.3f}{marca}")
