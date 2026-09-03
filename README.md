# Kiw_Ganfei

Investigação forense de detecção remota sobre o declínio de um pomar de
actinídea no Emparcelamento de Ganfei, Valença (CCDR-N · Avisos Agrícolas ·
Entre Douro e Minho).

Este repositório é o **registo reproduzível** do processo: o código, os
documentos da cadeia de certificação, os resultados em JSON/CSV e as oito peças
de apresentação. Não contém imagens de satélite nem produtos da DGT — ver
`.gitignore`, que explica porquê.

---

## ⛔ Ler primeiro

**[`ANTES_DE_COMECAR.md`](ANTES_DE_COMECAR.md)**

A pré-voo de onze perguntas, as seis condições do portão, a taxonomia das
**dezanove** retiradas em quatro famílias, o protocolo das sessões paralelas, e
as armadilhas mecânicas desta máquina.

> **Dezanove veredictos foram retirados em seis dias. Nenhum foi apanhado por
> recomputação — todos por ir a um instrumento diferente.**

## Porque é que este repositório existe

Até 03-09-2026 nada disto estava sob controlo de versões, e isso não era um
descuido administrativo: era um buraco na prova. O adversário independente
(Controlo 3) pôs em **NÃO TESTÁVEL** a afirmação «o critério de exclusão foi
escrito antes de correr», porque `git rev-parse` falhava na pasta e todos os
ficheiros tinham a mesma hora de modificação.

**Sem histórico, «pré-registado» é uma afirmação que ninguém pode verificar** —
e metade das conclusões deste caso depende dela. O histórico daqui para a frente
é a prova; o passado fica como está, e diz-se que fica.

## O portão

```bash
python _VALIDACAO_CAMADAS/certificar.py
```

Sete verificações, código de saída ≠ 0 quando alguma coisa não bate:

| | verifica |
|---|---|
| 1 | o auto-teste do `guarda.py` — sete retiradas históricas têm de bloquear, o controlo positivo tem de passar |
| 2 | as seis condições do portão sobre os 23 factos de `registo_de_factos.py` |
| 3 | a prosa da `LISTA_FINAL` não derivou do registo executável |
| 4 | nenhum documento vivo cita um documento retirado sem o marcar |
| 5 | os scripts que produzem cada facto existem em disco |
| 6 | o rastreio de descontinuidade está fresco |
| 7 | nenhuma figura é mais velha que a lista de factos |

`--completo` volta a correr o rastreio de descontinuidade (descarrega imagem).

## Layout

```
_VALIDACAO_CAMADAS/    a cadeia: certificados C0–C5, adversários, retractações
  guarda.py            o portão — seis condições, levanta excepção, não avisa
  certificar.py        as sete verificações
  registo_de_factos.py a LISTA_FINAL que corre em vez de se ler
  SAIDA_C0..C5/        o que cada camada produziu
_VALIDADE_GESTAO/      análise: REG-01, triagens, ortofoto, INS-04
ganfei_s2/figuras/     as peças P01–P08 e os scripts que as constroem
```

## Duas limitações, ditas à cabeça

**Os caminhos são absolutos.** Os scripts referem `C:\Users\Jackster2\Downloads\…`
e por isso **não correm a partir de um clone** sem edição. É dívida conhecida, e
a primeira coisa a corrigir se este repositório passar a ser o sítio onde se
trabalha em vez de o sítio onde se regista.

**Os dados não estão aqui.** As folhas LiDAR e as ortofotos são produtos da DGT
e não são nossos para redistribuir; as caches são regeneráveis. O
`.gitignore` diz o que fica de fora e porquê.

## Conteúdo de terceiros

Os documentos identificam **duas explorações pelo seu número de beneficiário**
no parcelário do IFAP, contêm coordenadas de uma exploração privada dadas pelo
seu gestor, e referem relatórios de laboratório por número. Isto é adequado num
repositório **privado**, de trabalho. **Antes de qualquer mudança para público,
essa passagem tem de ser uma decisão tomada de propósito**, e não um efeito
lateral de mudar uma opção.
