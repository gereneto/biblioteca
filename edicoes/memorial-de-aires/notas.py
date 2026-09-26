"""Memorial de Aires — texto da página «Sobre esta edição»."""

COMENTARIO = '''Memorial de Aires — Machado de Assis
   Gerado por ferramentas/texto.py a partir de edicoes/memorial-de-aires/.
   Não edite à mão: corrija as decisões nessa pasta e rode de novo com --publicar.

   Formato do texto de cada parte:
     - parágrafos separados por uma linha em branco;
     - _itálico_ entre sublinhados;
     - linhas começadas por "| " formam um bloco de versos (ou inscrição), uma linha por verso.'''

APRESENTACAO = '''**Texto-base.** Este texto reproduz a primeira e única edição publicada em vida do autor (Rio de Janeiro e Paris, H. Garnier, 1908, com o título _Memorial de Ayres_), saída meses antes da morte de Machado de Assis. Foi estabelecido palavra por palavra a partir da transcrição do Projeto Gutenberg e da leitura automática (OCR) de dois exemplares: um digitalizado pela Brasiliana USP, outro microfilmado e publicado no Internet Archive. O Gutenberg foi feito sobre o OCR do microfilme e herda parte dos erros dele; por isso os dois contam como um voto só. Onde os testemunhos divergem, decidiu o apoio das edições modernas, e os casos duvidosos foram conferidos no fac-símile.

**A advertência.** A «Advertência» do autor falta no Gutenberg e no microfilme; foi transcrita do exemplar da Brasiliana.

**Correções.** Corrigiram-se os erros tipográficos evidentes da edição de 1908 (letras trocadas, palavras e artigos faltando), listados abaixo. Onde a leitura de 1908 faz sentido, ficou, ainda que as edições modernas a emendem.

**Ortografia.** A grafia foi atualizada pelo Acordo Ortográfico de 1990 (_Ayres_ → Aires, _Fidelia_ → Fidélia, _elle_ → ele). As formas antigas de palavras que continuam em uso passaram à forma atual (_cousa_ → coisa, _dous_ → dois). As duas epígrafes, cantigas medievais, ficaram na grafia antiga, como o autor as citou. O vocabulário e as construções do autor ficaram como estão — as mesóclises, a colocação dos pronomes, os travessões e as aspas angulares, os itálicos e as abreviaturas _S._ (São), _D._ (Dona) e _V. Ex._ (Vossa Excelência).

**Divisão.** O memorial é um diário de 1888 e 1889. Cada entrada — uma data ou uma hora anotada — é uma página desta biblioteca, com o ano acima. As epígrafes abrem a primeira entrada.'''

BASE = 'Edição de 1908'

SECOES = {
    'erros': {'titulo': 'Erros tipográficos da edição de 1908 corrigidos',
              'explica': 'Grafia de 1908 nas duas colunas.'},
    'mantidas': {'titulo': 'Lições de 1908 mantidas',
                 'explica': 'Pontos em que as edições modernas leem diferente.'},
}

FONTES = [
    {'nome': 'Fac-símile da edição de 1908 (Brasiliana USP)', 'url': 'https://digital.bbm.usp.br/handle/bbm/4707',
     'nota': 'exemplar com dedicatória do autor; OCR usado no confronto; advertência transcrita daqui'},
    {'nome': 'Microfilme da edição de 1908 (Internet Archive)', 'url': 'https://archive.org/details/3438833',
     'nota': 'OCR usado no confronto'},
    {'nome': 'Projeto Gutenberg, nº 55797', 'url': 'https://www.gutenberg.org/ebooks/55797',
     'nota': 'transcrição da edição de 1908, grafia original (sem a advertência)'},
    {'nome': 'machadodeassis.net (Fundação Casa de Rui Barbosa)', 'url': 'https://machadodeassis.net/texto/memorial-de-aires/16866',
     'nota': 'texto moderno; referência para a ortografia'},
    {'nome': 'Obra Completa, Nova Aguilar, 1994 (MEC / Domínio Público)', 'url': 'https://archive.org/details/memorialAires',
     'nota': 'texto moderno'},
    {'nome': 'Biblioteca Virtual do Estudante (USP) / Curso Objetivo', 'url': 'https://www.curso-objetivo.br/vestibular/assets/download/obras-literarias/machado-de-assis/memorial-de-aires.pdf',
     'nota': 'outra digitação do texto do Aguilar'},
]

# (trecho do texto final, leitura de outras edições, observação)
MANTIDAS = [
    ('por mar e por terra, eram de sobra', 'era de sobra', ''),
    ('o que valer a pena guardar', 'o que vale a pena', ''),
    ('Hoje de manhã recebi', 'Hoje pela manhã', ''),
    ('todo arestas, toda secura', 'todo secura', ''),
]

ERROS_ANTERIORES = []
