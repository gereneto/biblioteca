"""Publica no site as obras traduzidas (seção Catolicismo, exceto Santa Teresinha, que tem o seu).

Cada obra fica em edicoes/<obra>/:
  obra.py        META (id, autor, titulo, ano, genero, divisao, traducao, edicao, original_ao_lado)
                 e PARTES: [(sigla, título, [arquivos])] — os arquivos de original/ e traducao/;
  original/      texto na língua original;
  traducao/      tradução, um arquivo para cada arquivo do original.

Grava:
  conteudo/<autor>/<obra>.js     texto de cada parte (e o original, se META['original_ao_lado']),
                                 carregado só quando a obra é aberta (BIBLIOTECA.textos);
  conteudo/catolicismo.js        índice das obras (BIBLIOTECA.obra com «arquivo»), carregado com o site.
Uma obra só entra quando todos os arquivos traduzidos existem.

Marcas: «[I.1]», «[12]» no começo do parágrafo viram «{§ I.1}» (marca discreta no site);
«{PG 26.837}» e outras colunas de edição saem do texto publicado.

Uso: python ferramentas/traducoes.py [obra ...]
"""
import importlib.util
import json
import os
import re
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
EDICOES = os.path.join(RAIZ, 'edicoes')
INDICE = os.path.join(RAIZ, 'conteudo', 'catolicismo.js')
sys.path.insert(0, os.path.join(RAIZ, 'ferramentas'))
from edicao import montar  # noqa: E402

PALAVRA = re.compile(r"[^\W_]+(?:[-'’][^\W_]+)*")


def carregar_obra(nome):
    arq = os.path.join(EDICOES, nome, 'obra.py')
    spec = importlib.util.spec_from_file_location(f'obra_{nome}', arq)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ler(arq):
    linhas = open(arq, encoding='utf-8').read().replace('\r', '').split('\n')
    cab, i = {}, 0
    while i < len(linhas) and (linhas[i].startswith('# ') or not linhas[i].strip()):
        m = re.match(r'# ([\w-]+):\s?(.*)$', linhas[i])
        if m:
            cab[m.group(1).lower()] = m.group(2).strip()
        i += 1
    return cab, '\n'.join(linhas[i:]).strip()


def marcas(texto):
    """[I.1] e [12] no começo do parágrafo → {§ I.1}; colunas {PG 26.837} saem."""
    texto = re.sub(r'\s*\{(PG|PL) [^}]+\}\s*', ' ', texto)
    texto = re.sub(r'(?m)^\[([IVXLC]+\.\d+|\d+)\]\s*', r'{§ \1} ', texto)
    return re.sub(r'[ \t]+\n', '\n', re.sub(r' {2,}', ' ', texto)).strip()


def palavras(textos):
    n = 0
    for t in textos:
        t = re.sub(r'\{[^}]*\}', ' ', t)
        t = re.sub(r'^[|@#]+ ?', '', t, flags=re.M).replace('_', ' ').replace('*', ' ')
        n += len(PALAVRA.findall(t))
    return n


def trecho(arq, faixa):
    """Corpo do arquivo; com faixa «a-b», só os parágrafos do capítulo [a] até o fim do [b]."""
    corpo = ler(arq)[1]
    if not faixa:
        return corpo
    a, b = (int(x) for x in faixa.split('-'))
    ps = [p for p in re.split(r'\n\s*\n', corpo) if p.strip()]
    def cap(p):
        m = re.match(r'\[(\d+)\]', p.strip())
        return int(m.group(1)) if m else None
    ini = next(i for i, p in enumerate(ps) if cap(p) == a)
    fim = next((i for i, p in enumerate(ps) if cap(p) == b + 1), len(ps))
    return '\n\n'.join(ps[ini:fim])


def publicar_obra(nome):
    o = carregar_obra(nome)
    meta = o.META
    pasta = os.path.join(EDICOES, nome)
    partes, titulos = [], []
    for sigla, titulo, arquivos in o.PARTES:
        t, orig = [], []
        for spec in arquivos:
            a, _, faixa = spec.partition('#')
            arq_t = os.path.join(pasta, 'traducao', a)
            if not os.path.exists(arq_t):
                print(f'{nome}: falta traducao/{a} — obra ainda incompleta')
                return None
            t.append(marcas(trecho(arq_t, faixa)))
            if meta.get('original_ao_lado'):
                orig.append(marcas(trecho(os.path.join(pasta, 'original', a), faixa)))
        partes.append({'n': sigla, 'titulo': titulo, 'texto': '\n\n'.join(t),
                       'original': '\n\n'.join(orig) if orig else None})
    arq_js = f"conteudo/{meta['autor']}/{meta['id']}.js"
    os.makedirs(os.path.join(RAIZ, 'conteudo', meta['autor']), exist_ok=True)
    mapa = {meta['id']: {'t': [p['texto'] for p in partes], 'o': [p['original'] for p in partes] if meta.get('original_ao_lado') else None,
                         'e': meta['edicao']}}
    if mapa[meta['id']]['o'] is None:
        del mapa[meta['id']]['o']
    with open(os.path.join(RAIZ, arq_js), 'w', encoding='utf-8') as f:
        f.write(f"/* {meta['titulo']} — em tradução. Gerado por ferramentas/traducoes.py a partir de edicoes/{nome}/;\n"
                "   não edite à mão. t: tradução de cada parte; o: original; e: página «Sobre». */\n")
        f.write('BIBLIOTECA.textos(' + json.dumps(mapa, ensure_ascii=False) + ');\n')
    registro = {k: meta.get(k) for k in ('id', 'autor', 'titulo', 'subtitulo', 'ano', 'datas', 'genero', 'divisao',
                                         'traducao', 'descricao')}
    registro['arquivo'] = arq_js
    registro['_palavras'] = palavras(p['texto'] for p in partes)
    registro['partes'] = [{'n': p['n'], 'titulo': p['titulo']} for p in partes]
    print(f"publicada: {meta['id']} ({len(partes)} partes, {registro['_palavras']} palavras)")
    return {k: v for k, v in registro.items() if v is not None}


def gravar_indice(novas):
    obras = {}
    if os.path.exists(INDICE):
        for m in re.finditer(r'BIBLIOTECA\.obra\((\{.*?\})\);\n', open(INDICE, encoding='utf-8').read(), re.S):
            x = json.loads(m.group(1))
            obras[x['id']] = x
    obras.update(novas)
    with open(INDICE, 'w', encoding='utf-8') as f:
        f.write('/* Catolicismo: obras em tradução (índice). Gerado por ferramentas/traducoes.py;\n'
                '   o texto de cada obra fica em conteudo/<autor>/<obra>.js e só é carregado quando a obra é aberta.\n'
                '   (Santa Teresinha tem índice próprio: conteudo/santa-teresinha/indice.js.) */\n\n')
        for x in sorted(obras.values(), key=lambda x: (x.get('ano') or 0, x['titulo'])):
            f.write('BIBLIOTECA.obra(' + json.dumps(x, ensure_ascii=False) + ');\n')
    if montar.registrar_no_index(os.path.join(RAIZ, 'index.html'), 'conteudo/catolicismo.js'):
        print('acrescentado ao index.html: conteudo/catolicismo.js')


if __name__ == '__main__':
    nomes = sys.argv[1:] or sorted(d for d in os.listdir(EDICOES) if os.path.exists(os.path.join(EDICOES, d, 'obra.py')))
    novas = {}
    for n in nomes:
        r = publicar_obra(n)
        if r:
            novas[r['id']] = r
    if novas:
        gravar_indice(novas)
