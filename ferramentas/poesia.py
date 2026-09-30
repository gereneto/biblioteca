"""Publica na biblioteca os poemas do Versificador (Solar Editora).

    python ferramentas/poesia.py                     # lê a pasta padrão do Versificador
    python ferramentas/poesia.py --fonte <pasta>     # outra cópia do Versificador

Lê `corpus/<autor>/*.txt` (texto em ortografia atualizada; `corpus/_bruto` fica de fora) e
as traduções de `traducao/<poema>/` (original e tradução). Os poemas infantis não entram.

Grava:
  conteudo/poesia.js            índice de todos os poemas (título, forma, livro, versos),
                                carregado com o site
  conteudo/<autor>/poesia.js    o texto dos poemas do autor e as notas sobre o texto,
                                carregado só quando um poema do autor é aberto

Formato do texto de cada poema: um verso por linha; estrofes separadas por linha em branco;
linhas começadas por "::" são marcas (::parte, ::subtitulo, ::fala, ::voz, ::epigrafe,
::dedicatoria, ::data, ::fecho, ::separador, ::lacuna, ::pagina).
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter, OrderedDict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE_PADRAO = os.path.join(os.path.dirname(os.path.dirname(RAIZ)),
                            'Solar', 'Editora', 'Versificador')

# pasta do corpus -> id do autor na biblioteca (conteudo/autores.js)
AUTORES = {
    'alberto-de-oliveira': 'alberto-de-oliveira',
    'alphonsus': 'alphonsus-de-guimaraens',
    'alvares-de-azevedo': 'alvares-de-azevedo',
    'antero-de-quental': 'antero-de-quental',
    'antonio-nobre': 'antonio-nobre',
    'augusto-dos-anjos': 'augusto-dos-anjos',
    'bilac': 'olavo-bilac',
    'bocage': 'bocage',
    'camilo-pessanha': 'camilo-pessanha',
    'camoes': 'luis-de-camoes',
    'casimiro-de-abreu': 'casimiro-de-abreu',
    'castro-alves': 'castro-alves',
    'cesario-verde': 'cesario-verde',
    'claudio-manuel-da-costa': 'claudio-manuel-da-costa',
    'cruz-e-sousa': 'cruz-e-sousa',
    'fagundes-varela': 'fagundes-varela',
    'fernando-pessoa': 'fernando-pessoa',
    'florbela-espanca': 'florbela-espanca',
    'francisca-julia': 'francisca-julia',
    'goncalves-dias': 'goncalves-dias',
    'gonzaga': 'tomas-antonio-gonzaga',
    'gregorio-de-matos': 'gregorio-de-matos',
    'junqueira-freire': 'junqueira-freire',
    'machado-de-assis': 'machado-de-assis',
    'mario-de-andrade': 'mario-de-andrade',
    'raimundo-correia': 'raimundo-correia',
    'raul-de-leoni': 'raul-de-leoni',
    'vicente-de-carvalho': 'vicente-de-carvalho',
}

# Livros de cada autor, em ordem de publicação: (prefixo do arquivo, título, ano).
# O prefixo é o que vem antes de "--" no nome do arquivo.
LIVROS = {
    'alberto-de-oliveira': [('meridionais', 'Meridionais', 1884), ('sonetos-e-poemas', 'Sonetos e Poemas', 1885),
                            ('versos-e-rimas', 'Versos e Rimas', 1895), ('por-amor-de-uma-lagrima', 'Por Amor de uma Lágrima', 1895),
                            ('alma-em-flor', 'Alma em Flor', 1900)],
    'alphonsus': [('setenario', 'Setenário das Dores de Nossa Senhora', 1899), ('camara-ardente', 'Câmara Ardente', 1899),
                  ('dona-mistica', 'Dona Mística', 1899), ('kiriale', 'Kiriale', 1902),
                  ('pastoral', 'Pastoral aos Crentes do Amor e da Morte', 1923), ('pulvis', 'Pulvis', 1938),
                  ('avulsos', 'Poemas avulsos', None)],
    'alvares-de-azevedo': [('lira-dos-vinte-anos', 'Lira dos Vinte Anos', 1853), ('poesias-diversas', 'Poesias Diversas', 1853)],
    'antero-de-quental': [('sonetos-1886', 'Sonetos Completos', 1886)],
    'antonio-nobre': [('so', 'Só', 1892)],
    'augusto-dos-anjos': [('eu', 'Eu', 1912)],
    'bilac': [('panoplias', 'Panóplias', 1888), ('via-lactea', 'Via Láctea', 1888), ('sarcas-de-fogo', 'Sarças de Fogo', 1888),
              ('alma-inquieta', 'Alma Inquieta', 1902), ('as-viagens', 'As Viagens', 1902),
              ('cacador-de-esmeraldas', 'O Caçador de Esmeraldas', 1902), ('avulsos', 'Poemas avulsos', 1906),
              ('tarde', 'Tarde', 1919)],
    'camilo-pessanha': [('clepsidra', 'Clepsidra', 1920)],
    'camoes': [('soneto', 'Sonetos', None)],
    'casimiro-de-abreu': [('primaveras', 'As Primaveras', 1859)],
    'castro-alves': [('espumas', 'Espumas Flutuantes', 1870), ('escravos', 'Os Escravos', 1883)],
    'cesario-verde': [('livro', 'O Livro de Cesário Verde', 1887)],
    'claudio-manuel-da-costa': [('soneto', 'Obras', 1768)],
    'cruz-e-sousa': [('broqueis', 'Broquéis', 1893), ('farois', 'Faróis', 1900), ('ultimos-sonetos', 'Últimos Sonetos', 1905)],
    'fagundes-varela': [('noturnas', 'Noturnas', 1861), ('vozes-da-america', 'Vozes da América', 1864),
                        ('cantos-e-fantasias', 'Cantos e Fantasias', 1865), ('cantos-meridionais', 'Cantos Meridionais', 1869),
                        ('poesias', 'Outros poemas', None)],
    'fernando-pessoa': [('mensagem', 'Mensagem', 1934), ('cancioneiro', 'Cancioneiro', None),
                        ('alberto-caeiro', 'Poemas de Alberto Caeiro', None), ('ricardo-reis', 'Odes de Ricardo Reis', None),
                        ('alvaro-de-campos', 'Poesias de Álvaro de Campos', None)],
    'florbela-espanca': [('livro-de-magoas', 'Livro de Mágoas', 1919), ('livro-de-soror-saudade', 'Livro de Sóror Saudade', 1923),
                         ('charneca-em-flor', 'Charneca em Flor', 1931)],
    'francisca-julia': [('marmores', 'Mármores', 1895), ('esfinges', 'Esfinges', 1903), ('avulsos', 'Poemas avulsos', None)],
    'goncalves-dias': [('primeiros-cantos', 'Primeiros Cantos', 1846), ('segundos-cantos', 'Segundos Cantos', 1848),
                       ('sextilhas', 'Sextilhas de Frei Antão', 1848), ('ultimos-cantos', 'Últimos Cantos', 1851),
                       ('novos-cantos', 'Novos Cantos', 1857), ('os-timbiras', 'Os Timbiras', 1857)],
    'gonzaga': [('lira', 'Marília de Dirceu', 1792)],
    'gregorio-de-matos': [('soneto', 'Poemas atribuídos', None)],
    'junqueira-freire': [('inspiracoes-do-claustro', 'Inspirações do Claustro', 1855)],
    'machado-de-assis': [('crisalidas', 'Crisálidas', 1864), ('falenas', 'Falenas', 1870), ('americanas', 'Americanas', 1875),
                         ('ocidentais', 'Ocidentais', 1901), ('reliquias', 'Relíquias de Casa Velha', 1906)],
    'mario-de-andrade': [('gota-de-sangue', 'Há uma Gota de Sangue em Cada Poema', 1917),
                         ('pauliceia', 'Pauliceia Desvairada', 1922), ('losango-caqui', 'Losango Cáqui', 1926),
                         ('cla-do-jabuti', 'Clã do Jabuti', 1927), ('remate-de-males', 'Remate de Males', 1930),
                         ('livro-azul', 'Livro Azul', 1941), ('costela-do-gra-cao', 'A Costela do Grã Cão', 1941),
                         ('lira-paulistana', 'Lira Paulistana', 1945)],
    'raimundo-correia': [('sinfonias', 'Sinfonias', 1883), ('versos-e-versoes', 'Versos e Versões', 1887),
                         ('aleluias', 'Aleluias', 1891), ('poesias', 'Poesias', 1898)],
    'raul-de-leoni': [('luz-mediterranea', 'Luz Mediterrânea', 1922), ('poemas-ineditos', 'Poemas inéditos', None)],
    'vicente-de-carvalho': [('poemas-e-cancoes', 'Poemas e Canções', 1908)],
}

# Bocage: as Obras Poéticas (1875) vêm divididas por gênero; cada seção vira um livro
BOCAGE = ['Sonetos', 'Idílios e Cantatas', 'Odes', 'Odes Anacreônticas', 'Canções', 'Elegias e Epicédios', 'Epístolas e Sátiras',
          'Apólogos', 'Cançonetas', 'Endechas', 'Epigramas', 'Madrigais']

# Autores cujos arquivos não têm prefixo de livro: um livro só
LIVRO_UNICO = {'camoes', 'claudio-manuel-da-costa', 'gregorio-de-matos'}

# Poemas longos que o corpus divide em vários arquivos: (autor, arquivos em ordem, título, título de cada parte)
# Com títulos de parte, cada arquivo é uma parte da obra; sem eles, os textos se juntam num só.
JUNTAR = [
    ('alberto-de-oliveira', ['alma-em-flor--01-primeiro-canto', 'alma-em-flor--02-segundo-canto',
                             'alma-em-flor--03-terceiro-canto'],
     'Alma em Flor', ['Primeiro canto', 'Segundo canto', 'Terceiro canto']),
    ('goncalves-dias', ['os-timbiras--introducao', 'os-timbiras--canto-1', 'os-timbiras--canto-2',
                        'os-timbiras--canto-3', 'os-timbiras--canto-4'],
     'Os Timbiras', ['Introdução', 'Canto primeiro', 'Canto segundo', 'Canto terceiro', 'Canto quarto']),
    ('goncalves-dias', ['sextilhas--02-gulnare-e-mustafa-1', 'sextilhas--02-gulnare-e-mustafa-2'],
     'Gulnare e Mustafá', None),
    ('mario-de-andrade', ['lira-paulistana--0%d-lira-paulistana-parte-0%d' % (i, i) for i in range(1, 7)],
     'Lira Paulistana', None),
]

# Pastas por forma, na ordem em que aparecem na página do autor
def pasta_da_forma(forma):
    f = forma.lower().strip()
    if re.match(r'(\d+|dois|duas|três|quatro|cinco) sonetos', f) or f.startswith('soneto'):
        return 'sonetos'
    if f.startswith('apólogo'):
        return 'apologos'
    if f.startswith('lira'):
        return 'liras'
    if re.match(r'odes?\b', f):
        return 'odes'
    # verso livre de fato (o modernista); o corpus também chama de "verso livre" a silva romântica
    # e o polimétrico, que declaram a medida ou a rima: esses vão para "outras"
    if re.match(r'versos? livres?\b', f) or re.search(r'\bem versos? livres?\b', f):
        if not re.search(r'decass|hexass|redondilh|polimétric|rimad|branc|metro', f):
            return 'verso-livre'
    return 'outras'

# Traduções: pasta em traducao/, autor, ano, língua, livro do original e notas do visualizador
TRADUCOES = [
    {'pasta': 'o-corvo', 'autor': 'edgar-allan-poe', 'ano': 1845, 'lingua': 'inglês', 'codigo': 'en',
     'livro': ('The Raven and Other Poems', 1845),
     'metroOriginal': 'Octâmetro trocaico: oito pés de tônica e átona, 15 sílabas até a última tônica (16 nos versos de final feminino). Uma só rima, em -ore, no poema inteiro; rima interna na metade do verso.',
     'metroTraducao': 'Duas redondilhas maiores trocaicas por verso (8 + 7), tônicas nas sílabas ímpares; o fecho de cada estrofe é uma redondilha aguda. Uma só rima, em -ais; rima interna na metade do verso.',
     'nota': ['Nenhum metro português tem quinze sílabas, mas a redondilha maior é o mais nosso dos metros, e duas redondilhas trocaicas somam exatamente o verso de Poe, com o mesmo martelar nas ímpares.',
              'A rima em -ore virou -ais porque só ela dá a “Nevermore” um equivalente curto, fechado e repetível: “Nunca mais”. O nome “Lenore” fica como no original e rima consigo mesmo onde Poe o repete; lê-se Lenor.']},
    {'pasta': 'annabel-lee', 'traducao': 'versoes/final.txt', 'autor': 'edgar-allan-poe', 'ano': 1849,
     'lingua': 'inglês', 'codigo': 'en', 'livro': None,
     'metroOriginal': 'Verso acentual de pé anapéstico: versos longos de 4 tempos e curtos de 3; dois terços dos intervalos entre tempos são de três sílabas.',
     'metroTraducao': 'Os mesmos 4 e 3 tempos, em metros ternários portugueses (3-6-9, 2-5-8-11, 3-6-9-12) e redondilha no refrão “Neste reino à beira-mar”.',
     'nota': ['O embalo ternário de Poe existe em português, mas mora em poucos metros: o eneassílabo 3-6-9 e o verso de arte maior. A tradução usa esses metros e guarda a proporção de intervalos do original: 65% ternários, contra 66% em Poe.',
              'O nome se lê como em inglês, Ánabel Li, para que o refrão caia no tempo.']},
    {'pasta': 'o-albatroz', 'autor': 'charles-baudelaire', 'ano': 1859, 'lingua': 'francês', 'codigo': 'fr',
     'livro': ('Les Fleurs du mal', 1861),
     'metroOriginal': 'Alexandrino clássico francês: 6 + 6 sílabas, cesura fixa; rimas cruzadas, alternando femininas e masculinas.',
     'metroTraducao': 'Alexandrino clássico português, com a lei do hemistíquio: 6.ª sílaba tônica e fim de palavra na cesura; rimas cruzadas ABAB.',
     'nota': ['O alexandrino tem equivalente direto: o de Bilac e Raimundo Correia, que respeita a cesura como o francês. Cada verso tem tônica na 6.ª e na 12.ª, e os demais tempos variam, como em Baudelaire.']},
    {'pasta': 'cancao-de-outono', 'autor': 'paul-verlaine', 'ano': 1866, 'lingua': 'francês', 'codigo': 'fr',
     'livro': ('Poèmes saturniens', 1866),
     'metroOriginal': 'Versos de 4 e 3 sílabas, contadas até a última tônica, em estrofes de 4-4-3 / 4-4-3; rimas AAB CCB. “Deçà, delà” rima com o átono “à la”.',
     'metroTraducao': 'As mesmas medidas, verso a verso, e as mesmas rimas AAB CCB; “Por cá, por lá” rima com o átono “Semelhante à”, como no francês.',
     'nota': ['Verlaine escreve quase só com o som: vogais nasais, versos curtíssimos, rima que cai em palavra átona. A tradução guarda a medida exata de todos os versos e o cognato “monótono”, e troca os soluços “longos” por “finos” para manter a nasal e a rima com “violinos”.']},
    {'pasta': 'o-rei-dos-elfos', 'autor': 'goethe', 'ano': 1782, 'lingua': 'alemão', 'codigo': 'de',
     'livro': ('Die Fischerin', 1782),
     'metroOriginal': 'Verso acentual de 4 tempos, com uma ou duas átonas entre eles (ritmo de galope); rimas emparelhadas, quase todas agudas.',
     'metroTraducao': 'Versos de 4 tempos em galope ternário: o verso de arte maior (2-5-8-11) e o de 3-6-9-12, misturados como em Goethe; rimas emparelhadas.',
     'nota': ['O galope de Goethe tem em português um parente próximo, o verso de arte maior, de tempo a cada três sílabas. A rima em -ento abre o poema, volta no meio e o fecha, como “Wind / Kind” no alemão.',
              'O último verso é mais curto, como o de Goethe, e cai seco: “estava morto”.']},
]

METADADOS = {'titulo', 'autor', 'obra', 'fonte', 'ortografia', 'forma', 'nota', 'lingua', 'numero',
             'tradutor', 'troca'}
MARCAS = {'parte', 'subtitulo', 'fala', 'voz', 'epigrafe', 'dedicatoria', 'data', 'fecho',
          'separador', 'lacuna', 'secao'}

ROMANOS = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}


def romano(s):
    s = s.upper()
    if not s or any(c not in ROMANOS for c in s):
        return None
    total = 0
    for i, c in enumerate(s):
        v = ROMANOS[c]
        total += -v if i + 1 < len(s) and ROMANOS[s[i + 1]] > v else v
    return total


def slug(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


avisos = []


def aviso(msg):
    avisos.append(msg)


# ------------------------------------------------------------------ leitura de um poema

def ler(caminho):
    """Cabeçalho (dict de listas) e linhas do corpo, com as marcas convertidas para '::chave valor'."""
    with open(caminho, encoding='utf-8') as f:
        linhas = f.read().replace('\r', '').replace('﻿', '').split('\n')
    meta = {}
    corpo = []          # (tipo, chave, valor): ('v', None, verso) | ('b',) | ('m', chave, valor)
    for l in linhas:
        m = re.match(r'#\s*(\w+):\s*(.*)$', l)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if k in METADADOS:
                meta.setdefault(k, []).append(v)
            elif k in MARCAS:
                corpo.append(('m', k, v))
            else:
                aviso('%s: chave desconhecida "%s"' % (caminho, k))
            continue
        if l.startswith('#'):
            aviso('%s: linha de comentário ignorada: %s' % (caminho, l[:60]))
            continue
        if not l.strip():
            corpo.append(('b', None, None))
        else:
            if l.startswith('::'):
                aviso('%s: verso começa com "::"' % caminho)
            corpo.append(('v', None, l.rstrip()))
    return meta, corpo


def primeiro(meta, k, padrao=''):
    return meta.get(k, [padrao])[0]


def extrair_topo(corpo):
    """Tira do corpo as marcas que são dados do poema: seção do livro, número e subtítulo no alto.
    Uma marca no alto só vira dado quando a mesma chave não aparece de novo no meio do poema."""
    ini = next((i for i, (t, _, _) in enumerate(corpo) if t == 'v'), len(corpo))
    depois = Counter(k for t, k, _ in corpo[ini:] if t == 'm')
    dados = {}
    resto = []
    for i, (t, k, v) in enumerate(corpo):
        if i < ini and t == 'm':
            if k == 'secao' and 'secao' not in dados:
                dados['secao'] = v
                continue
            if k == 'parte' and not depois['parte'] and 'n' not in dados:
                dados['n'] = v
                continue
            if k == 'subtitulo' and not depois['subtitulo'] and 'subtitulo' not in dados:
                dados['subtitulo'] = v
                continue
        resto.append((t, k, v))
    return dados, resto


def texto_do_corpo(corpo):
    """Linhas do formato da biblioteca; estrofes separadas por uma linha em branco."""
    saida = []
    for t, k, v in corpo:
        if t == 'b':
            if saida and saida[-1] != '':
                saida.append('')
        elif t == 'v':
            saida.append(v)
        else:
            if k == 'secao':            # no meio do poema, só marca página aberta com espaço
                k, v = 'pagina', ''
            saida.append(('::%s %s' % (k, v)).rstrip())
    while saida and saida[-1] == '':
        saida.pop()
    while saida and saida[0] == '':
        saida.pop(0)
    return '\n'.join(saida)


def contar_versos(texto):
    return sum(1 for l in texto.split('\n') if l.strip() and not l.startswith('::'))


def estrofes(texto):
    return [[l for l in e.split('\n') if l.strip() and not l.startswith('::')]
            for e in re.split(r'\n\s*\n', texto) if e.strip()]


# ------------------------------------------------------------------ notas sobre o texto

def limpar_forma(f):
    return re.sub(r',? ?metro dominante segundo o Versificador', '', f).replace('()', '').strip()


def nota_publicavel(n):
    return not re.search(r'\.txt|# ?\w+|Versificador|coletor|arquivo', n)


def frase(s):
    s = s.strip()
    if not s:
        return s
    s = s[0].upper() + s[1:]
    return s if s[-1] in '.!?…)»”"' else s + '.'


def edicao_do_poema(metas):
    """Página 'Sobre esta edição': de onde vem o texto, a ortografia, a forma e as notas."""
    m = metas[0]
    blocos = []
    obras = list(OrderedDict.fromkeys(primeiro(x, 'obra') for x in metas))
    blocos.append('**Publicação.** ' + frase('; '.join(obras)))
    ort = primeiro(m, 'ortografia')
    if ort:
        blocos.append('**Ortografia.** ' + frase(ort))
    forma = limpar_forma(primeiro(m, 'forma'))
    if forma:
        blocos.append('**Forma.** ' + frase(forma))
    notas = [n for x in metas for n in x.get('nota', []) if nota_publicavel(n)]
    notas = list(OrderedDict.fromkeys(notas))
    if notas:
        blocos.append('**Notas sobre o texto.**')
        blocos.extend(frase(n) for n in notas)
    fontes = []
    for x in metas:
        url = primeiro(x, 'fonte')
        if url and url not in [f['url'] for f in fontes]:
            fontes.append({'nome': rotulo_fonte(url), 'url': url})
    return {'apresentacao': '\n\n'.join(blocos), 'fontes': fontes}


def rotulo_fonte(url):
    if 'wikisource' in url:
        return 'Wikisource'
    if 'commons.wikimedia' in url:
        return 'Wikimedia Commons (fac-símile)'
    if 'archive.org' in url:
        return 'Internet Archive (fac-símile)'
    if 'gutenberg' in url:
        return 'Projeto Gutenberg'
    if 'bbm.usp' in url or 'brasiliana' in url:
        return 'Brasiliana USP'
    m = re.match(r'https?://(?:www\.)?([^/]+)', url)
    return m.group(1) if m else url


# ------------------------------------------------------------------ livros e ordem

def livro_bocage(obra):
    m = re.search(r'vol\. I+\s*(?:—|,)\s*([^,(]+)', obra)
    if not m:
        aviso('bocage: seção não reconhecida em "%s"' % obra)
        return 'Outros'
    s = m.group(1).strip().lower()
    for nome in BOCAGE:
        if nome.lower() == s:
            return nome
    aviso('bocage: seção "%s" fora da lista' % s)
    return m.group(1).strip()


def ordem_no_livro(pasta, arquivo, obra):
    """Posição do poema no livro: pelo número do arquivo ou, sem ele, pelo que diz o campo 'obra'."""
    nome = arquivo[:-4]
    if '--' in nome:
        m = re.match(r'(\d+)(?:-(\d+))?-', nome.split('--', 1)[1])
        if m:
            return int(m.group(1)) * 100 + int(m.group(2)) if m.group(2) else int(m.group(1))
    m = re.search(r'vol\. I+,? [^,]+, (\d+|[IVXLC]+)\b', obra)       # Bocage: número na seção
    if m:
        return int(m.group(1)) if m.group(1).isdigit() else romano(m.group(1))
    m = re.search(r'soneto (\d+)', obra)
    if m:
        return int(m.group(1))
    m = re.search(r'Sonetos, ([IVXLC]+)\b', obra)
    if m and romano(m.group(1)):
        return romano(m.group(1))
    m = re.search(r', (\d+)\b[^,]*$', obra)
    if m:
        return int(m.group(1))
    return 100000


# ------------------------------------------------------------------ corpus

def carregar_corpus(fonte):
    base = os.path.join(fonte, 'corpus')
    poemas = []         # dicts
    excluidos = []
    for pasta in sorted(os.listdir(base)):
        if pasta == '_bruto' or not os.path.isdir(os.path.join(base, pasta)):
            continue
        if pasta not in AUTORES:
            sys.exit('autor sem cadastro em AUTORES: ' + pasta)
        for arq in sorted(os.listdir(os.path.join(base, pasta))):
            if not arq.endswith('.txt'):
                continue
            caminho = os.path.join(base, pasta, arq)
            meta, corpo = ler(caminho)
            obra = primeiro(meta, 'obra')
            if re.search(r'infant', obra, re.I) or arq.startswith('poesias-infantis'):
                excluidos.append((pasta, arq, 'poema infantil'))
                continue
            poemas.append({'pasta': pasta, 'arquivo': arq, 'meta': meta, 'corpo': corpo})
    return poemas, excluidos


def tirar_duplicatas(poemas, excluidos):
    """Mesmo texto em dois arquivos (poema 'avulso' que também está no livro): fica o do livro."""
    grupos = OrderedDict()
    for p in poemas:
        corpo = ' '.join(v for t, _, v in p['corpo'] if t == 'v')
        chave = (p['pasta'], re.sub(r'\s+', ' ', corpo).strip().lower())
        grupos.setdefault(chave, []).append(p)
    fora = set()
    for grupo in grupos.values():
        if len(grupo) < 2:
            continue
        grupo = sorted(grupo, key=lambda p: p['arquivo'].startswith('avulsos'))
        for p in grupo[1:]:
            fora.add(id(p))
            excluidos.append((p['pasta'], p['arquivo'], 'mesmo texto de ' + grupo[0]['arquivo']))
    return [p for p in poemas if id(p) not in fora]


def montar(poemas):
    """Obras da biblioteca (um poema = uma obra), por autor."""
    por_arquivo = {(p['pasta'], p['arquivo'][:-4]): p for p in poemas}
    juntos = {}
    for pasta, arquivos, titulo, partes in JUNTAR:
        grupo = []
        for a in arquivos:
            p = por_arquivo.get((pasta, a))
            if not p:
                sys.exit('arquivo a juntar não encontrado: %s/%s.txt' % (pasta, a))
            grupo.append(p)
        for p in grupo[1:]:
            juntos[id(p)] = None
        juntos[id(grupo[0])] = (grupo, titulo, partes)

    obras = {}          # id do autor -> lista
    livros = {}         # id do autor -> OrderedDict prefixo -> {titulo, ano}
    usados = set()
    for p in poemas:
        if id(p) in juntos and juntos[id(p)] is None:
            continue
        pasta, arq = p['pasta'], p['arquivo']
        autor = AUTORES[pasta]
        grupo, titulo_junto, titulos_partes = juntos.get(id(p), ([p], None, None))
        meta = p['meta']
        obra_txt = primeiro(meta, 'obra')

        # livro
        if pasta == 'bocage':
            nome = livro_bocage(obra_txt)
            chave_livro, titulo_livro, ano_livro = slug(nome), nome, None
            ordem_livro = BOCAGE.index(nome) if nome in BOCAGE else len(BOCAGE)
        else:
            prefixo = pasta if pasta in LIVRO_UNICO else arq.split('--')[0]
            if pasta in LIVRO_UNICO:
                prefixo = LIVROS[pasta][0][0]
            tabela = LIVROS.get(pasta, [])
            achado = [(i, l) for i, l in enumerate(tabela) if l[0] == prefixo]
            if not achado:
                sys.exit('livro sem cadastro em LIVROS: %s/%s (prefixo "%s")' % (pasta, arq, prefixo))
            ordem_livro, (chave_livro, titulo_livro, ano_livro) = achado[0]
        livros.setdefault(autor, {})[chave_livro] = {'titulo': titulo_livro, 'ano': ano_livro, 'seq': ordem_livro}

        # texto e dados do alto
        partes = []
        dados = {}
        metas = [x['meta'] for x in grupo]
        if titulos_partes:
            for x, t in zip(grupo, titulos_partes):
                d, corpo = extrair_topo(x['corpo'])
                partes.append({'titulo': t, 'texto': texto_do_corpo(corpo)})
        else:
            textos = []
            for i, x in enumerate(grupo):
                d, corpo = extrair_topo(x['corpo'])
                if i == 0:
                    dados = d
                textos.append(texto_do_corpo(corpo))
            partes.append({'titulo': '', 'texto': '\n\n'.join(textos)})
        n = primeiro(meta, 'numero') or dados.get('n', '')
        m = re.search(r', soneto ([IVXLC]+)$', obra_txt)      # Via Láctea: sonetos numerados
        if not n and m:
            n = m.group(1)

        titulo = titulo_junto or primeiro(meta, 'titulo')
        base_id = slug(autor + '-' + (slug(titulo_junto) if titulo_junto else re.sub(r'--(\d+-)*', '-', arq[:-4])))
        pid, k = base_id, 2
        while pid in usados:
            pid, k = '%s-%d' % (base_id, k), k + 1
        usados.add(pid)

        forma = primeiro(meta, 'forma')
        o = {
            'id': pid,
            'titulo': titulo,
            'forma': pasta_da_forma(forma),
            'livro': chave_livro,
            'ordem': ordem_no_livro(pasta, arq, obra_txt),
            'versos': sum(contar_versos(x['texto']) for x in partes),
            '_partes': partes,
            '_edicao': edicao_do_poema(metas),
        }
        if n:
            o['n'] = n
        if dados.get('secao'):
            o['secao'] = secao_legivel(dados['secao'])
        if dados.get('subtitulo'):
            o['subtitulo'] = dados['subtitulo']
        lingua = primeiro(meta, 'lingua')
        if lingua:
            o['lingua'] = lingua.split()[0]
        if titulos_partes:
            o['partes'] = [{'titulo': x['titulo']} for x in partes]
        obras.setdefault(autor, []).append(o)
    return obras, livros


def secao_legivel(s):
    """'DIZIAM QUE...' -> 'Diziam que...'; '(p. 177)' some."""
    s = s.strip()
    if re.match(r'\(p\. ?\d+\)$', s):
        return ''
    if s.isupper():
        s = s.capitalize()
    s = s.rstrip('.') if not s.endswith('...') else s
    return {'Brazilianas': 'Brasilianas', 'Canticos': 'Cânticos'}.get(s, s)


# ------------------------------------------------------------------ traduções

def carregar_traducoes(fonte):
    base = os.path.join(fonte, 'traducao')
    obras = {}
    livros = {}
    for t in TRADUCOES:
        pasta = os.path.join(base, t['pasta'])
        mo, co = ler(os.path.join(pasta, t.get('original', 'original.txt')))
        mt, ct = ler(os.path.join(pasta, t.get('traducao', 'traducao.txt')))
        _, co = extrair_topo(co)
        _, ct = extrair_topo(ct)
        txo, txt = texto_do_corpo(co), texto_do_corpo(ct)
        forma_o = '+'.join(str(len(e)) for e in estrofes(txo))
        forma_t = '+'.join(str(len(e)) for e in estrofes(txt))
        if forma_o != forma_t:
            aviso('%s: estrofes do original %s, da tradução %s' % (t['pasta'], forma_o, forma_t))
        autor = t['autor']
        chave_livro = ''
        if t['livro']:
            chave_livro = slug(t['livro'][0])
            livros.setdefault(autor, {})[chave_livro] = {'titulo': t['livro'][0], 'ano': t['livro'][1], 'seq': t['livro'][1]}
        titulo_o = primeiro(mo, 'titulo')
        blocos = [
            '**Original.** _%s_, de %s: %s' % (titulo_o, primeiro(mo, 'autor'), frase(primeiro(mo, 'obra'))),
            '**Metro do original.** ' + t['metroOriginal'],
            '**Metro da tradução.** ' + t['metroTraducao'],
        ] + t['nota']
        notas = [n for n in mo.get('nota', []) if nota_publicavel(n)]
        if notas:
            blocos.append('**Notas sobre o texto original.**')
            blocos.extend(frase(n) for n in notas)
        o = {
            'id': t['pasta'],
            'titulo': primeiro(mt, 'titulo'),
            'forma': 'outras',
            'livro': chave_livro,
            'ordem': t['ano'],
            'ano': t['ano'],
            'versos': contar_versos(txt),
            'traducao': {'lingua': t['lingua'], 'codigo': t['codigo'], 'titulo': titulo_o},
            '_partes': [{'titulo': '', 'texto': txt, 'original': txo}],
            '_edicao': {
                'titulo': 'Sobre esta tradução',
                'apresentacao': '\n\n'.join(blocos),
                'fontes': [{'nome': 'Texto original: ' + rotulo_fonte(primeiro(mo, 'fonte')), 'url': primeiro(mo, 'fonte')}],
            },
        }
        obras.setdefault(autor, []).append(o)
    return obras, livros


# ------------------------------------------------------------------ gravação

CABECALHO_INDICE = '''/* Poesia: índice de todos os poemas da biblioteca.
   Gerado por ferramentas/poesia.py a partir do Versificador. Não edite à mão:
   rode a ferramenta de novo. O texto dos poemas de cada autor fica em conteudo/<autor>/poesia.js
   e só é carregado quando um poema dele é aberto.

   Por autor: livros (em ordem de publicação) e poemas, cada um com
     id, titulo, forma (pasta: sonetos, apologos, liras, odes, verso-livre, outras),
     livro, ordem (no livro), versos; e, quando há, n (número no livro), secao, subtitulo,
     lingua, partes (poemas longos) e traducao.
*/
'''

CABECALHO_TEXTO = '''/* Poesia de %s: texto dos poemas e notas sobre o texto.
   Gerado por ferramentas/poesia.py; não edite à mão.

   Texto: um verso por linha; estrofes separadas por linha em branco; linhas com "::" são marcas
   (::parte, ::subtitulo, ::fala, ::voz, ::epigrafe, ::dedicatoria, ::data, ::fecho, ::separador,
   ::lacuna, ::pagina). Nas traduções, "o" traz o original, parte por parte.
*/
'''


def js(v):
    return json.dumps(v, ensure_ascii=False, separators=(',', ':'))


def gravar(obras, livros, nomes):
    indice = [CABECALHO_INDICE]
    for autor in sorted(obras):
        tabela = sorted(livros.get(autor, {}).items(), key=lambda kv: (kv[1]['seq'], kv[1]['titulo']))
        lista_livros = [{'id': k, 'titulo': v['titulo'], 'ano': v['ano']} for k, v in tabela]
        pos = {k: i for i, (k, _) in enumerate(tabela)}
        poemas = sorted(obras[autor], key=lambda o: (pos.get(o['livro'], -1), o['ordem'], slug(o['titulo'])))
        arquivo = 'conteudo/%s/poesia.js' % autor
        itens = []
        textos = OrderedDict()
        for o in poemas:
            item = {k: v for k, v in o.items() if not k.startswith('_')}
            item['livro'] = pos[o['livro']] if o['livro'] else -1
            if item['ordem'] >= 100000:
                del item['ordem']
            itens.append(item)
            entrada = {'t': [p['texto'] for p in o['_partes']], 'e': o['_edicao']}
            if any('original' in p for p in o['_partes']):
                entrada['o'] = [p.get('original', '') for p in o['_partes']]
            textos[o['id']] = entrada
        indice.append('BIBLIOTECA.poemas({\n  autor: %s,\n  arquivo: %s,\n  livros: %s,\n  poemas: [\n    %s\n  ]\n});\n' % (
            js(autor), js(arquivo), js([{k: v for k, v in l.items() if v is not None} for l in lista_livros]),
            ',\n    '.join(js(i) for i in itens)))
        os.makedirs(os.path.join(RAIZ, 'conteudo', autor), exist_ok=True)
        with open(os.path.join(RAIZ, arquivo), 'w', encoding='utf-8', newline='\n') as f:
            f.write(CABECALHO_TEXTO % nomes.get(autor, autor))
            f.write('BIBLIOTECA.textos({\n')
            f.write(',\n'.join('%s: %s' % (js(k), js(v)) for k, v in textos.items()))
            f.write('\n});\n')
    with open(os.path.join(RAIZ, 'conteudo', 'poesia.js'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(indice))


def nomes_dos_autores():
    with open(os.path.join(RAIZ, 'conteudo', 'autores.js'), encoding='utf-8') as f:
        t = f.read()
    return dict(re.findall(r"id:\s*'([^']+)',\s*\n\s*nome:\s*'([^']+)'", t))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--fonte', default=FONTE_PADRAO, help='pasta do Versificador')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    if not os.path.isdir(os.path.join(args.fonte, 'corpus')):
        sys.exit('não achei o corpus do Versificador em ' + args.fonte)

    poemas, excluidos = carregar_corpus(args.fonte)
    poemas = tirar_duplicatas(poemas, excluidos)
    obras, livros = montar(poemas)
    obras_t, livros_t = carregar_traducoes(args.fonte)
    for a, l in obras_t.items():
        obras.setdefault(a, []).extend(l)
    for a, l in livros_t.items():
        livros.setdefault(a, {}).update(l)

    nomes = nomes_dos_autores()
    faltam = sorted(set(obras) - set(nomes))
    if faltam:
        sys.exit('autores sem cadastro em conteudo/autores.js: ' + ', '.join(faltam))
    gravar(obras, livros, nomes)

    total = sum(len(v) for v in obras.values())
    print('%d obras de poesia, %d autores' % (total, len(obras)))
    formas = Counter(o['forma'] for v in obras.values() for o in v)
    print('pastas: ' + ', '.join('%s %d' % kv for kv in formas.most_common()))
    for a in sorted(obras):
        c = Counter(o['forma'] for o in obras[a])
        print('  %-26s %4d  %s' % (a, len(obras[a]), ' '.join('%s:%d' % kv for kv in sorted(c.items()))))
    print('fora (%d):' % len(excluidos))
    for pasta, arq, motivo in excluidos:
        print('  %s/%s — %s' % (pasta, arq, motivo))
    if avisos:
        print('avisos (%d):' % len(avisos))
        for a in avisos:
            print('  ' + a)


if __name__ == '__main__':
    main()
