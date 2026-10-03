"""Santa Teresinha — conferências automáticas das traduções (rodar antes de publicar).

Para cada par original/tradução: mesóclise; «Bon Dieu»/«bon Dieu» × «Bom Deus»/«bom Deus»
(Teresa escolhe a maiúscula, a tradução segue); marcas de folha (manuscritos); número de
parágrafos (cartas e orações); restos de francês comuns (« ma Mère », « le bon Dieu »).

Uso: python edicoes/santa-teresinha/conferir.py [manuscritos|cartas|oracoes]
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MESOCLISE = re.compile(r"[A-Za-zÀ-ÿ]+-(lo|la|los|las|o|a|os|as|me|te|se|lhe|lhes|nos|vos|no|na)-(ei|as|á|ás|emos|eis|ão|ia|ias|íamos|íeis|iam)\b")
FRANCES = re.compile(r"\b(le bon Dieu|ma Mère|c'est|qu'il|je suis|avec|dans les)\b")


def corpo(arq):
    return '\n'.join(l for l in open(arq, encoding='utf-8').read().split('\n') if not l.startswith('# '))


def paragrafos(t):
    return [p for p in re.split(r'\n\s*\n', t.strip()) if p.strip()]


def conferir(pares):
    problemas = 0
    for nome, fr, pt in pares:
        f, p = corpo(fr), corpo(pt)
        msg = []
        for m in MESOCLISE.finditer(p):
            msg.append(f'mesóclise: {m.group(0)}')
        a = (f.count('Bon Dieu'), f.count('bon Dieu'))
        b = (p.count('Bom Deus'), p.count('bom Deus'))
        if a != b:
            msg.append(f'Bon Dieu/bon Dieu {a} × Bom Deus/bom Deus {b}')
        for m in FRANCES.finditer(p):
            msg.append(f'francês? «{m.group(0)}»')
        if msg:
            problemas += 1
            print(nome, '|', '; '.join(msg))
    return problemas


def manuscritos():
    pares = []
    t = os.path.join(AQUI, 'traducao', 'manuscritos')
    for arq in sorted(os.listdir(t)):
        if not re.match(r'ms-[abc](-\d)?\.txt$', arq):
            continue
        ms = arq[3]
        pt = os.path.join(t, arq)
        texto = open(pt, encoding='utf-8').read()
        m = re.search(r'# folhas: Ms [A-C] (\d+[rv]?) – Ms [A-C] (\d+[rv]?)', texto)
        fr_todo = open(os.path.join(AQUI, 'original', 'manuscritos', f'ms-{ms}.txt'), encoding='utf-8').read()
        # recorta o francês nas mesmas folhas
        i = fr_todo.find(f'[[Ms {ms.upper()} {m.group(1)}]]')
        prox = re.search(r'\[\[Ms [A-C] (\d+[rv]?)\]\]', fr_todo[fr_todo.find(f'[[Ms {ms.upper()} {m.group(2)}]]') + 5:])
        j = fr_todo.find(prox.group(0), fr_todo.find(f'[[Ms {ms.upper()} {m.group(2)}]]') + 5) if prox else len(fr_todo)
        trecho = fr_todo[i:j]
        tmp = os.path.join(AQUI, 'traducao', 'manuscritos', f'.fr-{arq}')
        open(tmp, 'w', encoding='utf-8').write(trecho)
        marcas_fr = re.findall(r'\[\[Ms ([A-C] \d+[rv]?)\]\]', trecho)
        marcas_pt = re.findall(r'\{Ms ([A-C] \d+[rv]?)\}', texto)
        if marcas_fr != marcas_pt:
            print(arq, '| marcas diferentes:', sorted(set(marcas_fr) ^ set(marcas_pt)) or 'ordem')
        pares.append((arq, tmp, pt))
    n = conferir(pares)
    for _, tmp, _ in pares:
        os.remove(tmp)
    return n


def por_arquivo(pasta):
    t = os.path.join(AQUI, 'traducao', pasta)
    o = os.path.join(AQUI, 'original', pasta)
    pares, faltam = [], []
    for arq in sorted(os.listdir(o)):
        if not arq.endswith('.txt'):
            continue
        if not os.path.exists(os.path.join(t, arq)):
            faltam.append(arq)
            continue
        pares.append((arq, os.path.join(o, arq), os.path.join(t, arq)))
    if faltam:
        print(f'{pasta}: faltam {len(faltam)} ({faltam[0]} ... {faltam[-1]})')
    for nome, fr, pt in pares:
        a, b = len(paragrafos(corpo(fr))), len(paragrafos(corpo(pt)))
        if abs(a - b) > max(2, a // 5):
            print(nome, f'| parágrafos: {a} no francês, {b} na tradução')
    return conferir(pares)


if __name__ == '__main__':
    alvos = sys.argv[1:] or ['manuscritos', 'cartas', 'oracoes']
    for a in alvos:
        print('=====', a)
        if a == 'manuscritos':
            manuscritos()
        elif os.path.isdir(os.path.join(AQUI, 'traducao', a)):
            por_arquivo(a)
