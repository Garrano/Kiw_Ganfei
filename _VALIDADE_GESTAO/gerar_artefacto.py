# -*- coding: utf-8 -*-
"""Gera a v13 do «Caso Ganfei» com as figuras embutidas.

A v12 e de 28-08-2026 e traz um aviso de que as areas por mascara estao
suspensas ate re-execucao. Essa re-execucao aconteceu, e com ela caiu a moldura
central do documento.

O que esta versao corrige, e nao e pouco:
  · a nomenclatura «Mancha W / Zona 0» estava INVERTIDA e foi retirada;
  · «dois focos, um calendario» nao se sustenta — metade do foco oriental nao
    tem pergola nenhuma;
  · a identidade do B1, que a v12 deixava «entre aspas», esta resolvida por
    documento administrativo;
  · a topografia, que a v12 dizia ter «invertido a leitura facil», foi testada
    a serio e a hipotese caiu;
  · entrou um instrumento independente do Sentinel-2 pela primeira vez.

Sistema visual: o da propria v12 — paleta agricola sobre papel quente,
Bricolage Grotesque com Public Sans e Spline Sans Mono. Acrescenta-se um unico
tom, para o que esta RESOLVIDO, que a v12 nao tinha porque nada estava.
"""
import base64
import io
import os

FIG = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
SAIDA = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO\caso_ganfei.html"


