"""Relatórios para a revisão humana de cada obra (gravados em ferramentas/cache/<obra>/relatorios/)."""
import csv
import os
import re
from collections import Counter

from .tokens import achatar, alinhar, divergencias, e_palavra, texto

PONT = {'«': '"', '»': '"', '“': '"', '”': '"', '–': '—', '-': '—', '…': '...', '....': '...'}


def _grava(pasta, nome, cab, linhas):
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, nome), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(cab)
        w.writerows(linhas)
    return len(linhas)


def sitios(pasta, sitios_):
    linhas = []
    for x in sitios_:
        if x['duvida'] or not x['por'].startswith('maioria'):
            linhas.append([x['por'], ','.join(x['apoio']), x['antes'][-40:], x['escolha_txt'],
                           ' || '.join(f'{k}: {v}' for k, v in x['leituras'].items()),
                           ' || '.join(f'{k}: {v}' for k, v in x['modernas'].items()), x['depois'][:40]])
    return _grava(pasta, 'sitios.tsv', ['decisão', 'apoio', 'antes', 'escolha', 'transcrições', 'modernas', 'depois'], linhas)


def revisoes(pasta, reg):
    """Leituras da moderna adotadas porque o OCR da edição-base as confirma (para conferência)."""
    return _grava(pasta, 'revisoes.tsv', ['antes', 'de', 'para', 'ocr', 'depois'],
                  [[r['antes'], r['de'], r['para'], r['ruidoso'], r['depois']] for r in reg])


def comparar_modernas(pasta, out, modernas, principal):
    """Palavras em que o texto final difere das edições modernas.
    Lista quando a referência principal difere ou quando todas as demais concordam entre si."""
    ours = [t for t in out if e_palavra(t)]
    nomes = list(modernas)
    M = {n: [t for t in achatar(modernas[n]) if e_palavra(t)] for n in nomes}
    ops = [alinhar(ours, M[n], chave=str.lower) for n in nomes]
    linhas = []
    for s, e, spans in divergencias(ours, ops):
        base = [x.lower() for x in ours[s:e]]
        ms = {n: M[n][a:b] for n, (a, b) in zip(nomes, spans)}
        difere = [n for n in nomes if [x.lower() for x in ms[n]] != base]
        if not difere:
            continue
        outras = [n for n in nomes if n != principal]
        unanimes = len(outras) >= 2 and len({tuple(x.lower() for x in ms[n]) for n in outras}) == 1 and set(outras) <= set(difere)
        if principal in difere or unanimes:
            linhas.append([','.join(difere), texto(ours[max(0, s - 7):s]), texto(ours[s:e]),
                           ' || '.join(f'{n}: {texto(ms[n])}' for n in nomes), texto(ours[e:e + 7])])
    return _grava(pasta, 'modernas.tsv', ['diferem', 'antes', 'este texto', 'modernas', 'depois'], linhas)


def pontuacao_unanime(pasta, out, modernas):
    """Pontuação em que TODAS as edições modernas concordam contra o texto."""
    k = lambda t: PONT.get(t, t).lower()
    limpa = lambda ts: [t for t in ts if t not in ('_', '¶', '/') and not t.startswith('#')]
    ours = limpa(out)
    nomes = list(modernas)
    M = {n: limpa(achatar(modernas[n])) for n in nomes}
    ops = [alinhar(ours, M[n], chave=k) for n in nomes]
    linhas = []
    for s, e, spans in divergencias(ours, ops):
        base = [k(x) for x in ours[s:e]]
        ms = [[k(x) for x in M[n][a:b]] for n, (a, b) in zip(nomes, spans)]
        if all(m == ms[0] for m in ms) and ms[0] != base and all(not re.match(r'\w', x) for x in base + ms[0]):
            linhas.append([texto(ours[max(0, s - 9):s]), texto(ours[s:e]), texto(M[nomes[0]][spans[0][0]:spans[0][1]]),
                           texto(ours[e:e + 6])])
    return _grava(pasta, 'pontuacao.tsv', ['antes', 'este texto', 'modernas', 'depois'], linhas)


def sem_par(pasta, E, rel):
    c = Counter()
    ex = {}
    for velho, novo, fonte, i in rel:
        if fonte == 'SEM_PAR':
            c[velho] += 1
            ex.setdefault(velho, texto(E[max(0, i - 6):i + 6]))
    return _grava(pasta, 'sem_par.tsv', ['palavra', 'vezes', 'exemplo'], [[w, n, ex[w]] for w, n in c.most_common()])


def vocabulario(pasta, partes_finais, modernas):
    palavras = lambda s: re.findall(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", s)
    ours = Counter()
    for p in partes_finais:
        for x in p['paragrafos']:
            ours.update(palavras(x if isinstance(x, str) else ' '.join(x['verso'])))
    ref = set()
    for obra in modernas.values():
        for c in obra:
            for p in c['paras']:
                ref.update(w.lower() for w in palavras(p))
    faltam = [[w, n] for w, n in sorted(ours.items()) if w.lower() not in ref]
    return _grava(pasta, 'vocabulario.tsv', ['palavra ausente das edições modernas', 'vezes'], faltam)
