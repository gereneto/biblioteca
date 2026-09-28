"""Papéis Avulsos — texto da página «Sobre esta edição» (o mesmo para todos os contos)."""

COMENTARIO = '''Papéis Avulsos — Machado de Assis
   Gerado por ferramentas/texto.py a partir de edicoes/papeis-avulsos/: um BIBLIOTECA.obra()
   por conto. Não edite à mão: corrija as decisões nessa pasta e rode de novo com --publicar.

   Formato do texto de cada parte:
     - parágrafos separados por uma linha em branco;
     - _itálico_ entre sublinhados;
     - linhas começadas por "| " formam um bloco de versos (ou inscrição), uma linha por verso;
     - parágrafos começados por "¤ " são notas do autor.'''

APRESENTACAO = '''**Texto-base.** Os contos seguem a primeira e única edição de _Papéis Avulsos_ publicada em vida do autor (Rio de Janeiro, Lombaerts, 1882). O texto foi estabelecido a partir da transcrição do Projeto Gutenberg e do OCR do exemplar digitalizado pela Brasiliana USP — os dois feitos sobre as mesmas imagens —, com as edições modernas como árbitro. A transcrição do Gutenberg tem muitos erros de leitura: as palavras inexistentes foram trocadas pelas das edições modernas, e os casos duvidosos, conferidos no fac-símile.

**Publicação original.** Quase todos os contos saíram antes em jornais e revistas (_A Estação_, _Gazeta de Notícias_, _O Cruzeiro_...), às vezes com pseudônimo; a indicação acompanha cada conto. O texto aqui é o do livro, que em alguns casos o autor refez (veja a nota a _Uma Visita de Alcibíades_).

**Notas do autor.** O livro traz, ao pé da página, notas de Machado de Assis à advertência e a alguns contos. Aqui elas aparecem no fim de cada texto.

**Correções.** Corrigiram-se os erros evidentes, do impresso de 1882 e das transcrições, listados abaixo. Onde a leitura de 1882 faz sentido, ficou, ainda que as edições modernas a emendem.

**Ortografia.** A grafia foi atualizada pelo Acordo Ortográfico de 1990 (_Itaguahy_ → Itaguaí, _theoria_ → teoria, _elle_ → ele). As formas antigas de palavras que continuam em uso passaram à forma atual (_cousa_ → coisa, _dous_ → dois, _noute_ → noite); os nomes bíblicos tomaram a forma portuguesa atual (_Japhet_ → Jafé, _Cham_ → Cam). O vocabulário e as construções do autor ficaram como estão — as mesóclises, a colocação dos pronomes, os travessões e as aspas angulares, os itálicos e as abreviaturas _S._ (São), _D._ (Dona) e _V. Ex._ (Vossa Excelência).'''

BASE = 'Edição de 1882'

SECOES = {
    'erros': {'titulo': 'Erros corrigidos',
              'explica': 'Do impresso de 1882 e das transcrições. Grafia de 1882.'},
    'mantidas': {'titulo': 'Lições de 1882 mantidas',
                 'explica': 'Pontos em que as edições modernas leem diferente.'},
}

FONTES = [
    {'nome': 'Fac-símile da edição de 1882 (Brasiliana USP)', 'url': 'https://digital.bbm.usp.br/handle/bbm/4774',
     'nota': 'texto-base; OCR usado no confronto'},
    {'nome': 'Projeto Gutenberg, nº 57001', 'url': 'https://www.gutenberg.org/ebooks/57001',
     'nota': 'transcrição da edição de 1882, feita sobre as imagens da Brasiliana'},
    {'nome': 'machadodeassis.net (Fundação Casa de Rui Barbosa)', 'url': 'https://machadodeassis.net/colecoes/papeis-avulsos/27340',
     'nota': 'texto moderno, conto a conto; dados da primeira publicação; referência para a ortografia'},
    {'nome': 'Obra Completa, Nova Aguilar, 1994 (MEC / Domínio Público)', 'url': 'https://archive.org/details/papeisAvulsos',
     'nota': 'texto moderno'},
    {'nome': 'Biblioteca Virtual do Estudante (USP) / Curso Objetivo', 'url': 'https://www.curso-objetivo.br/vestibular/assets/download/obras-literarias/machado-de-assis/papeis-avulsos.pdf',
     'nota': 'outra digitação do texto do Aguilar'},
]

# (trecho do texto final, leitura de outras edições, observação)
MANTIDAS = [
    ('provaste-me que muitas vezes o melhor drama', 'provaste-me ainda uma vez que o melhor drama', ''),
    ('a ama da civilização', 'a alma da civilização', ''),
    ('foi ele escrito incompletamente', 'inscrito', ''),
    ('a população do Itaguaí', 'de Itaguaí', ''),
    ('a carreira de barão', 'do barão', ''),
]

ERROS_ANTERIORES = []
