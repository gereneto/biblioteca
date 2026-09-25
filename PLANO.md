# Plano: a obra de Machado de Assis, livro por livro

Cada livro passa pelo mesmo processo de _Dom Casmurro_ (ver `ferramentas/README.md`):

1. **Edição-base**: a última edição publicada em vida do autor, quando ela existe em
   transcrição ou fac-símile; senão, a 1ª edição, completada pelas lições que toda a
   tradição posterior atesta (sinal de que vêm da edição revista).
2. **Confronto** de todas as transcrições digitais dessa edição, palavra por palavra;
   o fac-símile decide as dúvidas.
3. **Correção** apenas dos erros tipográficos evidentes, cada um registrado.
4. **Ortografia** atualizada pelo Acordo de 1990, e formas antigas de palavras atuais
   trocadas pela de hoje (_cousa_ → coisa, _dous_ → dois); sem tocar em vocabulário,
   colocação pronominal, mesóclises nem pontuação do autor.
5. **Divisão** do livro respeitada: capítulos nos romances, contos nas coletâneas,
   poemas nos livros de versos.
6. Página **Sobre esta edição** com a lista completa das intervenções.

As decisões de cada livro ficam em `edicoes/<obra>/`.

## Escopo e ordem de trabalho

Só romances, contos e poesia (sem teatro, traduções nem obra dispersa). Primeiro os
romances, da maturidade para a juventude; depois as coletâneas de contos; por fim, a poesia.
Das coletâneas que misturam gêneros (_Páginas Recolhidas_, _Relíquias de Casa Velha_),
entram só os contos.

## Bibliografia

Legenda das fontes: **PG** Projeto Gutenberg · **WS** Wikisource (fac-símile com transcrição
página a página) · **MDN** machadodeassis.net, da Fundação Casa de Rui Barbosa (texto moderno,
Acordo de 1990) · **MEC** Obra Completa, Nova Aguilar, 1994 (texto moderno).

### Romances

| # | Obra | 1ª edição | Revista em vida | Transcrições | Moderno | Situação |
|---|------|-----------|-----------------|--------------|---------|----------|
| 1 | _Dom Casmurro_ | 1899, Garnier | 2ª ed. 1900 (não digitalizada) | PG 55752 · WS · Stolfi | MDN 11503 · MEC | **publicado** |
| 2 | _Memórias Póstumas de Brás Cubas_ | 1881, Tip. Nacional (antes na _Revista Brasileira_, 1880) | «3ª ed.» 1896, Garnier, revista, com prólogo (fac-símile BBM 7815, só OCR); «4ª ed.» 1899 (não digitalizada) | PG 54829 (1881) · WS (1881, parcial) · OCR de 1896 | MDN 5985 · MEC · Câmara | **publicado** (base 1896) |
| 3 | _Quincas Borba_ | 1891, Garnier, com errata (antes em _A Estação_, 1886–1891) | 2ª ed. 1896, muito revista; 3ª ed. 1899, com prólogo (nenhuma digitalizada) | PG 55682 (1891) · WS (1891, parcial) · OCR BBM 5251 | MDN 8340 · MEC · Objetivo (= Aguilar) | **publicado** (1891 + lições da edição revista) |
| 4 | _Esaú e Jacó_ | 1904, Garnier | — | PG 56737 · WS (1904) | MDN 13998 · MEC | a fazer |
| 5 | _Memorial de Aires_ | 1908, Garnier | — | PG 55797 (1908) · WS (1908) | MDN 16866 · MEC | a fazer |
| 6 | _Iaiá Garcia_ | 1878, G. Vianna (antes em _O Cruzeiro_) | 2ª ed. 1898 | PG 67780 (reimpr. 1919) · WS (1878) | MDN 4304 · MEC | a fazer |
| 7 | _Helena_ | 1876, Garnier (antes em _O Globo_) | 2ª ed. 1905, com advertência | PG 67162 (1876) · WS (1876) | MDN 2554 · MEC | a fazer |
| 8 | _A Mão e a Luva_ | 1874, Gomes de Oliveira (antes em _O Globo_) | 2ª ed. 1907, com advertência | PG 53101 (reimpr. 1919 do texto de 1907) · WS (1874, incompleto) | MDN 1434 · MEC | a fazer |
| 9 | _Ressurreição_ | 1872, Garnier | 2ª ed. 1905, com advertência | WS (1872) | MDN 2 · MEC | a fazer |

### Contos

| # | Obra | 1ª edição | Transcrições | Moderno | Situação |
|---|------|-----------|--------------|---------|----------|
| 10 | _Papéis Avulsos_ | 1882, Lombaerts | PG 57001 (1882) · WS (1882) | MDN (conto a conto) · MEC | a fazer |
| 11 | _Histórias sem Data_ | 1884, Garnier | PG 33056 · WS (1884) | MDN · MEC | a fazer |
| 12 | _Várias Histórias_ | 1896, Laemmert | WS (1896) | MDN · MEC | a fazer |
| 13 | _Páginas Recolhidas_ | 1899, Garnier | WS (1899) | MDN (contos) · MEC | a fazer |
| 14 | _Relíquias de Casa Velha_ | 1906, Garnier | PG 67935 (reimpr.) · WS (1906) | MDN (contos) · MEC | a fazer |
| 15 | _Histórias da Meia-Noite_ | 1873, Garnier | WS (1873) | MDN · MEC | a fazer |
| 16 | _Contos Fluminenses_ | 1870, Garnier | WS (1870) | MDN · MEC | a fazer |

### Poesia

| # | Obra | 1ª edição | Transcrições | Moderno | Situação |
|---|------|-----------|--------------|---------|----------|
| 17 | _Poesias Completas_ (_Crisálidas_, _Falenas_, _Americanas_ revistas e o inédito _Ocidentais_) | 1901, Garnier | PG 61653 (1901) · WS (1901) | MEC | a fazer |
| 18 | _Crisálidas_ (versão original) | 1864, Garnier | WS (1864) | MEC | a fazer |
| 19 | _Falenas_ (versão original) | 1870, Garnier | WS (1870) | MEC | a fazer |
| 20 | _Americanas_ (versão original) | 1875, Garnier | WS (1875) | MEC | a fazer |