def img(nome):
    with open(os.path.join(FIG, nome), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


F10, F12, F9 = img("F10_altura_copado.png"), img("F12_landsat.png"), img("F9_serie_separada.png")
F13, F11, F14 = img("F13_hipoteses.png"), img("F11_matriz_diagnostico.png"), img("F14_plano.png")
F8 = img("F8_braudel.png")

HTML = """<title>O Caso Ganfei</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Public+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Spline+Sans+Mono:wght@400;500;600&display=swap">

<style>
:root{
  --paper:#F4F2E9; --surface:#FFFFFF; --sunk:#EAE8DC; --line:#D6D3C3;
  --ink:#212820; --ink2:#59604F; --ink3:#8A8F7C;
  --crop:#5E8A15; --crop-ink:#3D5A08;
  --closed:#4A6152; --closed-bg:#E6EBE2;
  --open:#B8451C; --open-bg:#F6E7DE;
  --instr:#2F6FA8; --instr-bg:#E2EBF3;
  --quote:#8A5A17; --quote-bg:#F6EDDC;
  --shadow:0 1px 2px rgba(33,40,32,.04), 0 10px 34px rgba(33,40,32,.07);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#191E18; --surface:#212820; --sunk:#293127; --line:#3A4237;
    --ink:#E9EADF; --ink2:#AEB3A1; --ink3:#7D8272;
    --crop:#8FB244; --crop-ink:#AFCB77;
    --closed:#8FAE99; --closed-bg:#25302A;
    --open:#E0774B; --open-bg:#33231B;
    --instr:#79ADDB; --instr-bg:#1E2A34;
    --quote:#D9AE63; --quote-bg:#2E2718;
    --shadow:0 1px 2px rgba(0,0,0,.3), 0 10px 34px rgba(0,0,0,.34);
  }
}
:root[data-theme="dark"]{
  --paper:#191E18; --surface:#212820; --sunk:#293127; --line:#3A4237;
  --ink:#E9EADF; --ink2:#AEB3A1; --ink3:#7D8272;
  --crop:#8FB244; --crop-ink:#AFCB77;
  --closed:#8FAE99; --closed-bg:#25302A;
  --open:#E0774B; --open-bg:#33231B;
  --instr:#79ADDB; --instr-bg:#1E2A34;
  --quote:#D9AE63; --quote-bg:#2E2718;
  --shadow:0 1px 2px rgba(0,0,0,.3), 0 10px 34px rgba(0,0,0,.34);
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:"Public Sans",system-ui,-apple-system,sans-serif;
  font-size:16.5px; line-height:1.62; -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1180px;margin:0 auto;padding:0 26px}
.col{max-width:680px}
h1,h2,h3{font-family:"Bricolage Grotesque","Public Sans",sans-serif;
  text-wrap:balance; margin:0; letter-spacing:-.015em}
.mono{font-family:"Spline Sans Mono",ui-monospace,monospace;
  font-variant-numeric:tabular-nums}

/* ---------------------------------------------------------------- cabeça */
header{padding:74px 0 20px}
.eyebrow{font-family:"Spline Sans Mono",monospace;font-size:11.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink3)}
h1{font-size:clamp(46px,7.4vw,80px);font-weight:800;line-height:.98;
  margin:20px 0 0}
.thesis{font-size:20px;line-height:1.52;color:var(--ink2);margin:26px 0 0;
  max-width:660px}
.thesis b{color:var(--ink);font-weight:600}

/* --------------------------------------------------------------- secções */
section{padding:56px 0 12px;border-top:1px solid var(--line);margin-top:52px}
.tag{display:inline-flex;align-items:center;gap:9px;
  font-family:"Spline Sans Mono",monospace;font-size:11.5px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--ink3);
  margin-bottom:16px}
.tag i{width:20px;height:1px;background:var(--line);display:block}
h2{font-size:clamp(28px,3.6vw,38px);font-weight:700;line-height:1.1}
.lede{font-size:18.5px;line-height:1.55;color:var(--ink2);margin:16px 0 0;
  max-width:660px}
p{margin:16px 0 0;max-width:680px}
p b,li b{font-weight:600;color:var(--ink)}
a{color:var(--crop-ink);text-decoration-thickness:1px;text-underline-offset:2px}

/* ---------------------------------------------------------------- figura */
figure{margin:40px 0 0}
figure img{display:block;width:100%;height:auto;border-radius:10px;
  border:1px solid var(--line);background:var(--surface);box-shadow:var(--shadow)}
figcaption{margin-top:14px;font-size:13.5px;line-height:1.6;color:var(--ink3);
  max-width:760px}
figcaption b{color:var(--ink2);font-weight:600}

/* ----------------------------------------------------------------- caixas */
.note{border-radius:10px;padding:22px 24px;margin:34px 0 0;max-width:760px;
  border:1px solid var(--line);background:var(--surface)}
.note.warn{background:var(--quote-bg);border-color:transparent}
.note.open{background:var(--open-bg);border-color:transparent}
.note h3{font-size:16px;font-weight:700;margin-bottom:8px}
.note.warn h3{color:var(--quote)} .note.open h3{color:var(--open)}
.note p{margin:10px 0 0;font-size:15px;max-width:none}

.grid{display:grid;gap:16px;margin:34px 0 0}
@media(min-width:760px){.grid.two{grid-template-columns:1fr 1fr}
  .grid.three{grid-template-columns:repeat(3,1fr)}}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:20px 22px}
.card .k{font-family:"Spline Sans Mono",monospace;font-size:26px;
  font-weight:600;letter-spacing:-.02em;line-height:1.1}
.card .t{font-size:13px;font-weight:600;margin-top:8px;color:var(--ink)}
.card .d{font-size:13px;color:var(--ink3);margin-top:5px;line-height:1.5}
.k.crop{color:var(--crop)} .k.open{color:var(--open)}
.k.closed{color:var(--closed)} .k.instr{color:var(--instr)}

ul{margin:16px 0 0;padding-left:0;list-style:none;max-width:680px}
ul li{position:relative;padding-left:22px;margin-top:11px}
ul li::before{content:"";position:absolute;left:2px;top:.66em;width:7px;
  height:7px;border-radius:50%;background:var(--line)}
ul.closed li::before{background:var(--closed)}
ul.open li::before{background:transparent;border:2px solid var(--open);
  width:8px;height:8px;top:.6em}

/* ---------------------------------------------------------------- tabela */
.tbl{margin:30px 0 0;overflow-x:auto;border:1px solid var(--line);
  border-radius:10px;background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:620px;font-size:14.5px}
th,td{text-align:left;padding:13px 18px;border-bottom:1px solid var(--line);
  vertical-align:top}
th{font-family:"Spline Sans Mono",monospace;font-size:11px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink3);font-weight:500}
tr:last-child td{border-bottom:none}
td.num{font-family:"Spline Sans Mono",monospace;font-variant-numeric:tabular-nums;
  white-space:nowrap;font-weight:600}

blockquote{margin:30px 0 0;padding:2px 0 2px 22px;
  border-left:3px solid var(--crop);max-width:680px;
  font-size:18px;line-height:1.55;color:var(--ink)}
blockquote cite{display:block;margin-top:10px;font-style:normal;font-size:13px;
  color:var(--ink3);font-family:"Spline Sans Mono",monospace}

footer{margin-top:64px;border-top:1px solid var(--line);padding:34px 0 80px;
  font-size:12.8px;line-height:1.7;color:var(--ink3)}
footer b{color:var(--ink2)}
@media(prefers-reduced-motion:no-preference){
  figure img{transition:box-shadow .25s ease}
}
</style>

<div class="wrap">

<header>
  <div class="eyebrow">CCDR-N · Avisos Agrícolas · Entre Douro e Minho · 29 de Agosto de 2026 · v13</div>
  <h1>O Caso Ganfei</h1>
  <p class="thesis">Um pomar de actinídea de cerca de 45&nbsp;ha em Valença perde plantas em manchas.
  Depois de uma auditoria em camadas, <b>a leitura anterior mudou de forma
  substancial</b>: o que se tratava como duas manchas do mesmo fenómeno são duas
  coisas diferentes — numa há videira viva a definhar, na outra <b>metade é
  chão</b>. Sete explicações caíram por medição. As que sobram não se decidiram
  porque <b>nunca foram procuradas</b>.</p>
</header>

<div class="note warn">
  <h3>O que mudou desde a versão de 28 de Agosto</h3>
  <p>A v12 assinalava que as áreas por máscara estavam suspensas até re-execução
  com máscaras geográficas independentes. Essa re-execução correu, e com ela
  caiu a moldura central do documento.</p>
  <p><b>A nomenclatura «Mancha W / Zona 0» foi retirada</b> — estava invertida, e
  as duas designações referiam sítios diferentes consoante quem escrevia. Tudo
  passa a levar coordenada.
  <b>«Dois focos, um calendário» não se sustenta:</b> o LiDAR mostra que metade
  do foco oriental não tem pérgola nenhuma.
  <b>A identidade do B1</b>, que a v12 deixava entre aspas com um candidato a
  750&nbsp;m a sul, está resolvida por documento administrativo.
  <b>A topografia</b>, que a v12 dizia ter «invertido a leitura fácil», foi
  testada com hipótese fixa e a explicação caiu.
  E entrou, pela primeira vez, <b>um instrumento independente do Sentinel-2</b>.</p>
</div>

<!-- ============================================================ 1 -->
<section>
  <div class="tag"><i></i>a correcção que muda tudo o resto</div>
  <h2>Os dois focos não são a mesma coisa</h2>
  <p class="lede">Todo o dossiê media reflectância — verdura vista do espaço.
  Em 6 de Julho de 2025 passou por cima um LiDAR, que mede <b>geometria</b>. E a
  geometria diz outra coisa.</p>

  <figure>
    <img src="__F10__" alt="Mapa de altura de copado do pomar de Ganfei medido por LiDAR em 6 de Julho de 2025. O foco ocidental aparece maioritariamente verde, com pérgola de 2,25 m; o foco oriental aparece em grande parte laranja, indicando ausência de pérgola.">
    <figcaption><b>Altura de copado, MDS menos MDT.</b> A escala está ancorada em
    dois controlos medidos no próprio voo e não escolhidos: terreno lavrado lê
    0,09&nbsp;m; a referência sistemática lê 2,34&nbsp;m. A data vem do tempo GPS
    dos pontos — os metadados só dão uma janela de catorze meses.</figcaption>
  </figure>

  <div class="grid three">
    <div class="card"><div class="k crop">2,25 m</div>
      <div class="t">foco ocidental · v8/B2</div>
      <div class="d">90&nbsp;% acima de 1,5&nbsp;m. Há pérgola e há videira. Está a
      definhar, não foi arrancada.</div></div>
    <div class="card"><div class="k open">0,47 m</div>
      <div class="t">foco oriental · v13-v14/B3</div>
      <div class="d">Metade das células abaixo de meio metro. Em Julho de 2025
      aquilo era chão.</div></div>
    <div class="card"><div class="k open">3,77 ha</div>
      <div class="t">de 30,31 sem pérgola</div>
      <div class="d">12,4&nbsp;% do polígono. E <b>40,7&nbsp;% do défice de 2026</b>
      cai nesse terreno.</div></div>
  </div>

  <p>A confirmação vem de um documento que não é nosso e não é óptico: no
  parcelário do IFAP, onde o LiDAR não vê pérgola <b>o beneficiário declarou
  erva, forragem ou nada</b> — 65&nbsp;% de kiwi contra 99,4&nbsp;% na parte com
  pérgola. Um instrumento geométrico e um registo administrativo, sem contacto
  entre si, a marcar o mesmo terreno.</p>

  <div class="note">
    <h3>O que isto obriga a retirar</h3>
    <p>A série do défice somava duas grandezas que não são a mesma: copado a
    declinar e chão onde a planta já não existe. Toda a afirmação que trate as
    7,86&nbsp;ha de 2026 como uma coisa só fica por rever — incluindo o degrau, a
    duplicação de 2024 para 2026, e o cruzamento com o radar do lado oriental.
    <b>Isto não destrói o caso: parte-o em dois.</b></p>
  </div>
</section>

<!-- ============================================================ 2 -->
<section>
  <div class="tag"><i></i>a prova, por instrumento que não é nosso</div>
  <h2>O declínio do foco ocidental é real</h2>
  <p class="lede">Toda a série do caso corre sobre Sentinel-2: um sensor, uma
  agência, uma cadeia de correcção. A regra deste processo é que nenhum facto
  passa verificado só pelo instrumento que o produziu.</p>

  <figure>
    <img src="__F12__" alt="Série Landsat 8 e 9 de 2013 a 2026 mostrando o fosso à referência. O foco ocidental mantém-se em zero durante onze anos e sobe para 0,046 em 2025 e 0,146 em 2026.">
    <figcaption><b>140 cenas Landsat 8 e 9, catorze anos.</b> USGS/NASA em vez de
    ESA, sensor OLI em vez de MSI, correcção LaSRC em vez de Sen2Cor, outra órbita
    e outra hora de passagem. O fosso é medido dentro de cada cena, o que remove
    atmosfera, sensor, ângulo e data de uma vez.</figcaption>
  </figure>

  <p>Onze anos dentro de <span class="mono">±0,004</span> do zero —
  indistinguível da referência. Depois <b>0,046 em 2025 e 0,146 em 2026</b>.</p>

  <p>E a figura traz o seu próprio controlo negativo: a parte oriental
  <b>sem pérgola</b> — chão, pelo LiDAR — tem fosso grande e ruidoso desde 2013,
  <b>sem tendência nenhuma em catorze anos</b>. Se o método fabricasse declínios,
  fabricava-o também ali.</p>

  <div class="note">
    <h3>A ressalva, dita por nós</h3>
    <p>O NDVI satura sobre copado fechado. A linha plana vale como «era
    indistinguível da referência», <b>não</b> como «não havia variação pequena».
    O que a torna interpretável é a dimensão do afastamento em 2025-26, não a
    planura anterior. E a referência do Landsat cai 0,026 onde o Sentinel-2 dá
    0,054 nas mesmas células — duas medições da mesma coisa com um factor de dois
    entre elas.</p>
  </div>

  <figure>
    <img src="__F9__" alt="Série do défice de copado separada em duas: copado vivo e chão sem pérgola.">
    <figcaption><b>A série, separada pelo que o LiDAR encontrou.</b> O copado vivo
    desce sete anos até um piso de 0,66&nbsp;ha em 2023-24 e multiplica por sete em
    dois anos. Uma versão anterior desta figura lia zeros nesses anos — eram
    artefacto da abertura morfológica aplicada dentro de cada subconjunto, e a
    correcção está no rodapé da própria figura, com o viés de sobrevivência que
    ela também carrega.</figcaption>
  </figure>
</section>

<!-- ============================================================ 3 -->
<section>
  <div class="tag"><i></i>hipóteses fixadas antes de correr</div>
  <h2>O que já não é</h2>
  <p class="lede">Sete explicações foram escritas como hipótese falsificável,
  corridas, e refutadas por medição. Duas delas eram as nossas apostas, e as duas
  morreram.</p>

  <figure>
    <img src="__F13__" alt="Quadro de sete hipóteses refutadas e três em aberto, cada uma com o número e o instrumento que a testou.">
    <figcaption>Cada linha traz o instrumento e o número. Nenhum valor foi
    transcrito à mão: todos são lidos dos ficheiros de resultado.</figcaption>
  </figure>

  <ul class="closed">
    <li><b>Não é seca.</b> Julho-Agosto de 2026 foi o mais húmido da década — 82&nbsp;mm, o valor mais alto da série.</li>
    <li><b>Não é um ano mau para a paisagem.</b> A mata madura da envolvente não se mexeu: −0,0035, p&nbsp;=&nbsp;0,81. O que cai é o ciclo curto — o milho perdeu 0,077.</li>
    <li><b>Não é encharcamento por posição no terreno.</b> O défice está no terreno <b>alto</b>, com ρ entre −0,46 e −0,20 e p&nbsp;&lt;&nbsp;0,001 nas onze cenas — e está lá desde 2017, sem emergir em 2025-26.</li>
    <li><b>Não é a rede de rega sobre-estendida.</b> O agrupamento por válvula cai dentro do nulo em 11 de 11 cenas, e a distância à origem decai para zero justamente nos anos do evento.</li>
    <li><b>Não é o porta-enxerto.</b> Summer Kiwi contra pé franco <b>dentro do mesmo bloco</b>, mesma água, mesmo solo: −0,0004, IC95 [−0,0015, +0,0014].</li>
    <li><b>Não é poda.</b> Em 132 cenas de Abril a Outubro, um único salto acima de três desvios em três anos — e é abrolhamento de Abril, não corte.</li>
    <li><b>Não é arranque, no foco ocidental.</b> A pérgola está lá: 2,25&nbsp;m, 90&nbsp;% acima de 1,5&nbsp;m.</li>
  </ul>
</section>

<!-- ============================================================ 4 -->
<section>
  <div class="tag"><i></i>a razão, e não é falta de trabalho</div>
  <h2>Porque ainda não dizemos o que é</h2>

  <figure>
    <img src="__F11__" alt="Matriz de vinte linhas de organismo por matriz, mostrando que treze assentam numa única amostra composta e apenas duas foram ensaiadas em unidade com posição.">
    <figcaption><b>Vinte linhas de organismo × matriz.</b> Uma coluna cheia, três
    vazias.</figcaption>
  </figure>

  <div class="grid three">
    <div class="card"><div class="k open">13 de 20</div>
      <div class="t">numa amostra composta</div>
      <div class="d">Um sítio, um dia — 6 de Junho de 2025. É o informe 331/2025,
      a amostra «Kiwi&nbsp;1000».</div></div>
    <div class="card"><div class="k instr">2 de 20</div>
      <div class="t">com posição</div>
      <div class="d">E são o <b>mesmo organismo</b> em duas matrizes:
      <i>Meloidogyne hapla</i>.</div></div>
    <div class="card"><div class="k open">ZERO</div>
      <div class="t">linhas bacterianas ou virais</div>
      <div class="d">A <b>PSA</b> — o cancro bacteriano do kiwi, a principal
      doença da cultura no mundo — nunca foi pedida.</div></div>
  </div>

  <p>Nenhum dos quatro resultados negativos vem de amostra comparável, pelo que
  <b>nenhum exclui o que parece excluir</b>. E a única linha com posição
  anticorrelaciona com o défice: ρ&nbsp;=&nbsp;−0,40 no solo e −0,80 na raiz, com
  n&nbsp;=&nbsp;4 e nenhum significativo.</p>

  <p>Há um facto novo que muda o estatuto disto. O gestor situou a amostra
  «Kiwi 1000» — que <b>é</b> o informe 331/2025 — no <b>lado oeste do maior vazio
  circular</b>, e confirmou que identificou esse vazio <b>no terreno</b>, não numa
  imagem nossa. A biologia deste caso passa a ter posição. Continua a discriminar
  mal, mas por outras razões.</p>

  <div class="note open">
    <h3>E é a forma que aponta o caminho</h3>
    <p>Um vazio aproximadamente circular, no interior do talhão, que <b>não
    respeita fronteira de parcela nem de válvula</b>. Manchas redondas que
    alastram a partir de um ponto são a assinatura de agentes de solo — a rede de
    raízes não conhece o parcelário. E o único patogénio de lenho identificado no
    caso é <i>Rosellinia</i>&nbsp;sp., provavelmente <i>R.&nbsp;necatrix</i>, por
    diagnóstico macroscópico numa planta arrancada.</p>
    <p><b>É uma hipótese com forma, não uma conclusão.</b> Forma circular é
    compatível com <i>Armillaria</i>, <i>Rosellinia</i> e <i>Phytophthora</i> e não
    distingue entre elas.</p>
  </div>
</section>

<!-- ============================================================ 5 -->
<section>
  <div class="tag"><i></i>ditas antes que alguém as aponte</div>
  <h2>As nuances</h2>

  <p><b>Uma correcção nossa, dita por nós — e é grande.</b> A designação dos dois
  focos esteve <b>invertida durante semanas</b>, e sobreviveu a quatro auditorias.
  Cada afirmação sobre a «Zona 0» referia dois sítios a 500&nbsp;m um do outro
  consoante quem a escrevia. A partir desta versão nada leva nome sem coordenada
  ao lado.</p>

  <p><b>O que o LiDAR não decide.</b> O voo de 6 de Julho de 2025 cai
  <b>dentro</b> da janela em análise. Não distingue «nunca teve pérgola» de «teve
  até Julho de 2024». Estabelece o que lá estava naquele dia, não a história — e
  a partição vale até essa data, sendo hipótese depois dela.</p>

  <p><b>O nemátodo não é desculpa nem sentença.</b> Não existe limiar de dano
  publicado para kiwi em lado nenhum — nem para o dispensar nem para o condenar.
  E aqui as contagens correm <i>contra</i> o padrão.</p>

  <p><b>O bloco B1 não é um controlo limpo, e agora sabe-se porquê.</b> Foi
  decotado e re-enxertado duas vezes — Enza Gold em 2016, Erica por volta de 2020,
  sobre base Summer Kiwi — e teve rede nesse período. Três corridas independentes
  confirmam que ele e o corpo principal divergem entre 2021 e 2026, com o B1 do
  lado bom, e a divergência é confirmada por <b>radar em duas órbitas</b>. Mas
  <b>não se atribui ao porta-enxerto</b>: 64&nbsp;% do ganho faz-se no primeiro
  passo, que é a curva de recuperação da re-enxertia a saturar.</p>

  <p><b>Um viés de sensor que circulou e não existe.</b> Durante todo o processo
  citou-se um viés de calibração do Sentinel-2C de −0,048&nbsp;NDVI. Quatro
  medições emparelhadas, de quatro análises independentes, dão <b>≈ zero</b>. O
  valor vinha de um degrau medido <i>fora</i> do pomar, onde sensor e ano estão
  confundidos. Está retirado.</p>

  <p><b>Radiometria de ortofoto não mede vigor.</b> Nem entre épocas nem dentro
  de uma imagem: o rio Minho lê NDVI <b>+0,314 em 2021 e +0,187 em 2025</b>, e a
  água não pode ter NDVI positivo. O que sobrevive da ortofoto é estrutura —
  periodicidade de pérgola —, e mesmo essa não é imune a material novo no chão:
  em 2025 o pomar aparece com <b>faixas reflectoras</b> ao longo das fileiras que
  não existem em 2021. É intensificação de gestão, não sintoma — mas não a
  sabemos datar.</p>

  <p><b>Uma cena por ano é o desenho mais fraco possível.</b> Das 208 combinações
  de datas 2024/2026 disponíveis no arquivo, <b>22&nbsp;% mostrariam o pomar a
  melhorar</b>. Todas as séries deste caso assentavam numa cena por ano.</p>

  <p><b>O que nos faria mudar de ideias, dito antes de qualquer resultado.</b>
  Se o transecto não encontrar gradiente entre o centro, a orla e fora, não há
  propagação a medir e o vazio é outra coisa. Se o agente aparecer também no par
  são, <b>deixa de explicar o padrão e sai da lista</b> — foi o que já aconteceu
  ao <i>M. hapla</i>.</p>
</section>

<!-- ============================================================ 6 -->
<section>
  <div class="tag"><i></i>o acontecimento contra o que o hospeda</div>
  <h2>Três registos de tempo</h2>
  <p class="lede">Os factos deste caso não correm todos ao mesmo ritmo, e por isso
  não cabem no mesmo eixo. O acontecimento ocupa dois anos; a conjuntura que o
  hospeda ocupa trinta e cinco; a estrutura não tem data.</p>
  <figure>
    <img src="__F8__" alt="Três faixas com escalas temporais diferentes: acontecimento em meses, conjuntura em décadas, estrutura sem data.">
    <figcaption>A estrutura não causa o acontecimento — condiciona-o. Os dois
    focos ocupam posições hidráulicas opostas e comportam-se de maneira
    diferente.</figcaption>
  </figure>
</section>

<!-- ============================================================ 7 -->
<section>
  <div class="tag"><i></i>o que decide</div>
  <h2>O plano, e o que cada ponto responde</h2>
  <p class="lede">Doze plantas, quatro unidades, uma data, um laboratório. É o
  único desenho deste caso em que cada ponto tem escrito, <b>antes de existir</b>,
  o que se conclui se der positivo e o que se conclui se der negativo.</p>

  <figure>
    <img src="__F14__" alt="Mapa do plano de amostragem com o transecto no foco ocidental, o foco oriental e dois pares sãos, mais o painel de decisão de cada unidade.">
    <figcaption><b>O transecto não leva coordenada nossa.</b> O centro e a orla
    são o que o gestor apontar no terreno, no dia. Ancorá-lo no centro que o
    satélite calculou seria ancorar a colheita no próprio sinal que se vai medir —
    o erro de que este processo nasceu.</figcaption>
  </figure>

  <div class="tbl"><table>
    <tr><th>unidade</th><th>o que é</th><th>o que decide</th></tr>
    <tr><td class="num">T1</td><td>Transecto no vazio de terreno — centro, orla, fora</td>
      <td>Gradiente do centro para fora, ou orla acima do centro: assinatura de
      agente de solo em propagação. Sem gradiente, o vazio é outra coisa.</td></tr>
    <tr><td class="num">U2</td><td>Foco oriental, só onde há pérgola</td>
      <td>Mesmo agente que T1: um problema com duas expressões. Agente diferente:
      o dossiê separa-se em dois.</td></tr>
    <tr><td class="num">U3</td><td>Par são ocidental · v6 — mesmo bloco, mesma água</td>
      <td>Se o agente estiver também aqui, deixa de explicar o padrão. É o único
      ensaio deste desenho que pode <b>baixar</b> o número de candidatos.</td></tr>
    <tr><td class="num">U4</td><td>Par são oriental · v17 — outro bloco, outro terreno</td>
      <td>Separa terreno de gestão do lado oriental.</td></tr>
  </table></div>

  <p>A v6 e a v17 são as <b>únicas duas unidades da exploração</b> com défice,
  declínio novo e chão lavrado todos a zero. E há uma frase que resume o que
  faltava a este caso desde o início:
  <b>nenhuma colheita teve alguma vez um assintomático com que comparar.</b></p>

  <div class="note open">
    <h3>Quatro correcções que o rastreio exigiu</h3>
    <p><b>Painel foliar</b> em todas as doze plantas — o desenho original tinha
    zero amostras de folha, e a perna foliar é a única comparação com padrão
    externo de todo o caso. <b>Segunda radial a 90°</b> obrigatória, não opcional:
    é o que distingue propagação de mancha estática. <b>Controlo de proximidade</b>
    no bloco oriental. E a <b>pergunta regional como condição de arranque</b>, não
    como tarefa — se a causa for regional, as quatro unidades dão todas o mesmo e
    a campanha não informa.</p>
  </div>
</section>

<!-- ============================================================ 8 -->
<section>
  <div class="tag"><i></i>o pedido</div>
  <h2>Três coisas, e duas não custam nada</h2>

  <div class="grid three">
    <div class="card"><div class="k crop">0 €</div>
      <div class="t">Duas leituras de GPS</div>
      <div class="d">No centro e na orla do vazio. Dizem se o objecto que o gestor
      vê no terreno e o que o satélite mede são o mesmo. Hoje são <b>dois objectos
      com o mesmo nome</b>.</div></div>
    <div class="card"><div class="k crop">0 €</div>
      <div class="t">Cinco documentos</div>
      <div class="d">Os quatro PDF de metagenómica ITS e o informe 331/2025
      completo. Não são informação inexistente — são <b>documento
      indisponível</b>.</div></div>
    <div class="card"><div class="k instr">360–1 100 €</div>
      <div class="t">O painel laboratorial</div>
      <div class="d">Tabela do INIAV em vigor, Deliberação n.º 603/2024. Não é um
      programa; é uma confirmação.</div></div>
  </div>

  <p>Que a CCDR-N promova junto do <b>INIAV</b> a realização do painel com
  isenção ou preço simbólico, ao abrigo do mecanismo de interesse público da
  Deliberação n.º 603/2024, por via da unidade de Sanidade Vegetal ou de
  protocolo de colaboração.</p>

  <ul class="open">
    <li><b>Um declínio documentado, datado e multi-instrumento</b> numa cultura estratégica regional, com valor de vigilância seja qual for a etiologia.</li>
    <li><b>Janela perecível.</b> A amostra de 2025 apanhou o início. Daqui a um ano só haverá plantas mortas e colonizadores secundários.</li>
    <li><b>Exposição regulamentar real.</b> <i>M. hapla</i> confirmado e <i>R. necatrix</i> suspeito são pragas regulamentadas não-de-quarentena, e a exploração tem viveiro próprio.</li>
    <li><b>Contrapartida imediata:</b> dossiê rastreável e reprodutível entregue como caso de estudo — incluindo a cadeia de validação em camadas, com sete rastreios adversariais e todas as retiradas documentadas.</li>
  </ul>

  <div class="note">
    <h3>E uma pergunta que deixou de ser cara</h3>
    <p>«Isto é deste pomar ou é da região?» O parcelário do IFAP dá, por serviço
    aberto, <b>1&nbsp;054&nbsp;ha de kiwi declarado por 204 beneficiários</b> na
    mesma região — e há uma exploração a 8,1&nbsp;km, com 76&nbsp;ha declarados,
    onde uma das análises independentes encontrou sinal semelhante com degrau em
    2024. Essa verificação nunca foi corrida, e passou a ser barata.</p>
  </div>
</section>

<footer>
  <p><b>Fontes.</b> Nota de visita CCDR-N 04/08/2026 · Informe Estación
  Fitopatolóxica Areeiro 331/2025 (expediente 2025045292) · Lote de nemátodos
  339–343/2026 · Boletins de solo A2 (2026) · Relatórios Becrop A32A0C/A32A0B
  (2023-24) · Metagenómica ITS ISFBV0314–17 (2025) · Sentinel-2 L2A 2017–2026
  (Copernicus / AWS Open Data) · Sentinel-1 SAR · <b>Landsat 8/9 Collection 2,
  140 cenas, 2013–2026</b> · <b>LiDAR DGT, MDS e MDT 50 cm, voo de 06-07-2025
  datado pelo tempo GPS dos pontos</b> · <b>Parcelário IFAP, campanha 2025, por
  WFS aberto da CCDR-N</b> · ERA5-Land · Ortofotos DGT 1995–2025.</p>
  <p><b>Método.</b> Cadeia de validação em seis camadas, cada uma com herança
  fechada e certificado próprio, e sete rastreios adversariais independentes.
  Duas rondas de multiverso analítico com seis analistas independentes sobre
  hipóteses fixadas antes de correr. Todas as retiradas estão documentadas com o
  número que as desmente ao lado.</p>
  <p>Documento de trabalho para decisão interna. Coordenadas em EPSG:32629.
  Máscaras por validar no terreno. <b>v13 · 29 de Agosto de 2026</b> — substitui
  a v12 de 28/08, cuja moldura de «dois focos, um calendário» não sobrevive à
  medição de altura de copado.</p>
</footer>

</div>
"""

HTML = (HTML.replace("__F10__", F10).replace("__F12__", F12)
        .replace("__F9__", F9).replace("__F13__", F13)
        .replace("__F11__", F11).replace("__F14__", F14)
        .replace("__F8__", F8))
io.open(SAIDA, "w", encoding="utf-8").write(HTML)
print("escrito %s — %.1f MB" % (SAIDA, os.path.getsize(SAIDA) / 1e6))
