"""Confronto das transcrições da edição-base e escolha da leitura em cada divergência.

Regras (as mesmas usadas em Dom Casmurro):
- divergências só de grafia miúda (acento, consoante dobrada) não contam: a grafia final
  vem da modernização;
- havendo maioria entre as transcrições, vale a maioria; mas se a maioria for de testemunhos
  aparentados (mesmo OCR de origem) e a minoria tiver mais apoio nas edições modernas,
  vale a minoria;
- sem maioria, vale a leitura com mais apoio nas edições modernas; empate, a da base.
Cada escolha fica registrada; as fracas (sem apoio moderno) vão para revisão.

Testemunho ruidoso (OCR de fac-símile, parâmetro `ruidoso`): quando nenhuma leitura tem apoio
moderno, mas as modernas concordam entre si (a principal e ao menos mais uma) e a leitura
ruidosa está claramente mais perto delas do que a escolhida, vale a leitura moderna: é o texto
do fac-símile lido através do ruído. Essas escolhas ficam marcadas para conferência.

Lacunas: trechos em que um testemunho não tem texto (tokens.LACUNA) não geram divergência e,
ali, o testemunho não vota.
"""
import bisect
from collections import Counter
from difflib import SequenceMatcher

from .grafia import chave, esqueleto, mesma_palavra
from .tokens import LACUNA, achatar, alinhar, divergencias, e_palavra, mapear, texto

IGNORAR = ('_', '*')


def _k(toks):
    return tuple(chave(t) for t in toks if t not in IGNORAR)


def _zonas_lacuna(ops, T):
    """Trechos da base (i1, i2) em que o testemunho T é lacunoso: a operação que contém a
    lacuna e as vizinhas até a primeira concordância longa (5 tokens) de cada lado."""
    zonas = []
    for k, (t, i1, i2, j1, j2) in enumerate(ops):
        if t == 'equal' or LACUNA not in T[j1:j2]:
            continue
        a = k
        while a > 0 and not (ops[a - 1][0] == 'equal' and ops[a - 1][2] - ops[a - 1][1] >= 5):
            a -= 1
        b = k
        while b + 1 < len(ops) and not (ops[b + 1][0] == 'equal' and ops[b + 1][2] - ops[b + 1][1] >= 5):
            b += 1
        zonas.append((ops[a][1], ops[b][2]))
    return zonas


def _toca(zonas, s, e):
    return any(zs <= e and s <= ze for zs, ze in zonas)


def _contexto(toks, palavras):
    """Chaves dos tokens até completar `palavras` palavras (a pontuação no meio vai junto)."""
    out, n = [], 0
    for t in toks:
        if t in IGNORAR:
            continue
        out.append(chave(t))
        n += e_palavra(t)
        if n == palavras:
            return out
    return []


class _Moderna:
    """Texto moderno com índice de chaves, para achar a leitura correspondente pelo contexto
    (o alinhamento sozinho erra quando há mais de um modo de alinhar o trecho)."""

    def __init__(self, toks, ops, flexivel=False):
        self.M = toks
        self.ops = ops
        self.flexivel = flexivel          # contexto tolerante a grafia (monarchica ~ monárquica)
        self.idx = [i for i, t in enumerate(toks) if t not in IGNORAR]
        self.chaves = [chave(toks[i]) for i in self.idx]

    def leitura(self, B, s, e, margem=25):
        a, b = mapear(self.ops, s, e)
        fa = bisect.bisect_left(self.idx, a)
        fb = bisect.bisect_left(self.idx, b)
        lo, hi = max(0, fa - margem), min(len(self.chaves), fb + margem)
        for palavras in (3, 2):
            antes = _contexto(reversed(B[max(0, s - 20):s]), palavras)[::-1]
            depois = _contexto(B[e:e + 20], palavras)
            if not antes or not depois:
                continue
            na, nd = len(antes), len(depois)
            fins = [p + na for p in range(lo, hi - na + 1) if self._casa(self.chaves[p:p + na], antes)]
            inis = [q for q in range(lo, hi - nd + 1) if self._casa(self.chaves[q:q + nd], depois)]
            pares = [(p, q) for p in fins for q in inis if q >= p]
            if pares:
                p, q = min(pares, key=lambda x: abs(x[0] - fa) + abs(x[1] - fb))
                ip = self.idx[p] if p < len(self.idx) else len(self.M)
                iq = self.idx[q] if q < len(self.idx) else len(self.M)
                return self.M[ip:iq]
        return self.M[a:b]


    def _casa(self, a, b):
        if a == b:
            return True
        if not self.flexivel or len(a) != len(b):
            return False
        return all(x == y or (len(x) > 3 and SequenceMatcher(None, x, y).ratio() >= 0.75) for x, y in zip(a, b))


