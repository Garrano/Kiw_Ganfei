# Ganfei · memorando de enquadramento

**Para quem entra agora no processo. 11-09-2026.**

Pomar de actinídea em declínio, Emparcelamento de Ganfei, Valença. Este
documento diz o que se quer, o que se fez, onde estamos e o que falta. Não
substitui o `tier1_framework_draft.md` (v1.6), que é a espinha técnica — resume-o
e situa-o.

**Leitura mínima antes de tocar em seja o que for:** este memorando,
`ANTES_DE_COMECAR.md` e `DECISOES_FECHADAS.csv`.

---

## 1 · O objectivo, em cinco etapas

1. **Recolher** dados do terreno e valores analíticos de amostragem.
2. **Cruzar** com a bibliografia.
3. **Avaliar** o diagnóstico.
4. **Desenhar** a estratégia que o valida ou refuta.
5. **Construir** o protocolo de mitigação possível.

Não é um exercício de detecção remota. O satélite é meio, e só entrou porque
responde a *onde* e *quando* — nunca a *o quê*.

**Nota de âmbito:** o *relatório de período experimental* da CCDR-N foi
**entregue a 14-08-2026**, e já incluía a *Nota sobre a visita a um pomar de
actinídea em declínio*. Tudo o que se fez desde 28-08 é **pós-entrega** e serve
o caso, não o relatório.

---

## 2 · O caso, em vinte linhas

~50 ha de kiwi sobre solos **aluvionares**, fortemente revolvidos no
emparcelamento há ~35 anos. As plantas declinam e morrem **apoplecticamente,
sobretudo em dias muito quentes**, em **manchas que se expandem**.

Na visita de 04-08-2026: sem sintomas primários de esca na madeira, mas folha
«compatível»; frutos mirrados; varas a morrer de ponta para a base; **uma**
planta arrancada com sintomas radiculares atribuídos visualmente a *Rosellinia*;
infestantes abundantes; sondagem de solo negativa para *Phytophthora* e
*Armillaria* (não excluídas); hipótese de camada impermeável a limitar arejamento
e drenagem.

**O diagnóstico de trabalho é frágil, e é preciso dizê-lo sem rodeios:**

- a atribuição a ***R. necatrix* assenta em observação a olho de UMA planta**, e
  a nota de visita **dispensa expressamente a confirmação molecular**. A síntese
  de *R. necatrix* deste próprio dossiê conclui o contrário — o diagnóstico
  macroscópico falha, e o PCR validado supera o visual em 50–80 %;
- **o KVDS está ausente do diferencial e é o melhor ajuste epidemiológico do
  processo**: colapso apopléctico com evapotranspiração alta, manchas que
  crescem, aluvião revolvido, camada impermeável suspeita → encharcamento e
  hipoxia;
- a ***Phytophthora sojae* nunca foi confirmada por laboratório de
  diagnóstico** — existe só na metagenómica da Becrop, e metagenómica não é
  diagnóstico.

> **Não temos diagnóstico. Temos uma hipótese de trabalho que a nossa própria
> bibliografia diz ser insegura, e uma hipótese concorrente que ajusta melhor e
> nunca foi testada.**

---

## 3 · Como se trabalha aqui, e porquê

Este processo **retirou 23 veredictos em duas semanas**. Nenhum foi apanhado por
recomputação; **todos por ir a um instrumento diferente** ou por alguém que
conhece o terreno dizer «não é assim».

Daí o aparelho. Não é burocracia — é a resposta medida a um modo de falha real.
Em resumo:

| | |
|---|---|
| **Três tipos de facto** | **testemunho** (tipo 1) · **medição** (2) · **inferência** (3). O testemunho ganha ao cálculo, e o cálculo que ele derruba é **retirado, não reconciliado** |
| **C9** | o critério escreve-se **antes** da corrida |
| **C10** | só é citável o que passou por **certificação *e* adversário independente** |
| **C11** | o que sai para fora não interroga, não fala do nosso processo, e usa **só os nomes do gestor** |
| **S1** | **procurar vem antes de criar** — `ja_existe.py`, e a cadeia falha se houver código novo num dia sem busca |
| **S4** | uma decisão fechada não se reabre por cálculo próprio |

Correr `certificar.py` **é** a certificação: dezasseis verificações, código de
saída ≠ 0 quando alguma coisa não bate, e corre sozinha ao fim de cada turno.

**Estado actual da cadeia:** CERTIFICADA · 27 factos passam o portão · 20
auditorias feitas · 27 inexactidões registadas · 8 decisões fechadas ·
**45 de 193 guiões citáveis (23 %)**.

---

## 4 · O que está CERTIFICADO **e** AUDITADO — usável sem ressalva

