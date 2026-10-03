"""Santa Teresinha — baixa os textos franceses dos Arquivos do Carmelo de Lisieux.

Fonte: https://archives.carmeldelisieux.fr (texto da Nouvelle Édition du Centenaire). O site tem
uma API WordPress: as cartas e as poesias vêm no corpo do post; os manuscritos, as orações e as
recreações vêm folha a folha, num JSON embutido na página (#json-cahiers).

Saída: edicoes/santa-teresinha/original/<obra>/<item>.txt, em texto simples:
  - linhas «# chave: valor» no topo (titulo, fonte, data...);
  - parágrafos separados por linha em branco;
  - versos: uma linha por verso, estrofes separadas por linha em branco;
  - nos manuscritos, «[[Ms A 2r]]» marca o começo de cada folha.

Uso: python edicoes/santa-teresinha/baixar.py
"""
import html
import json
import os
import re
import sys
import time
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, 'original')
CACHE = os.path.join(AQUI, '..', '..', 'ferramentas', 'cache', 'santa-teresinha')
SITE = 'https://archives.carmeldelisieux.fr'
API = SITE + '/wp-json/wp/v2'

TIPOS = {'manuscrit': 1279, 'poesies': 1274, 'prieres': 1282, 'recreations-pieuses': 1290}


def baixar(url, nome):
    os.makedirs(CACHE, exist_ok=True)
    arq = os.path.join(CACHE, nome)
    if os.path.exists(arq):
        return open(arq, encoding='utf-8').read()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (biblioteca de dominio publico)'})
    for tentativa in range(4):
        try:
            dado = urllib.request.urlopen(req, timeout=120).read().decode('utf-8')
            break
        except Exception as e:                      # noqa: BLE001
            if tentativa == 3:
                raise
            print('  de novo:', url, e)
            time.sleep(5)
    open(arq, 'w', encoding='utf-8').write(dado)
    time.sleep(0.5)
    return dado


def texto(h):
    """HTML -> texto: <p> e <div> separam blocos; <br> quebra linha; <em>/<u> viram _itálico_."""
    h = re.sub(r'<(script|style)\b.*?</\1>', '', h, flags=re.S)
    h = re.sub(r'\s+', ' ', h)                  # quebras de linha do HTML não contam
    h = re.sub(r'<(em|i|u)\b[^>]*>(.*?)</\1>', lambda m: '_' + m.group(2) + '_' if m.group(2).strip() else m.group(2), h, flags=re.S)
    h = re.sub(r'<br\s*/?>', '\n', h)
    h = re.sub(r'</(p|h\d|li|blockquote)>', '\n\n', h)
    h = re.sub(r'<(p|h\d|li|blockquote)\b[^>]*>', '\n\n', h)   # o site antigo abre <p> sem fechar
    h = re.sub(r'</div>', '\n', h)              # versos vêm em <div> seguidos
    h = re.sub(r'<[^>]+>', '', h)
    h = html.unescape(h).replace('\xa0', ' ').replace(' ', ' ')
    linhas = [re.sub(r'[ \t]+', ' ', l).strip() for l in h.split('\n')]
    t = '\n'.join(linhas)
    t = re.sub(r'_\s*_', '', t)
    return re.sub(r'\n{3,}', '\n\n', t).strip()


def cahiers(slug):
    pag = baixar(f'{SITE}/archive/{slug}/', f'pagina_{slug}.html')
    m = re.search(r'id="json-cahiers"[^>]*>(.*?)</script>', pag, re.S)
    return json.loads(m.group(1)) if m else []


def folhas(slug, sigla=None):
    """Texto de cada folha (recto e verso), na ordem."""
    out = []
    for f in cahiers(slug):
        tit = (f.get('page_title') or '').strip()
        for lado, campo in (('r', 'content_one'), ('v', 'content_two')):
            t = texto(f.get(campo) or '')
            if not t:
                continue
            marca = f'[[{tit}{lado}]]' if sigla and tit else ''
            out.append((marca, t))
    return out


def lista(tipo):
    itens, pagina = [], 1
    while True:
        dado = baixar(f'{API}/archive?type_archive={TIPOS[tipo]}&per_page=100&page={pagina}',
                      f'api_{tipo}_{pagina}.json')
        lote = json.loads(dado)
        if not isinstance(lote, list) or not lote:
            break
        itens += lote
        if len(lote) < 100:
            break
        pagina += 1
    return itens


