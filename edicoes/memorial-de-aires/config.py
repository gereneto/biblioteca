"""Memorial de Aires — fontes.

Uma só edição em vida do autor: Garnier, 1908 («Memorial de Ayres»). É a edição-base.
Testemunhos de 1908: Projeto Gutenberg; OCR do exemplar da Brasiliana USP (bbm/4707, com
dedicatória manuscrita); OCR do microfilme do Internet Archive (3438833, outro programa de
OCR). O outro exemplar da Brasiliana (bbm/7842) é a «nova edição», póstuma: não entra.
O Gutenberg e o microfilme não têm a «Advertência»: ela vem do fac-símile (transcrita aqui).

Divisão: as entradas do diário (cada data ou hora anotada), sob o ano (1888, 1889).
A estrutura vem do Gutenberg e é projetada sobre os demais testemunhos (ocr.estrutura_como).
"""
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ferramentas'))
from edicao import fontes, rede  # noqa: E402
from edicao.ocr import estrutura_como, limpar as limpar_ocr  # noqa: E402
from edicao.tokens import VERSO  # noqa: E402

OBRA = 'memorial-de-aires'

META = {
    'id': OBRA,
    'autor': 'machado-de-assis',
    'titulo': 'Memorial de Aires',
    'ano': 1908,
    'genero': 'Romance',
    'divisao': {'singular': 'entrada', 'plural': 'entradas', 'rotulo': 'titulo'},
    'descricao': 'Último romance de Machado de Assis, publicado em 1908, meses antes de sua morte: '
                 'o diário do conselheiro Aires nos anos de 1888 e 1889.',
}

BASE = 'pg'
CORRELACIONADOS = [('pg', 'ia')]         # o Gutenberg foi feito sobre o OCR do microfilme
UM_VOTO = True
DESEMPATE_LEXICO = True
REFERENCIAS = [('mdn', True), ('mec', False)]

PDF_4707 = 'https://digital.bbm.usp.br/bitstream/bbm/4707/4/45000018570_Output.o.pdf'
ADVERTENCIA = 'Advertência'

# Fac-símile bbm/4707, p. [V]; grafia do impresso.
ADVERTENCIA_1908 = [
    'Quem me leu _Esaú e Jacob_ talvez reconheça estas palavras do prefacio: «Nos lazeres do oficio '
    'escrevia o _Memorial_, que, apezar das paginas mortas ou escuras, apenas daria (e talvez dê) para '
    'matar o tempo da barca de Petropolis.»',
    'Referia-me ao conselheiro Ayres. Tratando-se agora de imprimir o _Memorial_, achou-se que a parte '
    'relativa a uns dous annos (1888-1889), se fôr decotada de algumas circumstancias, anedotas, '
    'descrições e reflexões, — pode dar uma narração seguida, que talvez interesse, apezar da fórma de '
    'diario que tem. Não houve pachorra de a redigir á maneira daquella outra, — nem pachorra, nem '
    'habilidade. Vae como estava, mas desbastada e estreita, conservando só o que liga o mesmo '
    'assunto. O resto aparecerá um dia, se aparecer algum dia.',
    'M. de A.',
]

# As duas epígrafes (página anterior à advertência), em português antigo: não se atualizam.
EPIGRAFES = [
    VERSO + 'Em Lixboa, sobre lo mar,\nBarcas novas mandey lavrar...',
    '_Cantiga_ de Joham Zorro.',
    VERSO + "Para veer meu amigo\nQue talhou preyto comigo,\nAlá vou, madre.\n"
            "Para veer meu amado\nQue mig'a preyto talhado,\nAlá vou, madre.",
    "_Cantiga d'el-rei_ Dom Denis.",
]

ANO = re.compile(r'^\s*(18\d\d)\s*$')
SEPARADOR = re.compile(r'^\s*([*—-]\s*){3,}$')


def _chave_titulo(t):
    t = unicodedata.normalize('NFD', _sem_tags(t)).lower()
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in t if not unicodedata.combining(c)))


def _titulos_modernos():
    """Datas e horas das entradas, segundo o machadodeassis.net (para achar as entradas que o
    Gutenberg não separa)."""
    out = set()
    for p in _mdn():
        for x in (p['n'], p['titulo']):
            x = re.sub(r'^\s*18\d\d\s*[–-]?\s*', '', _sem_tags(x))
            if x and 'ADVERT' not in x.upper() and x != 'epigrafe':
                out.add(_chave_titulo(x))
    return out


