"""Quincas Borba — texto da página «Sobre esta edição»."""

COMENTARIO = '''Quincas Borba — Machado de Assis
   Gerado por ferramentas/texto.py a partir de edicoes/quincas-borba/.
   Não edite à mão: corrija as decisões nessa pasta e rode de novo com --publicar.

   Formato do texto de cada parte:
     - parágrafos separados por uma linha em branco;
     - _itálico_ entre sublinhados;
     - linhas começadas por "| " formam um bloco de versos (ou inscrição), uma linha por verso.'''

APRESENTACAO = '''**Texto-base.** O texto segue a edição revista pelo autor: a segunda (1896), repetida na terceira (Rio de Janeiro, Garnier, 1899), que, segundo o prólogo, só emendou «alguns erros tipográficos». Nenhuma das duas está digitalizada. Por isso o ponto de partida é a primeira edição em livro (Rio de Janeiro, B. L. Garnier, 1891), estabelecida a partir de duas transcrições — a do Projeto Gutenberg e a do Wikisource — e da leitura automática (OCR) do exemplar digitalizado pela Brasiliana USP. Onde elas divergem, valeu a leitura apoiada pelas edições modernas.

**A revisão de 1896.** Da primeira para a segunda edição, Machado mexeu em centenas de passagens: trocou palavras repetidas (muitas vezes _ideia_ e _cousa_), cortou frases, tirou artigos antes de nomes, mudou a assinatura da carta de Quincas Borba. Essas lições só chegam até nós pelas edições modernas, todas feitas sobre o texto definitivo. Foram adotadas sempre que todas as edições modernas consultadas concordam contra a de 1891; vão listadas abaixo, palavra por palavra e sinal por sinal.

**Correções.** Aplicou-se a errata impressa no próprio livro de 1891 (quase toda ela já está na edição revista) e corrigiram-se os erros evidentes. Nada mais foi emendado.

**O prólogo.** O «Prólogo da terceira edição» (1899) vem do texto moderno, já que não há fac-símile dessa edição.

**Ortografia.** A grafia foi atualizada pelo Acordo Ortográfico de 1990 (_Sophia_ → Sofia, _idéa_ → ideia, _elle_ → ele). As formas antigas de palavras que continuam em uso passaram à forma atual (_cousa_ → coisa, _dous_ → dois, _doudo_ → doido). O vocabulário e as construções do autor ficaram como estão — as mesóclises, a colocação dos pronomes, os travessões e as aspas angulares, os itálicos e as abreviaturas _S._ (São), _D._ (Dona) e _cap._ (capítulo).

**Divisão.** O livro tem 201 capítulos curtos, numerados em romanos e sem título, precedidos do prólogo. Cada um é uma página desta biblioteca.'''

BASE = 'Edição de 1891'

SECOES = {
    'erros': {'titulo': 'Erros corrigidos',
              'explica': 'Da errata impressa no livro de 1891 e erros evidentes. Grafia de 1891.'},
    'tradicao': {'titulo': 'Lições da edição revista adotadas',
                 'explica': 'Pontos em que todas as edições modernas concordam contra a de 1891. '
                            'Na primeira coluna, a grafia de 1891; na segunda, a atual.',
                 'para': 'Edição revista'},
    'pontuacao': {'titulo': 'Pontuação da edição revista adotada',
                  'explica': 'Mesmo critério: só onde todas as edições modernas concordam. Grafia atualizada.',
                  'para': 'Edição revista'},
    'mantidas': {'titulo': 'Lições de 1891 mantidas',
                 'explica': 'Pontos em que as edições modernas leem diferente, mas não é lição do autor.'},
}

FONTES = [
    {'nome': 'Fac-símile da 1ª edição, 1891 (Brasiliana USP)', 'url': 'https://digital.bbm.usp.br/handle/bbm/5251',
     'nota': 'texto e errata; OCR usado no confronto'},
    {'nome': 'Fac-símile da 1ª edição, outro exemplar (Brasiliana USP)', 'url': 'https://digital.bbm.usp.br/handle/bbm/7808',
     'nota': ''},
    {'nome': 'Projeto Gutenberg, nº 55682', 'url': 'https://www.gutenberg.org/ebooks/55682',
     'nota': 'transcrição da edição de 1891, grafia original'},
    {'nome': 'Wikisource em português', 'url': 'https://pt.wikisource.org/wiki/Quincas_Borba',
     'nota': 'transcrição da edição de 1891; usadas só as páginas revisadas'},
    {'nome': 'machadodeassis.net (Fundação Casa de Rui Barbosa)', 'url': 'https://machadodeassis.net/texto/quincas-borba/8340',
     'nota': 'texto moderno da edição definitiva; referência para a ortografia'},
    {'nome': 'Obra Completa, Nova Aguilar, 1994 (MEC / Domínio Público)', 'url': 'https://archive.org/details/quincasBorbaMachado',
     'nota': 'texto moderno da edição definitiva'},
    {'nome': 'Biblioteca Virtual do Estudante (USP) / Curso Objetivo', 'url': 'https://www.curso-objetivo.br/vestibular/assets/download/obras-literarias/machado-de-assis/quincas-borba.pdf',
     'nota': 'outra digitação do texto do Aguilar'},
]

# (trecho do texto final, leitura de outras edições, observação)
MANTIDAS = [
    ('nos seus paços de S. Cloud', 'Saint-Cloud', 'abreviatura do autor'),
    ('sob a firma Palha & Comp.', 'Palha & Cia.', 'abreviatura do autor'),
]

ERROS_ANTERIORES = []