| instrumento | o que dá | prova |
|---|---|---|
| **Altura de copado por LiDAR** | geometria: MDS−MDT, limiar 0,5 m, voo único de 06-07-2025 | reproduzido dos ladrilhos brutos a **0,000e+00**; AUD-17 |
| **Perda de copado 2024→2025** | **2,20 ha** com copado em Jul-2024 e nenhum em Jul-2025 — B3 1,02 · B2 0,33 · Erica Novo 0,01 | AUD-17 |
| **Partição por sector** | válvula→talhão, 44,9 ha, cinco sectores | **testemunho tipo 1**, AUD-18 |
| **Escala do esquema de rega** | 1,2572 m/px no raster embebido; 1:3500 @ A1 | três medições independentes dentro de ±1,1 %; AUD-19 |
| **12 pontos de colheita** | margem em avanço + par assintomático, em coordenadas GPS | **AUD-20**, verificado por LiDAR bruto *e* Sentinel-2 |
| **Série NDVI no foco oriental** | vigor estival, polígono fixo | AUD-10 — limpo **do lado que interessa** |

**São seis.** Tudo o resto ou tem ressalva, ou não tem estatuto.

### Com ressalva que viaja com o número

- **magnitude da mancha ocidental: não estimável** (centro no percentil 0,17 de
  2421 candidatos);
- **piso óptico de Inverno**: a medição aguenta-se, **a inferência não**;
- **boletins A2 de solo**: faltam CTC e saturação em bases; **profundidade não
  sabida**; piso de ruído medido em 0,2 unidades de pH.

---

## 5 · O que está FECHADO — não reabrir sem o que a coluna diz

| | decisão |
|---|---|
| **DEC-01** | georreferenciamento das válvulas **abandonado**. Ao nível do **sector** está fixado por testemunho; ao nível da **válvula** não existe (duas reconstruções divergem até 398 m) |
| **DEC-03** | **SAR NÃO TESTÁVEL** para declínio-contra-arranque: falta de potência, não resultado negativo |
| **DEC-04** | **B1 não é comparador** — cortado à base e reenxertado **duas vezes** (2016, ~2020). Mata a COMP-01 e deixa o processo **sem controlo interno** |
| **DEC-06** | **a primeira mancha a aparecer foi a oriental — B3, válvulas 12-15.** É a origem |
| **DEC-07** | **a amostra de raiz retida NÃO EXISTE.** Toda a confirmação biológica passa a depender de colheita nova |
| **DEC-08** | as covas de perfil abrem-se **durante** a campanha, no mesmo ponto da colheita |

> **Armadilha de vocabulário, e já custou uma decisão errada:** o gestor chama
> **«Zona 0» às válvulas 8, 9 e 10**, que são a mancha **ocidental**. A
> **origem** é a **oriental**. **«Zona 0» e «origem» não são sinónimos neste
> processo.**

---

## 6 · O que está por desenvolver, do terreno à biologia

| | ferramenta | estado |
|---|---|---|
| **T2** | locais das covas de perfil, sobre as linhas de escoamento | por fazer — os dados de fluxo já estão na tabela dos pontos |
| **T3** | **RQ6 — as manchas seguem a drenagem, ou espalham-se em raio?** Radial = biótico; a seguir a água = abiótico | **por fazer, e é o único gabinete que ainda move o diagnóstico** |
| **T4** | detector de estrutura em ortofoto sem folha, com âncora nova | por fazer — o método falhou por **âncora**, não por conceito |
| **T5** | **ficha de colheita e cadeia de custódia** | **por fazer, e bloqueia a campanha** |
| **T6** | segundo leitor para chamadas visuais | por fazer — a forma G continua sem cobertura |

### O buraco que mais custa

> **Ortofoto: 14 guiões vivos, ZERO citáveis.**

É o único instrumento que vê **estrutura** — fiadas, postes — e portanto o único
que poderia separar *arranque* de *declínio* sem ir ao terreno. Falhou o critério
de âncoras: em 2025 o chão lavrado lê prominência 0,240, porque **os regos também
são periódicos**.

### As duas camadas novas

**H · rio e freático — PARADA.** Não há estação hidrométrica activa em Valença
(a mais próxima é Monção, 11 km a montante, e a espanhola de Salvaterra está à
mesma distância na outra margem). O **datum** — a cota do zero da escala — não
está publicado, e sem ele não se compara nível com cota. **Não existe piezómetro
utilizável**: os quatro pontos num raio de 25 km estão a 10–19,5 km, só um
activo.

