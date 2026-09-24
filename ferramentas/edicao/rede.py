"""Acesso à rede com cache em disco e paciência com limites de requisição."""
import json
import os
import time
import urllib.parse
import urllib.request

AGENTE = 'biblioteca-pessoal/0.2 (estabelecimento de textos em dominio publico; github.com/gereneto/biblioteca)'


def baixar(url, destino=None, dados=None, cabecalhos=None, tentativas=6, pausa=1.0):
    """Baixa `url`. Se `destino` existe, lê do disco. Devolve bytes."""
    if destino and os.path.exists(destino) and os.path.getsize(destino) > 0:
        with open(destino, 'rb') as f:
            return f.read()
    h = {'User-Agent': AGENTE}
    h.update(cabecalhos or {})
    ultimo = None
    for k in range(tentativas):
        try:
            req = urllib.request.Request(url, data=dados, headers=h)
            with urllib.request.urlopen(req, timeout=90) as r:
                corpo = r.read()
            break
        except Exception as e:  # 429, 5xx, rede
            ultimo = e
            time.sleep(pausa * 4 * (k + 1))
    else:
        raise RuntimeError(f'falhou: {url}: {ultimo}')
    time.sleep(pausa)
    if destino:
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, 'wb') as f:
            f.write(corpo)
    return corpo


def baixar_json(url, destino=None, **kw):
    return json.loads(baixar(url, destino, **kw).decode('utf-8'))


def wikisource_api(params, destino=None, lingua='pt'):
    params = dict(params, format='json')
    url = f'https://{lingua}.wikisource.org/w/api.php?' + urllib.parse.urlencode(params)
    return baixar_json(url, destino)
