# Confissões, de Santo Agostinho — convenções da tradução

Leia antes `edicoes/CONVENCOES-TRADUCAO.md` (regras gerais). Este guia acrescenta o específico.

## Texto-fonte

`original/livro-01.txt` ... `livro-13.txt`: o latim do The Latin Library (texto de O'Donnell). As marcas
`[I.1]` (capítulo em romano, seção em arábico) abrem os parágrafos: ficam iguais na tradução, no começo
do parágrafo correspondente. O latim vem sem maiúsculas no começo das frases: a tradução usa a
pontuação e as maiúsculas normais do português. O sinal `†` (lugar corrompido, livro I, XIV.23):
traduza a leitura mais provável e registre nas notas.

## Registro e tratamento

- O livro é uma oração dirigida a Deus, do começo ao fim: **tu** (*tu, te, ti, teu*), com o verbo na 2.ª
  pessoa do singular. Pronomes de Deus em minúscula; *Deus*, *Senhor*, *Cristo*, *Verbo*, *Espírito
  Santo* com maiúscula.
- Prosa elevada e musical, cheia de antíteses, perguntas, exclamações e ecos dos Salmos. Guarde as
  figuras (*sero te amavi, pulchritudo tam antiqua et tam nova* → «tarde te amei, beleza tão antiga e
  tão nova»), as repetições e o ritmo. Não explique os jogos de palavras; registre nas notas os que
  não passarem.
- Citações bíblicas: Agostinho cita a Bíblia latina antiga (muitas vezes a Vetus Latina, sobretudo os
  Salmos): traduza o latim dele, não uma Bíblia portuguesa. Ele raramente dá a referência; não
  acrescente referências no texto.
- Termos: *confessio* → confissão; *anima* → alma; *animus* → espírito ou ânimo (conforme o caso);
  *mens* → mente; *memoria* → memória; *cor* → coração; *gratia* → graça; *concupiscentia* → concupiscência;
  *libido* → desejo, paixão (evite «libido»); *continentia* → continência; *Manichaei* → os maniqueus;
  *Academici* → os acadêmicos; *grammaticus, rhetor* → gramático, retor; *catechumenus* → catecúmeno.

## Nomes

Mônica; Patrício; Adeodato; Alípio; Nebrídio; Ambrósio; Simpliciano; Vitorino (Mário Vitorino);
Ponticiano; Fausto (o bispo maniqueu); Verecundo; Romaniano; Hierio; Cícero, *Hortênsio*; Virgílio,
Eneias, Dido, Creúsa; Platão, os platônicos; Aristóteles, as *Categorias*; Tagaste; Madaura; Cartago;
Roma; Milão; Óstia; Cassicíaco; Hipona. Livros bíblicos e personagens na forma portuguesa usual.

## Formato

Cada livro traduzido vai para `traducao/livro-NN.txt`, com o cabeçalho
```
# titulo: Livro I
```
e depois os parágrafos, com as marcas `[I.1]`... no começo, como no original (um parágrafo traduzido
para cada parágrafo latino). O hino de Ambrósio citado em IX.12.32 (*Deus, creator omnium*) se traduz
em verso pelo método do Versificador (dímetros jâmbicos → octossílabos 4-8, com o número de versos e o
esquema do original), conferido com o `molde.mjs`; registre nas notas.