> **A conclusão útil: as covas de perfil SÃO o piezómetro.** A campanha é a única
> via para medir o freático onde importa. Isso acrescenta requisitos —
> profundidade ao nível da água **com hora** (o Minho é tidal em Valença), cota
> da boca por GPS, hidromorfia por horizonte, e **tubo de observação** se a cova
> for reaproveitável.

**M · meteorologia × fenologia — meia desbloqueada.** A rede portuguesa **não
cobre o período**: a estação do vale, Monção–Valinha, está desactivada desde
2008. **Sobrada (MeteoGalicia), a 5,2 km**, tem temperatura, chuva, radiação e
temperatura do solo, com série corrente. **Viés a declarar:** está a 59 m e o
pomar a 6–8 m; um terraço é sumidouro de ar frio, e a estação **comprime os
extremos** — que é a variável de que a hipótese depende. A correcção é um
*datalogger* no pomar durante a campanha.

**A fenologia não está resolvida.** As fontes portuguesas e galegas **nunca
coincidem no ano**, logo a amplitude entre locais não é calculável. O que se
mede é o **piso**: as datas de Areeiro são de *boletim*, não de observação, logo
**±7 dias por construção**. A transferência espacial e o desencontro de cultivar
(Hayward contra summerkiwi/Enza Gold/Erica) ficam **não medidos**.

---

## 7 · A fila, por ordem

| | acção | custo | quem |
|---|---|---|---|
| **1** | **Enviar o email das cinco perguntas** — pronto, por enviar | zero | nós |
| **2** | **Ficha de colheita e cadeia de custódia (T5)** | baixo | nós |
| **3** | **Campanha de campo** — colher nos 12 pontos + abrir covas nos mesmos pontos | médio | nós + MCosta |
| **4** | **Painel INIAV** — *R. necatrix* PCR em raiz, isolamento e qPCR de oomicetas, painel de madeira | médio | INIAV |
| **5** | **RQ6 — drenagem contra raio** | baixo | nós |
| 6 | Fechar as camadas H e M | baixo-médio | nós |
| 7 | Limiar que o laboratório usou para «insuficiente para causar dano» | zero | via Cátia |
| 8 | B3C3 como piloto com par não tratado | baixo | nós |

**Duas condições da AUD-20, antes de alguém viajar:** registar na ficha o **viés
de ordenação** (os pontos são deliberadamente os de maior escoamento dentro de
cada mancha — ninguém pode citar «a margem tem mais escoamento que o controlo»
como achado); e **dar um segundo olhar a M1** no local, porque a textura da
ortofoto ali é ambígua por um motivo já documentado.

---

## 8 · Os erros que este processo já cometeu — para não os repetir

Não é confissão: é a lista do que a próxima pessoa vai ser tentada a fazer.

1. **Derivar uma máscara do sinal que se vai medir.** O cabeçalho dizia
   «polígonos geográficos e estáticos» e o código definia o pomar por limiar de
   NDVI. **Quatro auditorias passaram por cima porque ninguém leu o cabeçalho e
   o código juntos.**
2. **Confirmar um instrumento consigo próprio.** Um NDVI não se confirma com
   outro NDVI.
3. **Não procurar antes de criar.** Numa só sessão, três vezes se começou
   trabalho sobre assunto que já estava em disco — e a ferramenta que o travava
   **já existia** e não disparou, porque varria quatro extensões e a
   inteligência deste caso vive em **dados**.
4. **Um critério pré-registado pode estar pré-registado *e* errado.** A
   definição de «margem em avanço» esteve **invertida**: punha os pontos em
   células com **0,11 m** de copado, ou seja em chão. A C9 impede escolher o
   caminho pelo resultado; **não impede especificar a coisa errada**. Só um
   leitor independente apanha essa classe.
5. **Fechar uma decisão com uma de duas fontes de tipo 1 em conflito.**
6. **Comparar unidades diferentes sem verificar o datum.**

---

## 9 · Por onde começar, se entras hoje

```bash
python Downloads\_VALIDACAO_CAMADAS\certificar.py
python Downloads\_VALIDACAO_CAMADAS\ja_existe.py <termos>
python Downloads\_VALIDACAO_CAMADAS\estatuto.py <ficheiro>
```

A primeira diz se a cadeia está de pé. A segunda corre-se **antes** de escrever
código — e a cadeia falha se houver guião tocado num dia sem busca. A terceira
responde CITÁVEL ou NÃO CITÁVEL sobre qualquer ficheiro.

**E a regra que resume tudo:** a máquina verifica **coerência**, não **verdade**.
As vinte e três retiradas foram todas apanhadas por ir a um instrumento diferente
ou por quem conhece o terreno. A cadeia garante que não nos contradizemos. **Não
garante que tenhamos razão.**
