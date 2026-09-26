"""Limpeza do OCR de um fac-símile com a ajuda de transcrições limpas (de outra edição, se preciso).

Só se trocam palavras que NÃO existem no léxico das guias (resíduo de OCR: «sens», «Gatumby»,
«memó rias»), e só por uma palavra parecida alinhada no mesmo ponto. Palavras válidas que
diferem (revisões do autor entre uma edição e outra) ficam intactas.
"""
from .grafia import chave
from .tokens import achatar, alinhar, e_palavra, texto


def _dist(a, b):
    if a == b:
        return 0
    if abs(len(a) - len(b)) > 3:
        return 99
    ant = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(ant[j] + 1, cur[j - 1] + 1, ant[j - 1] + (ca != cb)))
        ant = cur
    return ant[-1]


def _limite(k):
    return 1 if len(k) <= 4 else 2 if len(k) <= 8 else 3


def obra_de_tokens(toks):
    """Inverso de tokens.achatar()."""
    obra, parte, estado, atual = [], None, None, []

    def fecha():
        nonlocal atual
        if parte is not None and (atual or estado == 'titulo'):
            s = texto([t for t in atual])
            if estado == 'titulo':
                parte['titulo'] = s
            elif s:
                parte['paras'].append(s)
        atual = []

    for t in toks:
        if t == '¶':
            fecha()
            estado = 'titulo' if estado == 'num' else 'corpo'
            continue
        if t.startswith('#'):
            atual = []
            parte = {'n': t[1:], 'titulo': '', 'paras': []}
            obra.append(parte)
            estado = 'num'
            continue
        atual.append(t)
    fecha()
    return obra


def limpar(ocr, guias, lexico_extra=()):
    """ocr: obra (formato intermediário); guias: lista de obras limpas, em ordem de preferência.
    Devolve (obra limpa, número de trocas)."""
    T = achatar(ocr)
    lexico = {chave(w) for g in guias for w in achatar(g) if e_palavra(w)}
    lexico |= {chave(w) for w in lexico_extra}
    trocas = {}
    for g in guias:
        G = achatar(g)
        for tp, i1, i2, j1, j2 in alinhar(T, G, chave=chave):
            if tp != 'replace':
                continue
            velhos, novos = T[i1:i2], G[j1:j2]
            # 1:1
            if len(velhos) == len(novos):
                for k, (o, n) in enumerate(zip(velhos, novos)):
                    ko = chave(o)
                    if i1 + k in trocas or not e_palavra(o) or ko in lexico or not e_palavra(n):
                        continue
                    if _dist(ko, chave(n)) <= _limite(ko):
                        trocas[i1 + k] = [n]
            # palavra partida pelo OCR («memó rias») ou colada
            for k in range(len(velhos) - 1):
                a, b = velhos[k], velhos[k + 1]
                if not (e_palavra(a) and e_palavra(b)) or chave(a + b) not in lexico or i1 + k in trocas:
                    continue
                if chave(a) in lexico and chave(b) in lexico:
                    continue
                trocas[i1 + k] = [a + b]
                trocas[i1 + k + 1] = []
    novo = []
    for i, t in enumerate(T):
        novo.extend(trocas.get(i, [t]))
    return obra_de_tokens(novo), sum(1 for v in trocas.values() if v)


def paragrafos_como(obra, base):
    """Dá ao OCR as quebras de parágrafo da base: o OCR junta falas de diálogo e parágrafos
    partidos pela página, e dois OCRs juntos venceriam a base no voto."""
    from .tokens import _mapeador
    T = [t for t in achatar(obra) if t != '¶']
    B = achatar(base)
    B2, quebras = [], []
    for t in B:
        if t == '¶':
            quebras.append(len(B2))
        else:
            B2.append(t)
    mp = _mapeador(alinhar([chave(t) for t in B2], [chave(t) for t in T]))
    em = sorted({mp(q, True) for q in quebras})
    out, k = [], 0
    for i, t in enumerate(T):
        while k < len(em) and em[k] <= i:
            if not out or out[-1] != '¶':
                out.append('¶')
            k += 1
        if t.startswith('#') and (not out or out[-1] != '¶'):
            out.append('¶')
        out.append(t)
        if t.startswith('#'):
            out.append('¶')
    return obra_de_tokens(out)


def estrutura_como(obra, base):
    """Dá a um testemunho a divisão da base inteira — partes (#), títulos e parágrafos —,
    ignorando a dele. Para textos em que a divisão não vem legível no OCR (diários, com
    datas soltas no meio da página) ou vem diferente nas edições modernas."""
    from .tokens import _mapeador
    T = [t for t in achatar(obra) if t != '¶' and not t.startswith('#')]
    B2, marcas = [], []
    for t in achatar(base):
        if t == '¶' or t.startswith('#'):
            marcas.append((len(B2), t))
        else:
            B2.append(t)
    mp = _mapeador(alinhar([chave(t) for t in B2], [chave(t) for t in T]))
    onde = [(mp(p, True), k, t) for k, (p, t) in enumerate(marcas)]
    onde.sort()
    out, k = [], 0
    for i, t in enumerate(T):
        while k < len(onde) and onde[k][0] <= i:
            out.append(onde[k][2]); k += 1
        out.append(t)
    out += [m[2] for m in onde[k:]]
    return obra_de_tokens(out)