def gravar(obra, nome, cab, corpo):
    pasta = os.path.join(SAIDA, obra)
    os.makedirs(pasta, exist_ok=True)
    linhas = [f'# {k}: {v}' for k, v in cab.items() if v]
    corpo = re.sub(r'\n{3,}', '\n\n', corpo)
    open(os.path.join(pasta, nome + '.txt'), 'w', encoding='utf-8').write('\n'.join(linhas) + '\n\n' + corpo.strip() + '\n')


def titulo(x):
    return html.unescape(re.sub(r'<[^>]+>', '', x['title']['rendered'])).strip()


def manuscritos():
    for x in lista('manuscrit'):
        letra = x['slug'][-1].upper()
        partes = []
        for marca, t in folhas(x['slug'], sigla=True):
            partes.append(marca.replace(' 0', ' ') + '\n\n' + t)
        gravar('manuscritos', f'ms-{letra.lower()}', {'titulo': titulo(x), 'fonte': x['link']}, '\n\n'.join(partes))
        print('manuscrito', letra, len(partes), 'páginas')


def sigla_de(t, prefixo):
    m = re.search(prefixo + r'\s*0*(\d+)\s*(bis)?', t, re.I)
    return (int(m.group(1)), m.group(2) or '') if m else (999, '')


def oracoes():
    for x in lista('prieres'):
        n, _ = sigla_de(titulo(x), 'Pri')
        corpo = '\n\n'.join(t for _, t in folhas(x['slug'])) or texto(x['content']['rendered'])
        extra = texto(x['content']['rendered']) if folhas(x['slug']) else ''
        gravar('oracoes', f'pri-{n:02d}', {'titulo': titulo(x), 'fonte': x['link'], 'apresentacao': extra.replace('\n', ' ')}, corpo)
    print('orações ok')


NUM_LINHA = re.compile(r'(^|(?<=[\s.,;:!?»)]))(\d*[05])\s(?=[A-Za-zÀ-ÿ«_\[(])', re.M)


def sem_numeracao(t, log):
    """Tira a numeração de linhas da edição crítica (5, 10, 15... no começo ou no meio da linha)
    e os números de estrofe sozinhos numa linha."""
    def tira(m):
        log.append(m.group(0).strip())
        return m.group(1)
    t = NUM_LINHA.sub(tira, t)
    return re.sub(r'(?m)^\d{1,2}\.?\n', '', t)


def recreacoes():
    log = []
    for x in lista('recreations-pieuses'):
        n, _ = sigla_de(titulo(x), 'RP')
        corpo = sem_numeracao('\n\n'.join(t for _, t in folhas(x['slug'])), log)
        gravar('recreacoes', f'rp-{n}', {'titulo': titulo(x), 'fonte': x['link'],
                                          'apresentacao': texto(x['content']['rendered']).replace('\n', ' | ')}, corpo)
    print('recreações ok; números de linha retirados:', len(log), sorted(set(log), key=lambda s: int(re.match(r'\d+', s).group()))[:80])


def antigo(pagina):
    """Página do site antigo dos Arquivos (archives-carmel-lisieux.fr), pelo Wayback Machine."""
    url = f'https://web.archive.org/web/2019id_/http://www.archives-carmel-lisieux.fr/carmel/index.php/{pagina}'
    s = baixar(url, 'antigo_' + pagina.replace('/', '_') + '.html')
    i = s.find('<div class="content">')
    s = s[i:]
    for fim in ('View the embedded image gallery', 'sigProGalleria', '<div id="sidebar', 'Plus d\'articles'):
        j = s.find(fim)
        if j > 0:
            s = s[:j]
    s = re.sub(r'<[^>]*$', '', s)                # etiqueta cortada no fim
    return texto(s)


def antigo_opcional(pagina):
    try:
        return antigo(pagina)
    except Exception:                               # noqa: BLE001
        return ''


