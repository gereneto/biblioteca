/* ---------------------------------------------------------------
   Biblioteca — aplicação de leitura
   Autor → gênero → obra → parte (capítulo, conto, poema... conforme a obra).

   Rotas (usam # para funcionar em qualquer hospedagem estática
   e também abrindo o index.html direto do disco):
     #/                      capa: autores e "continuar a leitura"
     #/a/<autor>             gêneros em que o autor tem obras
     #/a/<autor>/<genero>    obras do autor nesse gênero (romances, contos, poesia...)
     #/o/<obra>              folha de rosto e índice da obra
     #/o/<obra>/<n>          parte n (1, 2, 3...) da obra
     #/o/<obra>/sobre        notas sobre o texto desta edição
   --------------------------------------------------------------- */

(function () {
  'use strict';

  var dados = { autores: [], obras: [] };

  /* API usada pelos arquivos de conteúdo (carregados depois deste script) */
  window.BIBLIOTECA = {
    autor: function (a) { dados.autores.push(a); },
    obra:  function (o) { dados.obras.push(o); }
  };

  var CHAVE_TEMA  = 'biblioteca:tema';
  var CHAVE_FONTE = 'biblioteca:fonte';
  var CHAVE_ULT   = 'biblioteca:ultimaLeitura';
  var CHAVE_POS   = 'biblioteca:posicao:';      /* + id da obra */

  var app, trilha, progresso;

  /* ----------------------------- utilidades ----------------------------- */

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* Marcação mínima dos textos: _itálico_ e **negrito** */
  function inline(s) {
    return esc(s)
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/_([^_]+)_/g, '<em>$1</em>');
  }

  /* Parágrafos separados por linha em branco; linhas com "| " formam versos;
     parágrafos com "¤ " são notas do autor, reunidas no fim do texto */
  function blocos(texto) {
    var todos = String(texto).trim().split(/\n\s*\n/);
    var notas = todos.filter(function (b) { return /^¤ /.test(b); });
    var html = paragrafos(todos.filter(function (b) { return !/^¤ /.test(b); }));
    if (notas.length) {
      html += '\n<aside class="nota-do-autor"><p class="rotulo">' + (notas.length > 1 ? 'Notas do autor' : 'Nota do autor') + '</p>' +
        paragrafos(notas.map(function (b) { return b.replace(/^¤ /, ''); })) + '</aside>';
    }
    return html;
  }

  function paragrafos(lista) {
    return lista.map(function (b) {
      var linhas = b.split('\n');
      var verso = linhas.every(function (l) { return /^\|\s?/.test(l); });
      if (verso) {
        return '<p class="verso">' + linhas.map(function (l) {
          return inline(l.replace(/^\|\s?/, ''));
        }).join('<br>') + '</p>';
      }
      var p = b.replace(/\s*\n\s*/g, ' ').trim();
      /* parágrafo que continua a frase depois de uma citação em verso */
      var cls = /^[a-zà-ÿ]/.test(p) ? ' class="continua"' : '';
      return '<p' + cls + '>' + inline(p) + '</p>';
    }).join('\n');
  }

  function incipit(texto, limite) {
    var t = String(texto).replace(/^\|\s?/gm, '').replace(/[_*]/g, '').replace(/\s+/g, ' ').trim();
    if (t.length <= limite) return esc(t);
    var corte = t.slice(0, limite);
    corte = corte.slice(0, corte.lastIndexOf(' '));
    return esc(corte) + '…';
  }

  function guardar(chave, valor) {
    try { localStorage.setItem(chave, valor); } catch (e) { /* modo privado */ }
  }
  function ler(chave) {
    try { return localStorage.getItem(chave); } catch (e) { return null; }
  }

  function plural(n, s, p) { return n + ' ' + (n === 1 ? s : p); }
  // partes numeradas (capítulos); dedicatória, prólogo etc. não entram na conta
  function numeradas(o) { return o.partes.filter(function (p) { return p.n; }).length || o.partes.length; }
  function rotuloPasso(p) { return [esc(p.n), p.titulo ? inline(p.titulo) : ''].filter(Boolean).join(' · '); }

  /* Ordem dos gêneros na página do autor e o nome de cada um */
  var GENEROS = ['Romance', 'Novela', 'Contos', 'Poesia', 'Teatro', 'Crônica', 'Crítica', 'Tradução'];
  var PLURAIS = { 'Romance': 'Romances', 'Novela': 'Novelas', 'Contos': 'Contos', 'Poesia': 'Poesia',
    'Teatro': 'Teatro', 'Crônica': 'Crônicas', 'Crítica': 'Crítica', 'Tradução': 'Traduções' };

  function nomeGenero(g) { return PLURAIS[g] || g; }
  /* "Romance" -> "romances" (endereço da página do gênero) */
  function slugGenero(g) {
    return nomeGenero(g).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-');
  }

  /* Contagem de palavras do texto da obra (calculada uma vez) */
  var PALAVRA = /[\p{L}\p{N}]+(?:[-'’][\p{L}\p{N}]+)*/gu;
  function palavras(o) {
    if (o._palavras === undefined) {
      o._palavras = o.partes.reduce(function (n, p) {
        return n + (String(p.texto).replace(/[_*|]/g, ' ').match(PALAVRA) || []).length;
      }, 0);
    }
    return o._palavras;
  }
  function milhar(n) { return n.toLocaleString('pt-BR'); }

  /* "1899 · 148 capítulos · 66.998 palavras"; num conto: "13 capítulos · 18.034 palavras" */
  function fichaObra(o) {
    var d = o.divisao || { singular: 'parte', plural: 'partes' };
    if (o.coletanea) {
      return [o.partes.length > 1 ? plural(numeradas(o), d.singular, d.plural) : '',
        milhar(palavras(o)) + ' palavras'].filter(Boolean).join(' · ');
    }
    return [o.ano ? String(o.ano) : '', plural(numeradas(o), d.singular, d.plural),
      milhar(palavras(o)) + ' palavras'].filter(Boolean).join(' · ');
  }

  /* ----------------------------- contos em coletânea ----------------------------- */

  /* um conto sem capítulos abre direto no texto */
  function linkObra(o) { return '#/o/' + o.id + (o.coletanea && o.partes.length === 1 ? '/1' : ''); }
  function nomeColetanea(o) { return o.coletanea.titulo + (o.coletanea.ano ? ' (' + o.coletanea.ano + ')' : ''); }
  function textoPublicacao(o) { return o.publicacao ? 'Primeira publicação: ' + o.publicacao : ''; }
  /* textos da mesma coletânea, na ordem do livro */
  function daColetanea(o) {
    return dados.obras.filter(function (x) { return x.coletanea && x.coletanea.id === o.coletanea.id; })
      .sort(function (a, b) { return a.coletanea.ordem - b.coletanea.ordem; });
  }
  /* livros: cada coletânea conta uma vez */
  function livros(obras) {
    var vistos = {};
    obras.forEach(function (o) { vistos[o.coletanea ? 'c:' + o.coletanea.id : o.id] = 1; });
    return Object.keys(vistos).length;
  }
  var TEXTOS = { 'Contos': ['conto', 'contos'], 'Poesia': ['poema', 'poemas'] };
  /* [{titulo, ano, obras}]: obras avulsas num grupo sem título, coletâneas pelo ano */
  function porColetanea(obras) {
    var grupos = [], idx = {};
    obras.forEach(function (o) {
      var k = o.coletanea ? o.coletanea.id : '';
      if (!(k in idx)) {
        idx[k] = grupos.length;
        grupos.push({ titulo: o.coletanea ? o.coletanea.titulo : '', ano: o.coletanea ? o.coletanea.ano : o.ano, obras: [] });
      }
      grupos[idx[k]].obras.push(o);
    });
    grupos.forEach(function (g) {
      g.obras.sort(function (a, b) { return a.coletanea && b.coletanea ? a.coletanea.ordem - b.coletanea.ordem : 0; });
    });
    return grupos.sort(function (a, b) { return (a.ano || 0) - (b.ano || 0); });
  }

  /* ----------------------------- consultas ----------------------------- */

  function acharAutor(id) {
    for (var i = 0; i < dados.autores.length; i++) if (dados.autores[i].id === id) return dados.autores[i];
    return null;
  }
  function acharObra(id) {
    for (var i = 0; i < dados.obras.length; i++) if (dados.obras[i].id === id) return dados.obras[i];
    return null;
  }
  function obrasDe(autorId) {
    return dados.obras.filter(function (o) { return o.autor === autorId; })
      .sort(function (a, b) { return (a.ano || 0) - (b.ano || 0) || a.titulo.localeCompare(b.titulo, 'pt'); });
  }
  /* gêneros do autor, na ordem de GENEROS: [{genero, obras}] */
  function generosDe(autorId) {
    var grupos = {};
    obrasDe(autorId).forEach(function (o) {
      var g = o.genero || 'Outros';
      (grupos[g] = grupos[g] || []).push(o);
    });
    return GENEROS.filter(function (g) { return grupos[g]; })
      .concat(Object.keys(grupos).filter(function (g) { return GENEROS.indexOf(g) < 0; }).sort())
      .map(function (g) { return { genero: g, obras: grupos[g] }; });
  }
  function trilhaGenero(a, g) { return { txt: nomeGenero(g), href: '#/a/' + a.id + '/' + slugGenero(g) }; }

  function autoresOrdenados() {
    return dados.autores.slice().sort(function (a, b) {
      return (a.ordem || a.nome).localeCompare(b.ordem || b.nome, 'pt');
    });
  }

  /* Rótulo de uma parte: "Capítulo XII" (numeral da obra) */
  function rotuloParte(obra, parte) {
    if (!parte.n && !parte.titulo) return obra.titulo;                        /* conto sem capítulos */
    if (!parte.n) return String(parte.titulo || '').replace(/[_*]/g, '');   /* contos, poemas: o título */
    /* diários: a data e o ano ("9 de janeiro, 1888") */
    if (obra.divisao && obra.divisao.rotulo === 'titulo') return String(parte.titulo || '').replace(/[_*]/g, '') + ', ' + parte.n;
    var d = obra.divisao ? obra.divisao.singular : 'parte';
    return d.charAt(0).toUpperCase() + d.slice(1) + ' ' + parte.n;
  }

  /* ----------------------------- posição de leitura ----------------------------- */

  function registrarLeitura(obra, i) {
    guardar(CHAVE_POS + obra.id, String(i));
    guardar(CHAVE_ULT, JSON.stringify({ obra: obra.id, i: i }));
  }

  function posicaoSalva(obra) {
    var v = parseInt(ler(CHAVE_POS + obra.id), 10);
    return isNaN(v) || v < 1 || v > obra.partes.length ? null : v;
  }

  function retomada() {
    try {
      var u = JSON.parse(ler(CHAVE_ULT) || 'null');
      if (!u) return null;
      var obra = acharObra(u.obra);
      if (!obra || !obra.partes[u.i - 1]) return null;
      return { obra: obra, i: u.i, parte: obra.partes[u.i - 1] };
    } catch (e) { return null; }
  }

  /* ----------------------------- moldura ----------------------------- */

  function definirTrilha(itens) {
    trilha.innerHTML = itens.map(function (it) {
      return it.href ? '<a href="' + it.href + '">' + esc(it.txt) + '</a>' : '<span>' + esc(it.txt) + '</span>';
    }).join('<span class="sep">›</span>');
  }

  function definirProgresso(frac) {
    if (frac === null) { progresso.hidden = true; return; }
    progresso.hidden = false;
    progresso.firstChild.style.width = (Math.max(0, Math.min(1, frac)) * 100).toFixed(2) + '%';
  }

  function render(html, titulo) {
    app.innerHTML = html;
    document.title = titulo ? titulo + ' · Biblioteca' : 'Biblioteca';
    window.scrollTo(0, 0);
    app.focus({ preventScroll: true });
  }

  /* ----------------------------- páginas ----------------------------- */

  function paginaCapa() {
    definirTrilha([]);
    definirProgresso(null);
    var html = '<div class="folha capa">' +
      '<h1>Biblioteca</h1>' +
      '<p class="subtitulo">Textos em domínio público</p>' +
      '</div><div class="folha">';

    var r = retomada();
    if (r) {
      var rot = rotuloParte(r.obra, r.parte);
      html += '<a class="retomar" href="#/o/' + r.obra.id + '/' + r.i + '">' +
        '<span class="rot">Continuar a leitura</span>' +
        '<span class="alvo">' + esc(r.obra.titulo) + (rot === r.obra.titulo ? '' : ' — ' + esc(rot) +
        (r.parte.titulo && rot.indexOf(String(r.parte.titulo).replace(/[_*]/g, '')) < 0 ? ': ' + inline(r.parte.titulo) : '')) + '</span></a>';
    }

    html += '<p class="secao-titulo">Autores</p>';
    autoresOrdenados().forEach(function (a) {
      var obras = obrasDe(a.id);
      html += '<a class="cartao" href="#/a/' + a.id + '">' +
        '<span class="cartao-titulo">' + esc(a.nome) + '</span>' +
        '<span class="cartao-meta">' + esc(a.vida || '') + (a.vida ? ' · ' : '') + plural(livros(obras), 'obra', 'obras') + '</span>' +
        (obras.length ? '<span class="cartao-texto">' + generosDe(a.id).map(function (x) { return esc(nomeGenero(x.genero)); }).join(' · ') + '</span>' : '') +
        '</a>';
    });
    html += '</div>';
    render(html, '');
  }

  function cabecaAutor(a) {
    return '<header class="cabeca">' +
      '<h1>' + esc(a.nome) + '</h1>' +
      '<p class="meta">' + esc([a.nomeCompleto, a.vida].filter(Boolean).join(' · ')) + '</p>' +
      (a.nota ? '<p class="nota-autor">' + inline(a.nota) + '</p>' : '') +
      '</header>';
  }

  /* Página do autor: escolha do gênero */
  function paginaAutor(id) {
    var a = acharAutor(id);
    if (!a) return naoAchei();
    definirTrilha([{ txt: a.nome }]);
    definirProgresso(null);
    var html = '<div class="folha">' + cabecaAutor(a) + '<p class="secao-titulo">Gêneros</p>';
    generosDe(a.id).forEach(function (x) {
      var grupos = porColetanea(x.obras);
      var titulos = [];
      grupos.forEach(function (g) {
        if (g.titulo) titulos.push(g.titulo);
        else g.obras.forEach(function (o) { titulos.push(o.titulo); });
      });
      var meta = plural(livros(x.obras), 'obra', 'obras');
      if (grupos.some(function (g) { return g.titulo; })) {
        var t = TEXTOS[x.genero] || ['texto', 'textos'];
        meta += ' · ' + plural(x.obras.filter(function (o) { return !o.paratexto; }).length, t[0], t[1]);
      }
      html += '<a class="cartao" href="#/a/' + a.id + '/' + slugGenero(x.genero) + '">' +
        '<span class="cartao-titulo">' + esc(nomeGenero(x.genero)) + '</span>' +
        '<span class="cartao-meta">' + meta + '</span>' +
        '<span class="cartao-texto">' + titulos.map(function (t) { return '<em>' + esc(t) + '</em>'; }).join(', ') + '</span>' +
        '</a>';
    });
    html += '</div>';
    render(html, a.nome);
  }

  /* Obras do autor num gênero: título e ficha (ano, capítulos, palavras) */
  function paginaGenero(id, slug) {
    var a = acharAutor(id);
    if (!a) return naoAchei();
    var x = generosDe(a.id).filter(function (x) { return slugGenero(x.genero) === slug; })[0];
    if (!x) return naoAchei();
    definirTrilha([{ txt: a.nome, href: '#/a/' + a.id }, { txt: nomeGenero(x.genero) }]);
    definirProgresso(null);
    var html = '<div class="folha">' +
      '<header class="cabeca"><h1>' + esc(nomeGenero(x.genero)) + '</h1><p class="meta">' + esc(a.nome) + '</p></header>';
    porColetanea(x.obras).forEach(function (g) {
      if (g.titulo) html += '<p class="secao-titulo"><em>' + esc(g.titulo) + '</em>' + (g.ano ? ' · ' + g.ano : '') + '</p>';
      g.obras.forEach(function (o) {
        var pub = textoPublicacao(o);
        html += '<a class="cartao' + (o.paratexto ? ' paratexto' : '') + '" href="' + linkObra(o) + '">' +
          '<span class="cartao-titulo">' + (o.coletanea ? esc(o.titulo) : '<em>' + esc(o.titulo) + '</em>') + '</span>' +
          '<span class="cartao-meta">' + esc(fichaObra(o)) + '</span>' +
          (pub ? '<span class="cartao-texto">' + inline(pub) + '</span>' : '') +
          '</a>';
      });
    });
    html += '</div>';
    render(html, nomeGenero(x.genero) + ' — ' + a.nome);
  }

  function paginaObra(id) {
    var o = acharObra(id);
    if (!o) return naoAchei();
    var a = acharAutor(o.autor) || { nome: o.autor, id: o.autor };
    var d = o.divisao || { singular: 'parte', plural: 'partes' };
    definirTrilha([{ txt: a.nome, href: '#/a/' + a.id }, trilhaGenero(a, o.genero || 'Outros'), { txt: o.titulo }]);
    definirProgresso(null);

    var pos = posicaoSalva(o);
    var html = '<div class="folha">' +
      '<header class="rosto">' +
      '<p class="rosto-autor">' + esc(a.nome) + '</p>' +
      '<h1>' + esc(o.titulo) + '</h1>' +
      (o.subtitulo ? '<p class="subtitulo-obra">' + inline(o.subtitulo) + '</p>' : '') +
      '<p class="meta">' + (o.coletanea ? '<em>' + esc(o.coletanea.titulo) + '</em>, ' + esc(o.coletanea.ano) + ' · ' : '') + esc(fichaObra(o)) + '</p>' +
      (o.publicacao ? '<p class="publicacao">' + inline(textoPublicacao(o)) + '</p>' : '') +
      (o.descricao ? '<p class="descricao">' + inline(o.descricao) + '</p>' : '') +
      '<p class="acoes">' +
      '<a class="botao" href="#/o/' + o.id + '/' + (pos || 1) + '">' + (pos && pos > 1 ? 'Continuar: ' + esc(rotuloParte(o, o.partes[pos - 1])) : 'Começar a ler') + '</a>' +
      (o.edicao ? ' <a class="botao secundario" href="#/o/' + o.id + '/sobre">Sobre esta edição</a>' : '') +
      '</p>' +
      '</header>' +
      '<p class="secao-titulo">' + esc(d.plural.charAt(0).toUpperCase() + d.plural.slice(1)) + '</p>' +
      '<ol class="indice">';
    /* nos diários, o ano só aparece no índice quando muda */
    var agrupa = o.divisao && o.divisao.rotulo === 'titulo';
    o.partes.forEach(function (p, i) {
      var num = agrupa && i && o.partes[i - 1].n === p.n ? '' : p.n;
      html += '<li' + (pos === i + 1 ? ' class="atual"' : '') + '><a href="#/o/' + o.id + '/' + (i + 1) + '">' +
        '<span class="num">' + esc(num) + '</span>' +
        '<span class="tit">' + (p.titulo ? inline(p.titulo) : '<span class="inc">' + incipit(p.texto, 60) + '</span>') + '</span>' +
        '</a></li>';
    });
    html += '</ol></div>';
    render(html, o.titulo);
  }

  function paginaParte(id, i) {
    var o = acharObra(id);
    if (!o) return naoAchei();
    var p = o.partes[i - 1];
    if (!p) return naoAchei();
    var a = acharAutor(o.autor) || { nome: o.autor, id: o.autor };
    var total = o.partes.length;
    var conto = !!o.coletanea;
    var passos = [
      { txt: a.nome, href: '#/a/' + a.id },
      { txt: o.titulo, href: '#/o/' + o.id },
      { txt: rotuloParte(o, p) }
    ];
    if (conto) {
      passos.splice(1, 0, trilhaGenero(a, o.genero || 'Outros'));
      if (total === 1) passos = passos.slice(0, 2).concat({ txt: o.titulo });
    }
    definirTrilha(passos);
    definirProgresso(i / total);

    /* vizinhos: a parte anterior e a seguinte; nas pontas de um conto, o texto vizinho da coletânea */
    function passo(cls, rel, dir, href, alvo) {
      return '<a class="passo ' + cls + '" href="' + href + '" rel="' + rel + '"><span class="dir">' + dir + '</span><span class="alvo">' + alvo + '</span></a>';
    }
    var navAnt = '<span class="passo vazio"></span>', navSeg;
    var irmaos = conto ? daColetanea(o) : [], k = irmaos.indexOf(o);
    if (i > 1) navAnt = passo('ant', 'prev', '← Anterior', '#/o/' + o.id + '/' + (i - 1), rotuloPasso(o.partes[i - 2]));
    else if (k > 0) navAnt = passo('ant', 'prev', '← Anterior', '#/o/' + irmaos[k - 1].id + '/' + irmaos[k - 1].partes.length, esc(irmaos[k - 1].titulo));
    if (i < total) navSeg = passo('seg', 'next', 'Seguinte →', '#/o/' + o.id + '/' + (i + 1), rotuloPasso(o.partes[i]));
    else if (k >= 0 && k < irmaos.length - 1) navSeg = passo('seg', 'next', 'Seguinte →', '#/o/' + irmaos[k + 1].id + '/1', esc(irmaos[k + 1].titulo));
    else if (conto) navSeg = '<a class="passo seg" href="#/a/' + a.id + '/' + slugGenero(o.genero) + '"><span class="dir">Índice</span><span class="alvo">' + esc(nomeGenero(o.genero)) + '</span></a>';
    else navSeg = '<a class="passo seg" href="#/o/' + o.id + '"><span class="dir">Índice</span><span class="alvo">' + esc(o.titulo) + '</span></a>';

    var cabeca;
    if (conto) {
      /* o conto se apresenta na 1ª parte; os capítulos seguintes só com número e título */
      cabeca = (i === 1 ?
        '<p class="coletanea-parte"><em>' + esc(o.coletanea.titulo) + '</em></p>' +
        '<h1 class="titulo-conto">' + esc(o.titulo) + '</h1>' +
        (o.subtitulo ? '<p class="subtitulo-obra">' + inline(o.subtitulo) + '</p>' : '') +
        (o.publicacao ? '<p class="publicacao">' + inline(textoPublicacao(o)) + '</p>' : '') : '') +
        (total > 1 ? (p.n ? '<p class="num-parte">' + esc(p.n) + '</p>' : '') + (p.titulo ? '<h2>' + inline(p.titulo) + '</h2>' : '') : '');
    } else {
      cabeca = (p.n ? '<p class="num-parte">' + esc(p.n) + '</p>' : '') +
        (p.titulo ? '<h1>' + inline(p.titulo) + '</h1>' : '');
    }

    var html = '<article class="folha leitura">' +
      '<header class="cabeca-parte' + (conto && i === 1 ? ' conto' : '') + '">' + cabeca + '</header>' +
      '<div class="texto">' + blocos(p.texto) + '</div>' +
      (i < total ? '' : '<p class="fim">Fim</p>') +
      '<nav class="passos" aria-label="Navegação entre ' + esc(o.divisao ? o.divisao.plural : 'partes') + '">' +
      navAnt + navSeg + '</nav>' +
      (total > 1 ? '<p class="posicao">' + i + ' de ' + total + ' · <a href="#/o/' + o.id + '">índice</a></p>' : '') +
      (conto && o.edicao && i === total ? '<p class="posicao"><a href="#/o/' + o.id + '/sobre">Sobre esta edição</a></p>' : '') +
      '</article>';
    render(html, (p.titulo && p.titulo !== o.titulo ? p.titulo + ' — ' : '') + o.titulo);
    registrarLeitura(o, i);
  }

  /* a coluna do lugar (capítulo, nota) some quando nenhuma linha a preenche: conto sem capítulos */
  function colunaLugar(itens, rotParte) {
    var tem = itens.some(function (v) { return v.cap; });
    return {
      th: tem ? '<th>' + esc(rotParte) + '</th>' : '',
      td: function (v) { return tem ? '<td class="cap">' + esc(v.cap || 'Texto') + '</td>' : ''; }
    };
  }

  function listaVariantes(itens, rotDe, rotPara, rotParte) {
    var c = colunaLugar(itens, rotParte);
    return '<table class="variantes"><thead><tr>' + c.th + '<th>' + esc(rotDe) + '</th><th>' + esc(rotPara) + '</th></tr></thead><tbody>' +
      itens.map(function (v) {
        return '<tr>' + c.td(v) + '<td>' + esc(v.de) + '</td><td>' + esc(v.para) + '</td></tr>';
      }).join('') + '</tbody></table>';
  }

  function paginaSobre(id) {
    var o = acharObra(id);
    if (!o || !o.edicao) return naoAchei();
    var a = acharAutor(o.autor) || { nome: o.autor, id: o.autor };
    var e = o.edicao;
    var d = o.divisao || { singular: 'parte' };
    var rotParte = o.coletanea && o.partes.length === 1 ? 'Onde' : d.singular.charAt(0).toUpperCase() + d.singular.slice(1);
    var rotBase = e.base || '1ª edição';
    definirTrilha([
      { txt: a.nome, href: '#/a/' + a.id },
      trilhaGenero(a, o.genero || 'Outros'),
      { txt: o.titulo, href: linkObra(o) },
      { txt: 'Sobre esta edição' }
    ]);
    definirProgresso(null);

    var html = '<article class="folha sobre">' +
      '<header class="cabeca"><h1>Sobre esta edição</h1><p class="meta">' +
      (o.coletanea ? esc(o.titulo) + ' · <em>' + esc(o.coletanea.titulo) + '</em>' : '<em>' + esc(o.titulo) + '</em>') + ' · ' + esc(a.nome) + '</p></header>' +
      '<div class="texto">' + blocos(e.apresentacao || '') + '</div>';

    // títulos das seções: cada obra pode trocá-los em edicao.secoes (o padrão é o de Dom Casmurro)
    var S = e.secoes || {};
    function secao(nome, padrao) {
      var s = S[nome] || {};
      return {
        titulo: s.titulo || padrao.titulo, explica: s.explica || padrao.explica,
        de: s.de || padrao.de || rotBase, para: s.para || padrao.para
      };
    }
    var s;
    if (e.erros && e.erros.length) {
      s = secao('erros', { titulo: 'Erros tipográficos da 1ª edição corrigidos', explica: 'Grafia da 1ª edição nas duas colunas.', para: 'Corrigido' });
      html += '<h2>' + esc(s.titulo) + '</h2>' +
        '<p class="explica">' + esc(s.explica) + ' ' + e.erros.length + ' correções.</p>' +
        listaVariantes(e.erros, s.de, s.para, rotParte);
    }
    if (e.tradicao && e.tradicao.length) {
      s = secao('tradicao', { titulo: 'Lições da 2ª edição adotadas', explica: 'Leituras em que todas as edições posteriores concordam contra a 1ª. Grafia da 1ª edição.', para: 'Adotado' });
      html += '<h2>' + esc(s.titulo) + '</h2>' +
        '<p class="explica">' + esc(s.explica) + '</p>' +
        listaVariantes(e.tradicao, s.de, s.para, rotParte);
    }
    if (e.pontuacao && e.pontuacao.length) {
      s = secao('pontuacao', { titulo: 'Pontuação da 2ª edição adotada', explica: 'Mesmo critério: só onde toda a tradição posterior concorda. Grafia atualizada.', para: 'Adotado' });
      html += '<h2>' + esc(s.titulo) + '</h2>' +
        '<p class="explica">' + esc(s.explica) + '</p>' +
        listaVariantes(e.pontuacao, s.de, s.para, rotParte);
    }
    if (e.mantidas && e.mantidas.length) {
      s = secao('mantidas', { titulo: 'Leituras da 1ª edição mantidas', explica: 'Pontos em que parte das edições modernas lê diferente.' });
      var cm = colunaLugar(e.mantidas, rotParte);
      html += '<h2>' + esc(s.titulo) + '</h2>' +
        '<p class="explica">' + esc(s.explica) + '</p>' +
        '<table class="variantes"><thead><tr>' + cm.th + '<th>Este texto</th><th>Outras edições</th></tr></thead><tbody>' +
        e.mantidas.map(function (v) {
          return '<tr>' + cm.td(v) + '<td>' + esc(v.texto) + '</td><td>' + esc(v.variante) +
            (v.obs ? '<span class="obs">' + esc(v.obs) + '</span>' : '') + '</td></tr>';
        }).join('') + '</tbody></table>';
    }
    if (e.fontes && e.fontes.length) {
      html += '<h2>Fontes consultadas</h2><ul class="fontes">' +
        e.fontes.map(function (f) {
          var nome = f.url ? '<a href="' + esc(f.url) + '" target="_blank" rel="noopener">' + esc(f.nome) + '</a>' : esc(f.nome);
          return '<li>' + nome + (f.nota ? ' — <span class="obs-inline">' + esc(f.nota) + '</span>' : '') + '</li>';
        }).join('') + '</ul>';
    }
    html += '<p class="posicao"><a href="' + linkObra(o) + '">' + (o.coletanea && o.partes.length === 1 ? 'Voltar ao texto' : 'Voltar ao índice') + '</a></p></article>';
    render(html, 'Sobre esta edição — ' + o.titulo);
  }

  function naoAchei() {
    definirTrilha([]);
    definirProgresso(null);
    render('<div class="folha cabeca"><h1>Página não encontrada</h1><p><a href="#/">Voltar à capa</a></p></div>', 'Não encontrado');
  }

  /* ----------------------------- roteador ----------------------------- */

  function rota() {
    var h = decodeURIComponent(location.hash.replace(/^#\/?/, ''));
    var p = h.split('/').filter(Boolean);
    if (!p.length) return paginaCapa();
    if (p[0] === 'a' && p[1]) return p[2] ? paginaGenero(p[1], p[2]) : paginaAutor(p[1]);
    if (p[0] === 'o' && p[1]) {
      if (!p[2]) return paginaObra(p[1]);
      if (p[2] === 'sobre') return paginaSobre(p[1]);
      var n = parseInt(p[2], 10);
      if (!isNaN(n)) return paginaParte(p[1], n);
    }
    naoAchei();
  }

  /* Setas do teclado passam de parte em parte */
  function teclado(ev) {
    if (ev.altKey || ev.ctrlKey || ev.metaKey || ev.shiftKey) return;
    var alvo = ev.target;
    if (alvo && (alvo.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(alvo.tagName))) return;
    var link = null;
    if (ev.key === 'ArrowLeft') link = app.querySelector('a[rel="prev"]');
    if (ev.key === 'ArrowRight') link = app.querySelector('a[rel="next"]');
    if (link) { ev.preventDefault(); location.hash = link.getAttribute('href'); }
  }

  /* ----------------------------- preferências ----------------------------- */

  function aplicarTema(t) {
    if (t === 'claro' || t === 'escuro') document.documentElement.setAttribute('data-tema', t);
    else document.documentElement.removeAttribute('data-tema');
  }

  function alternarTema() {
    var atual = document.documentElement.getAttribute('data-tema');
    var escuroSistema = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    var escuroAgora = atual ? atual === 'escuro' : escuroSistema;
    var novo = escuroAgora ? 'claro' : 'escuro';
    aplicarTema(novo);
    guardar(CHAVE_TEMA, novo);
  }

  var TAMANHOS = [0.9, 1, 1.1, 1.22, 1.35];
  function aplicarFonte(k) {
    document.documentElement.style.setProperty('--escala', TAMANHOS[k]);
  }
  function mudarFonte(delta) {
    var k = parseInt(ler(CHAVE_FONTE), 10);
    if (isNaN(k)) k = 1;
    k = Math.max(0, Math.min(TAMANHOS.length - 1, k + delta));
    aplicarFonte(k);
    guardar(CHAVE_FONTE, String(k));
  }

  /* ----------------------------- início ----------------------------- */

  aplicarTema(ler(CHAVE_TEMA));
  var kf = parseInt(ler(CHAVE_FONTE), 10);
  if (!isNaN(kf) && TAMANHOS[kf]) aplicarFonte(kf);

  document.addEventListener('DOMContentLoaded', function () {
    app = document.getElementById('app');
    trilha = document.getElementById('trilha');
    progresso = document.getElementById('progresso');
    document.getElementById('tema').addEventListener('click', alternarTema);
    document.getElementById('fonte-menos').addEventListener('click', function () { mudarFonte(-1); });
    document.getElementById('fonte-mais').addEventListener('click', function () { mudarFonte(1); });
    window.addEventListener('hashchange', rota);
    document.addEventListener('keydown', teclado);
    rota();
  });
})();
