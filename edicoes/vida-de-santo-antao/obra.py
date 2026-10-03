"""Vida de Santo Antão, de Santo Atanásio — dados para ferramentas/traducoes.py."""

META = {
    'id': 'vida-de-santo-antao', 'autor': 'santo-atanasio', 'titulo': 'Vida de Santo Antão',
    'ano': 357, 'datas': 'c. 357', 'genero': 'Hagiografia',
    'divisao': {'singular': 'parte', 'plural': 'partes', 'rotulo': 'nome'},
    'traducao': {'lingua': 'grego', 'codigo': 'grc', 'titulo': 'Βίος Ἀντωνίου'},
    'original_ao_lado': False,
    'edicao': {
        'titulo': 'Sobre esta tradução',
        'apresentacao': (
            '**O texto.** Santo Atanásio, bispo de Alexandria, escreveu a _Vida de Antão_ em grego pouco depois '
            'da morte do santo, em 356, em forma de carta aos monges do Ocidente, que lhe pediam notícias do '
            'pai dos monges do deserto. É a primeira grande vida de um santo monge e o modelo de toda a '
            'hagiografia posterior; Agostinho conta nas _Confissões_ (VIII, 6) o efeito que a leitura dela teve '
            'na conversão de dois oficiais em Tréveris. A tradução foi feita do grego, sobre o texto da '
            '_Patrologia Graeca_ de Migne (vol. 26, que reproduz a edição de Montfaucon), com o apoio da '
            'tradução latina antiga de Evágrio de Antioquia.\n\n'
            '**A divisão.** Os 94 capítulos da numeração usual (a pequena marca no começo dos parágrafos) '
            'estão agrupados em cinco partes, com títulos desta edição: a vocação e os primeiros combates; o '
            'longo discurso de Antão aos monges; a montanha interior; a fé e a sabedoria de Antão diante dos '
            'hereges, dos filósofos e dos imperadores; a morte.\n\n'
            '**A tradução.** Português do Brasil, fiel ao sentido e ao tom, sem acréscimos nem explicações. '
            'Atanásio aos destinatários e Antão aos monges falam por _vós_. As citações da Escritura são '
            'traduzidas do grego de Atanásio (a Septuaginta, nos salmos), e não de uma Bíblia moderna.\n\n'
            '**O original.** O grego não aparece ao lado: o texto digital disponível é uma digitação protegida.'),
        'fontes': [
            {'nome': 'Migne, Patrologia Graeca 26 (Paris, 1857), no Internet Archive',
             'url': 'https://archive.org/details/patrologiae_cursus_completus_gr_vol_026', 'nota': 'texto grego de base'},
            {'nome': 'Evágrio, Vita B. Antonii abbatis (Wikisource latina)', 'url': 'https://la.wikisource.org/wiki/Vita_B._Antonii_abbatis',
             'nota': 'tradução latina antiga, para conferência'},
        ],
    },
}

PARTES = [
    ('Prólogo, 1–15', 'A vocação e os primeiros combates', ['vida.txt#0-15']),
    ('16–43', 'O discurso aos monges', ['vida.txt#16-43']),
    ('44–66', 'A montanha interior', ['vida.txt#44-66']),
    ('67–88', 'A fé e a sabedoria de Antão', ['vida.txt#67-88']),
    ('89–94', 'A morte de Antão', ['vida.txt#89-94']),
]
