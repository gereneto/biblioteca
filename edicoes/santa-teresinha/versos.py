"""Confere a métrica dos versos de um texto no formato da Biblioteca (recreações piedosas).

Os versos são as linhas começadas por «| »; cada bloco de versos seguidos é uma estrofe. Falas,
rubricas e prosa ficam de fora. O resultado vai para o molde.mjs do Versificador.

Uso:
  python edicoes/santa-teresinha/versos.py <texto.txt> <molde.txt> [--so-problemas]
  python edicoes/santa-teresinha/versos.py <texto.txt> --extrair      (só imprime os versos)
"""
import os
import subprocess
import sys
import tempfile

VERSIFICADOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..',
                            'Solar', 'Editora', 'Versificador')
MOLDE = os.path.normpath(os.path.join(VERSIFICADOR, 'ferramentas', 'molde.mjs'))


def extrair(arq):
    estrofes, atual = [], []
    for linha in open(arq, encoding='utf-8').read().split('\n'):
        if linha.startswith('|'):
            atual.append(linha[1:].strip())
        elif atual:
            estrofes.append(atual)
            atual = []
    if atual:
        estrofes.append(atual)
    return '\n\n'.join('\n'.join(e) for e in estrofes) + '\n'


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    texto = extrair(sys.argv[1])
    if sys.argv[2] == '--extrair':
        sys.stdout.write(texto)
        return
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(texto)
    try:
        subprocess.run(['node', MOLDE, f.name, sys.argv[2]] + sys.argv[3:], check=False)
    finally:
        os.unlink(f.name)


if __name__ == '__main__':
    main()