def _aspas(anteriores, trecho):
    """Aspas retas ou curvas de um trecho vindo de edição moderna viram as angulares do texto:
    fecha («...») se há uma aberta antes no mesmo parágrafo; senão, abre."""
    aberta = False
    for t in reversed(anteriores):
        if t == '¶':
            break
        if t in ('«', '»'):
            aberta = t == '«'
            break
    out = []
    for t in trecho:
        if t in ('"', '“', '”'):
            t = '»' if aberta else '«'
            aberta = not aberta
        elif t in ('«', '»'):
            aberta = t == '«'
        out.append(t)
    return out


def _aponta(r, esc, km):
    """A leitura ruidosa r está claramente mais perto da moderna km do que a escolhida esc?"""
    def dist(x, y):
        a, b = ' '.join(x), ' '.join(y)
        sm = SequenceMatcher(None, a, b, autojunk=False)
        return sm.ratio(), len(a) + len(b) - 2 * sum(m.size for m in sm.get_matching_blocks())
    pr, dr = dist(r, km)
    pe, de = dist(esc, km)
    if pr >= 0.5 and pr > pe + 0.1:
        return True
    if dr * 5 < de and dr <= 20:          # supressão longa: no ruidoso sobra só lixo curto
        return True
    return dr <= max(3, 0.6 * len(' '.join(km))) and dr * 2 < de     # trechos curtos


def estabelecer(transcricoes, base, modernas, correlacionados=(), ruidoso=None, um_voto=False, lexico=False):
    """transcricoes/modernas: dict nome -> obra. Devolve (tokens, sítios)."""
    nomes_t = [base] + [n for n in transcricoes if n != base]
    T = {n: achatar(transcricoes[n]) for n in nomes_t}
    B = T[base]
    outros = nomes_t[1:]
    ops_t = [alinhar(B, T[n]) for n in outros]
    zonas = {n: _zonas_lacuna(ops, T[n]) for n, ops in zip(outros, ops_t)}
    nomes_m = list(modernas)
    M = {}
    for n in nomes_m:
        toks = achatar(modernas[n])
        M[n] = _Moderna(toks, alinhar(B, toks, chave=chave), flexivel=lexico)
    corr = [set(c) for c in correlacionados]
    # desempate pelo léxico: sem maioria nem apoio, vence a leitura com menos palavras que
    # não existem nas edições modernas (erros de digitação ou de OCR)
    lex = {esqueleto(t) for n in nomes_m for t in M[n].M if e_palavra(t)} if lexico else None

    def desconhecidas(toks):
        return sum(1 for t in toks if e_palavra(t) and esqueleto(t) not in lex) if lex else 0

    sitios = []
    # os pontos de divergência vêm só das transcrições; as modernas apenas dão apoio
    for s, e, spans in divergencias(B, ops_t, [zonas[n] for n in outros]):
        leit = {base: B[s:e]}
        for n, (a, b) in zip(outros, spans):
            if not _toca(zonas[n], s, e):        # testemunho lacunoso aqui: não vota
                leit[n] = T[n][a:b]
        if len({_k(v) for v in leit.values()}) == 1:
            continue
        votantes = [n for n in nomes_t if n in leit]
        mods = {n: M[n].leitura(B, s, e) for n in nomes_m}
        grupos = {}
        for n in votantes:
            grupos.setdefault(_k(leit[n]), []).append(n)
        apoio = {k: [m for m in nomes_m if _k(mods[m]) == k] for k in grupos}
        if um_voto:        # testemunhos aparentados valem um voto só
            def votos(ns):
                return len({min((i for i, c in enumerate(corr) if n in c), default=n) for n in ns})
        else:
            votos = len
        maior = max(grupos.values(), key=votos)
        if votos(maior) * 2 > votos(votantes):
            k_mai = _k(leit[maior[0]])
            escolha, por = k_mai, 'maioria (' + '='.join(maior) + ')'
            if any(set(maior) <= c for c in corr):
                rival = max((k for k in grupos if k != k_mai), key=lambda k: len(apoio[k]))
                if len(apoio[rival]) > len(apoio[k_mai]):
                    escolha, por = rival, 'minoria com apoio moderno (' + '='.join(grupos[rival]) + ')'
        else:
            ordem = sorted(grupos, key=lambda k: (-len(apoio[k]), desconhecidas(leit[grupos[k][0]]),
                                                  min(nomes_t.index(n) for n in grupos[k])))
            escolha = ordem[0]
            por = 'sem maioria; ' + '='.join(grupos[escolha])
        escolha_tokens = leit[grupos[escolha][0]]
        sup = apoio[escolha]
        if ruidoso in leit and not any(apoio.values()):
            # ninguém tem apoio: a leitura ruidosa aponta para a das modernas?
            gm = {}
            for m in nomes_m:
                gm.setdefault(_k(mods[m]), []).append(m)
            km = _k(mods[nomes_m[0]])
            r = _k(leit[ruidoso])
            if len(gm[km]) >= 2 and r != escolha and _aponta(r, escolha, km):
                escolha_tokens = [t for t in mods[nomes_m[0]] if t != '*']
                por = f'moderna lida no {ruidoso} (' + '='.join(gm[km]) + ')'
                sup = gm[km]
        sitios.append({
            's': s, 'e': e,
            'leituras': {n: texto(leit[n]) if n in leit else '(lacuna)' for n in nomes_t},
            'modernas': {n: texto(mods[n]) for n in nomes_m},
            'escolha': escolha_tokens, 'escolha_txt': texto(escolha_tokens), 'por': por,
            'apoio': sup,
            'duvida': not sup or por.startswith('moderna'),
            'antes': texto(B[max(0, s - 8):s]), 'depois': texto(B[e:e + 8]),
        })

    E, pos = [], 0
    for x in sitios:
        E.extend(B[pos:x['s']])
        E.extend(x['escolha'])
        pos = x['e']
    E.extend(B[pos:])
    E = [t for t in E if t != '*']
    limpo, i = [], 0
    while i < len(E):
        if E[i] == '[' and i + 2 < len(E) and E[i + 1] == 'sic' and E[i + 2] == ']':
            i += 3; continue
        limpo.append(E[i]); i += 1
    return limpo, sitios


