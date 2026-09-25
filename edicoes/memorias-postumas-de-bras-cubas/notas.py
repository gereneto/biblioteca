"""Memórias Póstumas de Brás Cubas — texto da página «Sobre esta edição»."""

COMENTARIO = '''Memórias Póstumas de Brás Cubas — Machado de Assis
   Gerado por ferramentas/texto.py a partir de edicoes/memorias-postumas-de-bras-cubas/.
   Não edite à mão: corrija as decisões nessa pasta e rode de novo com --publicar.

   Formato do texto de cada parte:
     - parágrafos separados por uma linha em branco;
     - _itálico_ entre sublinhados;
     - linhas começadas por "| " formam um bloco de versos (ou inscrição), uma linha por verso.'''

APRESENTACAO = '''**Texto-base.** Este texto reproduz a terceira edição das _Memórias póstumas de Brás Cubas_ (Rio de Janeiro, H. Garnier, 1896), a última revista pelo autor que hoje se pode ler em fac-símile, digitalizada pela Brasiliana USP. É a edição do «Prólogo da terceira edição», em que Machado conta ter emendado «ainda alguma cousa» e suprimido «duas ou três dúzias de linhas» do livro de 1881.

**Como foi estabelecido.** O fac-símile de 1896 só traz uma camada de texto feita por reconhecimento automático (OCR), cheia de ruído. Ela foi confrontada palavra por palavra com duas transcrições independentes da edição de 1881 (a do Projeto Gutenberg e a do Wikisource, esta só nas páginas já revisadas) e com três edições modernas. Onde 1896 difere de 1881 — um capítulo reescrito («Parêntesis», que substituiu a máxima de La Bruyère), trechos suprimidos, centenas de pequenas emendas —, valeu a lição de 1896 sempre que o OCR a confirma. Os pontos duvidosos foram conferidos nas imagens do fac-símile, assim como a dedicatória e o prólogo, que o OCR não lê.

**A edição de 1899.** A quarta edição (Garnier, 1899), a última publicada em vida do autor, não está disponível na internet. As edições modernas parecem segui-la (o machadodeassis.net intitula o prólogo «da quarta edição»), mas, onde elas diferem de 1896 sem que se possa conferir a fonte, ficou a lição de 1896. As diferenças mais notáveis vão listadas abaixo.

**Correções.** Corrigiram-se só os erros tipográficos evidentes da edição de 1896 (lista abaixo). Nada mais foi emendado.

**Ortografia.** A grafia foi atualizada pelo Acordo Ortográfico de 1990 (_Braz_ → Brás, _idéa_ → ideia, _elle_ → ele, _pae_ → pai). As formas antigas de palavras que continuam em uso passaram à forma atual (_cousa_ → coisa, _dous_ → dois, _doudo_ → doido, _subtil_ → sutil, _a mor parte_ → a maior parte). O vocabulário e as construções do autor ficaram como estão — as mesóclises, a colocação dos pronomes, a pontuação, os travessões e as aspas angulares, os itálicos e as abreviaturas _S._ (São), _D._ (Dona) e _cap._ (capítulo). Nomes estrangeiros de uso corrente em português tomaram a forma atual (_Job_ → Jó, _Jacob_ → Jacó, _Madrid_ → Madri, _Bagdad_ → Bagdá, _Smyrna_ → Esmirna).

**Divisão.** O livro tem 160 capítulos curtos, numerados em romanos e titulados pelo autor, precedidos da dedicatória, do prólogo e da nota «Ao leitor». Cada um é uma página desta biblioteca.'''

BASE = 'Edição de 1896'

SECOES = {
    'erros': {'titulo': 'Erros tipográficos da edição de 1896 corrigidos',
              'explica': 'Grafia de 1896 nas duas colunas.'},
    'pontuacao': {'titulo': 'Pontuação de 1896 restituída',
                  'explica': 'Pontos em que o texto saído do confronto (transcrições de 1881 e edições modernas) '
                             'pontua diferente da edição de 1896, conferida no fac-símile. Grafia atualizada.',
                  'de': 'Confronto', 'para': 'Edição de 1896'},
    'mantidas': {'titulo': 'Lições de 1896 mantidas',
                 'explica': 'Pontos em que as edições modernas leem diferente.'},
}

FONTES = [
    {'nome': 'Fac-símile da 3ª edição, 1896 (Brasiliana USP)', 'url': 'https://digital.bbm.usp.br/handle/bbm/7815',
     'nota': 'texto-base; usado para conferir as leituras'},
    {'nome': 'Fac-símile da 1ª edição em livro, 1881 (Brasiliana USP)', 'url': 'https://digital.bbm.usp.br/handle/bbm/4826',
     'nota': 'Typographia Nacional'},
    {'nome': 'Projeto Gutenberg, nº 54829', 'url': 'https://www.gutenberg.org/ebooks/54829',
     'nota': 'transcrição da edição de 1881, grafia original'},
    {'nome': 'Wikisource em português', 'url': 'https://pt.wikisource.org/wiki/Mem%C3%B3rias_P%C3%B3stumas_de_Br%C3%A1s_Cubas',
     'nota': 'transcrição da edição de 1881, página a página; usadas só as páginas revisadas'},
    {'nome': 'machadodeassis.net (Fundação Casa de Rui Barbosa)', 'url': 'https://machadodeassis.net/texto/memorias-postumas-de-bras-cubas/5985',
     'nota': 'texto moderno; referência para a ortografia'},
    {'nome': 'Obra Completa, Nova Aguilar (MEC / Domínio Público)', 'url': 'https://archive.org/details/memoriasPostumasBrasCubas',
     'nota': 'texto moderno'},
    {'nome': 'Edições Câmara', 'url': 'https://archive.org/details/memorias_postumas_bras_cubas',
     'nota': 'texto moderno de outra linhagem'},
]

# (trecho do texto final, leitura de outras edições, observação)
MANTIDAS = [
    ('Prólogo da terceira edição', 'Prólogo da quarta edição (machadodeassis.net)', 'título da edição de 1896'),
    ('repotreou-se', 'repoltreou-se', 'assim em 1881 e em 1896'),
    ('o da vida e da morte', 'e o da morte', ''),
    ('destruíram-lhe a flor das graças', 'destruíam-lhe', ''),
    ('que é a das últimas letras', 'que é das últimas letras', ''),
    ('singularmente espantoso este meu sistema', 'esse meu sistema', ''),
    ('Damasceno não sabia mais de nada', 'mais nada', ''),
    ('cinco contos da praia de Gamboa', 'de Botafogo', 'os cinco contos foram achados na praia de Botafogo (cap. LII); o deslize é do autor, em 1881 e em 1896'),
    ('Muhammed', 'Muamede', ''),
]

ERROS_ANTERIORES = []
