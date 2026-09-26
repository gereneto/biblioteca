"""Esaú e Jacó — fontes.

Uma só edição em vida do autor: Garnier, 1904 (título «Esaú e Jacob»). É a edição-base.
Testemunhos: Projeto Gutenberg (sem o último capítulo, transcrito aqui do fac-símile) e o OCR
de dois exemplares da Brasiliana USP. O Wikisource não entra: quase nada revisado.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ferramentas'))
from edicao import fontes  # noqa: E402
from edicao.ocr import limpar as limpar_ocr, paragrafos_como  # noqa: E402
from edicao.tokens import VERSO  # noqa: E402

OBRA = 'esau-e-jaco'

META = {
    'id': OBRA,
    'autor': 'machado-de-assis',
    'titulo': 'Esaú e Jacó',
    'ano': 1904,
    'genero': 'Romance',
    'divisao': {'singular': 'capítulo', 'plural': 'capítulos'},
    'descricao': 'Romance publicado em 1904, narrado a partir dos cadernos do conselheiro Aires.',
}

BASE = 'pg'
CORRELACIONADOS = [('o1', 'o2')]         # o mesmo OCR (mesmos erros sistemáticos) em dois exemplares
UM_VOTO = True                            # ... e por isso valem um voto só
DESEMPATE_LEXICO = True                   # empate sem apoio: vence a leitura sem palavras inexistentes
REFERENCIAS = [('mdn', True), ('mec', False)]

PDFS = {'o1': 'https://digital.bbm.usp.br/bitstream/bbm/4763/4/45000017798_Output.o.pdf',
        'o2': 'https://digital.bbm.usp.br/bitstream/bbm/7817/1/45000018599_Output.o.pdf'}
ADVERTENCIA = 'Advertência'
EPIGRAFE = VERSO + "Dico, che quando l'anima mal nata...\nDANTE."
TITULO_FALSO = 'ESAÚ E JACOB'

# O Gutenberg acaba no cap. CXX; o CXXI foi transcrito do fac-símile (exemplar bbm/4763,
# pp. 356–358), na grafia do impresso.
CAP_CXXI = {'n': 'CXXI', 'titulo': 'Ultimo.', 'paras': [
    'Castor e Pollux fôram os nomes que um deputado pôz aos dous gemeos, quando elles tornaram á '
    'camara, depois da missa do setimo dia. Tal era a união que parecia aposta. Entravam juntos, '
    'andavam juntos, saíam juntos. Duas ou trez vezes votaram juntos, com grande escandalo dos '
    'respectivos amigos politicos. Tinham sido eleitos para se baterem, e acabavam traindo os '
    'eleitores. Ouviram nomes duros, reprehensões acerbas. Quizeram renunciar ao cargo; Pedro, '
    'entretanto, achou um meio conciliatorio.',
    '— O nosso dever politico é votar com os amigos, disse elle ao irmão. Votemos com elles. Mamãe '
    'só nos pediu concordia pessoal. Na tribuna, sim, ninguem nos levará a atacar um ao outro; no '
    'debate e no voto podemos e devemos dissentir.',
    '— Apoiado; mas, se você um dia achar que deve vir para os meus arraiaes, venha. Você nem eu '
    'hypothecamos o juizo.',
    '— Apoiado.',
    'Pessoalmente, nem sempre havia este accordo. Os contrastes não eram raros, nem os impetos, mas '
    'a lembrança da mãe estava tão fresca, a morte tão proxima, que elles sopitavam qualquer '
    'movimento, por mais que lhes custasse, e viviam unidos. Na camara, o dissentimento politico e a '
    'fusão pessoal cada vez os fazia mais admiraveis.',
    'A camara terminou os seus trabalhos em dezembro. Quando tornou em maio seguinte, só Pedro lhe '
    'appareceu. Paulo tinha ido a Minas, uns diziam que a ver noiva, outros que a catar diamantes, '
    'mas parece que foi só a passeio. Pouco depois regressou, entrando na camara sósinho, ao '
    'contrario do anno anterior em que os dous irmãos subiam as escadas juntos, quasi pegados. O '
    'olho dos amigos não tardou em descobrir que não viviam bem, pouco depois que se detestavam. Não '
    'faltou indiscreto que lhes perguntasse a um e a outro o que houvera no intervallo das duas '
    'sessões; nenhum respondia nada. O presidente da camara, a conselho do _leader_, nomeou-os para a '
    'mesma commissão. Pedro e Paulo, cada um por sua vez, fôram pedir-lhe que os dispensasse.',
    '— São outros, disse o presidente na sala do café.',
    '— Totalmente outros, confirmaram os deputados presentes.',
    'Ayres soube daquella conclusão no dia seguinte, por um deputado, seu amigo, que morava em uma das '
    'casas de pensão do Cattete. Tinha ido almoçar com elle, e, em conversação, como o deputado '
    'soubesse das relações de Ayres com os dous collegas, contou-lhe o anno anterior e o presente, a '
    'mudança radical e inexplicavel. Contou tambem a opinião da camara.',
    'Nada era novidade para o conselheiro, que assistira á ligação e desligação dos dous gemeos. '
    'Emquanto o outro falava, elle ia remontando os tempos e a vida delles, recompondo as lutas, os '
    'contrastes, a aversão reciproca, apenas disfarçada, apenas interrompida por algum motivo mais '
    'forte, mas persistente no sangue, como necessidade virtual. Não lhe esqueceram os pedidos da '
    'mãe, nem a ambição desta em os ver grandes homens.',
    '— O senhor que se dá com elles diga-me o que é que os fez mudar, concluiu o amigo.',
    '— Mudar? Não mudaram nada; são os mesmos.',
    '— Os mesmos?',
    '— Sim, são os mesmos.',
    '— Não é possivel.',
    'Tinham acabado o almoço. O deputado subiu ao quarto para se compôr de todo. Ayres foi esperal-o '
    'á porta da rua. Quando o deputado desceu, vinha com um achado nos olhos.',
    '— Ora, espere, não será... Quem sabe se não será a herança da mãe que os mudou? Póde ter sido a '
    'herança, questões de inventario...',
    'Ayres sabia que não era a herança, mas não quiz repetir que elles eram os mesmos, desde o utero. '
    'Preferiu acceitar a hypothese, para evitar debate, e saiu apalpando a botoeira, onde viçava a '
    'mesma flôr eterna.',
]}


def arrumar(obra):
    """Números e títulos uniformes; a epígrafe de Dante no alto do cap. I; o título do livro
    (que a advertência anuncia) no fim dela."""
    for p in obra:
        n = re.sub(r'^CAP[ÍI]TULO\s+', '', p['n'].strip(), flags=re.I)
        if 'ADVERT' in (n + p['titulo']).upper():
            p['n'], p['titulo'] = '', ADVERTENCIA
        else:
            p['n'] = 'I' if n.upper() == 'PRIMEIRO' else n
    fora = re.compile(r"^\W*(_?Dico, che|DANTE|Dante|ESA[UÚ] E JAC)", re.I)
    for p in obra:
        p['paras'] = [x for x in p['paras'] if not fora.match(x.lstrip(VERSO))]
    adv = next((p for p in obra if p['titulo'] == ADVERTENCIA), None)
    if adv:
        adv['paras'].append(TITULO_FALSO)
    cap1 = next(p for p in obra if p['n'] == 'I')
    cap1['paras'].insert(0, EPIGRAFE)
    return [p for p in obra if p['paras'] or p['titulo']]


def ocr(chave, guias):
    t = fontes.pdf_texto(OBRA, PDFS[chave], 'bbm_' + PDFS[chave].split('/')[-3])
    obra = fontes.ocr_por_linhas(t, 'ADVERT', '\nÍNDICE' if '\nÍNDICE' in t else '\nINDICE',
                                 r'^.{0,6}?CAP[IÍ1l]\s?TU\s?L[O0]\s+(?P<n>[A-Za-zÍí1 .]{1,12})$',
                                 lixo=[r'^ESA\S{1,2}\s+E\s+JAC\S{1,3}B$'], titulo_seguinte=True,
                                 sem_numero=[(r'^ADVERT[ÊE]NCIA$', ADVERTENCIA)])
    obra, n = limpar_ocr(obra, guias)
    print(f'OCR {chave}: palavras corrigidas pelas guias:', n)
    return obra


def _mdn():
    return fontes.machadodeassis_net(OBRA, OBRA, 13998)


def transcricoes():
    pg = fontes.gutenberg(OBRA, 56737, [r'^(?P<t>ADVERTÊNCIA)$', r'^CAPITULO (?P<n>PRIMEIRO|[IVXLC]+)$'],
                          inicio='ADVERTÊNCIA', fim='ÍNDICE')
    pg = [p for p in pg if p['n'] != 'CXXI'] + [dict(CAP_CXXI, paras=list(CAP_CXXI['paras']))]
    mdn = _mdn()
    base = arrumar(pg)
    return {'pg': base,
            'o1': paragrafos_como(arrumar(ocr('o1', [pg, mdn])), base),
            'o2': paragrafos_como(arrumar(ocr('o2', [pg, mdn])), base)}


def modernas():
    mec = fontes.internet_archive(OBRA, 'esauJaco', 'esau.pdf').replace('\f', '\n')
    nup = fontes.pdf_texto(OBRA, 'https://www.curso-objetivo.br/vestibular/assets/download/obras-literarias/'
                           'machado-de-assis/esau-e-jaco.pdf', 'nupill').replace('\f', '\n')
    cab_mec = [r'^(?P<t>ADVERTÊNCIA)$', r'^CAPÍTULO (?P<n>PRIMEIRO|[IVXLC]+) (?P<t>.+)$']
    cab_nup = [r'^CAPÍTULO (?P<n>PRIMEIRO|[IVXLC]+) ?/ ?(?P<t>.+)$']
    return {
        'mdn': arrumar(_mdn()),
        'mec': arrumar(fontes.texto_por_linhas(mec, cab_mec)),
        'nup': arrumar(fontes.texto_por_linhas(nup, cab_nup)),
    }
