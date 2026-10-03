# Ortodoxia, de G. K. Chesterton: texto inglês de trabalho

Arquivos: `prefacio.txt` e `capitulo-1.txt` a `capitulo-9.txt`. UTF-8, cabeçalho `# chave: valor`, parágrafos separados por linha em branco. Nada foi traduzido.

## Fonte e edição

- Fonte: Project Gutenberg, eBook nº 130, `https://www.gutenberg.org/ebooks/130.txt.utf-8` (texto simples). Bruto em `ferramentas/cache/ortodoxia/gutenberg130.txt`.
- Edição: *Orthodoxy* (1908), na digitação do Project Gutenberg. O arquivo **não diz qual impressão serviu de base**. A grafia é americana (`civilization`, `gray`, `emphasize`, `recognized`).
- Conferência: `https://archive.org/details/orthodoxy00chesuoft`, arquivo `orthodoxy00chesuoft_djvu.txt` (426 KB), em `ferramentas/cache/ortodoxia/orthodoxy1908_djvu.txt`. **Esse scan não é a edição de 1908**, e sim uma reimpressão tardia da The Bodley Head, Londres (a folha de rosto lista reimpressões até 1957; exemplar da Leonard Library, Wycliffe College, Toronto). Grafia britânica (`civilisation`, `grey`, `emphasise`).
- Além dos arquivos pedidos, baixei `gutenberg130.html` (versão HTML do Gutenberg, `cache/epub/130/pg130-images.html`) só para ver se havia itálicos; não havia (ver abaixo). Fica no cache, ignorado pelo git.

## O que foi limpo

