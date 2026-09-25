"""Chaves de comparação e regras de grafia.

- chave():  neutraliza diferenças gráficas miúdas (acentos, consoantes dobradas...) para alinhar.
- esqueleto()/mesma_palavra(): iguala grafia antiga e moderna da MESMA palavra, mas mantém
  distintas as formas que o autor usa e a língua ainda registra (cousa/coisa, dous/dois).
- ao1990(): mudanças do Acordo Ortográfico de 1990 sobre a grafia brasileira de 1971.
"""
import re
import unicodedata

PONT = {'«': '"', '»': '"', '“': '"', '”': '"', '„': '"', '–': '—', '-': '—', '…': '...', '....': '...', '.....': '...'}


def sem_acento(s):
    return ''.join(ch for ch in unicodedata.normalize('NFD', s) if unicodedata.category(ch) != 'Mn')


def chave(w):
    """Chave de alinhamento (grafia antiga ~ moderna)."""
    if w.startswith('#'):
        return w
    if not re.match(r'\w', w) or w == '_':
        return PONT.get(w, w)
    k = sem_acento(w).lower().replace('’', "'").replace('~', '-').replace("'", '')
    k = k.replace('ph', 'f').replace('th', 't').replace('rh', 'r').replace('y', 'i')
    k = re.sub(r'ch(?=[rlt])', 'c', k)
    k = re.sub(r'([a-z])\1', r'\1', k)
    k = re.sub(r'(?<=[aeiou])h(?=[aeiou])', '', k)
    k = re.sub(r'sc(?=[ei])', 'c', k)
    k = re.sub(r'(?<=[aeiou])ct', 't', k)
    k = re.sub(r'(?<=[aeiou])pt', 't', k)
    k = k.replace('mn', 'n').replace('z', 's')
    k = re.sub(r'ae\b', 'ai', k)
    k = re.sub(r'ae(?=s\b)', 'ai', k)
    k = re.sub(r'oe\b', 'oi', k)
    return k


_DOBRADA = re.compile(r'([bcdfgjklmnpqrstvxz])\1')


def esqueleto(w, ch='x'):
    k = w.lower().replace('ç', 's')
    k = sem_acento(k).replace('’', "'").replace("'", '').replace('~', '-').replace('-', '')
    k = k.replace('ph', 'f').replace('th', 't').replace('rh', 'r').replace('y', 'i')
    k = _DOBRADA.sub(lambda m: m.group(1), k)
    k = re.sub(r'ch(?=[rl])', 'k', k)
    k = k.replace('ch', ch)                          # chicara->xícara / archanjo->arcanjo
    k = re.sub(r'x(?=[bcdfgjklmnpqrstvz])', 's', k)  # extranho, exquisito
    k = k.replace('gm', 'm').replace('bt', 't')      # augmentar, subtil
    k = re.sub(r'(?<=n)c(?=[tsç])', '', k)           # distincto, sancção
    k = re.sub(r'sc(?=[ei])', 's', k)
    k = k.replace('z', 's')
    k = re.sub(r'c(?=[ei])', 's', k)
    k = re.sub(r'g(?=[ei])', 'j', k)
    k = k.replace('h', '')
    k = _DOBRADA.sub(lambda m: m.group(1), k)
    k = re.sub(r'(?<=[aeiou])[cp](?=[tds])', '', k)  # acto, escripto, anecdota, acção
    k = re.sub(r'(?<=[ml])p(?=t)', '', k)            # prompto, assumpto, esculptor
    k = re.sub(r'm$', 'n', k)
    k = re.sub(r'm(?=[bcdfgjklnpqrstvxz])', 'n', k)
    k = re.sub(r'(?<=[aeiou])g(?=n)', '', k)         # signal
    k = k.replace('mn', 'n')
    k = k.replace('qu', 'k').replace('c', 'k')
    k = re.sub(r'ae(?=s?$)', 'ai', k)                # pae, vae
    k = re.sub(r'oe(?=s?$)', 'oi', k)
    k = re.sub(r'eo(?=s?$)', 'eu', k)                # chapéo
    k = k.replace('i', 'e').replace('u', 'o')        # vogais átonas
    k = re.sub(r'([a-z])\1', lambda m: m.group(1), k)
    return k