def pg():
    """Entradas do diário no texto do Gutenberg: ano, separadores, e a primeira linha de cada
    entrada (data ou hora) como título; entradas sem separador são achadas pela data."""
    titulos = _titulos_modernos()
    bruto = rede.baixar('https://www.gutenberg.org/cache/epub/55797/pg55797.txt',
                        fontes.cache(OBRA, 'pg55797.txt')).decode('utf-8').replace('\r', '')
    s = bruto.split('*** START OF THE PROJECT GUTENBERG EBOOK', 1)[1].split('\n', 1)[1]
    s = s.split('*** END OF THE PROJECT GUTENBERG EBOOK')[0]
    s = s[s.index('\n1888\n'):s.rindex('FIM')].replace('--', '—')
    obra, ano, espera = [], None, False
    for bloco in re.split(r'\n\s*\n', s):
        b = bloco.strip()
        if not b:
            continue
        if ANO.match(b):
            ano, espera = b, True
            continue
        if SEPARADOR.match(b):
            espera = True
            continue
        if espera or (len(b) < 50 and not bloco.startswith(' ') and _chave_titulo(b) in titulos):
            obra.append({'n': ano, 'titulo': b, 'paras': []})
            espera = False
            continue
        obra[-1]['paras'].append(fontes.limpar(b.replace('\n', ' ')))
    return fontes.normalizar(obra)


def _corrido(texto_):
    """Texto de uma fonte como uma parte só (a estrutura vem da base)."""
    return [{'n': '0', 'titulo': '', 'paras': [p for p in re.split(r'\n\s*\n', texto_) if p.strip()]}]


def ocr_4707(guias):
    t = fontes.pdf_texto(OBRA, PDF_4707, 'bbm_4707')
    t = t[re.search(r'\n\s*1888\s*\n', t).start():]
    obra = fontes.ocr_por_linhas(t, '1888', None, r'(?!x)x', lixo=[r'^.{0,3}MEMORIAL DE AYRES.{0,6}$'],
                                 sem_numero=[(r'^18\d\d$', 'ano')])
    for p in obra:
        p['titulo'] = ''
    obra, n = limpar_ocr(obra, guias)
    print('OCR bbm/4707: palavras corrigidas pelas guias:', n)
    return obra


def ocr_ia(guias):
    t = fontes.internet_archive(OBRA, '3438833', '3438833_djvu.txt')
    t = t[t.index('9  de  Janeiro'):t.rindex('FIM')]
    t = re.sub(r'[ \t]+', ' ', t)
    obra = fontes.ocr_por_linhas('1888\n' + t, '1888', None, r'(?!x)x',
                                 lixo=[r'^.{0,3}MEMORIAL DE AYRES.{0,6}$', r'^\d{1,3}\s*MEMORIAL.*$'],
                                 sem_numero=[(r'^18\d\d$', 'ano')])
    for p in obra:
        p['titulo'] = ''
    obra, n = limpar_ocr(obra, guias)
    print('OCR microfilme IA: palavras corrigidas pelas guias:', n)
    return obra


def com_abertura(obra, advertencia=ADVERTENCIA_1908):
    """Advertência antes do diário; as epígrafes no alto da primeira entrada."""
    corpo = [dict(p, paras=list(p['paras'])) for p in obra]
    corpo[0]['paras'] = EPIGRAFES + corpo[0]['paras']
    return [{'n': '', 'titulo': ADVERTENCIA, 'paras': list(advertencia)}] + corpo


def _mdn():
    return fontes.machadodeassis_net(OBRA, OBRA, 16866)


def _sem_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()


def transcricoes():
    base = pg()
    mdn = _mdn()
    o1 = estrutura_como(ocr_4707([base, mdn]), base)
    o2 = estrutura_como(ocr_ia([base, mdn]), base)
    return {'pg': com_abertura(base), 'o1': com_abertura(o1), 'ia': com_abertura(o2)}


def modernas():
    base = pg()
    mdn = _mdn()
    adv_mdn = next(p for p in mdn if 'ADVERT' in p['n'].upper())['paras']
    corpo = []
    for p in mdn:
        if 'ADVERT' in p['n'].upper() or p['n'] == 'epigrafe':
            continue
        for x in (p['n'], p['titulo']):
            x = re.sub(r'^\s*18\d\d\s*[–-]?\s*', '', _sem_tags(x))
            if x:
                corpo.append(x)
        corpo += p['paras']
    mec = fontes.internet_archive(OBRA, 'memorialAires', 'memorial-de-aires.pdf')
    nup = fontes.pdf_texto(OBRA, 'https://www.curso-objetivo.br/vestibular/assets/download/obras-literarias/'
                           'machado-de-assis/memorial-de-aires.pdf', 'nupill')
    adv_mec = re.search(r'Quem me leu.*?algum dia\.', mec, re.S).group(0).split('\n')
    corte = lambda t: t[re.search(r'9 de [Jj]aneiro\.?\s*\n\s*Ora bem', t).start():t.rindex('saudade de si mesmos') + 21]
    return {
        'mdn': com_abertura(estrutura_como([{'n': '0', 'titulo': '', 'paras': corpo}], base), adv_mdn),
        'mec': com_abertura(estrutura_como(_corrido(corte(mec).replace('\n', '\n\n')), base), adv_mec),
        'nup': com_abertura(estrutura_como(_corrido(corte(nup).replace('\n', '\n\n')), base)),
    }
