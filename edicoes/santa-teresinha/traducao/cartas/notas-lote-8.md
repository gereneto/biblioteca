# Cartas, lote 8 (LT 227–266): notas do tradutor

## Geral

- 40 cartas, de `lt-227.txt` a `lt-266.txt` (maio a agosto de 1897), uma tradução para cada arquivo-fonte. Destinatários: 8 ao padre Bellière, 1 ao padre Roulland, 7 a Madre Inês de Jesus, 5 à Irmã Genoveva, 6 à Irmã Maria da Trindade, 3 à Irmã Marta de Jesus, 3 à Irmã Maria da Eucaristia, 3 a Leônia, 2 aos tios Guérin, 1 à Irmã Maria de São José e 1 às três irmãs juntas (LT 245).
- **Linhas**: segui o desenho de linhas da fonte, linha por linha (quebra simples onde ela tem quebra simples, linha em branco onde ela tem linha em branco). Conferi por script: as 40 têm o mesmo desenho. Reticências, exclamações, interrogações, aspas, parênteses, ponto e vírgula, dois-pontos, travessões e itálicos batem em número com o original, salvo as diferenças de propósito: os `(...)` da LT 249, que viraram `[...]`, e os dois-pontos das indicações editoriais (*En haut :*, *Recto :*), que ficaram dentro dos colchetes sem os dois-pontos.
- Grep de mesóclise: nada. `conferir.py cartas`: não aponta nada nestas cartas («Bon Dieu»/«bon Dieu» × «Bom Deus»/«bom Deus» bate em todas).
- **Pontuação**: como nos outros lotes, não acrescentei vírgula de vocativo onde Teresa não a pôs («Obrigada Mãezinha!...», «Mas minha querida pequena b. eu sofro convosco», «Ó meu Deus como sois doce», «A Deus meu querido e muito amado irmão»), nem troquei as vírgulas dela por ponto e vírgula. Tirei só a vírgula entre sujeito e verbo das frases clivadas francesas (*Ce qui m'attire..., c'est* → *O que me atrai... é*; *la seule joie sur la terre, c'est d'accomplir* → *a única alegria na terra é cumprir*), que em português é erro, e fechei com vírgula os incisos que ela abriu sem fechar (*non de mon directeur, mais de mon père la permission* → *não do meu diretor, mas do meu pai, a permissão*).
- **Tratamento**: vós a Madre Inês, às irmãs do Carmelo (Maria da Trindade, Marta de Jesus, Maria da Eucaristia, Maria de São José), aos tios, aos padres Bellière e Roulland, e a Deus/Jesus nas cartas em que Teresa o trata por *vous* (LT 230, 259, 262). Vós também à Irmã Genoveva na LT 228, porque ali Teresa a trata por *vous* («faites comme vous voudrez»). Tu a Leônia. Na LT 230, a Irmã São João Batista trata Teresa por *vous* («vous m'avez fait pitié») e Jesus trata a adúltera por *tu* («Quelqu'un t'a-t-il condamnée?»): ficou assim.

## Cabeçalho e datas

- Destinatários: *A soeur Geneviève* → A Irmã Genoveva; *A soeur Marie de l'Eucharistie* → A Irmã Maria da Eucaristia; *A soeur Marie de la Trinité* → A Irmã Maria da Trindade; *A soeur Marthe de Jésus* → A Irmã Marta de Jesus; *A soeur Marie de Saint-Joseph* → A Irmã Maria de São José; *à Léonie* → A Leônia; *A l'abbé Bellière* → Ao padre Bellière; *Au P. Roulland* → Ao padre Roulland; *A M. et Mme Guérin* → Ao senhor e à senhora Guérin; *A Agnès de Jésus, Marie du Sacré-Coeur et Geneviève* → A Inês de Jesus, Maria do Sagrado Coração e Genoveva (sem os títulos, como no francês); *(Fragments)* → (Fragmentos).
- `# data`: *Avril-Mai 1897* → abril-maio de 1897; *Mi-Juillet* → meados de julho; *Fin Juin* → fim de junho; *Juin-Juillet (?)* → junho-julho (?); *1er Juin* → 1.º de junho. As datas dos editores no topo da carta ficaram sem colchetes, como nos outros lotes, com a maiúscula do começo de linha e a interrogação no lugar em que está na fonte (*3 juin (?) 1897* → *3 de junho (?) de 1897*; *3 (?) juin* → *3 (?) de junho*).
- No corpo: *Carmel de Lisieux 21 Juin 1897 Jésus* → *Carmelo de Lisieux 21 de junho de 1897 Jesus*, sem vírgulas, como na fonte; *15 oct. 95* → *15 de out. de 95*; *Fête de Ste Madeleine* → *Festa de Santa Madalena*.

## Indicações dos editores

- LT 245 (santinho): *Recto* → `[Frente]`; *En haut :* → `[Em cima]`; *En bas :* → `[Embaixo]`; *De chaque côté :* → `[De cada lado]`; *Verso* → `[Verso]`. LT 266: *Recto :*, *Verso :* → `[Frente]`, `[Verso]`.
- LT 238: a última linha, *Original à la Visitation de Caen*, é nota dos Arquivos sobre o paradeiro do original: → `[Original na Visitação de Caen]`.
- LT 249 (fragmentos): `(...)` → `[...]`, como na LT 104.
- Ficaram entre parênteses, porque são de Teresa: *(2e petit mot)* na LT 232 → *(2.º bilhetinho)*; *(St Jean de la Croix)* e *(Thérèse de l'Enfant Jésus empruntant les pensées de l'angélique Martyr Théophane Vénard.)* na LT 245; *(Très graves Explications pour le distribution des Fleurs)* na LT 260; *(A ma bien-aimée petite Soeur Geneviève de Ste Thérèse)* na LT 262; *(C'est par choix que je suis devenue votre sœur.)* na LT 263.

## Versos

- **LT 239**: *Il faut que je marche jusqu'à mon dernier instant - C'est lui qui finira mon tourment - Comme le pauvre Juif errant –* são três versos de canção popular (a queixa do Judeu Errante), que a fonte dá numa linha só, separados por travessões. Mantive a linha única (uma linha para cada linha da fonte) e comecei-a com `| `. Não metrifiquei; guardei a rima *instante/errante*: «É preciso que eu caminhe até o meu derradeiro instante - É ele quem dará fim ao meu tormento - Como o pobre Judeu errante –». O *lui* minúsculo ficou *ele*.
- **LT 245**, *Je vois ce que j'ai cru / Je possède ce que j'ai espéré / Je suis unie à Celui que j'ai aimé / de toute ma puissance d'aimer.*: não é verso, é prosa (a antífona de Santa Inês, adaptada) quebrada em linhas no santinho. Ficou sem `| `, uma linha para cada linha.
- **LT 255**: a estrofe de *Vivre d'Amour* citada no meio da prosa («Mourir d'Amour c'est un bien doux martyre») ficou na mesma linha, sem marca, traduzida ao pé da letra: «Morrer de Amor é um martírio bem doce». A PN 17 ainda não está traduzida; quando estiver, vale pôr aqui o verso tal como ficar lá. O título vai entre as aspas de Teresa, «Viver de Amor» (o Ms C traz *_Viver de Amor_*).

## Nomes

| francês | português | observação |
|---|---|---|
| Sr St J.Baptiste; ma Sr St Jean B. (LT 230) | a Irmã São J. Batista; a minha Irmã São João B. | § 4; ficam as iniciais dela |
| Sr Marie de Saint-Joseph | Irmã Maria de São José | nome novo |
| Sr M. de l'Eucharistie (LT 255) | Irmã M. da Eucaristia | |
| mère Agnès de Jésus (LT 258, minúscula) | madre Inês de Jesus | com a minúscula dela |
| Mr Clodion (LT 228) | o senhor Clodion | apelido, ao que parece de um dos médicos que a auscultavam (Clodion le Chevelu, rei franco de cabelos longos); o nome fica em francês |
| ce Pauvre Mr (LT 228) | esse Pobre senhor | |
| Mr de Cornière (LT 255) | o senhor de Cornière | o médico do Carmelo; § 3 (*M.* → *o senhor*) |
| N.D. des Victoires | Nossa Senhora das Vitórias | abreviatura desdobrada, como *N.-S.* |
| Notre Mère Immaculée (LT 254) | Nossa Mãe Imaculada | a Virgem: *Mère* → *Mãe* |
| Francis; Jeanne | Francis; Joana | |
| Louis de France (LT 263) | Luís de França | São Luís, rei |
| Salomon; Abraham; Madeleine | Salomão; Abraão; Madalena | |
| les hébreux (LT 261) | os hebreus | com a minúscula dela, que é também a do português |
| Juif errant (LT 239) | Judeu errante | |
| la Visitation de Caen | a Visitação de Caen | |
| Th.; Th. de E. J. (LT 266) | T.; T. do M. J. | iniciais adaptadas (Enfant Jésus → Menino Jesus) |
| r.c.i.; rel.carm.; rel. carm. ind. | ficam | como nas outras cartas |

## Termos e escolhas

- **Notre Mère / notre Mère**: segui a maiúscula de Teresa (*Nossa Madre* onde ela escreve *Notre*, também no meio da frase, como na LT 254 «priez pour Notre Mère»; *nossa Madre* onde escreve *notre*). O lote 4 pôs *nossa Madre* minúsculo no meio da frase; aqui preferi o § 3 (as maiúsculas ficam onde ela as pôs).
- **A Dieu**: nestas cartas Teresa escreve de propósito *A Dieu*, separado (LT 244, 253, 255, 257, 258, 261, 263). Traduzi *A Deus*, que guarda a separação e o sentido. Onde ela escreve *Adieu* junto (LT 249) ficou *Adeus*.
- **petite soeur / petite Soeur**: no corpo, *irmãzinha* (*Irmãzinha* com a maiúscula dela). Nas assinaturas, como no lote 4, *pequena Irmã* quando ela escreve *Soeur* e *pequena irmã* quando escreve *soeur* («Vossa indigna pequena Irmã T....», «Tua pequena irmã T. do Menino Jesus»). *Mon cher petit Frère* (Bellière) → *Meu querido Irmãozinho*; *Mon Frère* (Roulland) → *Meu Irmão*, com a maiúscula onde ela a põe.
- **votre petite fille / Votre toute petite fille** (a Madre Inês e aos tios) → *vossa filhinha*, *Vossa filhinha bem pequenina*; *ma petite maman* (LT 252) → *minha mamãezinha*, com a minúscula dela; *mon cher petit père* (LT 263, o pai) → *meu querido paizinho*.
- **Mes Parents chéris / mes chers parents** (os Guérin, LT 255 e 260) → *meus Parentes queridos*, *meus queridos parentes*: são os tios, não os pais.
- **Fala de bebê**: *Bébé va faire dodo* → *Bebê vai nanar*; *bébé ayant besoin de faire dodo* → *pois bebê precisa nanar*; *je ne vis que de lolo* → *só vivo de leitinho*; *petit bébé au lolo* → *bebezinho de leitinho*. *Lolo* é o leite na fala de criança; *leitinho* guarda o tom sem inventar palavra.
- **Grafias de brincadeira**: *gai raigrette* (LT 232 e 242, «j'ai regret» escrito de brincadeira) → *tenho pezar*, com o *z* errado de propósito; *trais riches* (LT 228) → *muinto ricos*.
- **p.** (LT 236 e 249, *ma chère petite p.*, *pauvre petite p.*): é *poupée*, o apelido da Irmã Maria da Trindade. Pus a inicial da palavra portuguesa, *b.* (boneca), como o lote 2 fez com *Poupée* → *Boneca*. Se se preferir não interpretar a abreviatura, basta voltar a *p.*
- **LT 260, *une Pensée*** (a flor amor-perfeito e o pensamento): traduzi *um Pensamento*, que os dicionários registram também como nome do amor-perfeito; o jogo com *todos os que desabrocham... no jardim do meu coração* fica de pé. *Boutons de Roses* → *Botões de Rosa*; *très graves Explications* → *Muito graves Explicações*.
- **LT 236, *aux pains***: o ofício das hóstias (os *pains d'autel*). Deixei literal, *irei convosco aos pães*, para não explicar; *le lavage* → *a lavagem* (o dia da roupa).
- **LT 240, *manger de la terre***: literal, *comer terra*, em oposição ao *Pão dos Anjos* da mesma frase.
- **LT 251, *attrapez tout le monde*** → *pregai uma peça em todo o mundo* (*attraper* = enganar, de brincadeira).
- **LT 242, *vous plaidez le faux pour savoir le vrai*** (o provérbio *prêcher le faux pour savoir le vrai*) → *advogais o falso para saber o verdadeiro*. *in-folio* → *in-fólios*, palavra portuguesa dicionarizada, sem itálico.
- **LT 237 e 256, *crever le coeur*** → *cortar o coração*.
- **LT 259, *briser*** (Sl 140, «Corripiet me justus») → *quebrantar*, que tem o sentido espiritual; *amollir* → *amolecer*; *huile répandue* → *óleo derramado*.
- **LT 229, *faire de la peine... sa petite peine*** → *causar pena... a sua pequena pena*, para guardar o eco; na LT 258, *lui avoir fait de la peine* → *ter-lhe causado pena*, pelo mesmo critério. *N'ayez pas de peine* (LT 231, 236) → *Não vos aflijais*; *chagrin* (LT 232) → *desgosto*.
- **LT 229 e 247, *le plus petit*** (Mt 25, 40; Mt 11, 25) → *o mais pequenino*, *aos mais pequeninos*, no masculino do original, para não cair no «menor» e guardar o jogo «E sou eu o mais pequenino!...».
- **enveloppe**: nas LT 231 e 232 é o envelope da carta (a imagem de Teresa: a alma é a carta) → *envelope*; nas LT 254 e 258, *l'enveloppe mortelle* → *o invólucro mortal*. *dépouille mortelle* (LT 261) → *despojo mortal*.
- *ici-bas* → *aqui na terra*; *d'ici-bas* e *de ce monde* → *deste mundo*. *combler (mes désirs)* → *satisfazer*; na LT 258 (*elle comblera vos désirs*, depois de *vous satisfaire*) → *atenderá plenamente*. *image* → *santinho*; *petit mot* → *bilhetinho*; *commissions* → *recados*; *brouillonner* → *rabiscar*; *Océan sans rivages* → *Oceano sem margens*; *boire le calice jusqu'à la lie* → *beber o cálice até a borra*; *gerbes fleuries* → *ramos floridos*; *couplet* → *estrofe*; *pinson* → *tentilhão* (a imagem continua: «os tentilhões dormitam»); *mon grand air* → *o meu ar solene*; *petite éphémère* → *pequena efêmera* (o inseto).
- **hélas** → *ai!*, como nos outros lotes.
- **LT 263, *C'est le vœu que forme.*** (a frase continua na assinatura) → *É o voto que faz.*, como no lote 4 (*les vœux qu'elle forme* → *os votos que faz*).

## Passagens duvidosas e correções

- **LT 257**: o fonte começa por *.M.J.T.* (falta o J): → *J.M.J.T.*
- **LT 236**: *j'irais vous trouver* (condicional) deve ser lapso por *j'irai*, como o *j'irai* da mesma frase: → *irei ter convosco*. *qq minutes* → *alguns minutos*, por extenso.
- **LT 253**: *9ne* → *novena*; **LT 263**: *ns* → *nós*. Abreviaturas desdobradas, como as do § 3.
- **LT 247**: *«Il y plusieurs demeures»* (falta o *a*) → *«Há várias moradas»*.
- **LT 255**: *que son sacrifice bien accepté feraient naître* (verbo no plural) → *faria nascer*.
- **LT 260**: *pour le distribution* → *para a distribuição*.
- **LT 261**: *plus tard elle revient dans le monde* (presente no meio de passados simples) → *mais tarde ela volta para o mundo*, no presente, como está; e o anacoluto *D'abord ce furent ses deux aînées, puis la troisième... fit un essai* ficou como na fonte.
- **LT 262**: *Ps XXII. 4.* → *Sl XXII. 4.*; **LT 243**: *Ps. xciii.* → *Sl. xciii.*, no formato dela. **LT 230**: *(cant. des cant.)* → *(cânt. dos cânt.)*. **LT 261**: *(Apocalypse)* → *(Apocalipse)*.
- **LT 258**: o espaço antes do fecho de aspas (*cette joie. »*) não passou.
- **LT 249**: as linhas truncadas dos fragmentos ficaram truncadas no mesmo ponto (*Agora ele não me*; *compreendido o vosso combate...*, que começa no particípio).
- **LT 228**: não sei se *Pauvre, Pauvre* é apelido de Celina ou só exclamação; como a maiúscula se repete em *ce Pauvre Mr* e a carta joga com *riches* no fim, mantive *Pobre* com maiúscula e o jogo *Pobre... ricos*.
- **LT 234**: *A ma chère petite Soeur chérie* (o adjetivo dobrado) → *À minha cara Irmãzinha querida*, para não repetir *querida*.