def manuscritos_antigos():
    """Os manuscritos pelo site antigo: o novo corta o texto de muitas folhas (ex.: Ms A 45r para
    em «mes souliers d», sem o episódio do Natal de 1886). Uma página por lado de folha."""
    def faixa(n):
        for a, b in ((2, 10), (11, 20), (21, 30), (31, 40), (41, 50), (51, 60), (61, 70), (71, 80), (81, 86)):
            if a <= n <= b:
                return f'{a:02d}-{b}'
    def lados_a(n):
        base = f'{faixa(n)}/{n:02d}'
        r, v = antigo_opcional(f'{base}/{n:02d}-recto'), antigo_opcional(f'{base}/{n:02d}-verso')
        return [('r', r), ('v', v)] if (r or v) else [('', antigo_opcional(base))]
    def lados_c(n):
        g = '01-10' if n <= 10 else '11-20' if n <= 20 else '21-30' if n <= 30 else '31-37'
        base = f'c{g}/c{n:02d}'
        return [('r', antigo_opcional(f'{base}/c{n:02d}r')), ('v', antigo_opcional(f'{base}/c{n:02d}v'))]
    def lados_b(n):
        return [('r', antigo_opcional(f'b{n:02d}/b{n:02d}r')), ('v', antigo_opcional(f'b{n:02d}/b{n:02d}v'))]
    for letra, folhas_, lados in (('a', range(2, 87), lados_a), ('b', range(1, 6), lados_b), ('c', range(1, 38), lados_c)):
        partes, faltam = [], []
        for n in folhas_:
            for lado, t in lados(n):
                if not t.strip():
                    faltam.append(f'{n}{lado}')
                    continue
                partes.append(f'[[Ms {letra.upper()} {n}{lado}]]\n\n{t}')
        gravar('manuscritos-site-antigo', f'ms-{letra}', {'titulo': f'Manuscrit {letra.upper()}',
               'fonte': 'web.archive.org: archives-carmel-lisieux.fr', 'faltam': ' '.join(faltam)}, '\n\n'.join(partes))
        print('manuscrito antigo', letra, len(partes), 'lados; faltam:', faltam)


def completar_manuscritos():
    """Lacunas do site novo, preenchidas pelo antigo (a continuidade das frases confirma a ordem):
    - Ms C 8r falta, e o texto da 8v aparece com o número 8r («Ma Mère chérie, je suis tout
      étonnée...» fica de fora);
    - Ms C 26v falta («il faut qu'elles puissent dire ce qu'elles pensent...»); no site antigo, a
      página da 26r traz esse texto e a da 26v repete-o, então ele é tirado da página da 26r.
    - Ms A 59v traz três parágrafos repetidos: ficam uma vez só."""
    def blocos(arq):
        t = open(arq, encoding='utf-8').read()
        p = re.split(r'^(\[\[Ms [A-C] \d+[rv]?\]\])$', t, flags=re.M)
        return p[0], [(p[i], p[i + 1].strip()) for i in range(1, len(p), 2)]
    novo = os.path.join(SAIDA, 'manuscritos', 'ms-c.txt')
    antigo = dict(blocos(os.path.join(SAIDA, 'manuscritos-site-antigo', 'ms-c.txt'))[1])
    cab, bl = blocos(novo)
    marcas = [m for m, _ in bl]
    if '[[Ms C 8v]]' not in marcas:
        k = marcas.index('[[Ms C 8r]]')
        bl[k] = ('[[Ms C 8v]]', bl[k][1])
        bl.insert(k, ('[[Ms C 8r]]', antigo['[[Ms C 8r]]']))
        marcas = [m for m, _ in bl]
    if '[[Ms C 26v]]' not in marcas:
        k = marcas.index('[[Ms C 26r]]')
        bl.insert(k + 1, ('[[Ms C 26v]]', antigo['[[Ms C 26r]]']))
    open(novo, 'w', encoding='utf-8').write(cab.rstrip() + '\n\n' + '\n\n'.join(m + '\n\n' + t for m, t in bl) + '\n')
    # lado cortado no fim (ex.: C 27r para em «qui tombent de la»): se o texto do site antigo
    # começa pelo do novo e vai além, fica o do antigo
    def chave(s):
        return re.sub(r"[^\w']+", ' ', s.lower().replace('’', "'")).strip()
    for ms in 'abc':
        arq = os.path.join(SAIDA, 'manuscritos', f'ms-{ms}.txt')
        velho = dict(blocos(os.path.join(SAIDA, 'manuscritos-site-antigo', f'ms-{ms}.txt'))[1])
        cab, bl = blocos(arq)
        for k, (m, t) in enumerate(bl):
            v = velho.get(m)
            if v and len(chave(v)) > len(chave(t)) + 10 and chave(v).startswith(chave(t)[:-3]):
                print('  lado completado pelo site antigo:', m)
                bl[k] = (m, v)
        open(arq, 'w', encoding='utf-8').write(cab.rstrip() + '\n\n' + '\n\n'.join(m + '\n\n' + t for m, t in bl) + '\n')
    arq_a = os.path.join(SAIDA, 'manuscritos', 'ms-a.txt')
    cab, bl = blocos(arq_a)
    for k, (m, t) in enumerate(bl):
        if m == '[[Ms A 59v]]':
            ps = re.split(r'\n\s*\n', t)
            vistos, out = set(), []
            for x in ps:
                if len(x) > 80 and x in vistos:
                    continue
                vistos.add(x)
                out.append(x)
            bl[k] = (m, '\n\n'.join(out))
    open(arq_a, 'w', encoding='utf-8').write(cab.rstrip() + '\n\n' + '\n\n'.join(m + '\n\n' + t for m, t in bl) + '\n')
    print('manuscritos completados (C 8r, C 26v; A 59v sem repetição)')


