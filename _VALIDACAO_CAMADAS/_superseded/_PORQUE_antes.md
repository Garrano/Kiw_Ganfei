# `antes.py` — retirado no dia em que foi escrito, 06-09-2026

**Era um duplicado do `ja_existe.py`**, que já existia desde 04-09 e pela mesma
razão exacta: nesse dia re-derivaram-se três coisas que já estavam em disco, uma
delas a própria leitura do esquema de rega.

Escrevi o `antes.py` para travar a repetição de trabalho **enquanto repetia
trabalho**. Não é irónico por acaso — é a demonstração de que a regra não pega
sem portão: eu tinha acabado de dizer que a causa raiz é não inventariar antes
de produzir, e não inventariei.

## O que valia, e passou para o `ja_existe.py`

1. **A tupla de extensões.** O `ja_existe.py` varria `.py .md .json .csv` e mais
   nada. As três coisas que me escaparam a 06-09 estavam todas fora dessa lista:
   `parcelas_ent.wkt`, `Esquema de rega retificado.pdf`, `_esquema_rega/*.png`.
   **A ferramenta correu-me pelos dedos por causa de uma tupla**, e a
   inteligência anterior deste caso vive em dados, não em código.
2. **O registo da busca** em `BUSCAS.csv`, e a verificação 16 da `certificar.py`
   que falha quando há guião tocado num dia sem busca. É isto que o torna
   comando: a versão de 04-09 estava disponível e nada a obrigava a correr.
3. **A referência cruzada** com a `DECISOES_FECHADAS.csv` e a `INEXACTOS.csv`.

Nada se perdeu. O que se perdeu foi a segunda ferramenta.