def resumo(sitios):
    return Counter(x['por'].split(' (')[0] for x in sitios)


# ------------------------------------------------------------------ segunda passada (edição-base só em OCR)

def revisar_pelo_ruidoso(E, ruidoso, moderna, folga=4):
    """Onde o texto difere da moderna principal e o testemunho ruidoso (a edição-base lida por
    OCR) confirma a moderna, vale a moderna. Pega as revisões da edição-base que o confronto
    trecho a trecho perde: passagens reescritas, cortadas ou acrescentadas.
    A comparação é por palavras; o trecho adotado vai de uma palavra comum à seguinte, com a
    pontuação da moderna. Devolve (E, registro)."""
    def filtrado(toks):
        idx = [i for i, t in enumerate(toks) if e_palavra(t) or t.startswith('#')]
        return idx, [chave(toks[i]) for i in idx]

    R, M = achatar(ruidoso), achatar(moderna)
    Ei, kE = filtrado(E)
    Mi, kM = filtrado(M)
    _, kR = filtrado(R)
    opsM, opsR = alinhar(kE, kM), alinhar(kE, kR)
    regioes = []
    for s, e, [(a, b)] in divergencias(kE, [opsM]):
        if regioes and s - regioes[-1][1] < folga and a - regioes[-1][3] < folga:
            regioes[-1][1], regioes[-1][3] = e, b          # trechos quase contíguos: uma região só
        else:
            regioes.append([s, e, a, b])
    novo, pos, reg = [], 0, []
    for s, e, a, b in regioes:
        em, mm = kE[s:e], kM[a:b]
        x, y = mapear(opsR, s, e)
        rr = kR[x:y]
        if rr == em or em == mm:
            continue
        if not (rr == mm or _aponta(rr, em, mm)):
            continue
        # de logo depois da palavra comum anterior até a palavra comum seguinte
        i0 = Ei[s - 1] + 1 if s else 0
        i1 = Ei[e] if e < len(Ei) else len(E)
        j0 = Mi[a - 1] + 1 if a else 0
        j1 = Mi[b] if b < len(Mi) else len(M)
        trecho = ['—' if t == '-' else t for t in M[j0:j1] if t not in IGNORAR]
        trecho = _aspas(E[max(0, i0 - 400):i0], trecho)
        novo.extend(E[pos:i0])
        novo.extend(trecho)
        pos = i1
        reg.append({'antes': texto(E[max(0, i0 - 8):i0]), 'de': texto(E[i0:i1]), 'para': texto(trecho),
                    'ruidoso': ' '.join(rr), 'depois': texto(E[i1:i1 + 6]), 'i': i0})
    novo.extend(E[pos:])
    return novo, reg


