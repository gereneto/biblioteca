# Santa Teresinha — convenções da tradução

Tradução da obra completa de Santa Teresa do Menino Jesus e da Sagrada Face (Thérèse Martin,
1873–1897) para o português do Brasil, a partir do texto francês da edição crítica (Nouvelle
Édition du Centenaire), tal como publicado pelos Arquivos do Carmelo de Lisieux.

Todo tradutor desta obra segue este guia. Na dúvida, a regra é: **fidelidade ao que Teresa
escreveu, em português correto, natural e literário**.

---

## 1. Fontes

| pasta (em `original/`) | conteúdo | observação |
|---|---|---|
| `manuscritos/ms-a.txt`, `ms-b.txt`, `ms-c.txt` | Manuscritos autobiográficos | `[[Ms A 2r]]` marca o começo de cada lado de folha; um parágrafo pode continuar na folha seguinte |
| `manuscritos-site-antigo/` | os mesmos, do site antigo dos Arquivos | segundo testemunho, para conferir passagens duvidosas |
| `cartas/lt-001.txt` ... `lt-266.txt` | 266 cartas de Teresa | as linhas `# ` do topo são do arquivo, não da carta |
| `oracoes/pri-01.txt` ... `pri-21.txt` | 21 orações | idem |
| `poesias/pn-01.txt` ... `pn-54.txt`, `pn-18bis.txt`, `ps-01.txt` ... `ps-08.txt` | poesias | o fim do arquivo traz notas dos Arquivos (Datation, Destinataire, comentário): não se traduzem |
| `poesias-site-antigo/` | as mesmas, do site antigo | segundo testemunho: o novo tem alguns erros («oint» por «Point», «F rancis»), o antigo outros («champs d blé»); o antigo traz algumas indicações de ária que o novo não tem; só o novo marca os itálicos |
| `recreacoes/rp-1.txt` ... `rp-8.txt` | recreações piedosas (teatro) | a numeração de linhas da edição crítica foi retirada; confira se sobrou algum número solto |

**O que não se traduz**: notas e comentários dos Arquivos, endereços da internet, a numeração de
linhas, «Datation», «Destinataire», remissões a partituras. **O que se traduz entre colchetes**: as
indicações editoriais do próprio texto, como `[Scène 2]` → `[Cena 2]`, `Recto :` → `[Frente]`.
Palavra que a edição crítica restituiu entre colchetes (`[en] délivrant`) entra na tradução sem
colchetes; correção de grafia (`Aolysia [Aloysia]`) vira só a forma certa.

Parágrafo partido entre duas folhas: junte-o na tradução (ver § 6).

---

## 2. Registro e tratamento

- Português do Brasil culto e literário, claro, sem afetação nem modernismos de gíria. A frase de
  Teresa é espontânea, cheia de vírgulas, reticências e exclamações: mantenha o movimento dela; não
  corte frases longas nem as "arrume".
- **tu** → **tu** (com o verbo na 2.ª pessoa do singular): Teresa trata assim Jesus (quase sempre),
  Celina, as noviças, a criança.
- **vous** → **vós** (com o verbo na 2.ª pessoa do plural, e *vosso*, *vos*), tanto no singular de
  respeito quanto no plural: Madre Inês, Madre Maria de Gonzaga, os tios, os padres, Deus nas
  orações formais. *«C'est à vous, ma Mère chérie»* → *«É a vós, minha Madre querida»*.
  Quando Teresa passa do *vous* ao *tu* no mesmo texto (Ms B, orações), a tradução passa junto.
- **Nunca mesóclise.** Reescreva com próclise, ênclise ou outra construção: *je vous dirai* → *eu
  vos direi* (nunca *dir-vos-ei*); *il se fera* → *há de fazer-se*. Antes de entregar, rode:
  ```
  grep -n -E -o "[A-Za-zÀ-ÿ]+-(lo|la|los|las|o|a|os|as|me|te|se|lhe|lhes|nos|vos|no|na)-(ei|as|á|ás|emos|eis|ão|ia|ias|íamos|íeis|iam)\b" <arquivos>
  ```
  Não pode sair nada.
