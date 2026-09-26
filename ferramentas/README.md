# Ferramentas: estabelecimento dos textos

Python 3 puro (sem dependências), mais `pdftotext` para fontes em PDF e Pillow para
recortar o fac-símile na conferência.

```bash
python ferramentas/texto.py dom-casmurro              # confronta e grava relatórios
python ferramentas/texto.py dom-casmurro --publicar   # e grava conteudo/<autor>/<obra>.js
python ferramentas/texto.py dom-casmurro --rebaixar   # ignora o cache das fontes
```

As fontes baixadas e os relatórios ficam em `ferramentas/cache/<obra>/` (fora do git).

## O método

1. **Fontes** (`edicoes/<obra>/config.py`): as transcrições da edição-base (Projeto
   Gutenberg, Wikisource, outras) e as edições modernas (machadodeassis.net, Aguilar/MEC,
   NUPILL...). Leitores prontos em `edicao/fontes.py`.
2. **Confronto** (`edicao/estabelecer.py`): as transcrições são alinhadas palavra por
   palavra. Diferenças só de grafia miúda não contam. Nas outras, vale a maioria; sem
   maioria (ou quando a maioria vem do mesmo OCR), vale a leitura apoiada pelas edições
   modernas. O relatório `sitios.tsv` lista as escolhas fracas, para conferir no
   fac-símile (`edicao/fac_simile.py`).
   - **Lacunas**: um testemunho pode faltar em trechos (páginas não revisadas do
     Wikisource: `wikisource(..., qualidade_minima=3)`); ali ele não vota.
   - **Edição-base só em OCR** (`RUIDOSO` no config; ex.: _Brás Cubas_, base 1896 com
     transcrições de 1881): quando nenhuma leitura tem apoio moderno e o OCR aponta para
     a das modernas, vale esta; e uma segunda passada (`revisar_pelo_ruidoso`) compara o
     texto com a moderna principal e adota as passagens que o OCR confirma (capítulos
     reescritos, cortes). Tudo vai para `revisoes.tsv`.
   - **Edição revista só nas modernas** (`TRADICAO` no config; ex.: _Quincas Borba_, base
     1891 e revisão de 1896 não digitalizada): onde todas as edições modernas concordam
     contra o texto em palavras (não só em grafia ou abreviatura), vale a leitura delas; o
     mesmo para a pontuação (sem aspas nem hífens). Cada troca vai para a página «Sobre
     esta edição».
   - **Vários OCRs do mesmo impresso** (ex.: _Esaú e Jacó_, dois exemplares da Brasiliana):
     `ocr.paragrafos_como` dá a eles os parágrafos da base (o OCR junta falas de diálogo);
     `CORRELACIONADOS` + `UM_VOTO = True` fazem os OCRs aparentados valerem um voto;
     `DESEMPATE_LEXICO = True` desempata, sem apoio moderno, pela leitura sem palavras
     inexistentes nas edições modernas (e compara o contexto tolerando a grafia antiga).
   - O itálico só é votado pelos testemunhos que o marcam (o OCR não marca).
3. **Intervenções** (`edicoes/<obra>/decisoes.py`, `EMENDAS`): erros tipográficos da
   edição-base (`erro`), lições da tradição posterior (`edicao`), erros das
   transcrições (`ocr`) e lições da edição-base conferidas no fac-símile que o confronto
   perdeu (`revisao`). Tudo na grafia do texto-base; trechos longos como
   `'começo […] fim'`.
4. **Grafia** (`edicao/modernizar.py`): cada palavra recebe a grafia da edição de
   referência (o machadodeassis.net já segue o Acordo de 1990; o Aguilar é convertido),
   só quando é a mesma palavra. Formas do autor que a língua ainda registra (_cousa_,
   _dous_) não mudam. O que sobra vai para `sem_par.tsv` e se resolve em `MANUAL`.
5. **Ajustes** (`AJUSTES`): pontuação atestada por toda a tradição posterior, acentos
   de locuções, leituras restauradas.
6. **Itálico** por votação entre as transcrições; **versos** e títulos em `VERSOS` e
   `TITULOS`.
7. **Relatórios** para a revisão: `modernas.tsv` (palavras em que o texto difere das
   edições modernas: erros a corrigir ou lições de edição revista), `pontuacao.tsv`
   (pontuação em que todas as modernas concordam contra o texto), `vocabulario.tsv`
   (palavras ausentes de todas as modernas: resíduo de OCR?) e `texto.txt` (o texto
   final corrido).

## Acrescentar uma obra

Copie `edicoes/dom-casmurro/` para `edicoes/<obra>/`, ajuste `config.py` (metadados e
fontes), rode o confronto, leia os relatórios e registre as decisões em `decisoes.py`
e `notas.py`. Repita até os relatórios só mostrarem escolhas conscientes; então publique.
Em `notas.py`, `BASE` e `SECOES` trocam os rótulos das tabelas da página «Sobre esta
edição» quando a edição-base não é a primeira (ver _Brás Cubas_).
