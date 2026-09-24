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
3. **Intervenções** (`edicoes/<obra>/decisoes.py`, `EMENDAS`): erros tipográficos da
   edição-base (`erro`), lições da tradição posterior (`edicao`) e erros das
   transcrições (`ocr`). Tudo na grafia da edição-base.
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
