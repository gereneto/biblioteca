"""Quincas Borba — decisões editoriais sobre o texto estabelecido.

EMENDAS: (tipo, busca, troca) na grafia do texto-base.
  'erro'  — erro tipográfico de 1891 (os da errata do próprio livro que as edições revistas
            ainda não corrigem por si);
  'ocr'   — erro das transcrições digitais, conferido no fac-símile.
As lições da edição revista (1896/1899) entram sozinhas: ver config.TRADICAO.
"""

EMENDAS = [
    # errata impressa na edição de 1891
    ('erro', 'nacional e previlegiada', 'nacional e privilegiada'),
    # transcrições
    ('ocr', 'com a tranca cahida', 'com a trança cahida'),
    ('erro', 'os seus pretextos de trabalho', 'os seus petrechos de trabalho'),
    # edição revista: lições em que as modernas concordam, mas que o confronto automático não
    # pegou (uma delas traz erro de digitação no mesmo ponto)
    ('edicao', 'Se a mana Piedade tem casado', 'Se mana Piedade tem casado'),
    ('edicao', 'disse uma ou duas cousas', 'disse uma ou duas frases'),
    ('edicao', 'conduzil-a aonde o seu desejo', 'conduzil-a onde o seu desejo'),
]

AJUSTES = [
    ('grafia', 'razões ditas no', 'capítulo', 'cap .', 'XXXV'),
]

MANUAL = {}
VERSOS = {}
TITULOS = {}
