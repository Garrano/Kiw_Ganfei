# Figuras do dossiê · Ganfei

Seis figuras estáticas, prontas para o dossiê. PNG a 200 dpi para inserir em
documento; SVG vectorial para impressão ou para reeditar num editor gráfico.
Cada figura tem o seu script em `scripts/` — correm de dentro de
`Downloads\ganfei_s2\figuras\`, porque lêem os CSV e os GeoTIFF a partir daí.

| Fig. | Título | O que decide |
|---|---|---|
| F1 | Matriz de diagnóstico diferencial | Que hipóteses continuam vivas, e com que força de prova |
| F2 | Livro-razão das exclusões | O que foi excluído, e o que a exclusão **não** cobre |
| F3 | Cronologia de três faixas | Satélite × gestão × laboratório num só eixo do tempo |
| F4 | Chave espacial | Onde estão os focos, e onde amostrar |
| F5 | Desenho de amostragem | Setembro de 2026: onde, quantas, que compartimentos |
| F6 | Árvore de decisão | O que fazer com cada resultado possível |

## Ordem de leitura

F1 → F2 estabelecem o estado da prova. F3 → F4 dão o tempo e o espaço.
F5 → F6 são prospectivas: o que fazer a seguir. Se só entrarem duas no
relatório, devem ser a **F1** (estado) e a **F6** (decisão).

## Convenções comuns

- **Cor nunca sozinha.** Todo o estado tem glifo (forma) + cor + rótulo. As
  figuras lêem-se a preto e branco e sob daltonismo.
- **Paleta validada.** Slots 1/2/3 da paleta de referência: Zona 0 azul
  `#2a78d6`, Mancha W laranja `#eb6834`, B1 verde. O par vermelho/verde usado
  nas figuras de trabalho antigas falha a separação sob protanopia (ΔE 2,5
  contra um mínimo de 8) e por isso não aparece aqui como par de identidade.
- **Um só eixo.** Nenhuma figura tem duplo eixo vertical.
- **Português pré-Acordo**, para coerência institucional.

## Ressalvas que estão escritas nas próprias figuras

- **F4** não desenha os sectores de válvulas: o esquema de rega é um desenho à
  mão sem coordenadas, e georreferenciá-lo seria inventar precisão. Pela mesma
  razão deixou de desenhar as parcelas dos 11,16 ha de pomar novo — o número é
  fiável, a localização exacta não está confirmada.
- **F3** e **F1** marcam a Zona 0 como o foco mais antigo e o menos analisado:
  nunca teve painel de patogénios, só comunidade ITS.
- **F6** é uma ordenação de prioridade de teste, não um diagnóstico.

## O que falta

Nenhuma destas seis figura o lado **biótico** — porque quase nenhum resultado
de laboratório deste processo tem coordenadas. Ver `LACUNA_BIOTICA.md`.

## Reproduzir

```
cd Downloads\ganfei_s2\figuras
python f1_matriz.py
```

Requer numpy, scipy, rasterio, matplotlib.
