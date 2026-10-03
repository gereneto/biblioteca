"""Ortodoxia, de G. K. Chesterton — dados para ferramentas/traducoes.py."""

META = {
    'id': 'ortodoxia', 'autor': 'g-k-chesterton', 'titulo': 'Ortodoxia',
    'ano': 1908, 'genero': 'Ensaio',
    'divisao': {'singular': 'capítulo', 'plural': 'capítulos'},
    'traducao': {'lingua': 'inglês', 'codigo': 'en', 'titulo': 'Orthodoxy'},
    'original_ao_lado': True,
    'edicao': {
        'titulo': 'Sobre esta tradução',
        'apresentacao': (
            '**O texto.** _Orthodoxy_ saiu em Londres, pela John Lane, em 1908. Chesterton, provocado por críticos '
            'que lhe cobravam uma exposição da própria filosofia, conta como chegou, por conta própria e quase '
            'sem querer, às verdades que encontrou depois inteiras no credo cristão: a loucura do racionalista, '
            'a lógica dos contos de fadas, os paradoxos do cristianismo, a revolução eterna. O livro é de antes '
            'da conversão dele ao catolicismo (1922), mas tornou-se um clássico da apologética e marcou, entre '
            'muitos outros, C. S. Lewis. A tradução foi feita do inglês, sobre o texto do Projeto Gutenberg, '
            'conferido com uma reimpressão da edição original.\n\n'
            '**A tradução.** Português do Brasil, fiel ao sentido e ao humor de Chesterton: o paradoxo tem de '
            'funcionar em português, com a mesma secura. Quando um jogo de palavras não passa, a tradução busca '
            'um equivalente que diga a mesma coisa. As citações em verso foram traduzidas em verso, pelo método '
            'do Versificador, com a medida e as rimas do original.\n\n'
            '**O original ao lado.** O botão «Inglês», no alto da página de leitura, mostra o texto de Chesterton '
            'junto da tradução.'),
        'fontes': [
            {'nome': 'Project Gutenberg, eBook nº 130', 'url': 'https://www.gutenberg.org/ebooks/130',
             'nota': 'texto inglês de base'},
            {'nome': 'Reimpressão da edição da Bodley Head, no Internet Archive', 'url': 'https://archive.org/details/orthodoxy00chesuoft',
             'nota': 'para conferência'},
        ],
    },
}

PARTES = [('', 'Prefácio', ['prefacio.txt'])] + [
    (r, t, [f'capitulo-{k}.txt']) for k, (r, t) in enumerate([
        ('I', 'Introdução em defesa de todo o resto'), ('II', 'O maníaco'), ('III', 'O suicídio do pensamento'),
        ('IV', 'A ética da Terra dos Elfos'), ('V', 'A bandeira do mundo'), ('VI', 'Os paradoxos do cristianismo'),
        ('VII', 'A revolução eterna'), ('VIII', 'O romance da ortodoxia'), ('IX', 'A autoridade e o aventureiro'),
    ], 1)]
