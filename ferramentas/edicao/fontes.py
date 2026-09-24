"""Leitores de fontes: cada um devolve a obra no formato intermediário (ver tokens.py).

Os arquivos baixados ficam em ferramentas/cache/<obra>/ (fora do git).
"""
import html
import json
import os
import re
import subprocess
import unicodedata

from . import rede
from .tokens import LACUNA, VERSO

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../ferramentas


def cache(obra, nome):
    return os.path.join(RAIZ, 'cache', obra, nome)


def nfc(s):
    return unicodedata.normalize('NFC', s)


def limpar(p):
    p = p.replace(' ', ' ')
    p = re.sub(r'[ \t]+', ' ', p)
    p = re.sub(r' *\n *', '\n', p)
    return p.strip()


def normalizar(obra):
    return [{'n': nfc(str(c['n'])), 'titulo': nfc(c.get('titulo') or ''),
             'paras': [nfc(p) for p in c['paras'] if p.strip(VERSO).strip()]} for c in obra]


# ------------------------------------------------------------------ texto com cabeçalhos

def partir_por_cabecalhos(blocos, cabecalhos, titulo_seguinte=True, verso_indentado=True):
    """blocos: lista de strings (parágrafos crus, com \\n internos).
    cabecalhos: lista de regex; o grupo 'n' dá o rótulo da parte e o grupo 't' (opcional) o título.
    Se titulo_seguinte, o bloco depois do cabeçalho (sem 't') é o título."""
    obra, atual, espera_titulo = [], None, False
    rx = [re.compile(c) for c in cabecalhos]
    for b in blocos:
        bs = b.strip()
        if not bs:
            continue
        m = None
        if '\n' not in bs:
            for r in rx:
                m = r.match(bs)
                if m:
                    break
        if m:
            gd = m.groupdict()
            if 'n' in gd:
                n = gd['n'] or ''
            else:
                n = '' if 't' in gd else bs          # cabeçalho sem número (Prólogo, Ao leitor...)
            atual = {'n': n.strip(), 'titulo': (gd.get('t') or '').strip(), 'paras': []}
            obra.append(atual)
            espera_titulo = titulo_seguinte and not gd.get('t')
            continue
        if atual is None:
            continue
        if espera_titulo:
            atual['titulo'] = bs.replace('\n', ' ')
            espera_titulo = False
            continue
        linhas = [l for l in b.split('\n') if l.strip()]
        if verso_indentado and linhas and all(l.startswith('  ') for l in linhas):
            atual['paras'].append(VERSO + '\n'.join(l.strip() for l in linhas))
        else:
            atual['paras'].append(limpar(bs.replace('\n', ' ')))
    return obra


# ------------------------------------------------------------------ Projeto Gutenberg

def gutenberg(obra_id, pg_id, cabecalhos, inicio=None, fim=None, titulo_seguinte=True, trocar=None):
    """Lê o texto do Projeto Gutenberg. `inicio`/`fim`: trechos que delimitam o corpo."""
    bruto = rede.baixar(f'https://www.gutenberg.org/cache/epub/{pg_id}/pg{pg_id}.txt',
                        cache(obra_id, f'pg{pg_id}.txt')).decode('utf-8')
    s = bruto.replace('\r', '')
    s = s.split('*** START OF THE PROJECT GUTENBERG EBOOK', 1)[1].split('\n', 1)[1]
    s = s.split('*** END OF THE PROJECT GUTENBERG EBOOK')[0]
    if inicio:
        s = s[s.index(inicio):]
    if fim:
        s = s[:s.rindex(fim)]
    s = re.sub(r'\[(?:Illustra[^\]]*|Ilustra[^\]]*)\]', '', s)
    s = s.replace('--', '—')
    for a, b in (trocar or []):
        s = s.replace(a, b)
    return normalizar(partir_por_cabecalhos(re.split(r'\n\s*\n', s), cabecalhos, titulo_seguinte))


# ------------------------------------------------------------------ Wikisource (páginas revisadas)

