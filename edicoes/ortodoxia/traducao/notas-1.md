# Ortodoxia — notas do tradutor, trecho 1 (Prefácio, I e II)

Parágrafos: prefácio 2/2, cap. I 7/7, cap. II 20/20. Grep de mesóclise sem resultado.

## Variantes do texto-fonte (LEIAME)

- II, § 15: segui o scan, `free to praise, to curse` → «livre para louvar, para amaldiçoar» (o Gutenberg traz `raise`).
- II, § 19: segui o scan, «The man who begins to think without the proper first principles goes mad, the man who
  begins to think at the wrong end» → «Enlouquece o homem que começa a pensar sem os devidos primeiros princípios, o
  homem que começa a pensar pela ponta errada» (o Gutenberg traz «goes mad; he begins...»). *End* → «ponta», e na
  frase seguinte «a ponta certa».
- II, § 1: «Joanna Southcote» fica como está no Gutenberg e no scan (a grafia corrente é Southcott).

## O verso de Dryden (II, § 6)

É a única citação em verso destes capítulos: dois versos isolados, a citação errada e a certa, cada um dentro de uma
frase da prosa. Pentâmetro jâmbico → decassílabo heroico, conferido com o `molde.mjs` (`10: 6`):

- «Great genius is to madness near allied» → «A loucura é do grande gênio irmã.» — ✓ 3-4-6-8-10.
- «Great wits are oft to madness near allied» → «A loucura é do grande engenho irmã.» — ✓ 3-4-6-8-10.

