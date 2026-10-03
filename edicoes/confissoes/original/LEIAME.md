# Confissões, de Santo Agostinho: texto latino de trabalho

Arquivos: `livro-01.txt` a `livro-13.txt`. UTF-8, cabeçalho `# chave: valor`, parágrafos separados por linha em branco. Nada foi traduzido.

## Fonte e edição

- Fonte: The Latin Library, `http://www.thelatinlibrary.com/augustine/conf1.shtml` a `conf13.shtml`. As páginas brutas estão em `ferramentas/cache/confissoes/conf1.html` a `conf13.html`.
- Edição: o texto do Latin Library é o de **James J. O'Donnell** (edição de Oxford, 1992), cedido pelo próprio O'Donnell, como consta no rodapé de cada página («Submitted by James J. O'Donnell (Univ. of Pennsylvania) from his new edition»). **Não é o texto de Knöll.** Convém decidir se isso serve ao projeto: o latim de Agostinho é domínio público, mas a recensão de O'Donnell é obra editorial moderna.
- Características do texto da página: quase tudo em minúsculas (maiúsculas só em nomes próprios), `u`/`v` e `i` como o Latin Library os grafa (`venire`, `iam`), pontuação de O'Donnell.

## Convenção das marcas

O Latin Library numera cada parágrafo como `livro.capítulo.seção` (ex.: `1.20.31`). A seção é contínua ao longo do livro. Cada parágrafo começa com `[capítulo em romano.seção em arábico]`:

- `1.1.1` vira `[I.1]`; `1.20.31` vira `[XX.31]`; `7.1.2` vira `[I.2]`.
- O número do livro fica no nome do arquivo e no cabeçalho.
- Os totais por livro (tabela abaixo) são os habituais da obra (20, 10, 12, 16, 14, 16, 21, 12, 13, 43, 31, 32 e 38 capítulos; 31, 18, 21, 31, 25, 26, 27, 30, 37, 70, 41, 43 e 53 seções); não foram conferidos capítulo a capítulo com o CSEL. Verificação feita nos arquivos: numeração das seções contínua de 1 a n em cada livro, capítulos em ordem crescente, nenhuma seção sem texto.

## O que foi limpo

- Cabeçalho da página (`AUGUSTINI CONFESSIONUM LIBER ...`), filetes, linha de crédito de O'Donnell, tabela de navegação e rodapé.
- O texto «commentary on 1.11.17» que ficou colado ao número do parágrafo `1.11.17`.
- Espaços e quebras de linha colapsados em parágrafos corridos.
- Entidades HTML da página: `&#134;` virou `†` (cruz de texto corrompido; duas ocorrências em `[XIV.23]` do livro 1) e `&#151;` virou `—` (livro 2: `[II.3]` e `[VI.12]`; livro 3: `[VI.11]`; livro 4: `[XIII.20]`).
- Livro 9, seção 32 (hino de Ambrósio, «deus, creator omnium»): os oito versos estão num parágrafo próprio, um verso por linha, sem marca (é continuação da seção `[XII.32]`). Foram descartados dois restos de HTML da página (`<` solto e uma aspa solta). **Atenção:** a página não traz a aspa de abertura do primeiro verso, e eu não a inventei.
- Aspas e parênteses da página foram mantidos como estão.

## Contagens

Palavras por arquivo (separação por espaços; marcas `[...]` e cabeçalho excluídos):

| arquivo | palavras | capítulos | seções |
|---|---:|---:|---:|
| livro-01.txt | 5.178 | 20 | 31 |
| livro-02.txt | 2.763 | 10 | 18 |
| livro-03.txt | 3.890 | 12 | 21 |
| livro-04.txt | 5.054 | 16 | 31 |
| livro-05.txt | 4.676 | 14 | 25 |
| livro-06.txt | 5.399 | 16 | 26 |
| livro-07.txt | 5.937 | 21 | 27 |
| livro-08.txt | 5.626 | 12 | 30 |
| livro-09.txt | 6.014 | 13 | 37 |
| livro-10.txt | 11.605 | 43 | 70 |
| livro-11.txt | 6.757 | 31 | 41 |
| livro-12.txt | 7.235 | 32 | 43 |
| livro-13.txt | 8.658 | 38 | 53 |
| **total** | **78.792** | | |

## Conferência com CSEL 33 (Knöll, 1896)

Fonte da conferência: `https://archive.org/details/sanctiaureliaugu33augu`, arquivo `sanctiaureliaugu33augu_djvu.txt` (1,1 MB), guardado em `ferramentas/cache/confissoes/csel33_djvu.txt`. O texto do Latin Library **não foi substituído** nem alterado com base nele.

Método: o OCR traz, em cada página, texto, números de linha, referências bíblicas e aparato crítico. Um script isolou o texto corrido (descarte de linhas de aparato, cabeçalhos e números), juntou as palavras hifenizadas no fim de linha, normalizou `v`→`u` e `j`→`i` e contou as palavras de cada livro. O número do livro 2 não aparece no OCR; o início foi achado pelas primeiras palavras. Os números abaixo são contagens de palavras alfabéticas (um pouco diferentes das contagens por espaços da tabela acima).

| livro | Latin Library | CSEL 33 (OCR filtrado) | diferença | 4-gramas do LL achados no CSEL |
|---|---:|---:|---:|---:|
| 1 | 5.175 | 5.169 | -0,12% | 90,4% |
| 2 | 2.761 | 2.744 | -0,62% | 91,6% |
| 3 | 3.889 | 3.835 | -1,39% | 88,1% |
| 4 | 5.053 | 5.054 | +0,02% | 91,4% |
| 5 | 4.676 | 4.687 | +0,24% | 90,2% |
| 6 | 5.398 | 5.356 | -0,78% | 90,0% |
| 7 | 5.934 | 5.972 | +0,64% | 89,9% |
| 8 | 5.625 | 5.643 | +0,32% | 89,9% |
| 9 | 6.014 | 6.028 | +0,23% | 90,5% |
| 10 | 11.604 | 11.607 | +0,03% | 89,7% |
| 11 | 6.755 | 6.746 | -0,13% | 93,6% |
| 12 | 7.232 | 7.229 | -0,04% | 91,6% |
| 13 | 8.655 | 8.672 | +0,20% | 89,3% |
| total | 78.771 | 78.742 | -0,04% | |

**Nenhum livro diverge mais de 5%** (o maior desvio é o do livro 3, -1,39%). Não há capítulos ou seções ausentes. Como os dois textos não são a mesma edição, cerca de 10% dos 4-gramas não coincidem: grafia (CSEL escreve `inconmutabiliter`, `conmutabili`; O'Donnell, `incommutabiliter`, `commutabili`), pontuação, algumas lições (em 13.16.19, `quoniam es` no CSEL contra `qui es` no Latin Library) e erros do OCR. Duas seções ficaram com menos de 70% de coincidência de 4-gramas: 10.27.38 (60%) e 13.16.19 (57%). Conferidas à vista, o texto é o mesmo; a queda vem de variantes ortográficas e de linhas que o filtro do OCR perdeu.

## Problemas encontrados

1. O texto-base é o de O'Donnell, não o de Knöll (ver acima).
2. O Latin Library não tem capitalização de início de frase; a pontuação é a de O'Donnell e não a de CSEL. Isso afeta só a leitura, não o conteúdo.
3. Cruz (`†`) em `[XIV.23]` do livro 1: sinal de passo corrompido na edição de O'Donnell; o tradutor deve decidir como tratá-lo.
4. A tabela de conferência depende de heurística sobre OCR; serve para detectar omissões grosseiras (não há nenhuma), não para estabelecer lições.
