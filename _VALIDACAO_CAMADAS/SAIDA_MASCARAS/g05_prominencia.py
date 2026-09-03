# -*- coding: utf-8 -*-
"""G05 — PROMINENCIA do primeiro pico secundario da autocorrelacao radial.

G04 mediu o maximo da autocorrelacao no anel 3-9 m e falhou pela razao classica:
a autocorrelacao decai monotonamente a partir de zero, portanto o "maximo no
anel" e quase sempre o bordo interior do anel, e mede suavidade, nao compasso.

A medida correcta e a PROMINENCIA: percorre-se o perfil radial r(d), encontra-se
o primeiro minimo local d0, e mede-se quanto o perfil volta a subir depois dele.

    prom = max_{d>d0} r(d) - r(d0)          (0 se nunca voltar a subir)

Textura aperiodica (sebe, mata, telhados, agua) nao volta a subir: prom ~ 0.
Uma malha de postes/fiadas volta a subir ao compasso: prom alto, e `dpico` da o
compasso em metros.

O perfil e calculado por sectores angulares, e fica-se com o melhor sector:
as fiadas sao direccionais, e a media sobre todas as direccoes dilui o pico.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
RES, JAN = 0.5, 80
DMAX = 12.0          # m
NSEC = 6             # sectores angulares de 30 graus


def perfis(lum):
    ny, nx = 100, 200
    alta = lum - ndimage.uniform_filter(lum, 30)
    hann = np.hanning(JAN)
    W2 = np.outer(hann, hann)

    d = np.fft.fftfreq(JAN, d=1.0 / JAN) * RES
    DY, DX = np.meshgrid(d, d, indexing="ij")
    RD = np.hypot(DY, DX)
    TH = np.rad2deg(np.arctan2(DY, DX)) % 180

    passos = np.arange(0.5, DMAX + 0.01, 0.5)
    nb = len(passos)
    # indices pre-calculados: (sector, bin) -> mascara
    idx = []
    for s in range(NSEC):
        a0, a1 = s * 180.0 / NSEC, (s + 1) * 180.0 / NSEC
        sec = (TH >= a0) & (TH < a1)
        idx.append([np.where(sec & (np.abs(RD - p) < 0.35)) for p in passos])

    prom = np.zeros((ny, nx), "float32")
    dpico = np.zeros((ny, nx), "float32")
    secm = np.zeros((ny, nx), "int8")
    H, L = lum.shape
    meia = JAN // 2
    for i in range(ny):
        y0 = min(max(i * 20 + 10 - meia, 0), H - JAN)
        faixa = alta[y0:y0 + JAN]
        for j in range(nx):
            x0 = min(max(j * 20 + 10 - meia, 0), L - JAN)
            w = faixa[:, x0:x0 + JAN] * W2
            w = w - w.mean()
            ac = np.real(np.fft.ifft2(np.abs(np.fft.fft2(w)) ** 2))
            c0 = ac[0, 0]
            if c0 <= 1e-9:
                continue
            ac = ac / c0
            melhor, dm, sm = 0.0, 0.0, 0
            for s in range(NSEC):
                r = np.array([ac[k].mean() if len(k[0]) else np.nan
                              for k in idx[s]])
                if np.isnan(r).any():
                    continue
                # primeiro minimo local
                k0 = None
                for t in range(1, nb - 1):
                    if r[t] <= r[t - 1] and r[t] <= r[t + 1]:
                        k0 = t
                        break
                if k0 is None or k0 >= nb - 2:
                    continue
                kp = k0 + 1 + int(np.argmax(r[k0 + 1:]))
                p = float(r[kp] - r[k0])
                if p > melhor:
                    melhor, dm, sm = p, float(passos[kp]), s
            prom[i, j] = melhor
            dpico[i, j] = dm
            secm[i, j] = sm
    return prom, dpico, secm


if __name__ == "__main__":
    for ano in ("2010", "2012", "2021", "2025"):
        lum = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano)).astype("float32")[:3].mean(0)
        prom, dpico, secm = perfis(lum)
        np.savez(os.path.join(SAI, "prom_%s.npz" % ano), prom=prom, dpico=dpico, sec=secm)
        print("%s: prominencia p50 %.4f p75 %.4f p90 %.4f max %.4f | dpico mediano %.1f m"
              % (ano, *np.percentile(prom, [50, 75, 90]), prom.max(), np.median(dpico)))

        fig, axes = plt.subplots(2, 1, figsize=(17, 9.4), dpi=100)
        im = axes[0].imshow(prom, extent=[AOI[0], AOI[2], AOI[1], AOI[3]],
                            cmap="inferno", origin="upper", interpolation="nearest",
                            vmin=0, vmax=float(np.percentile(prom, 99)))
        axes[0].set_title("%s — prominencia do pico de autocorrelacao" % ano, fontsize=11)
        plt.colorbar(im, ax=axes[0], fraction=0.023, pad=0.01)
        dm = np.where(prom > np.percentile(prom, 60), dpico, np.nan)
        im = axes[1].imshow(dm, extent=[AOI[0], AOI[2], AOI[1], AOI[3]],
                            cmap="turbo", origin="upper", interpolation="nearest",
                            vmin=1, vmax=10)
        axes[1].set_title("%s — compasso do pico (m), so onde ha pico" % ano, fontsize=11)
        plt.colorbar(im, ax=axes[1], fraction=0.023, pad=0.01)
        for ax in axes:
            ax.tick_params(labelsize=7)
        fig.tight_layout()
        fig.savefig(os.path.join(SAI, "v05_prom_%s.png" % ano), dpi=100)
        plt.close(fig)
        print("-> v05_prom_%s.png" % ano)
