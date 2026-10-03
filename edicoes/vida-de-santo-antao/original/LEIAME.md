# Vida de Santo Antão, de Santo Atanásio: texto grego de trabalho e apoio latino

Arquivos:

- `vida.txt`: texto grego (base de tradução).
- `evagrio-latim.txt`: tradução latina de Evágrio (apoio).

UTF-8, cabeçalho `# chave: valor`, parágrafos separados por linha em branco. Nada foi traduzido.

**Aviso de direitos.** A digitação grega é do TLG (Thesaurus Linguae Graecae, Universidade da Califórnia em Irvine), que autorizou o DCO a publicá-la em seu site. Por isso o cabeçalho de `vida.txt` leva a nota exigida: «digitação do TLG hospedada no DCO; texto de Migne, PG 26 (Montfaucon); só para uso como base de tradução, não republicar».

## Fontes

1. **Grego**: `http://www.documentacatholicaomnia.eu/02g/0295-0373,_Athanasius,_Vita_Antonii,_MGR.pdf` (3.097.384 bytes, 97 páginas; TLG 2035 047). Guardado em `ferramentas/cache/vida-de-santo-antao/vita.pdf`; texto extraído com PyMuPDF em `vita_pymupdf.txt` (mesma pasta). O texto corrido ocupa as páginas 1 a 40; o resto do PDF é estatística de letras e índice de formas (concordância), descartado.
2. **Latim**: `https://la.wikisource.org/wiki/Vita_B._Antonii_abbatis` (versão 268597), guardado em `evagrio.html`. A página reproduz Migne, *Patrologia Latina* 73 (1849), tradução de Evágrio de Antioquia.

## O que o PDF do DCO tem e não tem

- Cada frase vem numerada pela contagem interna do TLG: `[00001]` a `[01385]` (1.385 «frases»). Essa numeração **não é a da obra**.
- As colunas da *Patrologia Graeca* aparecem como `[26.837]`, `[26.840]`, `[26.841]`, `[26.844]` ..., até `[26.976]`: 70 marcas, só em alguns pontos (em pares: 840-841, 844-845 etc.).
- **O PDF não traz numeração de capítulos.** Nem `[1]`, nem «Κεφ.», nada. O pedido supunha que traria. Veja a seção seguinte.
- O texto tem muitas palavras partidas no fim de linha do original digitado (`εὐχοµέ νων`, `ἀσκή σεως`).
- Letras erradas de codificação: `µ` (U+00B5, micro) no lugar do mu grego e `∆` (U+2206) no lugar do delta maiúsculo.

## Divisão em capítulos: reconstruída, não copiada

Como o PDF não traz capítulos, os marcadores `[0]` (prólogo, ΠΡΟΟΙΜΙΟΝ) e `[1]` a `[94]` (numeração de Montfaucon/PG, a das traduções modernas) **foram colocados por mim**, assim:

- Li as aberturas de 89 dos 94 capítulos da tradução inglesa de Ellershaw (NPNF II.4) em páginas da internet (New Advent, tertullian.org, Fordham, Catholic Library, LibreTexts, Early Church Texts), apenas consultadas por leitura, sem salvar no repositório. Cada abertura foi localizada no grego por leitura (o sentido da frase inicial, não palavra por palavra).
- Para os capítulos 73 a 77, cujas aberturas inglesas não consegui ler, usei um comentário em PDF (lectio-divina.org) que resume o assunto de cada seção, também só consultado.
- Conferências feitas: marcas em ordem crescente; texto reconstituído idêntico às 1.385 frases do TLG, letra por letra e ignorados os pontos finais (sem lacuna nem repetição); três inícios no meio de frase (ver abaixo).

**Grau de confiança.** Alta para quase todas. Mais frágeis (início escolhido por conteúdo, não por abertura inglesa literal): **34** (`Διὸ, κἂν ἀληθῆ ποτε...`), **75, 76 e 77** (`Περὶ δὲ τοῦ σταυροῦ...`, `Εἴπατε δὲ καὶ ὑμεῖς ἡμῖν τὰ ὑμέτερα`, `Ἐκείνων δὲ διαπορούντων...`). Se algum capítulo for começar uma frase antes ou depois, o erro é de uma frase.

**Falta a conferência com o PG 26.** O próprio volume está em `https://archive.org/details/patrologiae_cursus_completus_gr_vol_026` (arquivo `..._djvu.txt`, cerca de 8,3 MB), mas não o baixei porque não estava entre as fontes autorizadas. Com autorização, dá para conferir os 94 inícios em minutos.