def wikisource_paginas(obra_id, arquivo, primeira, ultima):
    """Baixa o texto das páginas 'Página:<arquivo>/<n>' e o estado de revisão de cada uma."""
    destino = cache(obra_id, 'wikisource_paginas.json')
    if os.path.exists(destino):
        return {int(k): v for k, v in json.load(open(destino, encoding='utf-8')).items()}
    titulos = [f'Página:{arquivo}/{n}' for n in range(primeira, ultima + 1)]
    out = {}
    for i in range(0, len(titulos), 50):
        d = rede.wikisource_api({'action': 'query', 'titles': '|'.join(titulos[i:i + 50]),
                                 'prop': 'revisions|proofread', 'rvprop': 'content', 'rvslots': 'main'})
        for p in d['query']['pages'].values():
            n = int(p['title'].rsplit('/', 1)[1])
            if 'revisions' in p:
                out[n] = {'qualidade': p.get('proofread', {}).get('quality'),
                          'texto': p['revisions'][0]['slots']['main']['*']}
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    json.dump(out, open(destino, 'w', encoding='utf-8'), ensure_ascii=False)
    return out


CLITICOS = {'me', 'te', 'se', 'lhe', 'lhes', 'nos', 'vos', 'o', 'a', 'os', 'as', 'lo', 'la', 'los', 'las',
            'no', 'na', 'nas', 'mo', 'ma', "lh'o", "lh'a", "m'o", 'hia', 'ha', 'hei', 'hão', 'ia', 'iam', 'ei'}


def _juntar_hifen(a, b):
    m = re.match(r"[\w']+", b)
    frag = m.group(0).lower() if m else ''
    if frag in CLITICOS:
        return a + b
    return a[:-1] + b.lstrip('-')


def _expandir_modelos(t):
    t = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', t)                                  # [[alvo|texto]]
    t = re.sub(r'\|\s*(?:fs|lh|align|largura[\w-]*|width|style|class|margem[\w-]*|size|separador)\s*=\s*[^|}]*', '', t)
    t = re.sub(r'\{\{tabela\b.*?\n\}\}', '', t, flags=re.S)
    for _ in range(6):
        t = re.sub(r'\{\{pt\|[^|}]*\|([^|}]*)\}\}', r'\1', t, flags=re.I)
        t = re.sub(r'\{\{(?:fine|smaller|small|larger|x-larger|xx-larger|xxx-larger|xxxx-larger|sc|sc2|j|d|gap|c|C|ch|center|centro|Centralizado|direita)\|([^{}]*)\}\}',
                   lambda m: '\u0001C' + m.group(1) + '\u0002' if re.match(r'\{\{(c|C|ch|center|centro|Centralizado)\|', m.group(0)) else m.group(1), t)
        t = re.sub(r'\{\{(?:t2|T2|t3|T3)\|([^{}]*)\}\}', '\u0001C' + r'\1' + '\u0002', t)
        t = re.sub(r'\{\{Bloco centro\|(?:align=\w+\|)?([^{}]*)\}\}', '\n\n' + VERSO + r'\1' + '\n\n', t)
        t = re.sub(r'\{\{(?:dhr|lh|gap|nop|rule|extrair imagem|sic)(\|[^{}]*)?\}\}', lambda m: '\n\n' if 'nop' in m.group(0) else '', t)
        # demais modelos: fica o último argumento posicional ({{sb|Sterne}}, {{Reconstruído|...}})
        t = re.sub(r'\{\{([^{}]*)\}\}', _ultimo_argumento, t)
    t = re.sub(r'\{\{[^{}]*\}\}', '', t)
    return t


_MODELOS_TRATADOS = {'pt', 'Bloco centro', 'c', 'C', 'ch', 'center', 'centro', 'Centralizado', 't2', 'T2', 't3', 'T3',
                     'fine', 'smaller', 'small', 'larger', 'x-larger', 'xx-larger', 'xxx-larger', 'xxxx-larger',
                     'sc', 'sc2', 'j', 'd', 'gap', 'direita', 'dhr', 'lh', 'nop', 'rule', 'extrair imagem', 'sic'}


def _ultimo_argumento(m):
    partes = m.group(1).split('|')
    nome = partes[0].strip()
    if nome in _MODELOS_TRATADOS:
        return m.group(0)                  # tratado pelas regras específicas
    pos = [p for p in partes[1:] if '=' not in p]
    return pos[-1] if pos else ''


CAB_WS = r'^(?:CAP[IÍ]TULO\s+)?(?P<n>[IVXLC]+|PRIMEIRO)\.?$'


