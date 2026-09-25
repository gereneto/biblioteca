"""Intervenções no texto-base e atualização ortográfica palavra por palavra.

A grafia moderna de cada palavra vem das edições de referência (na ordem dada; a primeira
costuma ser o machadodeassis.net, já no Acordo de 1990) e só é aceita quando é a MESMA
palavra (esqueleto igual). Depois, as formas antigas de palavras atuais passam à forma de
hoje (grafia.FORMAS_ATUAIS: cousa -> coisa, dous -> dois...).
"""
from .grafia import ao1990, chave, forma_atual, igualar_caixa, mesma_palavra
from .tokens import TOK, achatar, alinhar, e_palavra


def _toks(s):
    return TOK.findall(s) if s else []


def localizar(E, busca):
    b = busca if isinstance(busca, list) else _toks(busca)
    return [i for i in range(len(E) - len(b) + 1) if E[i:i + len(b)] == b]


def parte_em(E, i):
    """Rótulo da parte em que está o token i: o número, ou o título se a parte não tem número."""
    k = max((j for j in range(i) if E[j].startswith('#')), default=None)
    if k is None:
        return None
    if E[k][1:]:
        return E[k][1:]
    titulo = []
    for t in E[k + 2:]:                   # '#', '¶', título..., '¶'
        if t == '¶':
            break
        titulo.append(t)
    return ' '.join(titulo)


def aplicar_emendas(E, italico, emendas):
    """emendas: [(tipo, busca, troca)] na grafia do texto-base. Devolve (E, italico, registro).
    Em trechos longos, a busca pode ser 'começo […] fim' (do começo, único, ao primeiro fim)."""
    reg = []
    for tipo, busca, troca in emendas:
        t = _toks(troca)
        if '[…]' in busca:
            ini, fim = (_toks(x) for x in busca.split('[…]'))
            achados = localizar(E, ini)
            if len(achados) != 1:
                raise SystemExit(f'emenda {busca!r}: começo com {len(achados)} ocorrências no texto-base')
            i = achados[0]
            fins = [k for k in localizar(E[i:], fim)]
            if not fins:
                raise SystemExit(f'emenda {busca!r}: fim não encontrado')
            b = E[i:i + fins[0] + len(fim)]
        else:
            b = _toks(busca)
            achados = localizar(E, b)
            if len(achados) != 1:
                raise SystemExit(f'emenda {busca!r}: {len(achados)} ocorrências no texto-base')
            i = achados[0]
        reg.append({'tipo': tipo, 'parte': parte_em(E, i), 'de': busca, 'para': troca})
        E = E[:i] + t + E[i + len(b):]
        italico = italico[:i] + [italico[i]] * len(t) + italico[i + len(b):]
    return E, italico, reg


