"""Geada radiativa tardia? ERA5-Land horaria, 15/abr-10/mai, 2019-2026.
Marca tambem as noites com condicoes radiativas (vento fraco + ceu limpo),
porque numa bacia fechada o fundo arrefece muito abaixo do valor da grelha."""
import requests, numpy as np, datetime as dt
LAT, LON = 42.047, -8.626
r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
    "latitude": LAT, "longitude": LON,
    "start_date": "2019-04-10", "end_date": "2026-05-15",
    "hourly": "temperature_2m,dew_point_2m,wind_speed_10m,cloud_cover",
    "timezone": "UTC"}, timeout=240).json()["hourly"]
T = np.array(r["time"], dtype="datetime64[h]")
t2 = np.array([x if x is not None else np.nan for x in r["temperature_2m"]], float)
dp = np.array([x if x is not None else np.nan for x in r["dew_point_2m"]], float)
ws = np.array([x if x is not None else np.nan for x in r["wind_speed_10m"]], float)
cc = np.array([x if x is not None else np.nan for x in r["cloud_cover"]], float)
dias = T.astype("datetime64[D]")

print("Janela 15/abr - 10/mai — minima horaria de t2m (ERA5-Land, celula ~9 km)\n")
print(f"{'ano':5s} {'min t2m':>9s} {'data do min':>12s} {'noites <=2C':>12s} "
      f"{'noites <=0C':>12s} {'noites radiativas':>18s}")
resumo = {}
for ano in range(2019, 2027):
    a = np.datetime64(f"{ano}-04-15"); b = np.datetime64(f"{ano}-05-10")
    m = (dias >= a) & (dias <= b)
    if not m.any(): continue
    tt, dd = t2[m], dias[m]
    imin = int(np.nanargmin(tt))
    # por noite: minima diaria e condicoes radiativas nas horas 0-7 UTC
    noites_2 = noites_0 = rad = 0
    detalhes = []
    for d0 in np.unique(dd):
        k = (dias == d0)
        noite = k & (T.astype("datetime64[h]").astype(int) % 24 <= 7)
        if not noite.any(): continue
        mn = np.nanmin(t2[noite])
        v = np.nanmean(ws[noite]); c = np.nanmean(cc[noite])
        radiativa = (v < 2.0) and (c < 30)
        if mn <= 2: noites_2 += 1
        if mn <= 0: noites_0 += 1
        if radiativa: rad += 1
        if mn <= 4 or (radiativa and mn <= 6):
            detalhes.append((str(d0), mn, v, c, radiativa))
    resumo[ano] = detalhes
    print(f"{ano:5d} {np.nanmin(tt):8.1f}C {str(dd[imin]):>12s} {noites_2:12d} "
          f"{noites_0:12d} {rad:18d}")

print("\nNoites mais frias ou radiativas em cada ano (min<=4C, ou radiativa com min<=6C):")
for ano in sorted(resumo):
    if not resumo[ano]: print(f"  {ano}: nenhuma"); continue
    print(f"  {ano}:")
    for d0, mn, v, c, rr in sorted(resumo[ano], key=lambda x: x[1])[:5]:
        print(f"    {d0}  min={mn:5.1f}C  vento={v:4.1f} m/s  nuvens={c:3.0f}%"
              f"  {'RADIATIVA' if rr else ''}")

print("\n--- janela critica 20/abr a 5/mai de 2025, hora a hora abaixo de 6 C ---")
m = (dias >= np.datetime64("2025-04-20")) & (dias <= np.datetime64("2025-05-05"))
frio = m & (t2 <= 6)
if frio.any():
    for i in np.where(frio)[0]:
        print(f"    {T[i]}  t2m={t2[i]:5.1f}C  orvalho={dp[i]:5.1f}C  "
              f"vento={ws[i]:4.1f}  nuvens={cc[i]:3.0f}%")
else:
    print("    nenhuma hora <= 6 C")