def wikisource(obra_id, arquivo, primeira, ultima, rom=CAB_WS, qualidade_minima=None):
    """Texto corrido das páginas; cabeçalhos (centrados ou soltos) que casam com `rom` viram partes.
    Com `qualidade_minima`, as páginas não revisadas viram lacunas (ver tokens.LACUNA)."""
    pags = wikisource_paginas(obra_id, arquivo, primeira, ultima)
    corpo = ''
    for n in range(primeira, ultima + 1):
        v = pags.get(n)
        if not v or v['qualidade'] == 0:
            continue
        if qualidade_minima and (v['qualidade'] or 0) < qualidade_minima:
            if not corpo.endswith(LACUNA + '\n\n'):
                corpo += '\n\n' + LACUNA + '\n\n'
            continue
        bruto = v['texto']
        t = re.sub(r'<noinclude>.*?</noinclude>', '', bruto, flags=re.S)
        t = t.replace('<nowiki />', '').replace('<nowiki/>', '')
        t = re.sub(r'\{\{(rh|RunningHeader|Cabeçalho)\|.*?\}\}\}?', '', t)
        t = t.strip('\n').rstrip()
        if re.search(r'\w-$', corpo) and not corpo.endswith('--'):
            corpo = _juntar_hifen(corpo, t.lstrip())
        else:
            sep = '\n\n' if bruto.split('</noinclude>', 1)[-1].startswith('\n\n') else '\n'
            corpo += sep + t
    t = _expandir_modelos(corpo)
    # blocos centrados de várias linhas (dedicatórias, epígrafes): sem linhas em branco por dentro
    t = re.sub('\u0001C(.*?)\u0002', lambda m: '\u0001C' + re.sub(r'\n\s*\n+', '\n', m.group(1)).strip() + '\u0002', t, flags=re.S)
    t = re.sub(r'\[sic\]', '', t)
    t = t.replace("'''", '')
    t = re.sub(r"''(.*?)''", r'_\1_', t, flags=re.S)
    t = re.sub(r'<br\s*/?>', '\u0004', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'(\S+-)\n(\S+)', lambda m: _juntar_hifen(m.group(1), m.group(2)), t)
    rx = re.compile(rom)
    obra, atual = [], None
    for bloco in re.split(r'\n\s*\n', t):
        for parte in re.split(r'(\u0001C.*?\u0002)', bloco.strip(), flags=re.S):
            parte = parte.strip()
            if not parte:
                continue
            centrado = parte.startswith('\u0001C')
            dentro = parte[2:-1].strip() if centrado else parte
            m = rx.match(dentro) if len(dentro) < 40 else None
            if m:
                n = m.groupdict().get('n') or dentro
                atual = {'n': 'I' if n == 'PRIMEIRO' else n, 'titulo': None, 'paras': []}
                obra.append(atual)
                continue
            if centrado:
                if atual is not None and atual['titulo'] is None and '\n' not in dentro.strip():
                    atual['titulo'] = dentro
                elif atual is not None:
                    atual['paras'].append(VERSO + '\n'.join(x.strip() for x in dentro.split('\n') if x.strip())
                                          if '\n' in dentro.strip() else limpar(dentro))
                else:
                    atual = {'n': '0', 'titulo': dentro, 'paras': []}
                    obra.append(atual)
                continue
            if atual is not None and atual['titulo'] is None and len(parte) < 80 and not atual['paras']:
                atual['titulo'] = parte.replace('\n', ' ')
                continue
            if atual is None:
                atual = {'n': '0', 'titulo': '', 'paras': []}
                obra.append(atual)
            if parte.startswith(VERSO) or '\u0004' in parte:
                p = re.sub(r'[ \t]+', ' ', parte.lstrip(VERSO).replace('\u0004', '\n'))
                atual['paras'].append(VERSO + '\n'.join(x.strip() for x in p.split('\n') if x.strip()))
            else:
                atual['paras'].append(limpar(parte.replace('\n', ' ')))
    return normalizar(obra)


# ------------------------------------------------------------------ machadodeassis.net