- Colocação pronominal brasileira culta: próclise onde soa natural (*que me disse*, *não te
  esqueço*), ênclise no início de frase (*Disse-me*).
- Citações bíblicas: traduza o texto como Teresa o escreve (ela cita de memória ou de Bíblias
  francesas da época), não copie uma Bíblia portuguesa. As referências dela vão traduzidas no
  mesmo formato: *(St Marc, Chap. III, v. 13)* → *(S. Marcos, cap. III, v. 13)*; *(Ep. aux Rom.
  chap. IX, v. 15 et 16)* → *(Ep. aos Rom., cap. IX, v. 15 e 16)*.
- Datas: *4 Avril 1877* → *4 de abril de 1877* (mês com minúscula).

## 3. Tipografia

- Aspas: as de Teresa, angulares: «...». Aspas dentro de aspas: “...”.
- **Reticências, exclamações e interrogações repetidas ficam como ela escreveu** (*...*, *....*,
  *!!!*, *!...*). Também os pontilhados longos que ela usa como separação.
- **Maiúsculas de reverência ficam onde ela as pôs**: *Amour* → *Amor*, *Ciel* → *Céu*, *Époux* →
  *Esposo*, *Bien-Aimé* → *Bem-Amado*, *Lui* (Jesus) → *Ele*, *Sa Face* → *Sua Face*. Não acrescente
  maiúsculas que ela não usou.
- Sublinhado no manuscrito (no texto-fonte, `_assim_`) → itálico `_assim_`. Palavra estrangeira
  ou título de livro → `_itálico_` também.
- Abreviaturas: *St*, *Ste* → *São*, *Santo*, *Santa* por extenso (*St Augustin* → *Santo
  Agostinho*); *N.-S.* → *Nosso Senhor*; *Mr*, *M.* → *o senhor*; *Mgr* → *dom*; *P.* (padre
  religioso) → *padre*. *J.M.J.T.* (Jesus, Maria, José, Teresa) fica como está.

## 4. Nomes

**Família**: *Papa* → *Papai*; *Maman* → *Mamãe*; *petite Mère* (Paulina, a «segunda mãe») →
*Mãezinha*; Louis Martin → Luís Martin; Zélie → Zélia; Marie → Maria; Pauline → Paulina;
Léonie → Leônia; Céline → Celina; Hélène → Helena; Thérèse → Teresa (*Thérésita* fica);
Isidore Guérin → Isidoro Guérin (*mon oncle* → *meu tio*, *ma tante* → *minha tia*);
Jeanne Guérin → Joana Guérin; Marie Guérin → Maria Guérin; Louise (a empregada) → Luísa;
Victoire → Vitória.

**Nomes de religião** (a forma portuguesa usual): Mère Agnès de Jésus → Madre Inês de Jesus;
Sœur Marie du Sacré-Cœur → Irmã Maria do Sagrado Coração; Sœur Geneviève de Sainte-Thérèse
(Celina) → Irmã Genoveva de Santa Teresa; Mère Geneviève (a fundadora) → Madre Genoveva;
Sœur Marie de l'Eucharistie → Irmã Maria da Eucaristia; Mère Marie de Gonzague → Madre Maria de
Gonzaga; Sœur Marie de la Trinité → Irmã Maria da Trindade; Sœur Marthe de Jésus → Irmã Marta de
Jesus; Sœur Marie-Madeleine du Saint-Sacrement → Irmã Maria Madalena do Santíssimo Sacramento;
Sœur Thérèse de Saint-Augustin → Irmã Teresa de Santo Agostinho; Sœur Saint-Vincent-de-Paul →
Irmã São Vicente de Paulo; Sœur Marie des Anges → Irmã Maria dos Anjos; Sœur Saint-Stanislas →
Irmã Santo Estanislau; Sœur Aimée de Jésus → Irmã Amada de Jesus; Sœur Marie-Philomène → Irmã
Maria Filomena; Sœur Saint-Jean-Baptiste → Irmã São João Batista; Sœur Françoise-Thérèse
(Leônia, visitandina) → Irmã Francisca Teresa; Mère Henriette → Madre Henriqueta.
Outros nomes de religião: traduza pelo mesmo critério e registre nas notas (§ 8).

