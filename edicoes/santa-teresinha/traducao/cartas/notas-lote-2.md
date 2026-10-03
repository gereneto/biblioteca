# Notas — Cartas LT 58–91 (lote 2)

34 cartas, de `lt-058.txt` a `lt-091.txt`, uma tradução para cada arquivo-fonte. Grep de mesóclise:
nada. Conferi por script que cada carta tem a mesma disposição de linhas e de linhas em branco do
arquivo-fonte e o mesmo número de reticências, exclamações e interrogações.

## Formato

- **Disposição do texto.** Segui linha por linha a do arquivo-fonte: onde a fonte quebra a linha
  sem deixar linha em branco, a tradução faz o mesmo, e as linhas em branco ficam onde a fonte as
  tem. É também o que faz o lote das LT 92–150, que já está na pasta. O § 6 pede parágrafos
  separados por linha em branco, mas o site junta num só parágrafo as linhas separadas por quebra
  simples, e o original francês, que aparece ao lado, também tem as linhas assim. Com a mesma
  disposição, as duas colunas se casam bloco a bloco. Proposta: se se quiser cada parágrafo da carta
  separado no site, é melhor mudar o `publicar.py` para os dois lados (original e tradução) do que
  mudar só a tradução.
- **Datas dos editores no topo** (*Septembre 1888*, *30 septembre 1888*, *6 ou 7 Janvier 1889*,
  *Début décembre 1888*, *Fin mai 1889*...): traduzidas sem colchetes, como no lote 92–150 (ver
  `lt-104.txt`). Cheguei a pô-las entre colchetes, porque são indicação dos editores, e voltei atrás
  para que os dois lotes fiquem iguais. Proposta: pô-las entre colchetes nos dois lotes. Nenhuma
  carta deste lote tem frente/verso nem trecho perdido.
- **Cabeçalho.** O «le» antes da data cai e vira vírgula («Carmel le 23 Août 88» → «Carmelo, 23 de
  agosto de 88»). Sem «le», fica sem vírgula. «6 h.M.» (LT 60) → «6 h da manhã». LT 70: «Au Carmel le
  Décembre 88» (sem o dia) → «No Carmelo, dezembro de 88».
- **Dias da semana** com a maiúscula de Teresa (Quinta-feira, Terça-feira, Quarta-feira), como no
  lote 92–150. Os meses vão em minúscula (§ 2).
- **Destinatários.** «A Mme Guérin» → «À senhora Guérin», com crase porque «senhora» pede artigo,
  como no lote 92–150. «A Mère Saint-Placide» → «A Madre São Plácido». «à Celine» (título da LT 82,
  sem acento) → «A Celina». Na LT 75, o título diz 6 de janeiro e a data no topo da carta diz «6 ou 7
  Janvier»: o `# data` segue o título, e o corpo segue a carta.
- **Assinaturas.** «Sr Thérèse» → «Irmã Teresa», por extenso. «Th.» → «T.». As abreviaturas
  «p.c.ind.», «post.carm.ind.» e «nov.carm.ind.» ficam como estão, porque também servem em português
  (postulante ou noviça carmelita indigna).
- **Pontuação.** Não pus vírgula de vocativo onde Teresa não pôs («pensar em ti meu Paizinho
  querido»), nem pontuação que falta na fonte: LT 64, «estou em retiro isso me é impossível»; LT 85 e
  89, frases que emendam na seguinte sem ponto.
- **Despedidas.** «Adieu» → «Adeus»; «Au revoir» → «Até a vista»; «A bientôt» → «Até breve».

## Nomes e termos novos

- **Pessoas.** Mlle Pauline (Pauline Romet, amiga da família; LT 58 e 83) → a senhorita Paulina.
  Monsieur David → o senhor David. Madame Fournet → a senhora Fournet. Mme Tifenne → a senhora
  Tifenne. ces demoiselles Primois → as senhoritas Primois. Th. Gilbert → T. Gilbert. son neveu
  Pierre → seu sobrinho Pedro. Hélène → Helena. Marcelline → Marcelina. ma Sœur St Vincent de Paul
  → minha Irmã São Vicente de Paulo. Sr M. du Sacré Cœur (LT 67) → Irmã M. do Sagrado Coração.
  Madame la Prieure (a priora beneditina da Abadia) → a senhora Priora.
- **Louploup** (LT 69) fica como está. É apelido, masculino («je l'aime... pour lui»), e não sei de
  quem.
- **Mme de Sévigné** (LT 62) → Madame de Sévigné, que é a forma consagrada em português. O guia não
  fala de «Mme». Nas outras ocorrências usei «senhora», como no Ms A.
- **le Père** (o padre Pichon, LT 65 e 76) → o Padre, com a maiúscula de Teresa.
- **Apelidos de família.** mon Roi → meu Rei. ta petite Reine → tua Rainhazinha (como
  «rainhazinha» no Ms A, com a maiúscula de Teresa). Reine de France et de Navarre → Rainha de França
  e de Navarra (a fórmula tradicional, sem artigo). La Reine à Papa → A Rainha de Papai. de toutes
  les Navarre → de todas as Navarras. le Diamant (Maria) → o Diamante. la perle fine (Paulina) → a
  pérola fina. ta grande → tua grande. l'Orpheline de la Bérésina → a Órfã do Berezina (o Ms A 4 tem
  «órfã do Berezina»). l'Intrépide N° 2 (Celina) → a Intrépida N.º 2. le petit hanneton blond → o
  besourinho louro. ma belle Poupée (Maria Guérin) → minha linda Boneca. petit lutin → duendezinho.
  petite maîtresse de maison → pequena dona de casa. Benjamin → Benjamim.
