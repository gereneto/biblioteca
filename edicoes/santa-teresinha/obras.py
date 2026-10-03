"""Santa Teresinha — as obras publicadas, a divisão dos manuscritos e as páginas «Sobre esta tradução»."""

FONTE_ARQUIVOS = {'nome': 'Arquivos do Carmelo de Lisieux', 'url': 'https://archives.carmeldelisieux.fr',
                  'nota': 'texto francês da edição crítica (Nouvelle Édition du Centenaire), base da tradução'}
FONTE_ANTIGA = {'nome': 'Site antigo dos Arquivos (cópia do Internet Archive)',
                'url': 'https://web.archive.org/web/2019/http://www.archives-carmel-lisieux.fr/carmel/index.php',
                'nota': 'segundo testemunho, para conferir passagens duvidosas'}

TRATAMENTO = (
    '**A tradução.** Português do Brasil, fiel ao sentido e ao tom de Teresa, sem acréscimos nem '
    'explicações. O _vous_ com que ela se dirige às madres, aos padres, aos tios e a Deus nas orações '
    'formais é traduzido por _vós_; o _tu_ (a Jesus, a Celina, às noviças) fica _tu_. As reticências, as '
    'exclamações repetidas e as maiúsculas de reverência (_Amor_, _Céu_, _Esposo_) estão onde ela as '
    'pôs; o que ela sublinhou vai em itálico. As citações da Escritura são traduzidas como Teresa as '
    'escreve, muitas vezes de memória. Os nomes de família e de religião tomam a forma portuguesa usual '
    '(Paulina, Celina, Madre Inês de Jesus, Irmã Maria do Sagrado Coração); os sobrenomes ficam em '
    'francês.\n\n'
    '**O original ao lado.** O botão «Francês», no alto da página de leitura, mostra o texto de Teresa '
    'junto da tradução.')

EDICAO = lambda apresentacao, fontes=None: {
    'titulo': 'Sobre esta tradução',
    'apresentacao': apresentacao,
    'fontes': fontes or [FONTE_ARQUIVOS, FONTE_ANTIGA],
}

TRADUCAO = lambda titulo: {'lingua': 'francês', 'codigo': 'fr', 'titulo': titulo}

# Partes da «História de uma alma»: (manuscrito, folha onde a parte começa, quantos parágrafos
# depois do primeiro que começa nessa folha, sigla, título). Teresa não dividiu os cadernos em
# capítulos; as partes seguem os três manuscritos e, no Ms A, as três épocas que ela mesma distingue
# na sua vida (até a morte da mãe, 13r; até o Natal de 1886, 45v; daí em diante). Títulos nossos.
PARTES_MANUSCRITOS = [
    ('A', 'A 2r', 0, 'Ms A', 'A história de uma florzinha branca'),
    ('A', 'A 4r', 0, 'Ms A', 'Primeira época: Alençon (1873–1877)'),
    ('A', 'A 13r', 1, 'Ms A', 'Segunda época: os Buissonnets (1877–1882)'),
    ('A', 'A 25v', 0, 'Ms A', 'A entrada de Paulina no Carmelo e a doença (1882–1883)'),
    ('A', 'A 33r', 0, 'Ms A', 'A primeira comunhão e os escrúpulos (1884–1886)'),
    ('A', 'A 45v', 0, 'Ms A', 'Terceira época: a graça do Natal (1886–1887)'),
    ('A', 'A 55v', 0, 'Ms A', 'A viagem a Roma (1887)'),
    ('A', 'A 67r', 0, 'Ms A', 'A entrada no Carmelo (1888–1890)'),
    ('A', 'A 76r', 0, 'Ms A', 'A profissão e a oferenda ao Amor (1890–1895)'),
    ('B', 'B 1r', 0, 'Ms B', 'Carta à Irmã Maria do Sagrado Coração'),
    ('B', 'B 2r', 0, 'Ms B', 'Minha vocação é o Amor'),
    ('C', 'C 1r', 0, 'Ms C', 'A pequena via e a provação da fé'),
    ('C', 'C 8r', 0, 'Ms C', 'O mandamento novo'),
    ('C', 'C 22r', 0, 'Ms C', 'As noviças e os irmãos missionários'),
    ('C', 'C 33v', 0, 'Ms C', '«Atrai-me, e correremos»'),
]