Três capítulos começam no meio de uma «frase» do TLG, porque o ponto final se perdeu na digitação: **13** (`Οἱ δὲ πρὸς αὐτὸν ἐρχόμενοι...`), **22** (`Πρῶτον τοίνυν τοῦτο γινώσκωμεν...`) e **24** (`Καὶ φαίνεσθαι αὐτοὺς πολλάκις ἔλεγε...`). Nesses três pontos acrescentei o ponto final que faltava ao fim do capítulo anterior (12, 21, 23). É a única pontuação inserida por mim.

## O que foi limpo em `vida.txt`

- Retirados: cabeçalho do PDF (aviso do TLG/DCO), rodapés de página («Cooperatorum Veritatis Societas», «Excerpta ex Documenta Catholica Omnia», `n/97`), números de frase `[0000n]`, e tudo depois da última frase (`Ἀμήν.`).
- Caracteres: `µ`→`μ` (4.277 ocorrências), `∆`→`Δ` (43), apóstrofo ASCII `'` → `’` (325, nas elisões: `παρ’`, `ἀλλ’`), normalização Unicode NFC (o ano teleia U+0387 passa a `·` U+00B7; o ponto de interrogação grego U+037E passa a `;`).
- Marcas da PG uniformizadas para `{PG 26.837}`; as 70 estão no texto, em ordem crescente. Quando a coluna muda no meio de uma palavra, a marca fica antes da palavra inteira.
- **Palavras partidas**: reuni 646. Primeira passada: 623 (591 pela heurística, 32 decididos à mão); depois, 23 achadas por conferências de ortografia e de contexto. A heurística usa as regras de acentuação grega (um token sem acento que não seja átono ou enclítico é fragmento; a junção só vale se der palavra com um acento em posição possível), o vocabulário do próprio texto e leitura dos casos duvidosos. As conferências posteriores procuraram palavras que começam com ρ sem espírito, terminam em consoante impossível ou formam par de juntada válida. Não há léxico: **podem restar poucas palavras partidas ou mal juntas**, sobretudo as de formas átonas ou enclíticas.
- O texto de cada capítulo foi unido num só parágrafo (não há marca de parágrafo na fonte). O título está sozinho no começo (primeiro parágrafo, sem marca).

## Contagens

| arquivo | palavras | observação |
|---|---:|---|
| vida.txt | 18.400 | título + prólogo + 94 capítulos (96 parágrafos); 70 marcas PG; 1.385 frases TLG |
| evagrio-latim.txt | 16.828 | 62 capítulos do latim (ver abaixo); 169 marcas de coluna da PL |

(Palavras por separação de espaços, sem cabeçalho, sem marcas `[n]`, `{PG ...}`, `{PL ...}`, `{p. n}`.)

## Problemas encontrados no grego (não corrigidos)

1. Leituras suspeitas do TLG: no cap. 65, `ἐξ έστω λόγον ποιῆσαι` (letra `έ` com tonos solto, sem sentido claro); no cap. 87, `οὐκ ἐγαληνία τῇ διανοίᾳ` (provável `ἐν γαληνίᾳ`).
2. Dois `«` soltos, sem fechamento, no começo das frases `Οὐκ ἐγὼ δὲ, ἀλλ’ ἡ χάρις...` (cap. 5) e `Τέλος γοῦν...` (cap. 6). Marcas de citação do TLG.
3. Pontuação ausente em outros pontos (ex.: `ὁδούς οἱ δὲ ἐπέμενον`, cap. 84).
4. Lugares onde a edição do TLG e a PG podem diferir: não conferi.
5. As citações bíblicas e os discursos não têm aspas na maior parte.

## Latim de Evágrio (`evagrio-latim.txt`)

- Conteúdo: prólogo de Evágrio a Inocêncio, prefácio de Atanásio, 62 capítulos, epílogo de Evágrio.
- **A numeração de capítulos é a de Migne, PL 73 (`CAP. I` a `LXII`), que NÃO coincide com os 94 capítulos do grego** nem com as traduções modernas. Está marcada `[I]` ... `[LXII]`. Use-a como apoio de leitura, não como chave de alinhamento.
- Marcas: `{PL 73.0127A}` é a coluna e subdivisão da PL; `{p. 35}` é um número que a página-fonte intercala (35 a 60, falta o 52) e que vem da edição que Migne reproduz (não identificada na página).
- O rótulo «CAP. LVII» está errado na página-fonte (`LXVII`); corrigido.
- Foram mantidas as referências bíblicas entre parênteses, que são de Migne. Retirados: a faixa de navegação do Wikisource e o resto «(no ap» no fim da página.
- Wikisource transcreve sem aparato crítico; erros de digitação da página podem existir.
