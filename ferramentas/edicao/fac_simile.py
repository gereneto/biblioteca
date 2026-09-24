"""Consulta ao fac-símile: acha a página de um trecho (pelo texto do Wikisource) e recorta a imagem
do Wikimedia Commons, empilhando vários trechos numa folha para conferência visual."""
import hashlib
import os
import re
import urllib.parse

from . import rede
from .fontes import cache


def _norm(s):
    return re.sub(r'\s+', ' ', re.sub(r"<[^>]+>|\{\{[^}]*\}\}|'''?", ' ', s)).lower()


def achar(paginas, trecho):
    q = _norm(trecho)
    achados = []
    for n, v in sorted(paginas.items()):
        corpo = re.sub(r'<noinclude>.*?</noinclude>', '', v['texto'], flags=re.S)
        linhas = [l for l in corpo.split('\n') if l.strip()]
        if q in _norm(' '.join(linhas)):
            pos = next((i for i, l in enumerate(linhas) if q.split(' ')[0] in _norm(l)
                        and q[:15] in _norm(' '.join(linhas[i:i + 3]))), None)
            achados.append((n, pos, len(linhas)))
    return achados


def imagem(obra_id, arquivo, n, largura=960):
    nome = arquivo.replace(' ', '_')
    h = hashlib.md5(nome.encode('utf-8')).hexdigest()
    url = (f'https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{urllib.parse.quote(nome)}/'
           f'page{n}-{largura}px-{urllib.parse.quote(nome)}.jpg')
    destino = cache(obra_id, f'facsimile/p{n}.jpg')
    rede.baixar(url, destino, pausa=1.5)
    return destino


def folha(obra_id, arquivo, paginas, trechos, saida):
    """Recorta cada trecho e empilha em imagens de 3 recortes: saida_0.png, saida_1.png..."""
    from PIL import Image, ImageDraw
    recortes = []
    for q in trechos:
        ach = achar(paginas, q)
        if not ach:
            print('não achei:', q)
            continue
        n, li, tot = ach[0]
        img = Image.open(imagem(obra_id, arquivo, n))
        W, H = img.size
        y = H / 2 if li is None else 0.10 * H + 0.83 * H * (li / max(tot, 1))
        c = img.crop((0, max(0, int(y - 0.16 * H)), W, min(H, int(y + 0.16 * H))))
        c = c.resize((int(c.width * 0.8), int(c.height * 0.8)))
        ImageDraw.Draw(c).rectangle((0, 0, c.width, 22), fill='white')
        ImageDraw.Draw(c).text((5, 5), f'{q}  [p.{n}]', fill='red')
        recortes.append(c)
    arquivos = []
    for k in range(0, len(recortes), 3):
        g = recortes[k:k + 3]
        folha_ = Image.new('RGB', (max(c.width for c in g), sum(c.height + 10 for c in g)), 'white')
        y = 0
        for c in g:
            folha_.paste(c, (0, y)); y += c.height + 10
        nome = f'{saida}_{k // 3}.png'
        folha_.save(nome)
        arquivos.append(nome)
    return arquivos


# ------------------------------------------------------------------ fac-símiles em PDF (Brasiliana USP etc.)

def pdf_folha(pdf, trechos, saida, dpi=110):
    """Acha cada trecho no texto (OCR) das páginas do PDF e empilha as páginas encontradas, 2 por folha."""
    import fitz
    from PIL import Image, ImageDraw
    doc = fitz.open(pdf)
    textos = [_norm(doc[k].get_text()) for k in range(doc.page_count)]
    imagens = []
    for q in trechos:
        qn = _norm(q)
        k = next((i for i, t in enumerate(textos) if qn in t), None)
        if k is None:
            print('não achei:', q)
            continue
        pix = doc[k].get_pixmap(dpi=dpi)
        im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        ImageDraw.Draw(im).rectangle((0, 0, im.width, 18), fill='white')
        ImageDraw.Draw(im).text((4, 3), f'{q}  [pág. {k + 1}]', fill='red')
        imagens.append(im)
    arquivos = []
    for k in range(0, len(imagens), 2):
        g = imagens[k:k + 2]
        f = Image.new('RGB', (sum(i.width for i in g) + 10, max(i.height for i in g)), 'white')
        x = 0
        for i in g:
            f.paste(i, (x, 0)); x += i.width + 10
        nome = f'{saida}_{k // 2}.png'
        f.save(nome)
        arquivos.append(nome)
    return arquivos