# Viradas entre os trechos de tradução em que a frase continua: o parágrafo é um só.
JUNTAR = {'A 24r', 'A 66r'}

OBRAS = [
    {
        'id': 'historia-de-uma-alma', 'fonte': 'manuscritos',
        'titulo': 'História de uma Alma', 'subtitulo': 'Manuscritos autobiográficos',
        'ano': 1895, 'datas': '1895–1897', 'genero': 'Autobiografia',
        'divisao': {'singular': 'parte', 'plural': 'partes', 'rotulo': 'nome', 'agrupar': True},
        'traducao': TRADUCAO('Manuscrits autobiographiques'),
        'edicao': EDICAO(
            '**O texto.** Teresa escreveu três cadernos, hoje chamados Manuscritos A, B e C. O primeiro '
            '(1895), dirigido à irmã Paulina, Madre Inês de Jesus, então priora, conta a infância e os '
            'primeiros anos no Carmelo. O segundo (setembro de 1896) é uma carta à irmã mais velha, Maria, '
            'Irmã Maria do Sagrado Coração, com a oração em que Teresa descobre que a sua vocação é o '
            'Amor. O terceiro (junho de 1897), dirigido a Madre Maria de Gonzaga, foi escrito nos últimos '
            'meses da doença. Depois da morte de Teresa, Madre Inês reuniu os três, com muitos retoques, '
            'sob o título _Histoire d\'une âme_ (1898). Esta tradução segue o que Teresa de fato escreveu, '
            'publicado pela primeira vez em 1956 e hoje na edição crítica dos Arquivos do Carmelo de '
            'Lisieux.\n\n'
            '**A divisão.** Teresa não dividiu os cadernos em capítulos: escreveu de seguida, folha após '
            'folha. As partes desta edição seguem os três manuscritos e, dentro do primeiro, as três épocas '
            'que a própria Teresa distingue na sua vida — até a morte da mãe; até o Natal de 1886; daí em '
            'diante —, com subdivisões nas viradas do relato. Os títulos das partes são desta edição. A '
            'pequena marca no meio do texto (A 45v) indica onde começa cada folha do manuscrito, que é como '
            'se costuma citar Teresa.\n\n' + TRATAMENTO),
    },
    {
        'id': 'cartas-de-santa-teresinha', 'fonte': 'cartas',
        'titulo': 'Cartas', 'ano': 1877, 'datas': '1877–1897', 'genero': 'Cartas',
        'divisao': {'singular': 'carta', 'plural': 'cartas', 'rotulo': 'n'},
        'traducao': TRADUCAO('Correspondance'),
        'edicao': EDICAO(
            '**O texto.** As cartas de Teresa que se conservaram, da primeira, de 1877, aos quatro anos, '
            'ao último bilhete, de agosto de 1897, na numeração da edição crítica (LT 1 a LT 266, mais a '
            'LT 31 B e três de número _bis_). Escritas à família, às irmãs carmelitas, às noviças e aos dois '
            '«irmãos» missionários, o padre Bellière e o padre Roulland. As cartas que Teresa recebeu não '
            'estão aqui.\n\n'
            '**Cabeçalho de cada carta.** Número, destinatário e data, como a edição crítica os fixou. '
            'Indicações dos editores, como frente e verso de um santinho, vão entre colchetes.\n\n' + TRATAMENTO),
    },
    {
        'id': 'poesias-de-santa-teresinha', 'fonte': 'poesias',
        'titulo': 'Poesias', 'ano': 1893, 'datas': '1893–1897', 'genero': 'Poesia',
        'divisao': {'singular': 'poema', 'plural': 'poemas', 'rotulo': 'n'},
        'traducao': TRADUCAO('Poésies'),
        'edicao': EDICAO(
            '**O texto.** Os 54 poemas de Teresa (PN 1 a PN 54, com o PN 18 _bis_) e os 8 suplementares '
            '(PS 1 a PS 8), na numeração e no texto da edição crítica. Quase todos foram escritos a pedido, '
            'para uma festa, uma profissão ou uma irmã, e muitos para serem cantados sobre árias conhecidas, '
            'cujo nome vai no começo do poema, em francês.\n\n'
            '**A tradução em verso.** Os poemas foram traduzidos em verso, pelo método do Versificador: '
            'cada verso português tem a medida do francês (o alexandrino continua alexandrino; o '
            'decassílabo, decassílabo), o esquema de rimas é o do original, com rima grave onde Teresa '
            'rima no feminino e aguda onde rima no masculino, e os refrões se repetem como no original. '
            'Assim os poemas podem, em princípio, ser cantados nas mesmas árias. Cada verso foi conferido '
            'com o programa de escansão do Versificador. Quando a medida e a rima obrigaram a ceder, '
            'cedeu-se primeiro a palavra literal, depois o ornamento; a imagem central de cada estrofe e o '
            'que ela diz da fé foram preservados.\n\n' + TRATAMENTO,
            [FONTE_ARQUIVOS, FONTE_ANTIGA,
             {'nome': 'Versificador (Solar Editora)', 'nota': 'método de tradução de poesia e conferência métrica'}]),
    },
    {
        'id': 'recreacoes-piedosas', 'fonte': 'recreacoes',
        'titulo': 'Recreações Piedosas', 'ano': 1894, 'datas': '1894–1897', 'genero': 'Teatro',
        'divisao': {'singular': 'recreação', 'plural': 'recreações', 'rotulo': 'n'},
        'traducao': TRADUCAO('Récréations pieuses'),
        'edicao': EDICAO(
            '**O texto.** As oito peças que Teresa escreveu para o recreio das festas da comunidade, '
            'representadas pelas próprias carmelitas (RP 1 a RP 8, na numeração da edição crítica): duas '
            'sobre Joana d\'Arc; três do Natal e da infância de Jesus (os anjos no presépio, o pequeno '
            'mendigo de Natal, a fuga para o Egito); Jesus em Betânia; o _Triunfo da humildade_; e Santo '
            'Estanislau Kostka. Misturam diálogo em prosa e canções em verso.\n\n'
            '**A tradução.** A prosa segue os critérios das outras obras; os versos foram traduzidos pelo '
            'método do Versificador, com a medida, as rimas e os refrões do original, conferidos verso a '
            'verso. Os nomes de quem fala vão em versalete; as rubricas, em itálico.\n\n' + TRATAMENTO,
            [FONTE_ARQUIVOS, FONTE_ANTIGA,
             {'nome': 'Versificador (Solar Editora)', 'nota': 'método de tradução de poesia e conferência métrica'}]),
    },
    {
        'id': 'oracoes-de-santa-teresinha', 'fonte': 'oracoes',
        'titulo': 'Orações', 'ano': 1889, 'datas': '1889–1897', 'genero': 'Orações',
        'divisao': {'singular': 'oração', 'plural': 'orações', 'rotulo': 'n'},
        'traducao': TRADUCAO('Prières'),
        'edicao': EDICAO(
            '**O texto.** As 21 orações de Teresa (Pri 1 a Pri 21, na numeração da edição crítica), entre '
            'elas o bilhete que ela levou sobre o coração no dia da profissão (Pri 2) e a Oferenda de mim '
            'mesma como vítima de holocausto ao Amor Misericordioso do bom Deus (Pri 6), de 9 de junho de '
            '1895.\n\n' + TRATAMENTO),
    },
]
