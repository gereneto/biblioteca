"""Esaú e Jacó — decisões editoriais sobre o texto estabelecido.

EMENDAS: (tipo, busca, troca) na grafia do texto-base.
  'erro' — erro tipográfico da edição de 1904 (os dois exemplares da Brasiliana o trazem);
  'ocr'  — erro só da transcrição do Gutenberg (o impresso traz a forma certa).
"""

EMENDAS = [
    # erros do impresso de 1904
    ('erro', 'gostou de Nativividade', 'gostou de Natividade'),
    ('erro', 'Perecem-lhe bons', 'Parecem-lhe bons'),
    ('erro', 'Provalmente era', 'Provavelmente era'),
    ('erro', 'dos antecendentes', 'dos antecedentes'),
    ('erro', 'dia das antiquidades', 'dia das antiguidades'),
    ('erro', 'pedra augular', 'pedra angular'),
    ('erro', 'mordia os beições', 'mordia os beiços'),
    ('erro', 'as duas carragens', 'as duas carruagens'),
    ('erro', 'não deliberamente', 'não deliberadamente'),
    ('erro', 'com a homoepathia', 'com a homoeopathia'),
    ('erro', 'correu inmediato', 'correu immediato'),
    ('erro', 'ou qualqer das', 'ou qualquer das'),
    ('erro', 'as rodam passam', 'as rodas passam'),
    ('erro', 'Paulo, vagorosamente', 'Paulo, vagarosamente'),
    ('erro', 'folhas de de papel', 'folhas de papel'),
    ('erro', 'entendeu que que eram', 'entendeu que eram'),
    ('erro', 'tenha a suas', 'tenha as suas'),
    ('erro', 'quebrar-me as as vidraças', 'quebrar-me as vidraças'),
    ('erro', 'são seu filhos', 'são seus filhos'),
    ('erro', 'Ora, meus Deus', 'Ora, meu Deus'),
    ('erro', 'morto deste alguns', 'morto desde alguns'),
    ('erro', 'desdobrou na duas pessoas', 'desdobrou nas duas pessoas'),
    ('erro', 'Era umas dessas', 'Era uma dessas'),
    ('erro', 'duplicada e e mysteriosa', 'duplicada e mysteriosa'),
    ('erro', 'outro no nariz', 'outra no nariz'),
    ('erro', 'Minas, Rio Janeiro', 'Minas, Rio de Janeiro'),
    ('erro', 'sabia ler escrever', 'sabia ler e escrever'),
    ('erro', 'arrancou a a dama', 'arrancou a dama'),
    ('erro', 'Ou então que que é', 'Ou então que é'),
    ('erro', 'claramente, com as de cima', 'claramente, como as de cima'),
    ('erro', 'as mariposas e as ratos', 'as mariposas e os ratos'),
    ('erro', 'Trazia até a desejo', 'Trazia até o desejo'),
    ('erro', 'um modo de de apanhar', 'um modo de apanhar'),
    ('erro', 'jornaes frequente', 'jornaes frequentes'),
    ('erro', 'noticia da um velho', 'noticia de um velho'),
    ('erro', 'escreveu as conselheiro', 'escreveu ao conselheiro'),
    ('erro', 'mais do que transparencia do papel', 'mais do que transparecia do papel'),
    # erros só do Gutenberg
    ('ocr', 'da barça de Petropolis', 'da barca de Petropolis'),
    ('ocr', 'duas barças', 'duas barcas'),
    ('ocr', 'um biIhetinho', 'um bilhetinho'),
    ('ocr', 'olhando paaa o', 'olhando para o'),
    ('ocr', 'como ura sonho', 'como um sonho'),
    ('ocr', 'conferiu, poi achar', 'conferiu, por achar'),
    ('ocr', 'estava de pé. Era novembro', 'estava de pé. Em novembro'),
]

AJUSTES = []

MANUAL = {
    'Almanack': 'Almanaque',
    'Nova-York': 'Nova York',
    'Smyrna': 'Esmirna',
    'absorpção': 'absorção',
    'alli': 'ali',
    'cans': 'cãs',
    'caranquejola': 'caranguejola',
    'cincoenta': 'cinquenta',
    'club': 'clube',
    'emphasis': 'ênfase',
    'historica': 'histórica',
    'homoeopathia': 'homeopatia',
    'presumpção': 'presunção',
    'psalmo': 'salmo',
    'póde': 'pode',
    'quinta-feiras': 'quintas-feiras',
    'registo': 'registro',
    'slavos': 'eslavos',
    'spirita': 'espírita',
    'spiritas': 'espíritas',
    'spiritismo': 'espiritismo',
    'stoicos': 'estoicos',
    'Jacob': 'Jacó',
}

VERSOS = {}
TITULOS = {}