**Clero**: *l'abbé X* → *o padre X* (também para o seminarista Bellière); *le P. Pichon* → *o
padre Pichon*; *Mgr Hugonin* → *dom Hugonin*; *Léon XIII* → *Leão XIII*; *M. Révérony* → *o padre
Révérony*. Sobrenomes ficam em francês (Martin, Guérin, Pichon, Roulland, Bellière, Youf,
Delatroëtte).

**Santos e devoções**: Jeanne d'Arc → Joana d'Arc; Cécile → Cecília; Agnès → Inês; Louis de
Gonzague → Luís Gonzaga; Stanislas Kostka → Estanislau Kostka; Théophane Vénard → Teófano
Vénard; Jean de la Croix → João da Cruz; Thérèse d'Avila → Teresa de Ávila; Augustin →
Agostinho; Marie-Madeleine → Maria Madalena; Sébastien → Sebastião; Martin → Martinho;
Notre-Dame des Victoires → Nossa Senhora das Vitórias; Notre-Dame du Mont-Carmel → Nossa
Senhora do Monte Carmelo; Notre-Dame du Perpétuel Secours → Nossa Senhora do Perpétuo Socorro.

**Lugares**: Lisieux, Alençon, Trouville, Bayeux, Caen e as cidades francesas pequenas ficam;
*les Buissonnets* → *os Buissonnets*; *l'Abbaye* (o colégio) → *a Abadia*; Rome → Roma; Milan →
Milão; Venise → Veneza; Bologne → Bolonha; Lorette → Loreto; Naples → Nápoles; Pompéi → Pompeia;
Assise → Assis; Florence → Florença; Pise → Pisa; Gênes → Gênova; Marseille → Marselha; Lyon →
Lião; le Colisée → o Coliseu; le Tonkin → o Tonquim.

## 5. Vocabulário

| francês | português |
|---|---|
| le bon Dieu, le Bon Dieu | o bom Deus, o Bom Deus (com a maiúscula onde Teresa a põe) |
| la petite Thérèse; votre petite Thérèse | a pequena Teresa; vossa pequena Teresa (não «Teresinha») |
| Monseigneur; Sa Grandeur | Monsenhor; Sua Grandeza |
| notre Père (o superior) | nosso Padre |
| le petit Jésus | o pequeno Jesus |
| Notre-Seigneur | Nosso Senhor |
| la Sainte Vierge | a Santíssima Virgem (*la Vierge Marie* → a Virgem Maria) |
| l'Enfant Jésus | o Menino Jesus |
| la Sainte Face | a Sagrada Face |
| le Sacré-Cœur | o Sagrado Coração |
| l'Amour Miséricordieux | o Amor Misericordioso |
| la petite voie | a pequena via |
| l'ascenseur | o elevador |
| le Ciel | o Céu |
| le Bien-Aimé, l'Époux | o Bem-Amado, o Esposo |
| holocauste, victime | holocausto, vítima |
| petite fleur (blanche) | florzinha (branca) |
| le petit oiseau | o passarinho |
| grain de sable | grão de areia |
| Carmel, carmélite | Carmelo, carmelita |
| prieure; sous-prieure | priora; subpriora |
| maîtresse des novices | mestra de noviças |
| prise d'habit; profession; prise de voile | tomada de hábito; profissão; tomada de véu |
| chœur; parloir; tour; cellule; réfectoire | coro; locutório; roda; cela; refeitório |
| récréation (da comunidade) | recreio |
| Office (divino) | Ofício |
| retraite | retiro |
| la clôture | a clausura |
| tourière | rodeira |
| le Saint-Père, le Pape | o Santo Padre, o Papa |