def poesias_antigas():
    """Segundo testemunho das poesias: o site antigo (o novo truncou ao menos uma estrofe)."""
    nomes = [f'pn-{n}' for n in range(1, 55)] + ['pn-18bis'] + [f'ps-{n}' for n in range(1, 9)]
    for p in nomes:
        try:
            t = antigo(p)
        except Exception as e:                      # noqa: BLE001
            print('  sem página antiga:', p, e)
            continue
        m = re.match(r'(pn|ps)-(\d+)(bis)?', p)
        gravar('poesias-site-antigo', f'{m.group(1)}-{int(m.group(2)):02d}{m.group(3) or ""}',
               {'fonte': 'web.archive.org: archives-carmel-lisieux.fr/carmel/index.php/' + p}, t)
    print('poesias do site antigo ok')


def poesias():
    for x in lista('poesies'):
        t = titulo(x)
        if t.startswith('-'):
            continue                                    # páginas de índice
        m = re.search(r'\b(PN|PS)\s*0*(\d+)\s*(bis)?', t)
        if not m:
            print('  sem sigla:', t)
            continue
        nome = f'{m.group(1).lower()}-{int(m.group(2)):02d}{m.group(3) or ""}'
        corpo = texto(x['content']['rendered'])
        f = folhas(x['slug'])
        if f and len(' '.join(c for _, c in f).split()) > len(corpo.split()) * 0.8:
            corpo = '\n\n'.join(c for _, c in f) + '\n\n' + corpo   # versos nas folhas, notas no corpo
        gravar('poesias', nome, {'titulo': t, 'fonte': x['link']}, corpo)
    print('poesias ok')


def cartas():
    itens, pagina = [], 1
    while True:
        lote = json.loads(baixar(f'{API}/correspondance?per_page=100&page={pagina}', f'api_cartas_{pagina}.json'))
        if not isinstance(lote, list) or not lote:
            break
        itens += lote
        if len(lote) < 100:
            break
        pagina += 1
    n_lt = 0
    for x in itens:
        t = titulo(x)
        # «LT 031 / LT 031 A» e «LT 031 B» são duas cartas; «LT 167 bis» também é outra
        m = re.match(r'LT\s*0*(\d+)\s*(?:/\s*LT\s*0*\d+\s*A\b)?\s*(bis|B\b)?', t)
        if not m:
            continue
        nome = f'lt-{int(m.group(1)):03d}{(m.group(2) or "").lower()}'
        gravar('cartas', nome, {'titulo': t, 'fonte': x['link']}, texto(x['content']['rendered']))
        n_lt += 1
    print('cartas:', n_lt)


if __name__ == '__main__':
    o = sys.argv[1:] or ['manuscritos', 'manuscritos_antigos', 'completar_manuscritos', 'oracoes', 'recreacoes',
                         'poesias', 'poesias_antigas', 'cartas']
    for f in o:
        globals()[f]()
