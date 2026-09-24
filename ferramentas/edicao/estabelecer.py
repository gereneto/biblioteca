"""Confronto das transcrições da edição-base e escolha da leitura em cada divergência.

Regras (as mesmas usadas em Dom Casmurro):
- divergências só de grafia miúda (acento, consoante dobrada) não contam: a grafia final
  vem da modernização;
- havendo maioria entre as transcrições, vale a maioria; mas se a maioria for de testemunhos
  aparentados (mesmo OCR de origem) e a minoria tiver mais apoio nas edições modernas,
  vale a minoria;
- sem maioria, vale a leitura com mais apoio nas edições modernas; empate, a da base.
Cada escolha fica registrada; as fracas (sem apoio moderno) vão para revisão.
"""
from collections import Counter

from .grafia import chave
from .tokens import achatar, alinhar, divergencias, texto


def _k(toks):
    return tuple(chave(t) for t in toks if t not in ('_', '*'))


def estabelecer(transcricoes, base, modernas, correlacionados=()):
    """transcricoes/modernas: dict nome -> obra. Devolve (tokens, sítios)."""
    nomes_t = [base] + [n for n in transcricoes if n != base]
    T = {n: achatar(transcricoes[n]) for n in nomes_t}
    B = T[base]
    outros = nomes_t[1:]
    ops_t = [alinhar(B, T[n]) for n in outros]
    nomes_m = list(modernas)
    M = {n: achatar(modernas[n]) for n in nomes_m}
    ops_m = [alinhar(B, M[n], chave=chave) for n in nomes_m]
    corr = [set(c) for c in correlacionados]

    sitios = []
    for s, e, spans in divergencias(B, ops_t + ops_m):
        leit = {base: B[s:e]}
        for n, (a, b) in zip(outros, spans[:len(outros)]):
            leit[n] = T[n][a:b]
        if len({_k(v) for v in leit.values()}) == 1:
            continue
        mods = {n: M[n][a:b] for n, (a, b) in zip(nomes_m, spans[len(outros):])}
        grupos = {}
        for n in nomes_t:
            grupos.setdefault(_k(leit[n]), []).append(n)
        apoio = {k: [m for m in nomes_m if _k(mods[m]) == k] for k in grupos}
        maior = max(grupos.values(), key=len)
        if len(maior) * 2 > len(nomes_t):
            k_mai = _k(leit[maior[0]])
            escolha, por = k_mai, 'maioria (' + '=' .join(maior) + ')'
            if any(set(maior) <= c for c in corr):
                rival = max((k for k in grupos if k != k_mai), key=lambda k: len(apoio[k]))
                if len(apoio[rival]) > len(apoio[k_mai]):
                    escolha, por = rival, 'minoria com apoio moderno (' + '='.join(grupos[rival]) + ')'
        else:
            ordem = sorted(grupos, key=lambda k: (-len(apoio[k]), min(nomes_t.index(n) for n in grupos[k])))
            escolha = ordem[0]
            por = 'sem maioria; ' + '='.join(grupos[escolha])
        dono = grupos[escolha][0]
        sitios.append({
            's': s, 'e': e,
            'leituras': {n: texto(leit[n]) for n in nomes_t},
            'modernas': {n: texto(mods[n]) for n in nomes_m},
            'escolha': leit[dono], 'escolha_txt': texto(leit[dono]), 'por': por,
            'apoio': apoio[escolha],
            'duvida': not apoio[escolha],
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