## 6. Formatos de saída

Toda tradução vai para `edicoes/santa-teresinha/traducao/`. Arquivos em UTF-8, parágrafos
separados por uma linha em branco, cabeçalho com linhas `# chave: valor`.

### Manuscritos (`traducao/manuscritos/<trecho>.txt`)

```
# manuscrito: A
# folhas: Ms A 2r – Ms A 23v

{Ms A 2r}

J.M.J.T.

...parágrafo... aos Santos que O tinham {Ms A 2v} ofendido, como São Paulo...
```

- Um parágrafo traduzido para cada parágrafo do original, na mesma ordem (títulos e linhas
  soltas do começo do Ms A também são parágrafos).
- `{Ms A 2v}` marca o começo de cada lado de folha, como `[[Ms A 2v]]` no original. Se a folha
  começa num parágrafo novo, a marca fica numa linha sozinha antes dele; se a folha começa no
  meio de uma frase, junte o parágrafo e ponha a marca dentro dele, entre as palavras que
  correspondem à virada da folha.
- Não acrescente títulos, notas nem explicações.

### Cartas (`traducao/cartas/lt-001.txt`)

```
# carta: LT 1
# destinatario: A Louise Magdelaine
# data: 4 de abril de 1877

texto da carta, com o cabeçalho (J.M.J.T., lugar, data) e a assinatura como no original
```

- O título do arquivo-fonte (`LT 001 – A Louise Magdelaine – 4 Avril 1877`) dá destinatário e
  data; traduza o destinatário (*A Pauline* → *A Paulina*; *A Mère Agnès de Jésus* → *A Madre Inês
  de Jesus*).

### Orações (`traducao/oracoes/pri-01.txt`)

```
# oracao: Pri 1
# titulo: Minha boa Santíssima Virgem
# data: (se o arquivo trouxer)

texto
```

### Poesias (`traducao/poesias/<sigla>/`, ex.: `pn-17/`)

O método é o do Versificador (§ 7). Arquivos:

- `original.txt` — o poema francês limpo: cabeçalho (`# titulo`, `# sigla: PN 17`, `# aria`, `# data`,
  `# destinatario`, `# fonte`), depois os versos, uma linha por verso, estrofes separadas por
  linha em branco, sem os números de estrofe. Dedicatórias, assinaturas e outras linhas que não
  são versos vão no cabeçalho (`# dedicatoria:`, `# assinatura:`, `# nota:`).
- `molde-original.txt` — escansão do francês (§ 7).
- `traducao-molde.txt` — molde português.
- `traducao.txt` — a tradução: cabeçalho (`# titulo`, `# sigla`, `# aria` — o nome da ária fica em
  francês, em itálico: `_Il est à moi_` —, `# data`, `# dedicatoria`, `# assinatura`, traduzidos), depois
  os versos, no mesmo número de estrofes e versos do original.
- `notas.md` — metro do original e da tradução (uma frase cada), esquema de rimas, escolhas e
  perdas (um parágrafo curto), e o resultado do `molde.mjs` (quantos ✓, ~, ✗, ≠).

### Recreações piedosas (`traducao/recreacoes/rp-1/`)

- `original.txt` e `traducao.txt` no formato de texto da Biblioteca:
  - `## Cena 2` — título de cena (o original traz `[Scène 2]`);
  - `@ JOANA` — nome de quem fala, numa linha sozinha, com a rubrica junto se houver:
    `@ CATARINA, _timidamente_.`;
  - rubrica solta: parágrafo em itálico `_..._`;
  - versos: linhas começadas por `| `, uma estrofe por bloco;
  - prosa: parágrafos comuns.
- `traducao-molde.txt` — o molde dos versos, na ordem em que aparecem, estrofes separadas por
  linha em branco (é o que `versos.py` extrai do texto).
