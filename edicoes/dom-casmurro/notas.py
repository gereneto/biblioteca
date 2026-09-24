"""Dom Casmurro — texto da página «Sobre esta edição»."""

COMENTARIO = '''Dom Casmurro — Machado de Assis
   Gerado por ferramentas/texto.py a partir de edicoes/dom-casmurro/. Não edite à mão:
   corrija as decisões em edicoes/dom-casmurro/ e rode de novo com --publicar.

   Formato do texto de cada parte:
     - parágrafos separados por uma linha em branco;
     - _itálico_ entre sublinhados;
     - linhas começadas por "| " formam um bloco de versos (ou inscrição), uma linha por verso.'''

APRESENTACAO = '''**Texto-base.** Este texto reproduz a primeira edição de _Dom Casmurro_ (Rio de Janeiro e Paris, H. Garnier, 1899; impressa em Paris no fim de 1899 e posta à venda em janeiro de 1900). Foi estabelecido palavra por palavra a partir de três transcrições independentes dessa edição — a do Projeto Gutenberg, feita sobre as imagens da Biblioteca Nacional, a do Wikisource e a de Jorge Stolfi (Unicamp), estas duas sobre o exemplar digitalizado pela Brasiliana USP. Onde elas discordavam, valeu o fac-símile.

**A segunda edição.** Em abril de 1900 saiu a segunda edição, a última publicada em vida do autor e base da edição crítica da Comissão Machado de Assis (1977). Ela não está disponível na internet. Por isso, só se adotaram as lições em que todas as edições posteriores consultadas concordam contra a primeira — sinal de que vêm da segunda. Onde a tradição se divide, ficou a leitura da primeira edição (ver as listas abaixo).

**Correções.** Corrigiram-se os erros tipográficos evidentes da primeira edição, quase todos de concordância («todo a pessoa», «todos os noites»), como já fizeram a segunda edição e a edição crítica. Nada mais foi emendado.

**Ortografia.** A grafia foi atualizada pelo Acordo Ortográfico de 1990 (_chapéo_ → chapéu, _elle_ → ele, _Capitú_ → Capitu, _idéa_ → ideia). Só a grafia: o vocabulário, as formas e as construções do autor ficaram como estão — _cousa_, _dous_, _quatorze_, as mesóclises (_dir-me-ia_, _dar-se-ia_), a colocação dos pronomes, a pontuação, os travessões e as aspas angulares, os itálicos, a abreviatura _S._ (São) e os contos de réis (_1:070$000_). Quando os dicionários registram duas grafias para a mesma palavra, ficou a do autor.

**Divisão.** O livro tem 148 capítulos curtos, numerados em romanos e titulados pelo autor. Cada capítulo é uma página desta biblioteca.'''

FONTES = [
    {'nome': 'Fac-símile da 1ª edição (Brasiliana USP)', 'url': 'https://digital.bbm.usp.br/handle/bbm/4828', 'nota': 'também no Wikimedia Commons, usado para conferir as leituras'},
    {'nome': 'Fac-símile da 1ª edição (Biblioteca do Senado)', 'url': 'https://www2.senado.leg.br/bdsf/item/id/242816', 'nota': 'outro exemplar da mesma edição'},
    {'nome': 'Projeto Gutenberg, nº 55752', 'url': 'https://www.gutenberg.org/ebooks/55752', 'nota': 'transcrição da 1ª edição, grafia original'},
    {'nome': 'Wikisource em português', 'url': 'https://pt.wikisource.org/wiki/Dom_Casmurro', 'nota': 'transcrição revisada, página a página, da 1ª edição'},
    {'nome': 'Jorge Stolfi, Unicamp', 'url': 'https://www.ic.unicamp.br/~stolfi/voynich/Notes/110/work/Texts/port/cso/', 'nota': 'transcrição da 1ª edição conferida com o fac-símile'},
    {'nome': 'machadodeassis.net (Fundação Casa de Rui Barbosa)', 'url': 'https://machadodeassis.net/texto/dom-casmurro/11503', 'nota': 'texto moderno feito a partir da edição crítica e da edição de A. da Gama Kury; referência para a ortografia'},
    {'nome': 'Obra Completa, Nova Aguilar, 1994 (MEC / Domínio Público)', 'url': 'https://machado.mec.gov.br/', 'nota': 'texto moderno'},
    {'nome': 'NUPILL-UFSC / Biblioteca Virtual do Estudante', 'url': 'https://www.literaturabrasileira.ufsc.br/', 'nota': 'texto moderno de outra linhagem'},
    {'nome': 'Edições Câmara (2016 e 2019) e Fundação Biblioteca Nacional', 'url': '', 'nota': 'textos modernos de uma terceira linhagem'},
    {'nome': 'M. M. Santiago-Almeida, «Para uma nova edição crítica de Dom Casmurro», Caligrama 15(2), 2010', 'url': 'https://periodicos.ufmg.br/index.php/caligrama/article/view/30000', 'nota': 'confronto das edições de 1899, 1900, 1924, 1957 e da edição crítica'},
]

# (trecho do texto final, leitura de outras edições, observação)
MANTIDAS = [
    ('servir a prolongar as frases', 'servia (edições posteriores); serviam (em «Um agregado», 1896)', 'lição das três primeiras edições, conservada também pela edição crítica'),
    ('sapatos de cordavão', 'cordovão', ''),
    ('não pode gostar disto', 'disso', ''),
    ('prima Justina lho ensinasse', 'lhe', 'também «depois de lho propor» e «Assim lho disse»'),
    ('aplaudiu a distinção', 'aplaudia', ''),
    ('despedia-se de três amigas', 'duas amigas', 'emenda da edição crítica (só duas são nomeadas); a tradição mais antiga conserva «três»'),
    ('pé de cadeira lascado', 'lascada', ''),
    ('dous vãos de telhado', 'telhados', ''),
    ('que no-las matassem', 'matasse', 'a edição crítica também conserva «matassem»'),
    ('Lembro-me de um preto', 'Lembra-me', ''),
    ('É bem, qualquer que seja', 'E bem', 'lição das três primeiras edições (1899, 1900, 1924), também no título; «E bem» vem da edição Jackson (1957)'),
]

# erros da 1ª edição que as transcrições já trazem corrigidos (registrados por J. Stolfi,
# marcados [sic] no Wikisource ou apontados por Santiago-Almeida): (capítulo, 1ª edição, corrigido)
ERROS_ANTERIORES = [
    ('XXXI', 'prima Justiina', 'prima Justina'),
    ('XXXIII', 'DesGrieux', 'Des Grieux'),
    ('XXXIX', 'teimeu com meu pae', 'teimou com meu pae'),
    ('XLI', 'manha, no, não podia', 'manha, não, não podia'),
    ('XLIII', 'Todos essas bellas', 'Todas essas bellas'),
    ('LXXXIII', 'dentro o por fóra', 'dentro e por fóra'),
    ('LXXXIV', 'portas meio-cerrados', 'portas meio-cerradas'),
    ('XCII', 'deste capitulo e só', 'deste capitulo é só'),
    ('CIII', 'A felicitade tem boa alma (título)', 'A felicidade tem boa alma'),
    ('CXXVI', 'ssocegar', 'socegar'),
    ('CXXVI', 'scismasse vontade', 'scismasse á vontade'),
    ('CXLV', 'et quiz apertal-o', 'e quiz apertal-o'),
]
