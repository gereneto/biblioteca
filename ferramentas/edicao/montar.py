"""Tokens finais -> partes com parágrafos -> arquivo conteudo/<autor>/<obra>.js."""
import json
import os
import re

from .tokens import e_palavra

SEM_ESPACO_ANTES = set(',.;:!?)»…') | {'...', '.º'}
SEM_ESPACO_DEPOIS = set('«(')
QUEBRA_ITALICO = {':', ';', '—', '«', '»', '(', ')'}


def _espaco(ant, t):
    if ant is None or t in SEM_ESPACO_ANTES or ant in SEM_ESPACO_DEPOIS:
        return False
    return True


def _preparar(toks, flags):
    t2, f2 = [], []
    for i, t in enumerate(toks):
        if re.fullmatch(r'\.{3,}', t):
            t = '...'
        if t in ('o', 'º', '°') and i >= 2 and toks[i - 1] == '.' and toks[i - 2].isdigit():
            t2[-1] = '.º'; continue          # vers. 6.º
        t2.append(t); f2.append(flags[i])
    return t2, f2


def juntar(toks, flags):
    s, aberto, ant = '', False, None
    for k, t in enumerate(toks):
        pal = e_palavra(t)
        if pal and flags[k] and not aberto:
            s += (' ' if _espaco(ant, t) else '') + '_' + t
            aberto, ant = True, t
            continue
        if aberto and pal and not flags[k]:
            s += '_'; aberto = False
        if aberto and t in QUEBRA_ITALICO:
            s += '_'; aberto = False
        if aberto and not pal:
            prox = next((j for j in range(k + 1, len(toks)) if e_palavra(toks[j])), None)
            if prox is None or not flags[prox]:
                s += '_'; aberto = False
        s += (' ' if _espaco(ant, t) else '') + t
        ant = t
    if aberto:
        s += '_'
    s = re.sub(r'(\d) ?\$ ?(\d)', lambda m: m.group(1) + '$' + m.group(2), s)   # 70$000
    s = re.sub(r'(\d): (\d{3})', lambda m: m.group(1) + ':' + m.group(2), s)     # 1:070$000
    return s.strip()


def aspas_angulares(out):
    """Aspas retas ou curvas que sobrarem viram as angulares do autor, abrindo e fechando
    dentro de cada parágrafo."""
    res, aberta = [], False
    for t in out:
        if t == '¶':
            aberta = False
        elif t in ('"', '“', '”'):
            t = '»' if aberta else '«'
            aberta = not aberta
        elif t in ('«', '»'):
            aberta = t == '«'
        res.append(t)
    return res


def partes(out, flags, versos=None, titulos=None, fim=('FIM',)):
    """versos: {texto do parágrafo: [linhas]} para citações em verso compostas à parte."""
    toks, fl = _preparar(out, flags)
    obra, atual, estado = [], None, None
    par, pf = [], []

    def fecha():
        nonlocal par, pf
        if not par:
            return
        if '/' in par:
            linhas, cl, cf = [], [], []
            for t, f in zip(par, pf):
                if t == '/':
                    linhas.append(juntar(cl, cf)); cl, cf = [], []
                else:
                    cl.append(t); cf.append(f)
            linhas.append(juntar(cl, cf))
            item = {'verso': [l for l in linhas if l]}
        else:
            item = juntar(par, pf)
        if estado == 'titulo':
            atual['titulo'] = item if isinstance(item, str) else ' '.join(item['verso'])
        elif atual is not None:
            atual['paragrafos'].append(item)
        par, pf = [], []

    for t, f in zip(toks, fl):
        if t.startswith('#'):
            fecha()
            atual = {'n': t[1:], 'titulo': '', 'paragrafos': []}
            obra.append(atual); estado = 'num'
            continue
        if t == '¶':
            fecha()
            if estado == 'num':
                estado = 'titulo'
            elif estado == 'titulo':
                estado = 'corpo'
            continue
        par.append(t); pf.append(f)
    fecha()
    for c in obra:
        t = c['titulo'] or ''
        t = re.sub(r'(?<!\.)\.$', '', t)       # ponto tipográfico do título
        t = re.sub(r'\.»$', '»', t)
        c['titulo'] = (titulos or {}).get(c['n'], (titulos or {}).get(t, t))   # pelo número ou pelo próprio título
        for k, p in enumerate(c['paragrafos']):
            if isinstance(p, str) and versos and p in versos:
                c['paragrafos'][k] = {'verso': versos[p]}
    if obra and obra[-1]['paragrafos'] and obra[-1]['paragrafos'][-1] in fim:
        obra[-1]['paragrafos'].pop()
    return obra


# ------------------------------------------------------------------ publicação

def _tpl(s):
    assert '`' not in s and '${' not in s, s[:80]
    return s.replace('\\', '\\\\')


def texto_da_parte(p):
    blocos = []
    for x in p['paragrafos']:
        blocos.append('\n'.join('| ' + l for l in x['verso']) if isinstance(x, dict) else x)
    return '\n\n'.join(blocos)


def publicar(destino, meta, obra, edicao, comentario=''):
    """Escreve o arquivo de conteúdo da obra. meta: id, autor, titulo, ano, genero, divisao, descricao."""
    linhas = []
    if comentario:
        linhas.append('/* ' + comentario.strip() + '\n*/')
    linhas.append('BIBLIOTECA.obra({')
    for k in ('id', 'autor', 'titulo', 'ano', 'genero'):
        if meta.get(k) is not None:
            linhas.append(f'  {k}: {json.dumps(meta[k], ensure_ascii=False)},')
    linhas.append(f"  divisao: {json.dumps(meta['divisao'], ensure_ascii=False)},")
    if meta.get('descricao'):
        linhas.append(f"  descricao: {json.dumps(meta['descricao'], ensure_ascii=False)},")
    linhas.append('  edicao: {')
    for k in ('base', 'secoes'):                 # rótulos próprios da obra (opcionais)
        if edicao.get(k):
            linhas.append(f'    {k}: {json.dumps(edicao[k], ensure_ascii=False)},')
    linhas.append(f"    apresentacao: `{_tpl(edicao.get('apresentacao', ''))}`,")
    chaves = [k for k in ('fontes', 'erros', 'tradicao', 'pontuacao', 'mantidas') if edicao.get(k)]
    for ci, k in enumerate(chaves):
        linhas.append(f'    {k}: [')
        itens = edicao[k]
        for i, it in enumerate(itens):
            linhas.append('      ' + json.dumps(it, ensure_ascii=False) + (',' if i < len(itens) - 1 else ''))
        linhas.append('    ]' + (',' if ci < len(chaves) - 1 else ''))
    linhas.append('  },')
    linhas.append('  partes: [')
    for i, p in enumerate(obra):
        linhas.append('    { n: %s, titulo: %s, texto: `%s` }%s' % (
            json.dumps(p['n'], ensure_ascii=False), json.dumps(p['titulo'], ensure_ascii=False),
            _tpl(texto_da_parte(p)), ',' if i < len(obra) - 1 else ''))
    linhas.append('  ]')
    linhas.append('});')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(linhas) + '\n')


def registrar_no_index(index_html, caminho_rel):
    """Acrescenta <script defer src=...> ao index.html, se ainda não estiver lá."""
    s = open(index_html, encoding='utf-8').read()
    tag = f'<script defer src="{caminho_rel}"></script>'
    if tag in s:
        return False
    marca = '</head>'
    s = s.replace(marca, tag + '\n' + marca, 1)
    with open(index_html, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)
    return True
