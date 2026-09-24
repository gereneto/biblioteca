"""Tokens, alinhamento de testemunhos e pontos de divergência.

Formato intermediário de uma obra (saída dos leitores de fontes):
  [{'n': 'I', 'titulo': 'Do título.', 'paras': ['...', '\\x03verso\\nverso', ...]}, ...]
  - parágrafo começado por \\x03 é bloco de versos (linhas separadas por \\n);
  - itálico entre sublinhados: _assim_.

Fluxo de tokens: '¶' separa parágrafos, '#<n>' marca o início de uma parte,
'/' separa linhas de verso, '_' abre/fecha itálico.
"""
import bisect
import re
from collections import Counter
from difflib import SequenceMatcher

TOK = re.compile(r"\.{2,}|[^\W_]+(?:['’\-~][^\W_]+)*|[—–]|_|[^\w\s]", re.U)
PALAVRA = re.compile(r"^[^\W_]")
VERSO = '\u0003'


def e_palavra(t):
    return bool(PALAVRA.match(t)) and not t.startswith('#')


def tokens_do_paragrafo(p):
    out = []
    p = p.lstrip(VERSO)
    for i, linha in enumerate(p.split('\n')):
        if i:
            out.append('/')
        out.extend(TOK.findall(linha))
    return out


def achatar(obra, com_titulos=True):
    """Lista de tokens da obra inteira."""
    toks = []
    for parte in obra:
        if com_titulos:
            toks += ['¶', '#' + parte['n'], '¶']
            toks += tokens_do_paragrafo(parte.get('titulo') or '')
        for p in parte['paras']:
            toks.append('¶')
            toks += tokens_do_paragrafo(p)
    return toks


# ------------------------------------------------------------------ alinhamento

def _lis(pares):
    """Maior subsequência crescente em j (pares ordenados por i)."""
    caudas, idx, ant = [], [], [None] * len(pares)
    for k, (i, j) in enumerate(pares):
        pos = bisect.bisect_left(caudas, j)
        if pos == len(caudas):
            caudas.append(j); idx.append(k)
        else:
            caudas[pos] = j; idx[pos] = k
        ant[k] = idx[pos - 1] if pos else None
    out, k = [], idx[-1] if idx else None
    while k is not None:
        out.append(pares[k]); k = ant[k]
    return out[::-1]


def _ancoras(A, B, n):
    ga = Counter(tuple(A[i:i + n]) for i in range(len(A) - n + 1))
    gb = Counter(tuple(B[i:i + n]) for i in range(len(B) - n + 1))
    posb = {}
    for j in range(len(B) - n + 1):
        g = tuple(B[j:j + n])
        if gb[g] == 1:
            posb[g] = j
    pares = []
    for i in range(len(A) - n + 1):
        g = tuple(A[i:i + n])
        if ga[g] == 1 and g in posb:
            pares.append((i, posb[g]))
    return _lis(pares)


def _alinhar_rec(A, B, a0, b0, prof=0):
    if not A and not B:
        return []
    if len(A) * len(B) <= 250000 or prof > 3:
        sm = SequenceMatcher(None, A, B, autojunk=False)
        return [(t, i1 + a0, i2 + a0, j1 + b0, j2 + b0) for t, i1, i2, j1, j2 in sm.get_opcodes()]
    anc = _ancoras(A, B, 6 if prof == 0 else 3)
    if not anc:
        sm = SequenceMatcher(None, A, B, autojunk=False)
        return [(t, i1 + a0, i2 + a0, j1 + b0, j2 + b0) for t, i1, i2, j1, j2 in sm.get_opcodes()]
    ops, pi, pj = [], 0, 0
    for i, j in anc:
        if i < pi or j < pj:
            continue
        ops += _alinhar_rec(A[pi:i], B[pj:j], a0 + pi, b0 + pj, prof + 1)
        ops.append(('equal', a0 + i, a0 + i + 1, b0 + j, b0 + j + 1))
        pi, pj = i + 1, j + 1
    ops += _alinhar_rec(A[pi:], B[pj:], a0 + pi, b0 + pj, prof + 1)
    return ops


def alinhar(a, b, chave=lambda x: x):
    """Alinha duas listas de tokens; opcodes no formato do SequenceMatcher, 'equal' fundidos."""
    A = [chave(x) for x in a]
    B = [chave(x) for x in b]
    unidos = []
    for op in _alinhar_rec(A, B, 0, 0):
        if op[1] == op[2] and op[3] == op[4]:
            continue
        if unidos and unidos[-1][0] == op[0] == 'equal' and unidos[-1][2] == op[1] and unidos[-1][4] == op[3]:
            unidos[-1] = ('equal', unidos[-1][1], op[2], unidos[-1][3], op[4])
        else:
            unidos.append(op)
    return unidos


# ------------------------------------------------------------------ divergências

def _mapeador(ops):
    inicios = [o[1] for o in ops]

    def m(b, baixo):
        c = []
        k = max(0, bisect.bisect_left(inicios, b) - 1)
        while k > 0 and ops[k - 1][2] >= b:
            k -= 1
        for t, i1, i2, j1, j2 in ops[k:]:
            if i1 > b:
                break
            if i1 <= b <= i2:
                if t == 'equal':
                    c.append(j1 + (b - i1))
                else:
                    if b == i1:
                        c.append(j1)
                    if b == i2:
                        c.append(j2)
        return min(c) if baixo else max(c)
    return m


def divergencias(base, opss):
    """Pontos em que algum testemunho diverge da base.
    Devolve [(s, e, [(j1, j2) por testemunho])] em fronteiras da base."""
    iv = sorted([i1, i2] for ops in opss for t, i1, i2, j1, j2 in ops if t != 'equal')
    unidos = []
    for a, b in iv:
        if unidos and a <= unidos[-1][1]:
            unidos[-1][1] = max(unidos[-1][1], b)
        else:
            unidos.append([a, b])
    mps = [_mapeador(o) for o in opss]
    return [(s, e, [(mp(s, True), mp(e, False)) for mp in mps]) for s, e in unidos]


def texto(toks):
    """Junta tokens em texto legível (para relatórios)."""
    s = ''
    for t in toks:
        if s and not re.match(r'^[,.;:!?»)…]|^\.\.', t) and not s.endswith(('«', '(')):
            s += ' '
        s += t
    return s