- Conferência dos versos:
  ```
  python edicoes/santa-teresinha/versos.py traducao/recreacoes/rp-1/traducao.txt traducao/recreacoes/rp-1/traducao-molde.txt --so-problemas
  ```
- `notas.md` — como nas poesias.

## 7. Versos: o método do Versificador

Toda tradução de versos segue o manual da Solar Editora. Leia antes de começar:

- `C:\Users\geren\OneDrive\Documentos\Onedrive do Gere\Solar\Editora\Versificador\traducao\MANUAL-DE-TRADUCAO.md`
  (princípios, passos, tabela de metros, lições, lista de conferência);
- `...\Versificador\estudo\ESTUDO-DO-RITMO.md`, § 5 (regras práticas) e § 6 (versos-modelo);
- um caso resolvido com francês: `...\Versificador\traducao\o-albatroz\` e `...\cancao-de-outono\`.

Em resumo:

1. **O que não se negocia**: português correto e natural; a medida de cada verso; o esquema de
   rimas do original (rima feminina francesa → rima grave; masculina → aguda); o número de versos
   e de estrofes; o refrão, traduzido sempre do mesmo modo.
2. **Sentido**: fiel dentro do possível. Ceda primeiro a palavra literal (sinônimo), depois o
   ornamento, depois a imagem secundária (que pode ir para o verso vizinho da mesma estrofe). A
   imagem central da estrofe e o conteúdo teológico só cedem em último caso, e a perda vai para
   `notas.md`. Estes poemas são orações e catequese: não troque uma afirmação de fé por outra.
3. **Medida**: a contagem francesa é a portuguesa (até a última tônica; o *e* mudo final vira
   `+1`). Alexandrino francês → alexandrino clássico (6.ª obrigatória, lei do hemistíquio:
   `12: 6`); decassílabo francês 4+6 → decassílabo com a 4.ª e, em cada verso, a 6.ª (heroico) ou
   a 8.ª (sáfico), sem misturar ao acaso (escolha uma cadência dominante por poema; ver regra 5 do
   estudo); octossílabo → octossílabo com a 4.ª (`8: 4`); heptassílabo → redondilha maior (sem
   acento na 6.ª); hexassílabo, pentassílabo e versos curtos → a mesma medida (`6: 2`, `5: 2`...).
   Muitos destes poemas foram escritos sobre árias conhecidas; guardar a medida e as rimas é
   também guardar a possibilidade de cantá-los.
4. **Moldes**: `molde-original.txt` com uma linha por verso (`12: 2-6-9-12 +1`), linha em branco entre
   estrofes, e duas ou três linhas `#` no topo que dizem o metro; `traducao-molde.txt` com os tempos
   obrigatórios (`12: 6`, `10: 4-6`, `10: 4-8`, `8: 4`, `7:` ...). Nomes de leitura difícil ganham
   `# troca: Thabor => Tabor`.
5. **Conferência**, a cada estrofe e no fim:
   ```
   node "C:\Users\geren\OneDrive\Documentos\Onedrive do Gere\Solar\Editora\Versificador\ferramentas\molde.mjs" traducao.txt traducao-molde.txt --so-problemas
   ```
   Meta: nenhum ✗, nenhum ≠, nenhuma «leitura natural tem N». Os ~ que ficarem têm de ser
   deliberados e justificados em `notas.md`. Teste um verso isolado com
   `--verso "..." --molde "10: 4-8"`.
6. **Varredura final**: grep de mesóclise; leia só as palavras finais e confira o esquema de rimas
   contra o original; quatro versos seguidos com o mesmo esqueleto pedem que se reescreva um;
   leia em voz alta.

## 8. Notas do tradutor

Cada tarefa grava, junto da tradução, um `notas-<trecho>.md` (prosa) ou o `notas.md` da pasta
(versos) com: nomes e termos novos e como foram traduzidos; passagens duvidosas do original (e o
que o site antigo diz); escolhas que fogem deste guia, com o motivo. Não altere este guia: as
propostas de mudança vão nas notas.
