# -*- coding: utf-8 -*-
"""Q6 · forense de datas — o que o `st_ctime` do Windows garante, e o que nao.

A afirmacao a testar: «`orto_297313_fraccao.json` foi criado as 23:23:22 e
`reg01_triagem_descontinuidade.py` as 23:25:25, logo o criterio foi escrito
123 s DEPOIS de a ortofoto ja ter identificado os cinco blocos.»

Isto e a base de uma afirmacao sobre honestidade metodologica. Nao se aceita
por leitura de documentacao: testa-se.

Sete experiencias, todas em `_controlo3_b1\\_lab\\`, nenhuma fora dela.
"""
import ctypes
import os
import shutil
import time

LAB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lab")
os.makedirs(LAB, exist_ok=True)
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
q = lambda p: (os.stat(p).st_ctime, os.stat(p).st_mtime)
fmt = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def mostra(rot, p):
    c, m = q(p)
    b = getattr(os.stat(p), "st_birthtime", None)
    print("  %-34s ctime %s   mtime %s%s"
          % (rot, fmt(c), fmt(m),
             "   birthtime %s" % fmt(b) if b else ""))
    return c, m


print("=" * 96)
print("0 · O QUE `st_ctime` E NESTA MAQUINA")
print("=" * 96)
print()
a = os.path.join(LAB, "a.txt")
open(a, "w").write("x")
c0, m0 = mostra("ficheiro acabado de criar", a)

# GetFileTime da API do Windows, para comparar
k32 = ctypes.windll.kernel32


class FT(ctypes.Structure):
    _fields_ = [("lo", ctypes.c_uint32), ("hi", ctypes.c_uint32)]


def win_times(p):
    h = k32.CreateFileW(p, 0x80000000, 7, None, 3, 0x02000000, None)
    cr, ac, wr = FT(), FT(), FT()
    k32.GetFileTime(h, ctypes.byref(cr), ctypes.byref(ac), ctypes.byref(wr))
    k32.CloseHandle(h)
    to = lambda f: ((f.hi << 32 | f.lo) / 1e7) - 11644473600.0
    return to(cr), to(wr)


wc, ww = win_times(a)
print("  GetFileTime CreationTime          %s" % fmt(wc))
print("  GetFileTime LastWriteTime         %s" % fmt(ww))
print("  st_ctime == CreationTime da API ? %s   (diferenca %.3f s)"
      % (abs(wc - c0) < 1.0, wc - c0))
print()
print("  -> No Windows, `st_ctime` NAO e o «change time» do POSIX. E a data de")
print("     CRIACAO DA ENTRADA NO SISTEMA DE FICHEIROS. Nao e a data em que o")
print("     conteudo foi escrito, nem a data em que foi pensado.")

print()
print("=" * 96)
print("1 · COPIAR REPOE O ctime? (o modo de falha mais provavel)")
print("=" * 96)
print()
time.sleep(1.2)
b = os.path.join(LAB, "b.txt")
shutil.copy2(a, b)                      # copy2 preserva mtime, NAO ctime
cb, mb = mostra("copia com shutil.copy2", b)
print("  ctime da copia menos o do original: %+.1f s" % (cb - c0))
print("  mtime da copia menos o do original: %+.1f s" % (mb - m0))
print("  -> COPIAR REPOE O ctime PARA AGORA e preserva o mtime. Um ficheiro")
print("     copiado para uma pasta nova tem ctime da copia e mtime do original:")
print("     o ctime pode ficar DEPOIS do mtime, e nao datar nada do conteudo.")

print()
print("=" * 96)
print("2 · MUDAR DE NOME / MOVER DENTRO DO MESMO VOLUME")
print("=" * 96)
print()
c_ = os.path.join(LAB, "c.txt")
os.rename(a, c_)
cc, _ = mostra("depois de os.rename", c_)
print("  ctime preservado? %s" % (abs(cc - c0) < 1.0))
sub = os.path.join(LAB, "sub")
os.makedirs(sub, exist_ok=True)
d_ = os.path.join(sub, "c.txt")
shutil.move(c_, d_)
cd, _ = mostra("depois de mover para subpasta", d_)
print("  ctime preservado? %s" % (abs(cd - c0) < 1.0))
print("  -> Mover dentro do volume PRESERVA. Logo o ctime tambem nao prova que")
print("     o ficheiro estava NESTA pasta na altura.")

