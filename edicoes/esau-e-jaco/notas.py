"""Esaú e Jacó — texto da página «Sobre esta edição»."""

COMENTARIO = '''Esaú e Jacó — Machado de Assis
   Gerado por ferramentas/texto.py a partir de edicoes/esau-e-jaco/.
   Não edite à mão: corrija as decisões nessa pasta e rode de novo com --publicar.

   Formato do texto de cada parte:
     - parágrafos separados por uma linha em branco;
     - _itálico_ entre sublinhados;
     - linhas começadas por "| " formam um bloco de versos (ou inscrição), uma linha por verso.'''

APRESENTACAO = '''**Texto-base.** Este texto reproduz a primeira e única edição publicada em vida do autor (Rio de Janeiro e Paris, H. Garnier, 1904, com o título _Esaú e Jacob_). Foi estabelecido palavra por palavra a partir da transcrição do Projeto Gutenberg e da leitura automática (OCR) de dois exemplares digitalizados pela Brasiliana USP. Os dois OCRs erram do mesmo modo e valem um voto só; onde discordam do Gutenberg, decidiu o apoio das edições modernas, e os casos duvidosos foram conferidos no fac-símile. O último capítulo, que falta no Gutenberg, foi transcrito do fac-símile.

**Correções.** A edição de 1904 tem muitos erros tipográficos: palavras repetidas, letras trocadas, concordâncias quebradas («Nativividade», «Provalmente», «as mariposas e as ratos»). Corrigiram-se os evidentes, listados abaixo. Onde a leitura de 1904 faz sentido, ficou, ainda que as edições modernas a emendem.

**Ortografia.** A grafia foi atualizada pelo Acordo Ortográfico de 1990 (_Jacob_ → Jacó, _Ayres_ → Aires, _elle_ → ele). As formas antigas de palavras que continuam em uso passaram à forma atual (_cousa_ → coisa, _dous_ → dois). O vocabulário e as construções do autor ficaram como estão — as mesóclises, a colocação dos pronomes, os travessões e as aspas angulares, os itálicos e as abreviaturas _S._ (São), _D._ (Dona) e _V. Ex._ (Vossa Excelência).

**Divisão.** O livro tem 121 capítulos curtos, numerados em romanos e titulados, precedidos da «Advertência». A epígrafe de Dante abre o primeiro capítulo, como no livro. Cada capítulo é uma página desta biblioteca.'''

BASE = 'Edição de 1904'

SECOES = {
    'erros': {'titulo': 'Erros tipográficos da edição de 1904 corrigidos',
              'explica': 'Grafia de 1904 nas duas colunas.'},
    'mantidas': {'titulo': 'Lições de 1904 mantidas',
                 'explica': 'Pontos em que as edições modernas leem diferente.'},
}

FONTES = [
    {'nome': 'Fac-símile da edição de 1904 (Brasiliana USP)', 'url': 'https://digital.bbm.usp.br/handle/bbm/4763',
     'nota': 'texto-base; OCR usado no confronto; último capítulo transcrito daqui'},
    {'nome': 'Fac-símile da edição de 1904, outro exemplar (Brasiliana USP)', 'url': 'https://digital.bbm.usp.br/handle/bbm/7817',
     'nota': 'OCR usado no confronto'},
    {'nome': 'Projeto Gutenberg, nº 56737', 'url': 'https://www.gutenberg.org/ebooks/56737',
     'nota': 'transcrição da edição de 1904, grafia original (sem o cap. CXXI)'},
    {'nome': 'machadodeassis.net (Fundação Casa de Rui Barbosa)', 'url': 'https://machadodeassis.net/texto/esau-e-jaco/13998',
     'nota': 'texto moderno; referência para a ortografia'},
    {'nome': 'Obra Completa, Nova Aguilar, 1994 (MEC / Domínio Público)', 'url': 'https://archive.org/details/esauJaco',
     'nota': 'texto moderno'},
    {'nome': 'Biblioteca Virtual do Estudante (USP) / Curso Objetivo', 'url': 'https://www.curso-objetivo.br/vestibular/assets/download/obras-literarias/machado-de-assis/esau-e-jaco.pdf',
     'nota': 'outra digitação do texto do Aguilar'},
]

# (trecho do texto final, leitura de outras edições, observação)
MANTIDAS = [
    ('depois de reler as palavras do irmão', 'reter', ''),
    ('Santos cumpriu tudo à risca', 'cumpriu à risca', ''),
    ('ambos sorriram de fé', 'sorriam', ''),
    ('Via, ouvia, corria', 'sorria', ''),
    ('É uma felicidade que o Batista', 'esperança', ''),
    ('a pobre retina de moça', 'da moça', ''),
    ('documentos do século XVII', 'XVIII', ''),
    ('os pés não saíam de chão', 'do chão', ''),
]

ERROS_ANTERIORES = []
