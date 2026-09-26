"""Memorial de Aires — decisões editoriais sobre o texto estabelecido.

EMENDAS: (tipo, busca, troca) na grafia do texto-base.
  'erro' — erro tipográfico da edição de 1908 (conferido no fac-símile ou atestado pelos OCRs);
  'ocr'  — erro só da transcrição do Gutenberg.
"""

EMENDAS = [
    # erros do impresso de 1908
    ('erro', 'provavalmente', 'provavelmente'),
    ('erro', 'convisesse', 'conviesse'),
    ('erro', 'comprenhendo', 'comprehendo'),
    ('erro', 'sucedará', 'succederá'),
    ('erro', 'perlo das', 'perto das'),
    ('erro', 'daquelle senhora', 'daquella senhora'),
    ('erro', 'interioramente', 'interiormente'),
    ('erro', 'ou no loja', 'ou na loja'),
    ('erro', 'daqui, mais não', 'daqui, mas não'),
    ('erro', 'ternura de mão', 'ternura de mãe'),
    ('erro', 'ideia da lá ir', 'ideia de lá ir'),
    ('erro', '20 do Março', '20 de Março'),
    ('erro', '10 Abril', '10 de Abril'),
    ('erro', 'ter bridado', 'ter brigado'),
    ('erro', 'da velhice D. Carmo', 'da velhice de D. Carmo'),
    ('erro', 'o nome de afilhado', 'o nome do afilhado'),
    ('erro', 'a alegria de restabelecimento', 'a alegria do restabelecimento'),
    ('erro', 'por cousa do tempo', 'por causa do tempo'),
    ('erro', 'Tristão adia viagem', 'Tristão adia a viagem'),
    # erros só do Gutenberg
    ('ocr', 'com que que ella', 'com que ella'),
    ('ocr', 'barça de Nicterohy', 'barca de Nicterohy'),
    ('ocr', 'a saudade-ou,', 'a saudade — ou,'),
]

AJUSTES = []

MANUAL = {
    'distingamos-nos': 'distingamo-nos',
    'enfasis': 'ênfase',
    'calis': 'cálix',
    'cans': 'cãs',
    "dou-lh'a": 'dou-lha',
    'cincoenta': 'cinquenta',
    'Excellencia': 'Excelência',
    'Westphalia': 'Westfália',
    'Jacob': 'Jacó',
}

VERSOS = {}
TITULOS = {}