A graça está em Dryden ter escrito *wits* e não *genius*. A dupla *gênio*/*engenho* (mesma raiz, *ingenium*) faz o
mesmo: os dois versos diferem só nessa palavra, e *engenho* (o de Camões, «engenho e arte») é a inteligência viva,
que Chesterton logo chama de «a pura presteza do intelecto». *Near allied* virou «irmã», parentesco próximo; na prosa,
«Such men are indeed to madness near allied» → «Desses homens, sim, a loucura é irmã», que ecoa o verso. **Perda:** o
*oft* («amiúde»), que não coube sem quebrar o paralelo. Rejeitei «O grande gênio é da loucura irmão», mais natural,
porque o molde dá choque na 5.ª (*gê-nio‿é*). (Nota à margem, não ao leitor: o verso real de *Absalom and Achitophel*
diz «sure to madness», e não «oft»; Chesterton também cita de memória. Traduzi o que ele escreveu.)

**Formato:** deixei os dois versos dentro da frase, entre aspas, sem linha `| `. Motivo: em `js/app.js` um bloco só
vira verso quando *todas* as linhas começam com `| `; uma linha `| ` no meio de um parágrafo apareceria com a barra, e
um bloco à parte acrescentaria parágrafos e desalinharia o modo bilíngue (o casamento é parágrafo com parágrafo).
No original os versos também correm na frase. **Proposta para o guia:** dizer que verso isolado citado dentro de uma
frase fica na linha, entre aspas (metrificado), e que `| ` vale para citações de vários versos em bloco.

## Trocadilhos, paradoxos e soluções

- **romance** (I, § 3): «that mixture of the familiar and the unfamiliar which Christendom has rightly named romance.
  For the very word "romance" has in it the mystery and ancient meaning of Rome». Em português *romance* também vem de
  Roma (*romanice*), então o jogo passa inteiro. Mantive *romance* nas outras ocorrências («vida de romance
  prático»), coerente com o título do cap. VIII, «O romance da ortodoxia». *Novel(s)* no cap. II também é «romance».
- **fool** (I, §§ 2 e 5): «bobo» em tudo («se sentiu meio bobo», «ficado com cara de bobo», «fazê-lo de bobo: o bobo
  desta história sou eu, e rebelde nenhum há de me derrubar do trono»); *bobo* é também o da corte, o que dá sentido
  ao trono.
- **in advance of the age / of the truth** (I, § 5): «andar à frente do meu tempo... uns dez minutos à frente da
  verdade. E descobri que estava mil e oitocentos anos atrás dela.»
- **wonder / welcome** (I, § 3): «uma ideia de assombro e uma ideia de abrigo» (aliteração no lugar da dele).
- **New South Wales / old South Wales**: «a Nova Gales do Sul... a velha Gales do Sul».
- **If a man prefers nothing I can give him nothing**: «Se alguém prefere o nada, nada tenho a lhe dar.»
- **soul / wits** (II, § 3): «perder a alma» / «perder o juízo».
- **Men deny hell, but not, as yet, Hanwell**: «Os homens negam o inferno, mas não, por enquanto, Hanwell.» Perdi a
  aliteração *hell/Hanwell* (idem no fecho do § 10, «no inferno — ou em Hanwell»).
- **picturesque / picture** (II, § 4): «pitoresco» / «pintura» (mesma família, via *pittore*).
- **oddities / odd people**: «esquisitices» / «pessoas esquisitas».
- **Shakespeare held horses... safest man to hold them**: «o homem mais seguro para segurá-los» (o jogo
  *seguro/segurar* é acréscimo de som, não de sentido).
- **knights and castles** (Poe e o xadrez): «cavaleiros e castelos», e não os nomes técnicos (*cavalo*, *torre*),
  que matariam a piada do «como um poema».
- **Calvin / Gilpin**: «Foi condenado por João Calvino; foi quase salvo por John Gilpin.» A rima se perde com a forma
  portuguesa de Calvino, exigida pelo guia; ficou o paralelo da frase.
- **To accept everything is an exercise, to understand everything a strain**: «Aceitar tudo é um exercício; entender
  tudo, uma estafa.»
- **head into the heavens / heavens into his head**: «meter a cabeça nos céus... meter os céus na cabeça. E é a cabeça
  dele que racha.»
- **Dryden... knew better**: «e tinha mais juízo» (o *juízo* do capítulo).
- **As mad as a hatter**: não há ditado português com chapeleiro; «por que se diz “louco como um chapeleiro”» (o
  impessoal não atribui o ditado ao leitor brasileiro, que conhece o Chapeleiro Maluco de Alice). A piada da cabeça
  medida passa inteira.
- **careless and causeless**: «despreocupadas e sem causa»; «Se o louco pudesse por um instante ficar despreocupado,
  ficaria são».
- **lost his reason / everything except his reason**: «perdeu a razão» é também a expressão portuguesa para a loucura;
  passa tal qual.
- **give it arguments... give it air**: «dar-lhe argumentos quanto dar-lhe ar».
- **are all men busy with your business?**: «E todo mundo só se ocupa de você?» Perdi o *busy/business*; «os seus
  negócios» ficaria ambíguo (o leitor leria «os negócios deles», o contrário do sentido).
- **your own little plot**: «a sua própria tramazinha» (*trama* = enredo e conspiração, como *plot*, para o homem que
  se crê vítima de conspiração). *Tiny and tawdry theatre*: «teatrinho tacanho e mambembe».
- **mad doctors are mad doctors in more senses than one**: «a maior parte dos alienistas são alienados em mais de um
  sentido».
- **spotless machine... slightest speck**: «máquina sem mácula... o menor cisco».
- **imp / pimpernel**: «diabrete... pimpinela» (nome que o leitor conhece de *O Pimpinela Escarlate*).
- **chain of causation**: «cadeia da causalidade»; *cadeia* também é prisão, o que reforça «a pior cadeia que jamais
  agrilhoou um ser humano».
- **come to bind, not to loose**: «vêm para atar, não para desatar» (eco do poder de atar e desatar).
- **looking for him in the looking-glass**: «vivem a procurá-lo no espelho»; perdeu-se o eco *looking*.
- **a mean infinity, a base and slavish eternity**: «uma infinitude mesquinha, uma eternidade vil e servil».
- **a blaze and a blur**: «um clarão e um borrão».
- **all moonshine** (II, § 20): «coisa do mundo da lua». *Moonshine* é «tolice»; o «mundo da lua» português é o
  alheamento, o que casa com *detached intellectualism*, e «no sentido exato» continua valendo (é luz da lua).
- **lunatics** (fecho do cap. II): aqui, e só aqui, «lunáticos» em vez de «louco» (guia), porque a frase é sobre a lua
  ter dado o nome a eles.

## Termos e nomes

| inglês | tradução |
|---|---|
| Heretics | “Hereges” (entre aspas, como no original) |
| Newman's Apologia | a _Apologia_ de Newman |
| Mr. G.S.Street, Mr. Shaw, Mr. McCabe, Mr. R.B.Suthers, Mr. Holbein | o sr. G. S. Street, o sr. Shaw etc. |
| the Reverend R.J.Campbell | o reverendo R. J. Campbell |
| the CLARION | o _Clarion_ (jornal) |
| the Pavilion at Brighton | o Pavilhão de Brighton |
| the Apostles' Creed | o Credo dos Apóstolos |
| egotistical | egocêntrico (*egotista* seria lido como erro por *egoísta*) |
| flippant | leviano |
| dull / dulness | tedioso, tédio (I); sem graça, monotonia (II) |
| rotter | traste |
| minister (com uma epopeia) | pastor |
| lunatic asylum, mad-house | hospício |
| maniac, maniacal | maníaco |
| madman, lunatic, insane man | louco |
| free will / free thought | livre-arbítrio / livre-pensamento |
| Super-men, Superman | Super-homens, Super-homem |
| necessitarianism | necessitarismo |
| panegoistic | panegoísta |
| theosophists | teósofos |
| Bloody Mary | Maria, a Sanguinária |
| the Inner Circle; Gower Street | o Inner Circle; Gower Street (sem explicar) |
| threepenny bit | moedinha de três pence |
| poached egg | ovo pochê |
| New Year resolutions | promessas de Ano-Novo |
| housemaid | criada |
| the white flat lilies of the Ouse | os brancos nenúfares espalmados do Ouse |
| signpost | poste indicador |

## Outras decisões

- Ênfases em maiúsculas do Gutenberg viraram itálico: «It is THIS achievement» → «É _esta_ conquista»; «MARK of
  madness» → «a _marca_»; «If thy HEAD offend thee» → «Se a tua _cabeça_ te escandalizar». Não acrescentei outras.
- «If thy HEAD offend thee... cast into hell»: paródia de Mt 5,29-30 e 18,8-9. Traduzi com o *tu* bíblico do
  começo ao fim («com todo o teu intelecto»), embora Chesterton escorregue para *your*; a mistura *tu/você* em
  português pareceria descuido. «Go and sin no more» → «Vai e não peques mais».
- «a god of whom the world is not worthy» (eco de Hb 11,38) → «um deus de quem o mundo não é digno».
- I, § 2: a última das três perguntas retóricas termina com ponto no Gutenberg; usei interrogação, como nas outras.
- Mr. Holbein é Montague Holbein, nadador do canal da Mancha; ficou «o sr. Holbein», sem nota (o «sr.» já indica que
  não se trata do pintor).
