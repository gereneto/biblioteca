"""Quincas Borba — fontes.

Edições em vida do autor: folhetim em A Estação (1886–1891); livro, Garnier (1891), com errata;
2ª edição (1896); 3ª edição (1899), com prólogo, «sem outra alteração além da emenda de alguns
erros tipográficos». Só a de 1891 está digitalizada (Brasiliana USP, dois exemplares).
Edição-base: 1891, com a errata do próprio livro e as lições que as edições modernas atestam
em conjunto. O prólogo de 1899 vem do texto moderno (não há fac-símile dessa edição).
Testemunhos de 1891: Projeto Gutenberg, Wikisource e o OCR de um dos exemplares da Brasiliana.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ferramentas'))
from edicao import fontes  # noqa: E402
from edicao.ocr import limpar as limpar_ocr  # noqa: E402

OBRA = 'quincas-borba'

META = {
    'id': OBRA,
    'autor': 'machado-de-assis',
    'titulo': 'Quincas Borba',
    'ano': 1891,
    'genero': 'Romance',
    'divisao': {'singular': 'capítulo', 'plural': 'capítulos'},
    'descricao': 'Romance publicado em 1891, o segundo da fase madura de Machado de Assis, '
                 'ligado às Memórias Póstumas de Brás Cubas pela figura do filósofo Quincas Borba.',
}

BASE = 'pg'
CORRELACIONADOS = [('ws', 'ocr')]         # o Wikisource revisou o mesmo OCR da Brasiliana
TRADICAO = ['mdn', 'mec', 'nup']           # a edição revista (1896/1899) só existe nas modernas
REFERENCIAS = [('mdn', True), ('mec', False)]

PDF_1891 = 'https://digital.bbm.usp.br/bitstream/bbm/5251/1/002113_COMPLETO.pdf'
PROLOGO = 'Prólogo da terceira edição'


def _capitulos(obra):
    """'CAPÍTULO PRIMEIRO' / 'PRIMEIRO' -> 'I'; o prólogo fica sem número, com título."""
    for p in obra:
        n = re.sub(r'^CAP[ÍI]TULO\s+', '', p['n'].strip(), flags=re.I)
        if n.upper().startswith('PRÓLOGO') or n.upper().startswith('PROLOGO'):
            p['n'], p['titulo'] = '', PROLOGO
        else:
            p['n'] = 'I' if n.upper() == 'PRIMEIRO' else n
    return obra


def _prologo(mdn):
    """O prólogo de 1899, do texto moderno, com as aspas angulares do autor e a assinatura
    completa («M. de A.», como no Aguilar; o machadodeassis.net perde o ponto final)."""
    p = next(p for p in mdn if p['titulo'] == PROLOGO)
    paras = [re.sub(r'"([^"]*)"', r'«\1»', x) for x in p['paras']]
    paras = [x + '.' if x.strip() == 'M. de A' else x for x in paras]
    return dict(p, paras=paras)


def com_prologo(obra, prologo):
    """As transcrições de 1891 não têm o prólogo de 1899: entra o do texto moderno."""
    return [dict(prologo, paras=list(prologo['paras']))] + [p for p in obra if p['titulo'] != PROLOGO]


def _mdn():
    return _capitulos(fontes.machadodeassis_net(OBRA, OBRA, 8340))


def ocr_1891():
    t = fontes.pdf_texto(OBRA, PDF_1891, 'bbm_5251')
    return fontes.ocr_por_linhas(t, 'CAPITULO PRIMEIRO', '\nFIM', r'^\W*CAP[IÍ1l]TUL[O0]\s+(?P<n>\S+)$',
                                 lixo=[r'^Q\S{1,3}[IÍ1l]NCAS\s+B\S{2,4}A$'])


def transcricoes():
    pg = fontes.gutenberg(OBRA, 55682, [r'^CAPITULO (?P<n>PRIMEIRO|[IVXLC]+)$'], inicio='CAPITULO PRIMEIRO',
                          fim='FIM', titulo_seguinte=False)
    ws = fontes.wikisource(OBRA, 'Quincas Borba.pdf', 11, 443, qualidade_minima=3, titulos=False)
    mdn = _mdn()
    ocr, n = limpar_ocr(ocr_1891(), [pg, ws, mdn])
    print('OCR de 1891: palavras corrigidas pelas guias:', n)
    pro = _prologo(mdn)
    return {n: com_prologo(_capitulos(o), pro) for n, o in (('pg', pg), ('ws', ws), ('ocr', ocr))}


def modernas():
    cab = [r'^CAPÍTULO (?P<n>PRIMEIRO|[IVXLC]+)$']
    sep = lambda t: re.sub(r'(CAPÍTULO (?:PRIMEIRO|[IVXLC]+))[ \t]+(?=\S)', r'\1\n', t.replace('\f', '\n'))
    mec = fontes.internet_archive(OBRA, 'quincasBorbaMachado', 'quincas.pdf')
    nup = fontes.pdf_texto(OBRA, 'https://www.curso-objetivo.br/vestibular/assets/download/obras-literarias/'
                           'machado-de-assis/quincas-borba.pdf', 'nupill')
    mdn = _mdn()
    pro = _prologo(mdn)
    return {
        'mdn': mdn,
        'mec': com_prologo(_capitulos(fontes.texto_por_linhas(sep(mec), cab)), pro),
        'nup': com_prologo(_capitulos(fontes.texto_por_linhas(sep(nup), cab)), pro),
    }
