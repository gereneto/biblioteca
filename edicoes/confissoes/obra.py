"""Confissões, de Santo Agostinho — dados para ferramentas/traducoes.py."""

ROMANOS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII']

META = {
    'id': 'confissoes', 'autor': 'santo-agostinho', 'titulo': 'Confissões',
    'ano': 397, 'datas': 'c. 397–401', 'genero': 'Autobiografia',
    'divisao': {'singular': 'livro', 'plural': 'livros'},
    'traducao': {'lingua': 'latim', 'codigo': 'la', 'titulo': 'Confessiones'},
    'original_ao_lado': False,
    'edicao': {
        'titulo': 'Sobre esta tradução',
        'apresentacao': (
            '**O texto.** Agostinho escreveu as _Confissões_ entre 397 e 401, já bispo de Hipona: treze livros '
            'dirigidos a Deus, em forma de oração. Os nove primeiros contam a vida dele até a conversão, em '
            'Milão, em 386, e a morte da mãe, Mônica, em Óstia, no ano seguinte; o décimo examina a memória e '
            'o estado da alma no tempo em que escreve; os três últimos meditam sobre o tempo, a criação e o '
            'começo do Gênesis. A tradução foi feita do latim, sobre o texto do The Latin Library, conferido '
            'com a edição de Knöll (_Corpus Scriptorum Ecclesiasticorum Latinorum_, vol. 33, Viena, 1896).\n\n'
            '**A tradução.** Português do Brasil, fiel ao sentido e ao movimento da prosa de Agostinho — as '
            'perguntas, as antíteses, as exclamações, os ecos dos Salmos —, sem acréscimos nem explicações. '
            'Deus é tratado por _tu_, como no original. As citações da Escritura são traduzidas do latim de '
            'Agostinho, que usava a Bíblia latina antiga, e não de uma Bíblia moderna; as referências não '
            'foram acrescentadas. A pequena marca no começo dos parágrafos (I.1) dá o capítulo e a seção, na '
            'numeração usual das edições, que é como se cita a obra.\n\n'
            '**O original.** O latim não aparece ao lado: o texto digital disponível vem de uma edição moderna.'),
        'fontes': [
            {'nome': 'The Latin Library: Augustinus, Confessiones', 'url': 'http://www.thelatinlibrary.com/august.html',
             'nota': 'texto latino de base'},
            {'nome': 'Knöll, CSEL 33 (Viena, 1896), no Internet Archive', 'url': 'https://archive.org/details/sanctiaureliaugu33augu',
             'nota': 'edição crítica antiga, para conferência'},
        ],
    },
}

PARTES = [(f'Livro {r}', '', [f'livro-{k:02d}.txt']) for k, r in enumerate(ROMANOS, 1)]