# ------------------------------------------------------------------ edição revista só nas modernas

# normalizações editoriais das edições modernas que não são lições do autor
EXPANSOES = {('s', 'sao'), ('d', 'dom'), ('d', 'dona'), ('cap', 'capitulo'), ('sr', 'senhor'), ('sra', 'senhora'),
             ('srs', 'senhores'), ('dr', 'doutor'), ('v', 'vossa'), ('exa', 'excelencia'), ('mr', 'm')}


def _semelhanca(x, y):
    return SequenceMatcher(None, ' '.join(x), ' '.join(y), autojunk=False).ratio()


def _editorial(em, mm, ew=None, mw=None):
    """Diferença que não é lição: abreviatura, número por extenso ou só grafia (creado/criado,
    em quanto/enquanto). em/mm: chaves; ew/mw: as palavras."""
    if ew is not None and mw is not None and ew and mw:
        if mesma_palavra(''.join(ew), ''.join(mw)):
            return True
        if len(ew) == len(mw) and all(mesma_palavra(a, b) or (chave(a), chave(b)) in EXPANSOES or a.isdigit()
                                      for a, b in zip(ew, mw)):
            return True
    if len(em) != len(mm):
        return False
    return all(a == b or (a, b) in EXPANSOES or a.isdigit() for a, b in zip(em, mm))


def adotar_modernas(E, modernas, folga=4):
    """Onde TODAS as edições modernas (a primeira é a principal) concordam contra o texto em
    palavras, vale a leitura delas: é a edição revista pelo autor que só elas transmitem.
    Diferenças só de abreviatura ou de número por extenso não contam. Devolve (E, registro)."""
    def filtrado(toks):
        idx = [i for i, t in enumerate(toks) if e_palavra(t) or t.startswith('#')]
        return idx, [chave(toks[i]) for i in idx]

    Ms = [achatar(m) for m in modernas]
    Ei, kE = filtrado(E)
    fM = [filtrado(M) for M in Ms]
    ops = [alinhar(kE, k) for _, k in fM]
    (Mi, kM), M = fM[0], Ms[0]
    regioes = []
    for s, e, [(a, b)] in divergencias(kE, [ops[0]]):
        if regioes and s - regioes[-1][1] < folga and a - regioes[-1][3] < folga:
            regioes[-1][1], regioes[-1][3] = e, b
        else:
            regioes.append([s, e, a, b])
    novo, pos, reg = [], 0, []
    for s, e, a, b in regioes:
        em, mm = kE[s:e], kM[a:b]
        if em == mm or _editorial(em, mm, [E[i] for i in Ei[s:e]], [M[j] for j in Mi[a:b]]):
            continue
        outras = []
        for (_, k), o in zip(fM[1:], ops[1:]):
            x, y = mapear(o, s, e)
            outras.append(k[x:y])
        sem_hifen = lambda ks: ''.join(ks).replace('-', '')
        iguais = [r for r in outras if sem_hifen(r) == sem_hifen(mm)]
        # todas concordam; ou a maioria concorda e quem discorda tem só um erro de digitação
        if len(iguais) < len(outras):
            if (len(iguais) + 1) * 2 <= len(outras) + 1:
                continue
            if any(_semelhanca(r, mm) <= _semelhanca(r, em) for r in outras if r not in iguais):
                continue
        i0 = Ei[s - 1] + 1 if s else 0
        i1 = Ei[e] if e < len(Ei) else len(E)
        j0 = Mi[a - 1] + 1 if a else 0
        j1 = Mi[b] if b < len(Mi) else len(M)
        trecho = ['—' if t == '-' else t for t in M[j0:j1] if t not in IGNORAR]
        trecho = _aspas(E[max(0, i0 - 400):i0], trecho)
        novo.extend(E[pos:i0])
        novo.extend(trecho)
        pos = i1
        reg.append({'antes': texto(E[max(0, i0 - 8):i0]), 'de': texto(E[i0:i1]), 'para': texto(trecho),
                    'depois': texto(E[i1:i1 + 6]), 'i': i0, 'parte': _parte(E, i0)})
    novo.extend(E[pos:])
    return novo, reg


def _parte(E, i):
    k = max((j for j in range(i) if E[j].startswith('#')), default=None)
    return E[k][1:] if k is not None else None
