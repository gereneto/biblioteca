"""Dom Casmurro — fontes.

Edição-base: 1ª edição (H. Garnier, 1899), em três transcrições independentes.
A 2ª edição (1900), última em vida do autor, não está disponível: suas lições entram só
quando toda a tradição moderna concorda contra a 1ª (ver decisoes.py).
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ferramentas'))
from edicao import fontes, rede  # noqa: E402
from edicao.tokens import VERSO  # noqa: E402

META = {
    'id': 'dom-casmurro',
    'autor': 'machado-de-assis',
    'titulo': 'Dom Casmurro',
    'ano': 1899,
    'genero': 'Romance',
    'divisao': {'singular': 'capítulo', 'plural': 'capítulos'},
    'descricao': 'Romance publicado em 1899, reconhecido por muitos como a obra-prima de Machado de Assis.',
}

BASE = 'pg'
CORRELACIONADOS = [('st', 'ws')]          # Stolfi e Wikisource partem do mesmo OCR da Brasiliana
REFERENCIAS = [('mdn', True), ('mec', False)]  # grafia moderna: (edição, já no Acordo de 1990?)


def stolfi():
    s = rede.baixar('https://www.ic.unicamp.br/~stolfi/voynich/Notes/110/work/Texts/port/cso/main.txt',
                    fontes.cache('dom-casmurro', 'stolfi_main.txt'))
    try:
        s = s.decode('utf-8')
    except UnicodeDecodeError:
        s = s.decode('latin-1')
    s = re.sub(r'(?m)^%.*\n', '', s)
    obra, atual = [], None
    for b in re.split(r'\n\s*\n', s):
        st = b.strip()
        if not st:
            continue
        m = re.match(r'\\chapt\{([IVXLC]+)\}\{(.*)\}$', st, re.S)
        if m:
            atual = {'n': m.group(1), 'titulo': m.group(2), 'paras': []}
            obra.append(atual)
            continue
        if atual is None:
            continue
        if b.startswith('  '):
            atual['paras'].append(VERSO + '\n'.join(l.strip() for l in st.split('\n') if l.strip()))
            continue
        p = st.replace('\n', ' ').replace('---', '—').replace('§', '')
        p = re.sub(r'_/(.*?)/_', r'_\1_', p)
        atual['paras'].append(fontes.limpar(p))
    return fontes.normalizar(obra)


def transcricoes():
    return {
        'pg': fontes.gutenberg('dom-casmurro', 55752, [r'^(?P<n>[IVXLC]+)\.?$'], fim='INDICE'),
        'st': stolfi(),
        'ws': fontes.wikisource('dom-casmurro', 'Dom Casmurro-1899.pdf', 8, 406),
    }


def modernas():
    mec = fontes.pdf_texto('dom-casmurro', 'https://machado.mec.gov.br/obra-completa-lista/item/download/13_7101e1a36cda79f6c97341757dcc4d04', 'mec')
    nup = fontes.pdf_texto('dom-casmurro', 'https://www.curso-objetivo.br/vestibular/assets/download/obras-literarias/machado-de-assis/dom-casmurro.pdf', 'nupill')
    return {
        'mec': fontes.texto_por_linhas(mec, [r'^CAPÍTULO (?P<n>PRIMEIRO|[IVXLC]+) (?P<t>.+)$']),
        'nup': fontes.texto_por_linhas(nup, [r'^CAPÍTULO (?P<n>PRIMEIRO|[IVXLC]+) ?/ ?(?P<t>[^a-zà-ÿ]+)$']),
        'mdn': fontes.machadodeassis_net('dom-casmurro', 'dom-casmurro', 11503),
    }
