# `georref_rega.json` — RETIRADO em 06-09-2026, no dia em que foi escrito

**Não se apaga; move-se e regista-se** (`CLAUDE.md`, regra 5).

O ficheiro afirmava um **teste cego** — `lobo_dentro_b1_frac: 0.0`,
`lobo_dist_centroides_m: 1272,5`. O adversário correu as próprias funções do
guião e mostrou que **o teste nunca viu o lobo**:

```
comps[0] n= 66979  x 1394..1865   <- o guiao chamou-lhe CORPO
comps[1] n= 47733  x 1001..1287   <- o guiao chamou-lhe LOBO
comps[2] n= 25133  x  356.. 624   |
comps[3] n= 16463  x  227.. 466   |  o lobo a serio
comps[5] n=  4803  x  130.. 265   |
```

`comps[0]` e `comps[1]` são **as duas metades do corpo**. O «0,0 %» tinha de dar
zero por construção: projectou o corpo contra o polígono do B1.

E o cabeçalho do guião diz «**O lobo oeste não entra**» a descrever a cegueira.
O que não entrava era o lobo inteiro — do ajuste **e** do teste. Cabeçalho a
dizer o contrário do código, que é a forma E, e a mesma leitura conjunta que o
`CLAUDE.md` manda fazer.

O único portão era `if len(comps) < 2`. Passou a verde com sete componentes, sem
saber distinguir «corpo + lobo» de «corpo partido ao meio». **A guarda da §4 do
pré-registo não guardava nada.**

Nada deste ficheiro é citável. A escala `0,9434` e a `escala_so_area 3,0234` que
lá estão não medem coisa nenhuma.
