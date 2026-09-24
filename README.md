# Biblioteca

Sítio de leitura de textos em domínio público. Escolhe-se o autor, depois a obra, e lê-se
parte por parte, seguindo a divisão interna do próprio livro (capítulos, cantos, atos...).

Primeira obra: **Machado de Assis — _Dom Casmurro_**, em texto estabelecido para esta
biblioteca (ver abaixo).

## Como funciona

Site estático puro: HTML, CSS e um arquivo de JavaScript. Sem build, sem dependências,
sem npm. Basta abrir o `index.html` no navegador; funciona até sem servidor.

```
index.html                              página única; lista os arquivos de conteúdo
css/estilo.css                          toda a aparência
js/app.js                               roteador e renderização
conteudo/autores.js                     cadastro dos autores
conteudo/<autor>/<obra>.js              uma obra por arquivo
netlify.toml                            configuração de publicação (opcional)
```

As rotas usam `#`, de modo que qualquer hospedagem estática serve:

| Rota                     | Página                                  |
| ------------------------ | --------------------------------------- |
| `#/`                     | capa: autores e "continuar a leitura"   |
| `#/a/machado-de-assis`   | obras do autor                          |
| `#/o/dom-casmurro`       | folha de rosto e índice                 |
| `#/o/dom-casmurro/12`    | 12ª parte (aqui, o capítulo XII)        |
| `#/o/dom-casmurro/sobre` | notas sobre o texto desta edição        |

Na leitura, as setas ← e → do teclado passam de uma parte para outra. O site guarda no
navegador a última parte lida de cada obra, o tema (claro ou escuro) e o tamanho da letra.

Para ver no computador com um servidor local:

```bash
python -m http.server 8765
```

e abrir `http://localhost:8765`.

## Acrescentar um autor

Em `conteudo/autores.js`:

```js
BIBLIOTECA.autor({
  id: 'eca-de-queiros',              // usado nas rotas e no campo "autor" das obras
  nome: 'Eça de Queirós',
  nomeCompleto: 'José Maria de Eça de Queirós',
  vida: '1845–1900',
  ordem: 'Queirós, Eça de',          // posição na lista de autores
  nota: 'Uma linha de apresentação (opcional).'
});
```

## Acrescentar uma obra

1. Crie `conteudo/<autor>/<obra>.js`:

```js
BIBLIOTECA.obra({
  id: 'o-primo-basilio',             // único no site inteiro
  autor: 'eca-de-queiros',
  titulo: 'O Primo Basílio',
  ano: 1878,
  genero: 'Romance',
  divisao: { singular: 'capítulo', plural: 'capítulos' },
  descricao: 'Uma frase sobre o livro, não sobre o enredo (opcional).',
  edicao: { apresentacao: `Notas sobre o texto (opcional).` },
  partes: [
    { n: 'I', titulo: '', texto: `Primeiro parágrafo.

Segundo parágrafo.` },
    { n: 'II', titulo: '', texto: `...` }
  ]
});
```

2. Acrescente a linha no `index.html`, junto das outras (sempre depois do `app.js`):

```html
<script defer src="conteudo/eca-de-queiros/o-primo-basilio.js"></script>
```

### Formato do texto

- Use crases (`` ` ``) para abrir e fechar o texto de cada parte.
- Parágrafos separados por uma linha em branco.
- `_itálico_` entre sublinhados; `**negrito**` só nas notas de edição.
- Versos, inscrições e citações compostas à parte: uma linha por verso, começando com `| `.
- Um parágrafo que começa com minúscula (continuação da frase depois de uma citação em
  verso) aparece sem recuo.
- Partes sem título mostram no índice o começo do texto.

## O texto de _Dom Casmurro_

Base: a 1ª edição (H. Garnier, 1899), estabelecida palavra por palavra a partir de três
transcrições independentes (Projeto Gutenberg, Wikisource e J. Stolfi/Unicamp), com o
fac-símile como árbitro. Foram corrigidos os erros tipográficos evidentes e adotadas as
lições da 2ª edição (1900, a última em vida do autor) atestadas por toda a tradição
posterior. A ortografia foi atualizada pelo Acordo de 1990 sem tocar no vocabulário, nas
formas e na sintaxe do autor (mesóclises, _cousa_, _dous_, colocação pronominal,
pontuação). A lista completa das intervenções está na página
**Sobre esta edição** do próprio site (`#/o/dom-casmurro/sobre`).

## Publicar

Qualquer hospedagem estática serve, com a raiz do repositório como pasta publicada:

- **GitHub Pages**: Settings → Pages → *Deploy from a branch* → `main` / raiz.
- **Netlify**: importar o repositório, sem comando de build, *publish directory* `.`
  (o `netlify.toml` já traz isso).