- Retirados: cabeçalho e licença do Gutenberg (tudo antes de `*** START` e depois de `*** END`), título e índice, a linha de título de cada capítulo (que passou para o cabeçalho de cada arquivo).
- Linhas quebradas a 70 colunas juntadas em parágrafos corridos; o recuo de 5 espaços do Gutenberg foi descartado. Cada bloco separado por linha em branco virou um parágrafo; os blocos sem recuo (citações em bloco e a retomada depois delas) ficaram como parágrafos próprios.
- Espaços duplos depois de ponto e outros excessos de espaço colapsados em um espaço.
- Texto mantido tal como está no mais: aspas retas, aspas internas com crase e apóstrofo (`` `Hanwell' ``), `--` como travessão, `Mr. G.S.Street`.
- Os versos citados (os de Arnold no cap. 5, «Ride on the crest of the dishevelled tide...» no cap. 4 e os de Swinburne no cap. 8) vêm corridos na prosa, sem quebra de verso, porque assim estão no Gutenberg. Nos do cap. 4 e do cap. 8 o Gutenberg separava os versos com seis espaços, que foram colapsados como os demais; nos de Arnold nem isso.
- O livro não tem numeração interna de parágrafos; por isso não há marcas `[n]` nos arquivos. O número do capítulo está no nome do arquivo e no cabeçalho.

## Itálicos

O texto simples do Gutenberg nº 130 **não marca nenhum itálico** (não há um só `_` no arquivo), e a versão HTML também não tem `<i>` nem `<em>`. Logo não há `_assim_` em nenhum arquivo. Os itálicos de Chesterton só podem ser recuperados de uma edição impressa ou de outra transcrição. O OCR do scan não os marca.

## Contagens

| arquivo | palavras | parágrafos |
|---|---:|---:|
| prefacio.txt | 207 | 2 |
| capitulo-1.txt | 1.887 | 7 |
| capitulo-2.txt | 6.737 | 20 |
| capitulo-3.txt | 6.366 | 27 |
| capitulo-4.txt | 8.511 | 34 |
| capitulo-5.txt | 6.488 | 26 |
| capitulo-6.txt | 8.757 | 32 |
| capitulo-7.txt | 9.369 | 38 |
| capitulo-8.txt | 6.858 | 27 |
| capitulo-9.txt | 8.524 | 27 |
| **total** | **63.704** | |

(Palavras por separação de espaços, sem o cabeçalho. O prefácio tem dois blocos: o texto e a assinatura «Gilbert K. Chesterton.».)

## Conferência com o scan

Método: o OCR foi dividido nos nove «CHAPTER ...»; retirei cabeçalhos correntes e números de página, juntei as palavras hifenizadas e comparei, capítulo a capítulo, as sequências de palavras (difflib).

| capítulo | OCR | Gutenberg | diferença |
|---|---:|---:|---:|
| 1 | 1.900 | 1.893 | +0,37% |
| 2 | 6.782 | 6.760 | +0,33% |
| 3 | 6.411 | 6.391 | +0,31% |
| 4 | 8.573 | 8.555 | +0,21% |
| 5 | 6.576 | 6.522 | +0,83% |
| 6 | 8.805 | 8.786 | +0,22% |
| 7 | 9.471 | 9.412 | +0,63% |
| 8 | 6.918 | 6.889 | +0,42% |
| 9 | 8.583 | 8.574 | +0,10% |

(Contagens por palavras alfabéticas; a pequena sobra do OCR vem de cabeçalhos correntes que escaparam ao filtro e de palavras quebradas.)

**Os nove capítulos estão completos**, do primeiro ao último parágrafo («... it was His mirth.»); não há trecho ausente nem acrescentado. Diferenças de extensão: nenhuma acima de 1%.

Diferenças de conteúdo entre o scan e o Gutenberg:

- O **prefácio** («This book is meant to be a companion to "Heretics"...») está no Gutenberg e **não está no scan**; o scan tem a dedicatória «To my mother», que o Gutenberg **não traz**.
- Grafia: americana no Gutenberg, britânica no scan; compostos soltos ou ligados diferentes (`cross roads`/`cross-roads`, `any one`/`anyone`).
- Variantes de palavra (excluídos os erros evidentes de OCR). O Gutenberg parece errado nos itens marcados com *:
  - II: `free to praise, to curse` (scan) / `free to raise, to curse` (PG)*; `goes mad the man who begins to think` (scan) / `goes mad he begins to think` (PG)*, onde o PG omite palavras.
  - III: `prostration` / `prostrations`.
  - IV: `that the philanthropic old men` / `that these philanthropic old men`; `Mr. Yeats read into elfland` / `reads`; `it is vast` / `it was vast`.
  - V: `throne of the mystic` / `throne or the mystic`*; `liberal and human` / `liberal and humane`.
  - VI: `Coeur de Lion` / `Coeur de Leon`; `rose in a high and strange` / `rose into a high and strange`; `that is what makes Christendom` / `this is what makes Christendom`.
  - VII: `the materials for a world` / `the material for a world`; `Cunningham Grahame` (scan) / `Cunninghame Grahame` (PG, correto); `not daring to stir` / `nor daring to stir`*.
  - VIII: `the doctrine of one of them` / `the discovery of one of them`; `as of divine love` / `as a divine love`*.
  - IX: `Christ has even a literary style` / `Christ had even`; `upon human evidence` / `human evidences`; `spiritualist incidents` / `spiritualistic incidents`; `privilege of woman` / `privilege of women`; `entered at least the gate` / `entered at last the gate`.
- Pontuação e hifenização também diferem em dezenas de lugares (o scan usa `to-morrow`, `dullness`; o Gutenberg `to morrow`, `dulness`). Não as listei.

## Problemas encontrados

1. Nenhum itálico disponível (ver acima).
2. O Gutenberg não identifica a impressão que digitou; o scan do archive.org é uma reimpressão de 1957 ou posterior, e não a primeira edição. A conferência prova a integridade do texto, não a fidelidade ao exemplar de 1908.
3. Os itens com asterisco acima parecem erros do Gutenberg; não os corrigi, por instrução de não substituir o texto-base. Convém decidir antes de traduzir o capítulo 2 (a omissão de «the man who»).
4. Versos citados sem quebra de verso (ver acima).
