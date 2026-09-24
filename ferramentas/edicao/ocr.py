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