def mesma_palavra(antiga, nova):
    return esqueleto(antiga) == esqueleto(nova) or esqueleto(antiga, 'k') == esqueleto(nova)


# ------------------------------------------------------------------ Acordo de 1990

_AO_PALAVRAS = {
    'pára': 'para', 'péla': 'pela', 'pélas': 'pelas', 'pêlo': 'pelo', 'pêlos': 'pelos', 'pélo': 'pelo',
    'pólo': 'polo', 'pólos': 'polos', 'pêra': 'pera', 'côa': 'coa', 'côas': 'coas',
}


def ao1990(w):
    lw = w.lower()
    if lw in _AO_PALAVRAS:
        n = _AO_PALAVRAS[lw]
        return n[0].upper() + n[1:] if w[:1].isupper() else n
    w = w.replace('ü', 'u').replace('Ü', 'U')
    w = re.sub(r'êem\b', 'eem', w)
    w = re.sub(r'ôo(s?)\b', r'oo\1', w)
    m = re.search(r'([éó])i', w)
    if m and re.search(r'[aeiouáéíóú]', w[m.end():]):
        w = w[:m.start()] + ('e' if m.group(1) == 'é' else 'o') + 'i' + w[m.end():]
    w = re.sub(r'(?<=[aeiou][iu])ú(?=[a-z]+[aeo]s?\b)', 'u', w)
    w = re.sub(r'(?<=[aeiou][iu])í(?=[a-z]+[aeo]s?\b)', 'i', w)
    return w


MESES = {'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto',
         'setembro', 'outubro', 'novembro', 'dezembro'}


def igualar_caixa(antiga, nova):
    """A caixa segue a edição antiga, salvo meses (minúscula pelo Acordo)."""
    if not nova:
        return nova
    if len(nova) > 1 and nova.isupper() and not antiga.isupper():
        nova = nova.lower()
    if antiga[:1].isupper() and not nova[:1].isupper():
        return nova if nova.lower() in MESES else nova[0].upper() + nova[1:]
    if antiga[:1].islower() and nova[:1].isupper() and not antiga.isupper():
        return nova[0].lower() + nova[1:]
    return nova


# ------------------------------------------------------------------ formas antigas de palavras atuais
# Variantes que a língua abandonou (ou que só Portugal conserva) trocadas pela forma brasileira
# atual. Não entram aqui palavras que continuam vivas no registro literário (mui, assaz,
# outrossim), nem a sintaxe do autor (mesóclises, colocação dos pronomes, contrações como «lho»).
FORMAS_ATUAIS = [
    (r'cous(a|as|inha|inhas)', r'cois\1'),
    (r'dous', 'dois'),
    (r'doud(o|a|os|as|amente|ice|ices|ejar|ejava|ejavam|ivanas)', r'doid\1'),
    (r'endoud(\w+)', r'endoid\1'),
    (r'afout(o|a|os|as|eza|amente)', r'afoit\1'),
    (r'subti(l|s|leza|lezas|lmente)', r'suti\1'),
    (r'mor', 'maior'),                                   # «a mor parte» (capitão-mor fica: é outra palavra)
    (r'contacto(s?)', r'contato\1'),
    (r'estupefact(o|a|os|as)', r'estupefat\1'),
    (r'erect(o|a|os|as)', r'eret\1'),
]
_FORMAS = [(re.compile(a + r'\Z'), b) for a, b in FORMAS_ATUAIS]


def forma_atual(w):
    """cousa -> coisa, Dous -> Dois; as demais palavras voltam iguais."""
    baixa = w.lower()
    for rx, sub in _FORMAS:
        if rx.match(baixa):
            nova = rx.sub(sub, baixa)
            if w.isupper() and len(w) > 1:
                return nova.upper()
            return nova[0].upper() + nova[1:] if w[:1].isupper() else nova
    return w