def machadodeassis_net(obra_id, slug, conteudo):
    """Todos os capítulos de um texto do machadodeassis.net (Fundação Casa de Rui Barbosa)."""
    destino = cache(obra_id, f'mdn_{conteudo}.json')
    if os.path.exists(destino):
        caps = json.load(open(destino, encoding='utf-8'))
    else:
        nav = {'User-Agent': 'Mozilla/5.0'}   # o site recusa agentes que não pareçam navegador
        pagina = rede.baixar(f'https://machadodeassis.net/texto/{slug}/{conteudo}',
                             cache(obra_id, f'mdn_{conteudo}.html'), cabecalhos=nav).decode('utf-8')
        ids = re.findall(r'data-order="(\d+)" data-size="\d+" data-id="(\d+)"', pagina)
        ids = sorted({(int(o), int(i)) for o, i in ids})
        corpo = b'--XX\r\nContent-Disposition: form-data; name="loaded_chapters"\r\n\r\n\r\n--XX--\r\n'
        vistos = {}
        for _, cid in ids:
            if cid in vistos:
                continue
            for c in rede.baixar_json(f'https://machadodeassis.net/capitulo/content_id/{conteudo}/chapter_id/{cid}',
                                      dados=corpo, cabecalhos=dict(nav, **{'Content-Type': 'multipart/form-data; boundary=XX'}),
                                      pausa=0.4):
                vistos[c['content_id']] = c
        if not ids:  # texto de um capítulo só
            m = re.search(r'textManager\.chapterManager\.gotoChapter\(\s*(\d+)', pagina)
            if m:
                for c in rede.baixar_json(f'https://machadodeassis.net/capitulo/content_id/{conteudo}/chapter_id/{m.group(1)}',
                                          dados=corpo, cabecalhos=dict(nav, **{'Content-Type': 'multipart/form-data; boundary=XX'})):
                    vistos[c['content_id']] = c
        caps = [vistos[i] for _, i in ids] if ids else list(vistos.values())
        json.dump(caps, open(destino, 'w', encoding='utf-8'), ensure_ascii=False)
    obra = []
    for c in caps:
        paras = []
        for m in re.finditer(r'<p[^>]*>(.*?)</p>', c['text'], re.S):
            p = re.sub(r'<br\s*/?>', '\n', m.group(1))
            p = re.sub(r'</?(i|em)>', '_', p)
            p = html.unescape(re.sub(r'<[^>]+>', '', p)).replace(' ', ' ')
            p = re.sub(r'[ \t]+', ' ', p).strip()
            p = re.sub(r'\s+([,.;:!?])', r'\1', p)
            if p:
                paras.append(p)
        obra.append({'n': (c.get('title') or '').strip(), 'titulo': (c.get('subtitle') or '').strip(), 'paras': paras})
    return normalizar(obra)


# ------------------------------------------------------------------ PDF / texto simples

def pdf_texto(obra_id, url, nome):
    """Baixa um PDF e extrai o texto com pdftotext (Git Bash / poppler)."""
    pdf = cache(obra_id, nome + '.pdf')
    txt = cache(obra_id, nome + '.txt')
    if not os.path.exists(txt):
        rede.baixar(url, pdf, cabecalhos={'User-Agent': 'Mozilla/5.0'})
        subprocess.run(['pdftotext', '-enc', 'UTF-8', pdf, txt], check=True)
    return open(txt, encoding='utf-8').read()


def texto_por_linhas(s, cabecalhos, titulo_seguinte=False):
    """Texto em que cada linha é um parágrafo (PDFs modernos); junta parágrafos cortados por página."""
    s = s.replace('\f', '\n')
    linhas = [l.strip() for l in s.split('\n')]
    linhas = [l for l in linhas if l and not re.fullmatch(r'\d+', l)]
    blocos = []
    for l in linhas:
        if blocos and (re.match(r'^[a-zà-ÿ]', l) or
                       (not re.search(r'[.!?:»"”…)\-—]$', blocos[-1]) and not re.match(r'^[—\-]', l)
                        and not any(re.match(c, l) for c in cabecalhos) and not any(re.match(c, blocos[-1]) for c in cabecalhos))):
            blocos[-1] += ' ' + l
        else:
            blocos.append(l)
    return normalizar(partir_por_cabecalhos(blocos, cabecalhos, titulo_seguinte, verso_indentado=False))


def internet_archive(obra_id, item, arquivo):
    """Texto de um item do Internet Archive (arquivo _djvu.txt ou PDF com texto)."""
    import urllib.parse
    url = f'https://archive.org/download/{item}/{urllib.parse.quote(arquivo)}'
    if arquivo.lower().endswith('.pdf'):
        return pdf_texto(obra_id, url, 'ia_' + item)
    return rede.baixar(url, cache(obra_id, f'ia_{item}.txt')).decode('utf-8', errors='replace')
