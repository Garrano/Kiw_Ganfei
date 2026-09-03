import os, sys, numpy as np, rasterio
from PIL import Image
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
RAIZ = r"C:\Users\Jackster2\Downloads\ganfei_s2"
AQUI = os.path.dirname(os.path.abspath(__file__))
# 400 m centrados entre os dois focos, apanha pomar, sebes, campos e ribeira
CX, CY, LADO = 530730.0, 4655080.0, 420.0
for ep, f in [("2021","ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif"),
              ("2025","ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")]:
    ds = rasterio.open(os.path.join(RAIZ,"orto",f))
    b = transform_bounds("EPSG:32629", ds.crs, CX-LADO/2, CY-LADO/2, CX+LADO/2, CY+LADO/2)
    w = from_bounds(*b, transform=ds.transform)
    rgb = np.dstack([ds.read(i, window=w) for i in (1,2,3)]).astype("uint8")
    nir = ds.read(4, window=w).astype("float32")
    red = ds.read(1, window=w).astype("float32")
    nd = (nir-red)/(nir+red+1e-6)
    print("%s  %dx%d  NDVI-orto: mediana %.3f  p90 %.3f  fraccao>0.3 %.1f%%"
          % (ep, rgb.shape[1], rgb.shape[0], np.median(nd), np.percentile(nd,90),
             float((nd>0.3).mean()*100)))
    Image.fromarray(rgb).resize((640,640), Image.LANCZOS).save(
        os.path.join(AQUI,"VISTA_%s.png"%ep))
