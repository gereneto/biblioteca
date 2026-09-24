"""Memórias Póstumas de Brás Cubas — decisões editoriais sobre o texto estabelecido.

EMENDAS: (tipo, busca, troca) na grafia do texto-base (tokens separados como no texto).
  'revisao' — lição da edição de 1896, conferida no fac-símile, que o confronto automático
              perdeu (o OCR estava ilegível no ponto e as transcrições são da edição de 1881);
  'erro'    — erro tipográfico da própria edição de 1896, corrigido.
AJUSTES: (tipo, antes, de, para, depois) em tokens do texto já atualizado.
MANUAL: grafia atual de palavras que as edições de referência não resolvem.
"""

EMENDAS = [
    # --- lições de 1896 (fac-símile)
    ('revisao', 'supplicas; ainda grunhiu', 'supplicas, grunhiu'),
    ('revisao', 'Cuido haver dito, no cap. XIII', 'Cuido haver dito, no cap. XIV'),
    ('revisao', 'a das ultimas lettras; com a differenca', 'a das ultimas lettras; com a differença'),
    ('revisao', 'continuou o Luiz Dutra', 'continuou Luiz Dutra'),
    ('revisao', 'duvida que o Luiz Dutra exultava', 'duvida que Luiz Dutra exultava'),
    ('revisao', 'Confidencia ¶ O Lobo Neves', 'Confidencia ¶ Lobo Neves'),
    ('revisao', 'o futuro bacharel do cap. VIII', 'o futuro bacharel do cap. VI'),
    ('revisao', 'vamos levai-o ao Pharoux', 'vamos leval-o ao Pharoux'),
    ('revisao', 'o nosso lunch', 'o nosso luncheon'),
    ('revisao', 'desejoso do a ver', 'desejoso de a ver'),
    ('revisao', 'andando o tempo, desabotou-se', 'andando o tempo, desabotoou-se'),
    ('revisao', '13 ¶ O Cotrim tirou-me', '13 ¶ Cotrim tirou-me'),
    ('revisao', 'para mim. E referiu-lhe', 'para mim. Referiu-lhe'),
    ('revisao', 'Relêde o Cap. XXVIII', 'Relêde o cap. XXVII'),
    ('revisao', 'ainda se lembra do cap. XXXIII', 'ainda se lembra do cap. XXIII'),
    ('revisao', 'á porta da sala. O Jacob foi', 'á porta da sala. Jacob foi'),
    ('revisao', 'o Dr. B. pergutou-lhe', 'o Dr. B. perguntou-lhe'),
    ('revisao', 'fechei-lhe a porta... Uf!', 'fechei-lhe a porta...'),
    ('revisao', 'a fórma é pittoresca', 'a fórma é pintoresca'),
    ('revisao', '¶ Vá de intermedio, e contemos […] Mas vamos ao epitaphio.', ''),
    ('revisao', 'os seus mortos á valla commum', 'os seus mortos na valla commum'),
    ('revisao', '— Disputai-a aos outros', '— Disputal-a aos outros'),
    ('revisao', 'e, çomquanto a minha', 'e, comquanto a minha'),
    ('revisao', 'cinco contos da praia da Gambôa', 'cinco contos da praia de Gambôa'),
    ('revisao', 'preferi dormir, que é modo interino', 'preferi dormir, que é um modo interino'),
    ('revisao', 'vi passar a cavallo afilha', 'vi passar a cavallo a filha'),
    ('revisao', 'camarote, como Cotrim, e', 'camarote, com o Cotrim, e'),
    # --- erros de 1896
    ('erro', 'se pode talver dizer', 'se pode talvez dizer'),
    ('erro', 'Machado de Assiz.', 'Machado de Assis.'),
    ('erro', 'impressão suave e linsongeira', 'impressão suave e lisongeira'),
    ('erro', 'era ainda um fórma de egoismo', 'era ainda uma fórma de egoismo'),
    ('erro', 'Eu fiz-lhe ainda alguma objecções', 'Eu fiz-lhe ainda algumas objecções'),
    ('erro', 'perguntou-me Quincas Borbas', 'perguntou-me Quincas Borba'),
]

AJUSTES = [
    ('grafia', 'enfado , de', 'máu estar', 'mal-estar', ', de fadiga'),
    # pontuação de 1896 (fac-símile), contra as transcrições de 1881
    ('pontuacao', 'admitir-me às anedotas', ',', '', 'reais ou não'),
    ('pontuacao', 'anos de peregrinação', '', ',', 'atendi'),
    ('pontuacao', 'frouxamente as cortinas', ';', ',', 'e eu fiquei'),
    ('pontuacao', 'olhando para a mulher', '..', '.', '¶ — Que'),
    ('pontuacao', 'abrigo da mendicidade', ';', ':', 'era uma'),
    ('pontuacao', 'o nosso filho', ', por exemplo .', 'por exemplo ...', '¶ Lá me'),
    ('pontuacao', 'Quero deixar aqui , entre parêntesis', '', ',', 'meia dúzia'),
    ('pontuacao', 'que de um terceiro andar .', ')', '', '¶ #CXX'),
]

MANUAL = {
    'Job': 'Jó',
    'Jacob': 'Jacó',
    'emphasis': 'ênfase',
    'Madrid': 'Madri',
    'Bagdad': 'Bagdá',
    'presumpção': 'presunção',
    'Smyrna': 'Esmirna',
    'stigmada': 'estigmada',
    'cincoenta': 'cinquenta',
    'Cincoenta': 'Cinquenta',
    'tic-tac': 'tique-taque',
    'asthma': 'asma',
    'anti-asthmaticas': 'antiasmáticas',
    'Almanak': 'Almanaque',
    'stoicismo': 'estoicismo',
    'statica': 'estática',
    'absorpção': 'absorção',
    'extasis': 'êxtase',
    'circumstancias': 'circunstâncias',
    'mór': 'mor',
    'lisongeira': 'lisonjeira',
    'Gambôa': 'Gamboa',
    'Ursa-Maior': 'Ursa Maior',
    'destruiram-lhe': 'destruíram-lhe',
}

VERSOS = {}

TITULOS = {'X': 'Naquele dia', 'XXXVII': 'Enfim!', 'CXIX': 'Parêntesis', 'CXXXIX': "De como não fui ministro d'Estado"}
