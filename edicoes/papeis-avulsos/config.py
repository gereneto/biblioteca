"""Papéis Avulsos — fontes.

Coletânea de contos (Rio de Janeiro, Lombaerts, 1882), única edição em vida do autor.
Testemunhos de 1882: Projeto Gutenberg (feito sobre as imagens da Brasiliana) e o OCR desse
mesmo exemplar (bbm/4774). Modernas: machadodeassis.net (conto a conto), Aguilar, Objetivo.

A coletânea é estabelecida inteira e publicada conto a conto (ver CONTOS). No fluxo de
tokens, cada unidade (advertência, conto) começa numa parte sem número; os capítulos de um
conto (O Alienista, Na Arca) são as partes numeradas seguintes. As notas do autor, que o
livro traz ao pé da página, vão juntas numa unidade «Notas» no fim, como no Aguilar; na
publicação, cada nota volta ao seu conto.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ferramentas'))
from edicao import fontes, rede  # noqa: E402
from edicao.ocr import estrutura_como, limpar as limpar_ocr  # noqa: E402

OBRA = 'papeis-avulsos'

META = {
    'id': OBRA,
    'autor': 'machado-de-assis',
    'titulo': 'Papéis Avulsos',
    'ano': 1882,
    'genero': 'Contos',
    'divisao': {'singular': 'capítulo', 'plural': 'capítulos'},
}

# Na ordem do livro. 'pg': título no Gutenberg; 'mdn': (slug, id) no machadodeassis.net;
# 'publicacao': primeira publicação (dados do machadodeassis.net; «O Anel de Polícrates» lá traz
# 1872, impossível — a Gazeta de Notícias é de 1875 —, corrigido para 1882).
CONTOS = [
    {'id': 'papeis-avulsos-advertencia', 'titulo': 'Advertência', 'pg': 'ADVERTENCIA', 'paratexto': True,
     'publicacao': ''},
    {'id': 'o-alienista', 'titulo': 'O Alienista', 'pg': 'O ALIENISTA', 'mdn': ('o-alienista', 27353), 'capitulos': True,
     'publicacao': '_A Estação_, de outubro de 1881 a março de 1882'},
    {'id': 'teoria-do-medalhao', 'subtitulo': 'Diálogo', 'titulo': 'Teoria do Medalhão', 'pg': 'THEORIA DO MEDALHÃO',
     'mdn': ('teoria-do-medalhao', 27839), 'publicacao': '_Gazeta de Notícias_, 18 de dezembro de 1881'},
    {'id': 'a-chinela-turca', 'titulo': 'A Chinela Turca', 'pg': 'A CHINELA TURCA', 'mdn': ('a-chinela-turca', 27943),
     'publicacao': '_A Época_, 14 de novembro de 1875, com o pseudônimo Manassés'},
    {'id': 'na-arca', 'subtitulo': 'Três capítulos inéditos do Gênesis', 'titulo': 'Na Arca', 'pg': 'NA ARCA', 'mdn': ('na-arca', 28059), 'capitulos': True,
     'publicacao': '_O Cruzeiro_, 14 de maio de 1878, com o pseudônimo Eleazar'},
    {'id': 'd-benedita', 'subtitulo': 'Um retrato', 'titulo': 'D. Benedita', 'pg': 'D. BENEDICTA', 'mdn': ('dona-benedita', 28160), 'capitulos': True,
     'publicacao': '_A Estação_, de abril a junho de 1882'},
    {'id': 'o-segredo-do-bonzo', 'subtitulo': 'Capítulo inédito de Fernão Mendes Pinto', 'titulo': 'O Segredo do Bonzo', 'pg': 'O SEGREDO DO BONZO',
     'mdn': ('o-segredo-do-bonzo', 28376), 'publicacao': '_Gazeta de Notícias_, 30 de abril de 1882'},
    {'id': 'o-anel-de-policrates', 'titulo': 'O Anel de Polícrates', 'pg': 'O ANNEL DE POLYCRATES',
     'mdn': ('o-anel-de-policrates', 28415), 'publicacao': '_Gazeta de Notícias_, 2 de julho de 1882'},
    {'id': 'o-emprestimo', 'titulo': 'O Empréstimo', 'pg': 'O EMPRESTIMO', 'mdn': ('o-emprestimo', 28511),
     'publicacao': '_Gazeta de Notícias_, 30 de julho de 1882'},
    {'id': 'a-serenissima-republica', 'subtitulo': 'Conferência do cônego Vargas', 'titulo': 'A Sereníssima República', 'pg': 'A SERENISSIMA REPUBLICA',
     'mdn': ('a-serenissima-republica-conferencia-do-conego-vargas', 28599),
     'publicacao': '_Gazeta de Notícias_, 20 de agosto de 1882'},
    {'id': 'o-espelho', 'subtitulo': 'Esboço de uma nova teoria da alma humana', 'titulo': 'O Espelho', 'pg': 'O ESPELHO', 'mdn': ('o-espelho', 28653),
     'publicacao': '_Gazeta de Notícias_, 8 de setembro de 1882'},
    {'id': 'uma-visita-de-alcibiades', 'subtitulo': 'Carta do desembargador X... ao chefe de polícia da Corte', 'titulo': 'Uma Visita de Alcibíades', 'pg': 'UMA VISITA DE ALCIBIADES',
     'mdn': ('uma-visita-de-alcibiades', 28724),
     'publicacao': '_Jornal das Famílias_, outubro de 1876, com o pseudônimo Victor de Paula, em outra versão'},
    {'id': 'verba-testamentaria', 'titulo': 'Verba Testamentária', 'pg': 'VERBA TESTAMENTARIA',
     'mdn': ('verba-testamentaria', 28831), 'publicacao': '_Gazeta de Notícias_, 8 de outubro de 1882'},
]
NOTAS = 'Notas'

BASE = 'pg'
CORRELACIONADOS = []
UM_VOTO = True
DESEMPATE_LEXICO = True
REFERENCIAS = [('mdn', True), ('mec', False)]

PDF_1882 = 'https://digital.bbm.usp.br/bitstream/bbm/4774/4/45000018579_Output.o.pdf'
ROMANO = re.compile(r'^(?P<n>[IVXLC]+)\.?$')
CAPITULO_LETRA = re.compile(r'^CAPITULO (?P<n>[A-Z])$')
FIM = re.compile(r'^FIM D[AEO]S? ')


def _sem_marca(s):
    return re.sub(r'\[\d+\]|\*+', '', s).strip()


def pg():
    """Unidades do livro no Gutenberg; as notas de rodapé vão para a unidade final «Notas»."""
    bruto = rede.baixar('https://www.gutenberg.org/cache/epub/57001/pg57001.txt',
                        fontes.cache(OBRA, 'pg57001.txt')).decode('utf-8').replace('\r', '')
    s = bruto.split('*** START OF THE PROJECT GUTENBERG EBOOK', 1)[1].split('*** END OF THE PROJECT')[0]
    s = s[s.index('\nADVERTENCIA\n'):s.rindex('INDICE')].replace('--', '—').replace('\xad', '')
    titulos = {c['pg']: c for c in CONTOS}
    obra, notas, atual, espera_sub, espera_tit, em_nota = [], [], None, False, False, None
    for bloco in re.split(r'\n\s*\n', s):
        b = bloco.strip()
        if not b:
            continue
        chave = _sem_marca(b)
        if chave in titulos:
            atual = {'n': '', 'titulo': '', 'paras': []}
            obra.append(atual)
            espera_sub, espera_tit, em_nota = True, False, None
            unidade = titulos[chave]
            continue
        if FIM.match(b):
            em_nota = None
            continue
        m = (ROMANO.match(b) or CAPITULO_LETRA.match(b)) if unidade.get('capitulos') else None
        if m:
            atual = {'n': m.group('n'), 'titulo': '', 'paras': []}
            obra.append(atual)
            espera_sub, espera_tit, em_nota = False, bool(ROMANO.match(b)), None
            continue
        if espera_tit and b == b.upper() and len(b) < 90:
            atual['titulo'] = _sem_marca(b)
            espera_tit = False
            continue
        espera_tit = False
        if espera_sub and b == b.upper() and 3 < len(b) < 90 and not b.startswith('['):
            atual['titulo'] = _sem_marca(b).strip('()')
            espera_sub = False
            continue
        espera_sub = False
        if b.startswith('[1]'):
            em_nota = {'n': '', 'titulo': unidade['titulo'], 'paras': []}
            notas.append(em_nota)
            b = b[3:]
        alvo = em_nota['paras'] if em_nota is not None else atual['paras']
        linhas = [l for l in b.split('\n') if l.strip()]
        alvo.append(fontes.limpar(re.sub(r'\[\d\]', '', ' '.join(linhas))))   # chamada de nota
    obra.append({'n': '', 'titulo': NOTAS, 'paras': []})
    for k, nt in enumerate(notas, 1):
        obra.append({'n': f'N{k}', 'titulo': nt['titulo'], 'paras': nt['paras']})
    return fontes.normalizar(obra)


def _corrido(texto_):
    return [{'n': '0', 'titulo': '', 'paras': [p for p in re.split(r'\n\s*\n', texto_) if p.strip()]}]


def ocr_1882(base, guias):
    t = re.sub(r'­\s*', '', fontes.pdf_texto(OBRA, PDF_1882, 'bbm_4774'))    # hífen de divisão silábica
    t = t[t.index('Este titulo de'):]
    t = t[:t.rindex('INDICE')] if 'INDICE' in t else t
    cabecos = [c['pg'] for c in CONTOS] + ['PAPEIS AVULSOS']
    linhas = []
    for l in t.replace('\f', '\n').split('\n'):
        x = l.strip()
        if re.fullmatch(r'[\divxlcIVXLC.]{1,6}', x) or any(x.startswith(c) and len(x) < len(c) + 8 for c in cabecos):
            continue
        linhas.append(l)
    obra = _corrido('\n'.join(linhas))
    obra, n = limpar_ocr(obra, guias)
    print('OCR bbm/4774: palavras corrigidas pelas guias:', n)
    return estrutura_como(obra, base)


def _mec_corrido():
    mec = fontes.internet_archive(OBRA, 'papeisAvulsos', 'papeisAvulsos.pdf').replace('\f', '\n')
    return _corrido(mec[mec.index('ADVERT'):].replace('\n', '\n\n'))


def _mdn_corrido():
    paras = []
    adv = fontes.machadodeassis_net(OBRA, 'papeis-avulsos', 27340)
    for p in adv:
        paras += p['paras']
    for c in CONTOS:
        if 'mdn' not in c:
            continue
        for p in fontes.machadodeassis_net(OBRA, *c['mdn']):
            for x in (p['n'], p['titulo']):
                x = re.sub(r'^CAPÍTULO\s+', '', x or '').strip()
                if x and not re.fullmatch(r'b\d+-s\d+-c\d+', x):
                    paras.append(x)
            paras += p['paras']
    return [{'n': '0', 'titulo': '', 'paras': paras}]


def pg_limpo():
    """O Gutenberg desta coletânea saiu de um OCR mal revisto («pareceu-lbe», «ltaguahy»): as
    palavras que não existem são trocadas pela forma alinhada das edições modernas."""
    base, n = limpar_ocr(pg(), [_mdn_corrido(), _mec_corrido()])
    print('Gutenberg: palavras corrigidas pelas modernas:', n)
    return base


def transcricoes():
    base = pg_limpo()
    return {'pg': base, 'ocr': ocr_1882(base, [base, _mdn_corrido()])}


def modernas():
    base = pg_limpo()
    nup = fontes.pdf_texto(OBRA, 'https://www.curso-objetivo.br/vestibular/assets/download/obras-literarias/'
                           'machado-de-assis/papeis-avulsos.pdf', 'nupill').replace('\f', '\n')
    nup = nup[nup.upper().index('ADVERT'):] if 'ADVERT' in nup.upper() else nup
    return {
        'mdn': estrutura_como(_mdn_corrido(), base),
        'mec': estrutura_como(_mec_corrido(), base),
        'nup': estrutura_como(_corrido(nup.replace('\n', '\n\n')), base),
    }
