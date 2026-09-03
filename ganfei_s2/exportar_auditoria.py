"""Exporta para CSV os resultados que ate agora so existiam em texto.
Sem isto nao ha auditoria possivel: cada afirmacao tem de cair numa celula."""
import json, csv, glob, os, numpy as np, rasterio
from scipy import ndimage
from matplotlib.path import Path as MP
from rasterio.warp import transform as tr

AOI = (529950, 4654600, 531950, 4655600)
masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]; pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
Z_alarg = ndimage.binary_dilation(mk["zona0"], np.ones((15, 15))) & mk["pomar"]
datas = sorted(os.path.basename(p)[:-4] for p in glob.glob("sentinel/*.tif"))

# ---- A. datacao do foco + geometria da expansao ---------------------------
def eixos(m):
    ys, xs = np.where(m)
    C = np.cov(np.vstack((xs - xs.mean(), ys - ys.mean())))
    w, v = np.linalg.eigh(C)
    return (np.sqrt(w[-1]/max(w[0],1e-9)),
            np.degrees(np.arctan2(v[1,-1], v[0,-1])) % 180,
            2*np.sqrt(w[-1])*10, 2*np.sqrt(w[0])*10, xs.mean(), ys.mean())
rows = []
for d in datas:
    with rasterio.open(f"sentinel/{d}.tif") as ds: nd = ds.read(1)
    ref = float(np.nanmean(nd[sau]))
    r = {"data": d, "ref_saudavel": round(ref, 4)}
    for nome, reg in (("manchaW", mk["manchaW"]), ("zona0", mk["zona0"]),
                      ("zona0_alargada", Z_alarg)):
        m = ndimage.binary_opening((nd < ref - 0.05) & reg, np.ones((2, 2)))
        r[f"{nome}_defice_ha"] = round(m.sum()/100, 2)
        r[f"{nome}_mascara_ha"] = round(reg.sum()/100, 2)
        lab, n = ndimage.label(m)
        if n:
            big = lab == (1 + int(np.argmax(ndimage.sum(m, lab, range(1, n+1)))))
            e, ang, L, S, cx, cy = eixos(big)
            r.update({f"{nome}_nucleo_ha": round(big.sum()/100, 2),
                      f"{nome}_centro_x": round(cx, 1), f"{nome}_centro_y": round(cy, 1),
                      f"{nome}_alongamento": round(e, 2), f"{nome}_orientacao_deg": round(ang),
                      f"{nome}_eixo_maior_m": round(L), f"{nome}_eixo_menor_m": round(S)})
        else:
            for k in ("nucleo_ha","centro_x","centro_y","alongamento","orientacao_deg",
                      "eixo_maior_m","eixo_menor_m"): r[f"{nome}_{k}"] = ""
    rows.append(r)
with open("focos_datacao_geometria.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("-> focos_datacao_geometria.csv")

# ---- B. topografia por mascara + cota vs NDVI ------------------------------
dem = np.load("lidar/dem_aoi.npy"); meta = json.load(open("lidar/dem_aoi.json"))
T = rasterio.Affine(*meta["transform"]); H, W = dem.shape
gy, gx = np.mgrid[0:H, 0:W]; gp = np.vstack((gx.ravel(), gy.ravel())).T
def para(p):
    ux=[AOI[0]+q[0]*10 for q in p]; uy=[AOI[3]-q[1]*10 for q in p]
    ex,ny = tr("EPSG:32629","EPSG:3763",ux,uy)
    return [[(x-T.c)/T.a,(y-T.f)/T.e] for x,y in zip(ex,ny)]
mkL = {k: MP(para(v)).contains_points(gp).reshape(H,W) for k,v in masks.items()}
mkL["saudavel"] = mkL["saudavel"]|mkL["saudavel_2"]|mkL["saudavel_3"]
pv = dem[mkL["pomar"]]; pv = pv[~np.isnan(pv)]
trows = []
for k in ("pomar","saudavel","manchaW","zona0"):
    v = dem[mkL[k]]; v = v[~np.isnan(v)]
    trows.append({"mascara": k, "n_px_50cm": int(v.size), "ha": round(mkL[k].sum()*0.25/1e4,2),
        "cota_media_m": round(float(v.mean()),3), "cota_mediana_m": round(float(np.median(v)),3),
        "dp_m": round(float(v.std()),3), "p5": round(float(np.percentile(v,5)),2),
        "p95": round(float(np.percentile(v,95)),2),
        "percentil_no_pomar": round(float(100*(pv < np.median(v)).mean()),1)})
with open("lidar_topografia_por_mascara.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(trows[0].keys())); w.writeheader(); w.writerows(trows)
for r in trows: print("  ", r["mascara"], r["cota_mediana_m"], "m  percentil", r["percentil_no_pomar"])
print("-> lidar_topografia_por_mascara.csv")

# ---- C. cota vs NDVI 2026 fora dos focos ----------------------------------
with rasterio.open("sentinel/2026-07-27.tif") as ds: nd26 = ds.read(1)
py, px = np.where(mk["pomar"])
cot, ndv, cls = [], [], []
for j, i in zip(py, px):
    ux = AOI[0]+i*10; uy = AOI[3]-j*10
    ex, ny = tr("EPSG:32629","EPSG:3763",[ux,ux+10],[uy,uy-10])
    c0=int((min(ex)-T.c)/T.a); c1=int((max(ex)-T.c)/T.a)
    r0=int((max(ny)-T.f)/T.e); r1=int((min(ny)-T.f)/T.e)
    blk = dem[max(0,r0):r1, max(0,c0):c1]
    if blk.size == 0 or np.all(np.isnan(blk)): continue
    cot.append(np.nanmean(blk)); ndv.append(nd26[j,i])
    cls.append("manchaW" if mk["manchaW"][j,i] else ("zona0" if mk["zona0"][j,i] else "resto"))
cot=np.array(cot); ndv=np.array(ndv); cls=np.array(cls)
m0 = cls=="resto"; a,b = np.polyfit(cot[m0], ndv[m0], 1)
crows=[{"faixa":"regressao_fora_dos_focos","n":int(m0.sum()),
        "declive_ndvi_por_m":round(float(a),4),"ordenada":round(float(b),4),
        "r":round(float(np.corrcoef(cot[m0],ndv[m0])[0,1]),3)}]
for nm in ("manchaW","zona0"):
    s = cls==nm
    crows.append({"faixa":nm,"n":int(s.sum()),
        "declive_ndvi_por_m":"","ordenada":"",
        "r":"", "cota_media":round(float(cot[s].mean()),2),
        "ndvi_observado":round(float(ndv[s].mean()),3),
        "ndvi_previsto_pela_cota":round(float(a*cot[s].mean()+b),3),
        "defice_vs_previsto":round(float(ndv[s].mean()-(a*cot[s].mean()+b)),3)})
with open("cota_vs_ndvi.csv","w",newline="",encoding="utf-8") as f:
    ks = sorted({k for r in crows for k in r})
    w = csv.DictWriter(f, fieldnames=ks, extrasaction="ignore"); w.writeheader(); w.writerows(crows)
print(f"   r = {crows[0]['r']}  |  manchaW defice vs previsto = {crows[1]['defice_vs_previsto']}")
print("-> cota_vs_ndvi.csv")
