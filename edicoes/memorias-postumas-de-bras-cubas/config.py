"""Memórias Póstumas de Brás Cubas — fontes.

Edições em vida do autor: folhetim na Revista Brasileira (1880); livro, Tipografia Nacional (1881);
«terceira edição», Garnier (1896), revista pelo autor, com prólogo; «quarta edição», Garnier (1899).
Edição-base: a de 1896, a última revista que se pode ler em fac-símile (Brasiliana USP).
Testemunhos: o OCR desse fac-símile e duas transcrições independentes da edição de 1881, que
servem para limpar o ruído do OCR. Onde o texto de 1896 difere do de 1881 e as edições
modernas (que seguem a de 1899) confirmam, vale 1896.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ferramentas'))
from edicao import fontes, rede  # noqa: E402
from edicao.tokens import VERSO  # noqa: E402
from edicao.ocr import limpar as limpar_ocr  # noqa: E402

OBRA = 'memorias-postumas-de-bras-cubas'

META = {
    'id': OBRA,
    'autor': 'machado-de-assis',
    'titulo': 'Memórias Póstumas de Brás Cubas',
    'ano': 1881,
    'genero': 'Romance',
    'divisao': {'singular': 'capítulo', 'plural': 'capítulos'},
    'descricao': 'Romance publicado em 1881, com que Machado de Assis abre a fase de sua maturidade; um marco da ficção brasileira.',
}

BASE = 'pg'
CORRELACIONADOS = [('pg', 'ws')]           # as duas transcrições são da mesma edição (1881), não da base
RUIDOSO = 'ocr'                            # o OCR de 1896: onde está ilegível, valem as modernas que ele confirma
REFERENCIAS = [('mdn', True), ('mec', False)]

PDF_1896 = 'https://digital.bbm.usp.br/bitstream/bbm/7815/1/45000018600_Output.o.pdf'
ROMANOS = 'IVXLC'


def dedicatoria_primeiro(obra):
    """Põe a dedicatória («Ao verme...») numa parte própria, no começo, como na edição de 1896."""
    for parte in obra:
        for k, p in enumerate(parte['paras']):
            if not re.match(r'^\W*AO VERME', p.lstrip(VERSO), re.I):
                continue
            fim = k
            while (fim + 1 < len(parte['paras']) and not re.search(r'MEM[ÓO]RIAS', parte['paras'][fim].upper())
                   and len(parte['paras'][fim + 1]) < 60):
                fim += 1
            bloco = '\n'.join(x.lstrip(VERSO) for x in parte['paras'][k:fim + 1])
            del parte['paras'][k:fim + 1]
            linhas = [l.strip() for l in bloco.split('\n') if l.strip()]
            if len(linhas) == 1:   # tudo numa linha (edições modernas)
                linhas = [l.strip() for l in re.split(r'(?<=\S) (?=QUE\b|PRIMEIRO\b|DO MEU\b|DEDICO\b|COMO\b|ESTAS\b|MEM)',
                                                      bloco, flags=re.I) if l.strip()]
            ded = {'n': '', 'titulo': '', 'paras': [VERSO + '\n'.join(linhas)]}
            return [ded] + [x for x in obra if x['paras'] or x['titulo']]
    return obra


# Páginas de abertura de 1896 transcritas do fac-símile: a dedicatória (p. V) não tem camada de
# texto no PDF e o OCR do prólogo (pp. VII–VIII) é falho. Grafia e erros do impresso mantidos.
DEDICATORIA_1896 = ('AO VERME\nQUE\nPRIMEIRO ROEU AS FRIAS CARNES\nDO MEU CADAVER\nDEDICO\n'
                    'COMO SAUDOSA LEMBRANÇA\nESTAS\nMEMORIAS POSTHUMAS')
PROLOGO_1896 = [
    'A primeira edição d’estas _Memorias posthumas de Braz Cubas_ foi feita aos pedaços na _Revista '
    'Brazileira_, pelos annos de 1880. Postas mais tarde em livro, corrigi o texto em varios logares. '
    'Agora que tive de o rever para a terceira edição, emendei ainda alguma cousa e supprimi duas ou '
    'tres duzias de linhas. Assim composto, sáe novamente á luz esta obra que alguma benevolencia '
    'parece ter encontrado no publico.',
    'Capistrano de Abreu, noticiando a publicação do livro, perguntava: « As _Memorias posthumas de '
    'Braz Cubas_ são um romance? » Macedo Soares, em carta que me escreveu por esse tempo, recordava '
    'amigamente as _Viagens na minha terra_. Ao primeiro respondia já o defuncto Braz Cubas (como o '
    'leitor viu e verá no prologo d’elle que vai adeante) que sim e que não, que era romance para uns '
    'e não o era para outros. Quanto ao segundo, assim se explicou o finado: « Trata-se de uma obra '
    'diffusa, na qual eu, Braz Cubas, se adoptei a fórma livre de um Sterne ou de um Xavier de '
    'Maistre, não sei se lhe mettí algumas rabugens de pessimismo. » Toda essa gente viajou: Xavier '
    'de Maistre á roda do quarto, Garrett na terra d’elle, Sterne na terra dos outros. De Braz Cubas '
    'se pode talver dizer que viajou á roda da vida.',
    'O que faz do meu Braz Cubas um autor particular é o que elle chama « rabugens de pessimismo. » '
    'Ha na alma d’este livro, por mais risonho que pareça, um sentimento amargo e aspero, que está '
    'longe de vir dos seus modelos. É taça que pode ter lavores de egual escola, mas leva outro vinho. '
    'Não digo mais para não entrar na critica de um defunto, que se pintou a sí e a outros, conforme '
    'lhe pareceu melhor e mais certo.',
    'Machado de Assiz.',
]
PROLOGO = 'Prólogo da terceira edição'


def abertura_1896(obra, prologo=True):
    """Dedicatória, prólogo e «Ao leitor», nesta ordem e com estes títulos, como em 1896.
    prologo=True põe o prólogo transcrito do fac-símile (as transcrições de 1881 não o têm)."""
    ded, pro, leitor, resto = None, None, None, []
    for parte in obra:
        rot = (parte['n'] + ' ' + parte['titulo']).strip().upper()
        if not ded and parte['paras'] and re.match(r'^\W*AO VERME', parte['paras'][0].lstrip(VERSO), re.I):
            ded = parte
        elif not pro and rot.startswith(('PROLOGO', 'PRÓLOGO')):
            pro = parte
        elif not leitor and rot.endswith('AO LEITOR'):
            leitor = parte
        else:
            resto.append(parte)
    ded = ded or {'paras': [VERSO + DEDICATORIA_1896]}
    ded.update(n='', titulo='Dedicatória')
    if prologo:
        pro = {'n': '', 'titulo': PROLOGO, 'paras': list(PROLOGO_1896)}
    else:
        pro.update(n='', titulo=pro['titulo'] or pro['n'].capitalize())
    leitor.update(n='', titulo='Ao leitor')
    return [ded, pro, leitor] + resto


def ocr_1896():
    """Texto do OCR do fac-símile de 1896, limpo de cabeços, números de página e ruído."""
    s = fontes.pdf_texto(OBRA, PDF_1896, 'bbm_1896')
    s = s.replace('\f', '\n')
    s = re.sub(r'\xad\s*', '', s)                       # hífen de divisão silábica
    s = s[s.index('PROLOGO'):]
    fim = [m.start() for m in re.finditer(r'(?m)^\s*[IÍ]NDICE', s)]
    if fim:
        s = s[:fim[-1]]
    brutas = [l.strip() for l in s.split('\n')]
    cab = re.compile(r'^C\s?A\s?P\s?[IÍ1l]\s?T\s?U\s?L\s?\S*\s+(.*)$')
    linhas = []                                          # (texto, havia linha em branco antes)
    branco = False
    for k, t in enumerate(brutas):
        if not t:
            branco = True
            continue
        seguinte = next((x for x in brutas[k + 1:] if x), '')
        pula = (
            (re.search(r'C[UR][BR]AS\s*$', t) and len(t) < 50 and sum(c.isupper() for c in t) > len(t) * 0.5)
            or (t == 'PROLOGO' and not seguinte.startswith('DA TERCEIRA'))
            or t in ('AO LEITOR', 'MEMÓRIAS POSTHUMAS', 'MEMORIAS POSTHUMAS', 'DE', 'BRAZ CUBAS')   # cabeços e falso-rosto
            or re.fullmatch(r'[IVXLCivxlc\d]{1,6}\.?', t)
            or sum(c.isalpha() for c in t) < 3
            or (len(t) < 14 and sum(c.isalpha() for c in t) < len(t) * 0.6)
        )
        if pula:
            continue
        linhas.append((t, branco))
        branco = False

    obra, parte, espera_titulo = [], None, False
    par = ''

    def fecha():
        nonlocal par
        if par and parte is not None:
            parte['paras'].append(fontes.limpar(par.replace('®', '»')))
        par = ''

    for t, branco in linhas:
        m = cab.match(t)
        if m or t == 'PROLOGO' or re.fullmatch(r'AO\s+L\s?E\s?I\s?T\s?O\s?R', t):
            fecha()
            if m:
                resto = m.group(1).split()
                num = []
                while resto and re.fullmatch(r'[IVXLCÍíGl1]+|P\S*MEIRO', resto[0]):
                    num.append(resto.pop(0))
                n = 'I' if num and 'MEIRO' in num[0] else ''.join(num)
                n = n.replace('Í', 'I').replace('í', 'I').replace('G', 'C').replace('l', 'I').replace('1', 'I')
                parte = {'n': n, 'titulo': ' '.join(resto), 'paras': []}
                espera_titulo = not resto
            elif t == 'PROLOGO':
                parte = {'n': '', 'titulo': 'Prólogo da terceira edição', 'paras': []}
                espera_titulo = False
            else:
                parte = {'n': '', 'titulo': 'Ao leitor', 'paras': []}
                espera_titulo = False
            obra.append(parte)
            continue
        if parte is None or t.startswith('DA TERCEIRA'):
            continue
        if espera_titulo:
            parte['titulo'] = t
            espera_titulo = False
            continue
        novo = branco and re.search(r'[.!?:»…]\s*$', par) and re.match(r'^[A-ZÁÉÍÓÚÂÊÔÃÕÇ—«\-]', t)
        if par and (novo or (re.search(r'[.!?»]\s*$', par) and re.match(r'^[—\-]', t))):
            fecha()
        if par.endswith('-') and not par.endswith('--'):
            par = par[:-1] + t
        else:
            par = (par + ' ' + t) if par else t
    fecha()
    return fontes.normalizar(obra)


def transcricoes():
    pg = fontes.gutenberg(OBRA, 54829, [r'^(?P<t>AO LEITOR)$', r'^CAPITULO (?P<n>[IVXLC]+)$'], inicio='AO LEITOR')
    ws = fontes.wikisource(OBRA, 'Memórias Pósthumas de Braz Cubas.djvu', 9, 393, qualidade_minima=3)
    mdn = fontes.machadodeassis_net(OBRA, OBRA, 5985)
    ocr, n = limpar_ocr(ocr_1896(), [pg, ws, mdn])
    print('OCR de 1896: palavras corrigidas pelas guias:', n)
    return {
        'pg': abertura_1896(dedicatoria_primeiro(pg)),
        'ws': abertura_1896(dedicatoria_primeiro(ws)),
        'ocr': abertura_1896(ocr),
    }


def modernas():
    cab = [r'^(?:CAPÍTULO|Capítulo) (?P<n>PRIMEIRO|[IVXLC]+)\b\s*(?P<t>.*)$']
    mec = fontes.internet_archive(OBRA, 'memoriasPostumasBrasCubas', 'memoriasBras.pdf')
    cam = fontes.internet_archive(OBRA, 'memorias_postumas_bras_cubas', 'memorias_postumas_bras_cubas_djvu.txt')
    cam = cam[cam.index('Ao verme'):] if 'Ao verme' in cam else cam
    mdn = fontes.machadodeassis_net(OBRA, OBRA, 5985)
    return {
        'mdn': abertura_1896(dedicatoria_primeiro(mdn), prologo=False),
        'mec': dedicatoria_primeiro(fontes.texto_por_linhas(mec, cab)),
        'cam': dedicatoria_primeiro(fontes.texto_por_linhas(cam, cab)),
    }
