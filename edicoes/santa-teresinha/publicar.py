"""Santa Teresinha — publica as traduções no site.

Lê edicoes/santa-teresinha/traducao/ (e o francês de original/) e grava:
  conteudo/santa-teresinha/indice.js   obras e partes (títulos), carregado com o site;
  conteudo/santa-teresinha/<obra>.js   texto traduzido e original francês de cada parte,
                                       carregado só quando a obra é aberta (BIBLIOTECA.textos).
Uma obra só entra quando a tradução dela está completa.

Uso: python edicoes/santa-teresinha/publicar.py [obra ...]
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, '..', '..'))
TRAD = os.path.join(AQUI, 'traducao')
ORIG = os.path.join(AQUI, 'original')
DESTINO = os.path.join(RAIZ, 'conteudo', 'santa-teresinha')
sys.path.insert(0, os.path.join(RAIZ, 'ferramentas'))
from edicao import montar  # noqa: E402
from obras import JUNTAR, OBRAS, PARTES_MANUSCRITOS  # noqa: E402

PALAVRA = re.compile(r"[^\W_]+(?:[-'’][^\W_]+)*")
MARCA = re.compile(r'\{Ms ([A-C]) (\d+[rv]?)\}')
MARCA_FR = re.compile(r'^\[\[Ms ([A-C]) (\d+[rv]?)\]\]$')


# ------------------------------------------------------------------ leitura

def ler(arq):
    """-> (cabeçalho {chave: valor}, corpo)"""
    cab, corpo = {}, []
    linhas = open(arq, encoding='utf-8').read().replace('\r', '').split('\n')
    i = 0
    while i < len(linhas) and (linhas[i].startswith('# ') or not linhas[i].strip()):
        m = re.match(r'# ([\w-]+):\s?(.*)$', linhas[i])
        if m:
            cab[m.group(1).lower()] = m.group(2).strip()
        i += 1
    corpo = '\n'.join(linhas[i:]).strip()
    return cab, corpo


def paragrafos(corpo):
    return [p.strip() for p in re.split(r'\n\s*\n', corpo) if p.strip()]


def palavras(textos):
    n = 0
    for t in textos:
        t = MARCA.sub(' ', t)
        t = re.sub(r'^[|@#]+ ?', '', t, flags=re.M).replace('_', ' ').replace('*', ' ')
        n += len(PALAVRA.findall(t))
    return n


def sem_url(corpo):
    """Tira do original o que é do site dos Arquivos, não de Teresa: endereços, códigos de galeria,
    legendas de link («Lire ici...»), notas dos editores marcadas com asterisco."""
    fora = ('http', 'carmeldelisieux', '{gallery}', 'Lire ici')
    linhas = [l for l in corpo.split('\n') if not any(x in l for x in fora) and not l.startswith('_*')]
    return '\n'.join(linhas).strip()


def linhas_em_paragrafos(corpo):
    """Cartas e orações seguem as linhas do original (o site dos Arquivos quebra os parágrafos com
    <br>): cada linha vira um parágrafo; versos seguidos («| ») ficam juntos numa estrofe."""
    blocos, verso = [], []
    for l in corpo.split('\n'):
        if l.startswith('|'):
            verso.append(l)
            continue
        if verso:
            blocos.append('\n'.join(verso))
            verso = []
        if l.strip():
            blocos.append(l.strip())
    if verso:
        blocos.append('\n'.join(verso))
    return '\n\n'.join(blocos)


# ------------------------------------------------------------------ manuscritos

def manuscritos():
    """Junta os trechos traduzidos, divide nas partes de PARTES_MANUSCRITOS e casa cada parágrafo
    com o do francês. Devolve (partes, avisos) ou None se faltar tradução."""
    pasta = os.path.join(TRAD, 'manuscritos')
    trad = {}
    for ms, trechos in (('A', ['ms-a-1', 'ms-a-2', 'ms-a-3', 'ms-a-4']), ('B', ['ms-b']), ('C', ['ms-c-1', 'ms-c-2'])):
        corpo = ''
        for t in trechos:
            arq = os.path.join(pasta, t + '.txt')
            if not os.path.exists(arq):
                return None
            texto = ler(arq)[1].strip()
            m = re.match(r'\{Ms ([A-C]) (\d+[rv]?)\}', texto)
            if corpo and m and f'{m.group(1)} {m.group(2)}' in JUNTAR:
                # a frase atravessa a virada entre dois trechos: um parágrafo só, com a marca dentro
                corpo = corpo.rstrip() + ' ' + re.sub(r'^(\{Ms [A-C] \d+[rv]?\})\s*\n\s*\n', r'\1 ', texto)
            else:
                corpo = (corpo.rstrip() + '\n\n' if corpo else '') + texto
        trad[ms] = corpo
    avisos = []
    pt = {ms: unidades_pt(trad[ms]) for ms in trad}
    fr = {ms: unidades_fr(open(os.path.join(ORIG, 'manuscritos', f'ms-{ms.lower()}.txt'), encoding='utf-8').read(), pt[ms]) for ms in trad}
    for ms in trad:
        if len(fr[ms]) != len(pt[ms]):
            raise SystemExit(f'Ms {ms}: {len(pt[ms])} parágrafos na tradução e {len(fr[ms])} no francês; '
                             'confira com conferir.py e acerte os parágrafos antes de publicar')
    # começo de cada parte: o parágrafo francês que começa pelo texto dado (a tradução tem os
    # mesmos parágrafos, na mesma ordem)
    inicios, ultimo = [], {}
    for ms, comeco, n, titulo in PARTES_MANUSCRITOS:
        a_partir = ultimo.get(ms, -1) + 1
        if not comeco:
            i = 0
        else:
            i = next((j for j in range(a_partir, len(fr[ms])) if sem_marca(fr[ms][j]['texto']).startswith(comeco)), None)
            if i is None:
                raise SystemExit(f'Ms {ms}: começo de parte não encontrado: {comeco!r}')
        ultimo[ms] = i
        inicios.append((ms, i, n, titulo))
    partes = []
    for k, (ms, i0, n, titulo) in enumerate(inicios):
        i1 = inicios[k + 1][1] if k + 1 < len(inicios) and inicios[k + 1][0] == ms else len(pt[ms])
        partes.append({'n': n, 'titulo': titulo,
                       'texto': '\n\n'.join(u['texto'] for u in pt[ms][i0:i1]),
                       'original': '\n\n'.join(u['texto'] for u in fr[ms][i0:i1]),
                       'folhas': f"{folha_de(pt[ms][i0]) if pt[ms][i0]['texto'].startswith('{Ms') else folha_ant(pt[ms], i0)}"
                                 f"–{folha_fim(pt[ms], i1)}"})
    return partes, avisos


def sem_marca(s):
    return MARCA.sub('', s).strip()


def folha_ant(unidades, i):
    """Folha em que está o começo do parágrafo i (a última marca antes dele)."""
    for u in reversed(unidades[:i]):
        if u['folhas']:
            return u['folhas'][-1].split(' ', 1)[1]
    return ''


def unidades_pt(corpo):
    """Parágrafos da tradução; a marca de folha sozinha numa linha passa para o começo do parágrafo
    seguinte. Cada unidade guarda as folhas que começam nela."""
    out, pend = [], []
    for p in paragrafos(corpo):
        if MARCA.fullmatch(p):
            pend.append(p)
            continue
        texto = ' '.join(pend + [p]) if pend else p
        out.append({'texto': texto, 'folhas': [f'{a} {b}' for a, b in MARCA.findall(texto)], 'abre': bool(pend)})
        pend = []
    return out


def unidades_fr(bruto, pt):
    """Parágrafos do francês, juntados nas viradas de folha como a tradução juntou: se na tradução
    a marca está dentro do parágrafo, o parágrafo francês partido pela folha vira um só."""
    dentro = set()
    for u in pt:
        for f in u['folhas']:
            if not u['texto'].startswith('{Ms ' + f + '}'):
                dentro.add(f)
    linhas = [l for l in bruto.replace('\r', '').split('\n') if not l.startswith('# ')]
    blocos = paragrafos('\n'.join(linhas))
    out, pend = [], None
    for b in blocos:
        m = MARCA_FR.match(b)
        if m:
            f = f'{m.group(1)} {m.group(2)}'
            if f in dentro and out:
                out[-1] = out[-1] + ' {Ms ' + f + '}'
                pend = 'junta'
            else:
                pend = '{Ms ' + f + '}'
            continue
        if pend == 'junta':
            out[-1] = out[-1] + ' ' + b
        elif pend:
            out.append(pend + ' ' + b)
        else:
            out.append(b)
        pend = None
    return [{'texto': t} for t in out]


def indice_inicio(unidades, folha, desvio):
    """Índice do parágrafo que abre uma parte: o (desvio+1)-ésimo parágrafo que começa na folha."""
    alvo = '{Ms ' + folha + '}'
    for i, u in enumerate(unidades):
        if alvo in u['texto']:
            j = i + (desvio if u['texto'].startswith(alvo) else desvio + 1)
            return j
    raise SystemExit(f'folha não encontrada na tradução: {folha}')


def folha_de(u):
    return u['folhas'][0].split(' ', 1)[1] if u['folhas'] else ''


def folha_fim(unidades, i1):
    for u in reversed(unidades[:i1]):
        if u['folhas']:
            return u['folhas'][-1].split(' ', 1)[1]
    return ''


# ------------------------------------------------------------------ cartas, orações

def cartas():
    pasta = os.path.join(TRAD, 'cartas')
    fontes = sorted(f for f in os.listdir(os.path.join(ORIG, 'cartas')) if f.endswith('.txt'))
    if not os.path.isdir(pasta) or any(not os.path.exists(os.path.join(pasta, f)) for f in fontes):
        return None
    partes = []
    for f in fontes:
        cab, corpo = ler(os.path.join(pasta, f))
        cab_fr, corpo_fr = ler(os.path.join(ORIG, 'cartas', f))
        n = cab.get('carta') or 'LT ' + str(int(re.search(r'\d+', f).group())) + ('bis' if 'bis' in f else '')
        titulo = ' · '.join(x for x in (cab.get('destinatario', ''), cab.get('data', '')) if x)
        partes.append({'n': n, 'titulo': titulo, 'texto': linhas_em_paragrafos(corpo),
                       'original': linhas_em_paragrafos(sem_url(corpo_fr)),
                       'tituloOriginal': re.sub(r'^LT\s*\d+\w*\s*[–-]\s*', '', cab_fr.get('titulo', '')).replace(' – ', ' · ')})
    return partes, []


def oracoes():
    pasta = os.path.join(TRAD, 'oracoes')
    fontes = sorted(f for f in os.listdir(os.path.join(ORIG, 'oracoes')) if f.endswith('.txt'))
    if not os.path.isdir(pasta) or any(not os.path.exists(os.path.join(pasta, f)) for f in fontes):
        return None
    partes = []
    for f in fontes:
        cab, corpo = ler(os.path.join(pasta, f))
        cab_fr, corpo_fr = ler(os.path.join(ORIG, 'oracoes', f))
        n = cab.get('oracao') or 'Pri ' + str(int(re.search(r'\d+', f).group()))
        partes.append({'n': n, 'titulo': cab.get('titulo', ''), 'texto': linhas_em_paragrafos(corpo),
                       'original': linhas_em_paragrafos(sem_url(corpo_fr)),
                       'tituloOriginal': re.sub(r'^Pri\s*\d+\s*[–-]\s*', '', cab_fr.get('titulo', ''))})
    return partes, []


# ------------------------------------------------------------------ poesias e recreações

def estrofes_site(corpo):
    """Versos simples (um por linha, estrofes por linha em branco) -> formato da Biblioteca."""
    return '\n\n'.join('\n'.join('| ' + l.strip() for l in e.split('\n') if l.strip()) for e in paragrafos(corpo))


def abertura(cab):
    """Linhas que antecedem os versos: dedicatória e ária (em itálico)."""
    linhas = []
    if cab.get('dedicatoria'):
        linhas.append('_' + cab['dedicatoria'].strip('_') + '_')
    if cab.get('aria'):
        linhas.append('(' + ('Ária' if not cab['aria'].lower().startswith(('air', 'ária')) else '') +
                      (': ' if not cab['aria'].lower().startswith(('air', 'ária')) else '') + cab['aria'] + ')')
    return linhas


def fecho(cab):
    return ['_' + cab[k].strip('_') + '_' for k in ('assinatura', 'data') if cab.get(k)]


def poesias():
    pasta = os.path.join(TRAD, 'poesias')
    fontes = sorted(f[:-4] for f in os.listdir(os.path.join(ORIG, 'poesias')) if f.endswith('.txt'))
    if not os.path.isdir(pasta) or any(not os.path.exists(os.path.join(pasta, s, 'traducao.txt')) for s in fontes):
        return None
    def chave(s):
        m = re.match(r'(pn|ps)-(\d+)(bis)?', s)
        return (m.group(1) == 'ps', int(m.group(2)), m.group(3) or '')
    partes = []
    for s in sorted(fontes, key=chave):
        cab, corpo = ler(os.path.join(pasta, s, 'traducao.txt'))
        cab_fr, corpo_fr = ler(os.path.join(pasta, s, 'original.txt'))
        t = abertura(cab) + [estrofes_site(corpo)] + fecho(cab)
        o = abertura(cab_fr) + [estrofes_site(corpo_fr)] + fecho(cab_fr)
        sigla = cab.get('sigla') or s.upper().replace('-', ' ')
        partes.append({'n': re.sub(r'\b0(\d)', r'\1', sigla), 'titulo': cab.get('titulo', ''), 'tituloOriginal': cab_fr.get('titulo', ''),
                       'texto': '\n\n'.join(x for x in t if x), 'original': '\n\n'.join(x for x in o if x)})
    return partes, []


def recreacoes():
    pasta = os.path.join(TRAD, 'recreacoes')
    if not os.path.isdir(pasta) or any(not os.path.exists(os.path.join(pasta, f'rp-{n}', 'traducao.txt')) for n in range(1, 9)):
        return None
    partes = []
    for n in range(1, 9):
        cab, corpo = ler(os.path.join(pasta, f'rp-{n}', 'traducao.txt'))
        cab_fr, corpo_fr = ler(os.path.join(pasta, f'rp-{n}', 'original.txt'))
        partes.append({'n': f'RP {n}', 'titulo': cab.get('titulo', ''), 'tituloOriginal': cab_fr.get('titulo', ''),
                       'texto': corpo, 'original': corpo_fr})
    return partes, []


# ------------------------------------------------------------------ gravação

def js(v):
    return json.dumps(v, ensure_ascii=False)


def publicar(nomes):
    os.makedirs(DESTINO, exist_ok=True)
    feitas = {}
    for obra in OBRAS:
        if nomes and obra['id'] not in nomes:
            continue
        r = globals()[obra['fonte']]()
        if r is None:
            print('ainda incompleta:', obra['id'])
            continue
        partes, avisos = r
        for a in avisos:
            print('  aviso:', a)
        feitas[obra['id']] = (obra, partes)
        arq = f"conteudo/santa-teresinha/{obra['id']}.js"
        mapa = {obra['id']: {'t': [p['texto'] for p in partes], 'o': [p.get('original') for p in partes],
                             'e': obra['edicao']}}
        with open(os.path.join(RAIZ, arq), 'w', encoding='utf-8') as f:
            f.write(f"/* {obra['titulo']} — Santa Teresinha, em tradução. Gerado por edicoes/santa-teresinha/publicar.py;\n"
                    "   não edite à mão. t: tradução de cada parte; o: original francês; e: página «Sobre». */\n")
            f.write('BIBLIOTECA.textos(' + js(mapa) + ');\n')
        print('publicada:', obra['id'], len(partes), 'partes')
    # o índice traz todas as obras prontas (as já publicadas antes continuam)
    indice = os.path.join(DESTINO, 'indice.js')
    antigas = {}
    if os.path.exists(indice):
        for m in re.finditer(r'BIBLIOTECA\.obra\((\{.*?\})\);\n', open(indice, encoding='utf-8').read(), re.S):
            o = json.loads(m.group(1))
            antigas[o['id']] = o
    for oid, (obra, partes) in feitas.items():
        antigas[oid] = {
            'id': oid, 'autor': 'santa-teresinha', 'titulo': obra['titulo'], 'subtitulo': obra.get('subtitulo'),
            'ano': obra['ano'], 'datas': obra.get('datas'), 'genero': obra['genero'], 'divisao': obra['divisao'],
            'traducao': obra['traducao'], 'descricao': obra.get('descricao'),
            'arquivo': f'conteudo/santa-teresinha/{oid}.js', '_palavras': palavras([p['texto'] for p in partes]),
            'partes': [{k: v for k, v in (('n', p['n']), ('titulo', p['titulo']), ('tituloOriginal', p.get('tituloOriginal')),
                                          ('folhas', p.get('folhas'))) if v is not None} for p in partes],
        }
    ordem = [o['id'] for o in OBRAS]
    with open(indice, 'w', encoding='utf-8') as f:
        f.write('/* Santa Teresinha: obras em tradução (índice). Gerado por edicoes/santa-teresinha/publicar.py;\n'
                '   o texto de cada obra fica em conteudo/santa-teresinha/<obra>.js e só é carregado quando a obra é aberta. */\n\n')
        for oid in sorted(antigas, key=lambda x: ordem.index(x) if x in ordem else 99):
            o = {k: v for k, v in antigas[oid].items() if v is not None}
            f.write('BIBLIOTECA.obra(' + js(o) + ');\n')
    if montar.registrar_no_index(os.path.join(RAIZ, 'index.html'), 'conteudo/santa-teresinha/indice.js'):
        print('acrescentado ao index.html')


if __name__ == '__main__':
    publicar(sys.argv[1:])
