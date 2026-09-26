"""Estabelece o texto de uma obra e gera o arquivo do site.

uso:
  python ferramentas/texto.py <obra>              confronta, moderniza e grava os relatórios
  python ferramentas/texto.py <obra> --publicar   idem, e grava conteudo/<autor>/<obra>.js

A obra é descrita em edicoes/<obra>/:
  config.py    META, fontes (transcrições da edição-base e edições modernas)
  decisoes.py  EMENDAS, AJUSTES, MANUAL, VERSOS, TITULOS
  notas.py     APRESENTACAO, FONTES, MANTIDAS, ERROS_ANTERIORES
"""
import importlib.util
import json
import os
import pickle
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

from edicao import estabelecer, modernizar, montar, relatorios  # noqa: E402
from edicao.fontes import cache  # noqa: E402
from edicao.tokens import texto  # noqa: E402


def carregar(obra, nome):
    caminho = os.path.join(RAIZ, 'edicoes', obra, nome + '.py')
    spec = importlib.util.spec_from_file_location(f'{obra}_{nome}', caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fontes(obra, config):
    """Lê (ou tira do cache) todas as fontes da obra."""
    arq = cache(obra, 'fontes.pkl')
    if os.path.exists(arq) and '--rebaixar' not in sys.argv:
        return pickle.load(open(arq, 'rb'))
    tr = config.transcricoes()
    md = config.modernas()
    pickle.dump((tr, md), open(arq, 'wb'))
    return tr, md


def processar(obra, publicar=False):
    config = carregar(obra, 'config')
    dec = carregar(obra, 'decisoes')
    notas = carregar(obra, 'notas')
    tr, md = fontes(obra, config)
    pasta = cache(obra, 'relatorios')

    # 1. texto-base
    E0, sitios = estabelecer.estabelecer(tr, config.BASE, md, getattr(config, 'CORRELACIONADOS', ()),
                                         getattr(config, 'RUIDOSO', None), getattr(config, 'UM_VOTO', False),
                                         getattr(config, 'DESEMPATE_LEXICO', False))
    print('divergências entre transcrições:', len(sitios), dict(estabelecer.resumo(sitios)))
    ruidoso = getattr(config, 'RUIDOSO', None)
    revisoes = []
    if ruidoso:
        E0, revisoes = estabelecer.revisar_pelo_ruidoso(E0, tr[ruidoso], md[config.REFERENCIAS[0][0]])
        print(f'leituras da moderna confirmadas pelo {ruidoso}:', len(revisoes))
    tradicao = []
    if getattr(config, 'TRADICAO', None):     # edição revista transmitida só pelas modernas
        E0, tradicao = estabelecer.adotar_modernas(E0, [md[n] for n in config.TRADICAO])
        print('lições da edição revista (todas as modernas concordam):', len(tradicao))
        revisoes += [dict(r, ruidoso='') for r in tradicao]

    # 2. itálico (o testemunho ruidoso não vota: o OCR não traz itálico)
    # só votam os testemunhos que marcam itálico (o OCR não marca; tem só sublinhados soltos)
    marcas = {n: sum('_' in x for p in o for x in p['paras']) for n, o in tr.items()}
    votam = {n: o for n, o in tr.items() if n != ruidoso and marcas[n] * 4 >= max(marcas.values())}
    E, ital = modernizar.italico_por_votacao(E0, votam, md.get(config.REFERENCIAS[0][0]))

    # 3. intervenções no texto-base
    E, ital, reg_em = modernizar.aplicar_emendas(E, ital, dec.EMENDAS)

    # 4. grafia
    refs = [(n, md[n], pos) for n, pos in config.REFERENCIAS]
    out, origem, rel = modernizar.modernizar(E, refs, getattr(dec, 'MANUAL', {}))
    flags = [ital[o] if (t[:1].isalpha()) else False for t, o in zip(out, origem)]

    # 5. pontuação da edição revista (só com config.TRADICAO) e ajustes finais
    reg_pt = []
    if getattr(config, 'TRADICAO', None):
        out, flags, reg_pt = modernizar.pontuacao_das_modernas(out, flags, [md[n] for n in config.TRADICAO])
        print('pontuação da edição revista:', len(reg_pt))
    out, flags, reg_aj = modernizar.ajustes_finais(out, flags, [a[1:] for a in dec.AJUSTES])
    for r, a in zip(reg_aj, dec.AJUSTES):
        r['tipo'] = a[0]
    reg_aj = reg_pt + reg_aj
    out = montar.aspas_angulares(out)

    partes = montar.partes(out, flags, getattr(dec, 'VERSOS', None), getattr(dec, 'TITULOS', None))

    # relatórios
    n = {
        'sitios': relatorios.sitios(pasta, sitios),
        'revisoes': relatorios.revisoes(pasta, revisoes),
        'modernas': relatorios.comparar_modernas(pasta, out, md, config.REFERENCIAS[0][0]),
        'pontuacao': relatorios.pontuacao_unanime(pasta, out, md),
        'sem_par': relatorios.sem_par(pasta, E, rel),
        'vocabulario': relatorios.vocabulario(pasta, partes, md),
    }
    print('relatórios em', pasta, n)
    with open(os.path.join(pasta, 'texto.txt'), 'w', encoding='utf-8') as f:
        for p in partes:
            f.write(f"\n\n{p['n']}\n{p['titulo']}\n\n")
            for x in p['paragrafos']:
                f.write(('\n'.join('    ' + l for l in x['verso']) if isinstance(x, dict) else x) + '\n\n')
    pickle.dump({'E0': E0, 'sitios': sitios, 'E': E, 'out': out, 'flags': flags, 'rel': rel,
                 'emendas': reg_em, 'ajustes': reg_aj, 'partes': partes}, open(cache(obra, 'resultado.pkl'), 'wb'))
    print(len(partes), 'partes;', sum(len(p['paragrafos']) for p in partes), 'parágrafos')

    if publicar:
        edicao = notas_da_edicao(notas, reg_em, reg_aj, partes, tradicao)
        meta = config.META
        destino = os.path.join(RAIZ, 'conteudo', meta['autor'], meta['id'] + '.js')
        montar.publicar(destino, meta, partes, edicao, getattr(notas, 'COMENTARIO', ''))
        rel_js = f"conteudo/{meta['autor']}/{meta['id']}.js"
        if montar.registrar_no_index(os.path.join(RAIZ, 'index.html'), rel_js):
            print('acrescentado ao index.html:', rel_js)
        print('publicado:', destino)


def notas_da_edicao(notas, reg_em, reg_aj, partes, tradicao=()):
    rotulo = lambda p: p['n'] or p['titulo']         # partes sem número (prólogo...): pelo título
    ordem = {rotulo(p): i for i, p in enumerate(partes)}
    completo = {rotulo(p): ' '.join((x if isinstance(x, str) else ' '.join(x['verso'])) for x in p['paragrafos']) + ' ' + p['titulo']
                for p in partes}

    def onde(frase):
        achou = [n for n, t in completo.items() if frase in t]
        if not achou:
            raise SystemExit(f'trecho não encontrado no texto final: {frase!r}')
        return ', '.join(achou)

    sem_par = lambda x: x.replace(' ¶', '')
    erros = [(r['parte'], sem_par(r['de']), sem_par(r['para'])) for r in reg_em if r['tipo'] == 'erro']
    erros += list(getattr(notas, 'ERROS_ANTERIORES', []))
    erros.sort(key=lambda x: ordem.get(x[0], 9999))
    sem_cab = lambda x: ' '.join(t for t in x.split() if not t.startswith('#'))
    trad = [(r['parte'], sem_par(r['de']), sem_par(r['para'])) for r in reg_em if r['tipo'] == 'edicao']
    trad += [(r['parte'], sem_cab(sem_par(r['de'])), sem_cab(sem_par(r['para']))) for r in tradicao]
    trad.sort(key=lambda x: ordem.get(x[0], 9999))
    pont = []
    for r in reg_aj:
        if r['tipo'] != 'pontuacao':
            continue
        juntar = lambda s: texto([t for t in s.split() if t != '¶' and not t.startswith('#')])
        pont.append((r['parte'], juntar(f"{r['antes']} {r['de']} {r['depois']}"), juntar(f"{r['antes']} {r['para']} {r['depois']}")))
    pont.sort(key=lambda x: ordem.get(x[0], 9999))
    mant = [{'cap': onde(fr), 'texto': fr, 'variante': v, 'obs': o} for fr, v, o in getattr(notas, 'MANTIDAS', [])]
    extra = {k: v for k, v in (('base', getattr(notas, 'BASE', None)), ('secoes', getattr(notas, 'SECOES', None))) if v}
    return {
        **extra,
        'apresentacao': notas.APRESENTACAO,
        'fontes': notas.FONTES,
        'erros': [{'cap': c, 'de': d, 'para': p} for c, d, p in erros],
        'tradicao': [{'cap': c, 'de': d, 'para': p} for c, d, p in trad],
        'pontuacao': [{'cap': c, 'de': d, 'para': p} for c, d, p in pont],
        'mantidas': mant,
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    processar(sys.argv[1], publicar='--publicar' in sys.argv)