print()
print("=" * 96)
print("3 · EDITAR O CONTEUDO DEPOIS")
print("=" * 96)
print()
time.sleep(1.2)
open(d_, "a").write("mais conteudo, escrito muito depois")
ce, me = mostra("depois de reescrever o conteudo", d_)
print("  ctime mudou? %s   ·   mtime mudou? %s"
      % (abs(ce - c0) > 1.0, abs(me - m0) > 1.0))
print("  -> O ctime NAO acompanha o conteudo. Um ficheiro criado as 23:25 e")
print("     reescrito de alto a baixo as 03:00 continua a dizer 23:25.")

print()
print("=" * 96)
print("4 · TUNELAMENTO DO NTFS — apagar e recriar com o MESMO nome")
print("=" * 96)
print()
t = os.path.join(LAB, "tunel.txt")
open(t, "w").write("primeiro")
c1, _ = mostra("criado agora", t)
time.sleep(2.0)
os.remove(t)
open(t, "w").write("segundo, escrito %d s depois" % 2)
c2, _ = mostra("apagado e recriado 2 s depois", t)
print("  ctime do segundo == ctime do primeiro? %s   (diferenca %+.2f s)"
      % (abs(c2 - c1) < 0.5, c2 - c1))
print("  -> Se sim, e o TUNELAMENTO do NTFS: durante ~15 s, recriar um ficheiro")
print("     com o mesmo nome na mesma pasta RESSUSCITA a data de criacao antiga.")
print("     Um script corrido duas vezes seguidas herda o ctime da primeira.")

print()
print("=" * 96)
print("5 · O ctime E ESCRITAVEL SEM PRIVILEGIOS?")
print("=" * 96)
print()
z = os.path.join(LAB, "z.txt")
open(z, "w").write("x")
cz, _ = q(z)
h = k32.CreateFileW(z, 0x40000000, 0, None, 3, 0x02000000, None)
alvo = int((time.time() - 86400 * 365 + 11644473600.0) * 1e7)
ft = FT(alvo & 0xFFFFFFFF, alvo >> 32)
r = k32.SetFileTime(h, ctypes.byref(ft), None, None)
k32.CloseHandle(h)
cz2, _ = q(z)
print("  SetFileTime devolveu %s" % bool(r))
print("  ctime antes  %s" % fmt(cz))
print("  ctime depois %s" % fmt(cz2))
print("  -> %s" % ("QUALQUER processo do utilizador pode reescrever a data de "
                   "criacao. Nao ha privilegio nenhum a proteger este campo."
                   if abs(cz2 - cz) > 1000 else "nao foi possivel reescrever"))

print()
print("=" * 96)
print("6 · A CADEIA REAL — o que os ficheiros deste caso dizem")
print("=" * 96)
print()
ALVO = ["orto_297313_fraccao.json", "orto_297313_fraccao.py",
        "reg01_triagem_descontinuidade.py", "reg01_triagem.json",
        "reg01_landsat.py", "reg01_landsat.json",
        "b1_como_unidade.py", "b1_como_unidade.json"]
print("%-38s %-21s %-21s %s" % ("ficheiro", "ctime (criacao)", "mtime (escrita)",
                                "mtime - ctime"))
for f in ALVO:
    p = os.path.join(VG, f)
    if not os.path.exists(p):
        print("%-38s  (nao existe)" % f)
        continue
    c, m = q(p)
    print("%-38s %-21s %-21s %+8.0f s" % (f, fmt(c), fmt(m), m - c))
print()
print("volume de _VALIDADE_GESTAO : %s" % os.path.splitdrive(VG)[0])
print("volume de CLAUDE\\          : %s"
      % os.path.splitdrive(r"C:\Users\Jackster2\Documents\D\CLAUDE")[0])
print()
print("=" * 96)
print("O QUE O ctime GARANTE, E O QUE NAO GARANTE")
print("=" * 96)
print("""
GARANTE (fraco):  que a ENTRADA com este nome apareceu nesta pasta a esta hora.

NAO GARANTE:
  · que o conteudo actual seja dessa hora — editar nao mexe no ctime (3);
  · que o ficheiro nao tenha vindo de outro sitio ja escrito — mover preserva
    o ctime de origem (2), e copiar poe o ctime a hora da copia (1);
  · que a ordem entre dois ficheiros seja a ordem do PENSAMENTO — so a ordem
    em que duas entradas de directorio apareceram;
  · nada, se o ficheiro foi recriado com o mesmo nome em 15 s (4);
  · nada contra alteracao deliberada — o campo e escrivel por qualquer
    processo do utilizador, sem privilegios (5).
""")
shutil.rmtree(LAB, ignore_errors=True)
print("laboratorio apagado (so tocou em _controlo3_b1\\_lab\\)")