def _emparelhar(velhos, novos):
    """Emparelha um bloco 'replace' de tamanhos diferentes (junções e separações de palavras)."""
    n, m = len(velhos), len(novos)
    if n * m > 3000:           # bloco grande demais (texto que não se corresponde): não emparelha
        return [(list(range(n)), [])] if n else []
    NEG = -10 ** 9
    melhor = [[NEG] * (m + 1) for _ in range(n + 1)]
    volta = [[None] * (m + 1) for _ in range(n + 1)]
    melhor[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if melhor[i][j] == NEG:
                continue
            for di, dj in ((1, 1), (1, 2), (2, 1), (1, 0), (0, 1), (1, 3), (3, 1)):
                if i + di > n or j + dj > m:
                    continue
                o, w = velhos[i:i + di], novos[j:j + dj]
                if di and dj:
                    ok = mesma_palavra(''.join(o), ''.join(w)) and all(e_palavra(t) for t in o + w)
                    if not ok and not (di == 1 and dj == 1):
                        continue
                    sc = 3 if ok else 0
                else:
                    sc = 0
                if melhor[i][j] + sc > melhor[i + di][j + dj]:
                    melhor[i + di][j + dj] = melhor[i][j] + sc
                    volta[i + di][j + dj] = (di, dj)
    pares, i, j = [], n, m
    while i or j:
        di, dj = volta[i][j]
        pares.append((list(range(i - di, i)), list(range(j - dj, j))))
        i -= di; j -= dj
    return pares[::-1]


def _mapa(E, M, ops):
    res = {}
    for t, i1, i2, j1, j2 in ops:
        if t == 'equal':
            for k in range(i2 - i1):
                res[i1 + k] = ((i1 + k,), (M[j1 + k],))
        elif t == 'replace':
            for vi, nj in _emparelhar(E[i1:i2], M[j1:j2]):
                grupo = tuple(i1 + x for x in vi)
                for g in grupo:
                    res[g] = (grupo, tuple(M[j1 + y] for y in nj))
    return res


def modernizar(E, referencias, manual=None):
    """referencias: [(nome, obra, pos_acordo: bool)]. Devolve (tokens, origem, relatorio)."""
    manual = manual or {}
    mapas = []
    for nome, obra, pos_acordo in referencias:
        M = [t for t in achatar(obra) if t != '_']
        mapas.append((nome, _mapa(E, M, alinhar(E, M, chave=chave)), (lambda x: x) if pos_acordo else ao1990))
    out, origem, rel = [], [], []
    i = 0
    while i < len(E):
        t = E[i]
        if not e_palavra(t):
            out.append(t); origem.append(i); i += 1
            continue
        escolha = None
        for nome, mp, ajuste in mapas:
            if i in mp:
                grupo, novo = mp[i]
                if grupo[0] != i:
                    continue
                if novo and mesma_palavra(''.join(E[g] for g in grupo), ''.join(novo)) and all(e_palavra(x) for x in novo):
                    escolha = (grupo, [ajuste(x) for x in novo], nome)
                    break
        if escolha is None:
            escolha = ((i,), manual[t].split(' '), 'manual') if t in manual else ((i,), [t], 'SEM_PAR')
        grupo, novo, fonte = escolha
        velho = ' '.join(E[g] for g in grupo)
        if velho in manual and fonte != 'manual':
            novo, fonte = manual[velho].split(' '), 'manual'
        novo = [igualar_caixa(E[grupo[0]], novo[0])] + novo[1:]
        novo = [forma_atual(x) for x in novo]          # cousa -> coisa, dous -> dois...
        rel.append((velho, ' '.join(novo), fonte, i))
        out.extend(novo)
        origem.extend([grupo[0]] * len(novo))
        i = grupo[-1] + 1
    return out, origem, rel


def ajustes_finais(out, flags, ajustes):
    """ajustes: [(antes, de, para, depois)] em tokens da grafia moderna, separados por espaço."""
    reg = []
    for antes, de, para, depois in ajustes:
        a, d, p, z = antes.split(), de.split(), para.split(), depois.split()
        pad = a + d + z
        achados = [i for i in range(len(out) - len(pad) + 1) if out[i:i + len(pad)] == pad]
        if len(achados) != 1:
            raise SystemExit(f'ajuste {antes!r} [{de}] {depois!r}: {len(achados)} ocorrências')
        i = achados[0] + len(a)
        out = out[:i] + p + out[i + len(d):]
        flags = flags[:i] + [False] * len(p) + flags[i + len(d):]
        reg.append({'parte': parte_em(out, i), 'antes': antes, 'de': de, 'para': para, 'depois': depois})
    return out, flags, reg


# ------------------------------------------------------------------ itálico por votação

def _palavras_italico(tokens):
    ws, fs, idx = [], [], []
    on = False
    for k, t in enumerate(tokens):
        if t == '¶':
            on = False
        if t == '_':
            on = not on
            continue
        if e_palavra(t):
            ws.append(t); fs.append(on); idx.append(k)
    return ws, fs, idx


def italico_por_votacao(E0, transcricoes, desempate=None):
    """Tira os '_' de E0 e marca, palavra a palavra, o itálico da maioria das transcrições.
    desempate: obra moderna usada quando só há dois votos divergentes. Devolve (E, flags)."""
    ws, _, idx = _palavras_italico(E0)
    votos = [[] for _ in ws]
    fontes = list(transcricoes.items()) + ([('_desempate', desempate)] if desempate else [])
    for nome, obra in fontes:
        w, f, _ = _palavras_italico(achatar(obra))
        for t, i1, i2, j1, j2 in alinhar(ws, w, chave=chave):
            if t == 'equal' or (t == 'replace' and i2 - i1 == j2 - j1):
                for k in range(i2 - i1):
                    votos[i1 + k].append((nome, f[j1 + k]))
    marca = []
    for v in votos:
        d = dict(v)
        prin = [d[n] for n in transcricoes if n in d]
        sim = sum(prin)
        if prin and sim * 2 != len(prin):
            marca.append(sim * 2 > len(prin))
        else:
            marca.append(bool(d.get('_desempate', sim > 0)))
    E, F, wi = [], [], 0
    idxset = set(idx)
    for k, t in enumerate(E0):
        if t == '_':
            continue
        E.append(t)
        if k in idxset:
            F.append(marca[wi]); wi += 1
        else:
            F.append(False)
    return E, F


# ------------------------------------------------------------------ pontuação da edição revista

_PONT_K = {'«': '"', '»': '"', '“': '"', '”': '"', '–': '—', '…': '...', '....': '...'}


def pontuacao_das_modernas(out, flags, modernas):
    """Onde todas as edições modernas pontuam igual entre si e diferente do texto (só pontuação,
    sem aspas nem hífens), vale a pontuação delas. Devolve (out, flags, registro)."""
    from .tokens import divergencias
    k = lambda t: _PONT_K.get(t, t).lower()
    fora = lambda t: t in ('_', '¶', '/') or t.startswith('#')
    idx = [i for i, t in enumerate(out) if not fora(t)]
    ours = [out[i] for i in idx]
    Ms = [[t for t in achatar(m) if not fora(t)] for m in modernas]
    opss = [alinhar(ours, M, chave=k) for M in Ms]
    trocas = []
    for s, e, spans in divergencias(ours, opss):
        base = [k(x) for x in ours[s:e]]
        ms = [[k(x) for x in M[a:b]] for M, (a, b) in zip(Ms, spans)]
        if not all(m == ms[0] for m in ms) or ms[0] == base:
            continue
        todos = base + ms[0]
        if any(e_palavra(x) or x in ('"', '-', "'", '(', ')') for x in todos):
            continue
        a, b = spans[0]
        trocas.append((s, e, Ms[0][a:b]))
    reg = []
    for s, e, novo in reversed(trocas):
        i0 = idx[s] if s < e else (idx[s - 1] + 1 if s else 0)
        i1 = idx[e - 1] + 1 if s < e else i0
        antes = ' '.join(t for t in out[max(0, i0 - 6):i0])
        depois = ' '.join(t for t in out[i1:i1 + 4])
        reg.append({'tipo': 'pontuacao', 'parte': parte_em(out, i0), 'antes': antes,
                    'de': ' '.join(out[i0:i1]), 'para': ' '.join(novo), 'depois': depois})
        out = out[:i0] + list(novo) + out[i1:]
        flags = flags[:i0] + [False] * len(novo) + flags[i1:]
    return out, flags, reg[::-1]