- **Imagens do Carmelo.**
  - agneau (Paulina) e agnelet (Teresa) → cordeiro e cordeirinho. Para manter a diferença, «Petit
    agneau» → «Pequeno cordeiro», como no lote 92–150.
  - Lion (Maria) → Leão. balle e petite balle → bola e bolinha. jouet de Jésus → brinquedo de Jesus.
  - Lys-immortelle → Lírio-imortal, com as maiúsculas de Teresa (Lírio-Imortal, lírio-imortal).
    «immortelle de Jésus» (LT 90) → «imortal de Jesus». Perde-se a flor (sempre-viva, perpétua), mas
    fica coerente com Lírio-Imortal.
  - grain de Sable → grão de Areia (com maiúscula onde Teresa a põe). petite ombre de Jésus →
    pequena sombra de Jesus.
- **Outros termos.**
  - Objetos e comidas: image → santinho; petit mot → bilhetinho; point d'Alençon → ponto de
    Alençon; sucre de pomme → açúcar de maçã (é o bastão de açúcar de Rouen; deixei literal);
    pain d'épices → pão de mel; encre de Chine → tinta-nanquim; râteau → ancinho; un sou → um
    vintém; corne d'abondance → cornucópia.
  - Vida religiosa: répons → responsórios; enfants de Marie → filhas de Maria (em minúscula, como
    Teresa); réception au chapitre → admissão pelo capítulo; fiançailles → noivado (fiancé →
    noivo).
  - Vida espiritual: piqûres d'épingles → alfinetadas; sécheresse → aridez; creuset → crisol (como
    na Pri 6); grâces de choix e amis de choix → graças de escol e amigos de escol.
  - Outras palavras: lice → liça; plages éthérées → plagas etéreas; limon → limo; Ps. de David → Sl.
    de Davi; bonne année → feliz ano-novo.
- **Tratamento.** Vós com os tios, com a Madre São Plácido, a Irmã Inês, a Irmã Maria do Sagrado
  Coração e a Irmã Marta. Vós também com Jesus na LT 89 («Vous voyez par là...»), e no plural com os
  Guérin na LT 88 («les bontés que vous avez pour elles»). Tu com Papai, Celina e Maria Guérin.

## Passagens duvidosas e escolhas

- **LT 84.** «ces cinq lettres» são as cinco letras de «merci». Em português a palavra é «obrigada»,
  que tem oito. Pus «estas oito letras», para que a frase continue dizendo a mesma coisa.
- **LT 72.** «émerveillaison» é palavra inventada: é o francês estropiado do guia italiano da
  peregrinação, como os «cornichons» do Ms A. Pus «maravilhação», que também não existe.
- **LT 62.**
  - «Que mon cœur, que mon cœur a de peine» é verso de canção. Traduzi: «Quanta pena, quanta pena
    tem meu coração».
  - «C'est la marraine qui plantait des verveines» parece alusão a algo que não identifiquei.
    Traduzi ao pé da letra.
  - «si tu avais une glande, elle serait percée comme avant le voyage à Rome» → «se tivesses uma
    íngua, ela furaria como antes da viagem a Roma».
- **LT 63.** «de la dentelle digne de : la reine de France et de Navarre» → «renda digna de: a rainha
  de França e de Navarra». Não fiz a contração «da», para manter os dois-pontos antes do título.
- **LT 65.** «mettre la cognée au pied de l'arbre» → «pôr o machado ao pé da árvore». «on puise dans
  les diamants» → «mete-se a mão nos diamantes».
- **LT 69.** «Je suis bien bienheureuse» (com a repetição) → «Sou muito bem-aventurada».
- **LT 76.** Teresa joga com o sentido de «ravir» (arrebatar): «la date du 9 était trop
  ravissante... lui seul est ravissant dans toute la FORCE du terme». Por isso usei «arrebatador» nas
  três vezes. Nas outras cartas, «ravissant» → «encantador» (LT 73, 78) ou «arrebatador» (LT 77, 87).
  «Je vous EN PRIE» → «Eu vos SUPLICO».
- **LT 78.** «Ne mourez pas encore tout de suite» → «Não morrais logo agora».
- **LT 80.** «sera aussi Celui de Sr Marthe» → «será também O da Irmã Marta», com a maiúscula no
  pronome.
- **LT 81.** «Dieu tournerait le monde» → «Deus reviraria o mundo».
- **LT 82.** «l'amour de Jésus sur nos âmes ?...»: mantive o «sobre» e a interrogação, como na fonte.
- **LT 88.** A carta é endereçada a Maria Guérin, mas fala dela na terceira pessoa («le cœur de ma
  petite Marie»). Traduzi como está. O título do livro, «Le bouquet de la jeune fille», ficou «O
  ramalhete da jovem», entre as aspas de Teresa.
- **LT 91.** «aime incomparablement mieux Papa» → «ama Papai incomparavelmente melhor». «le petit
  enfant du bon Dieu» → «o menininho do bom Deus».
- **Gralhas da fonte** que não passaram para a tradução:
  - LT 65: «dan su acte» (= dans un acte).
  - LT 69: «d 'affection».
  - LT 71: «le vie».
  - LT 72: «rien en saurait» (= ne saurait).
  - LT 76: «le plus intimes».
