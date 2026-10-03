/* ---------------------------------------------------------------
   Biblioteca — aplicação de leitura
   Autor → gênero → obra → parte (capítulo, conto, poema... conforme a obra).

   Rotas (usam # para funcionar em qualquer hospedagem estática
   e também abrindo o index.html direto do disco):
     #/                      capa: as pastas (Literatura, Catolicismo) e "continuar a leitura"
     #/s/<area>              autores de uma pasta
     #/a/<autor>             gêneros em que o autor tem obras
     #/a/<autor>/<genero>    obras do autor nesse gênero (romances, contos, poesia...)
     #/a/<autor>/poesia/<forma>  poemas de uma forma (sonetos, apólogos...), por livro
     #/o/<obra>              folha de rosto e índice da obra
     #/o/<obra>/<n>          parte n (1, 2, 3...) da obra
     #/o/<obra>/sobre        notas sobre o texto desta edição

   Poemas: cada poema é uma obra. O índice (conteudo/poesia.js) chega com o site; o texto
   de cada autor (conteudo/<autor>/poesia.js) só é carregado quando um poema dele é aberto.

   Traduções: uma parte com "original" é lida em modo bilíngue — dois botões independentes
   mostram o original (à esquerda) e a tradução (à direita), lado a lado quando os dois estão
   ligados; em tela estreita, um de cada vez.
   --------------------------------------------------------------- */

(function () {
  'use strict';

  var dados = { autores: [], obras: [], porId: {} };

  function registrar(o) {
    dados.obras.push(o);
    dados.porId[o.id] = o;
  }

  /* API usada pelos arquivos de conteúdo (carregados depois deste script) */
  window.BIBLIOTECA = {
    autor: function (a) { dados.autores.push(a); },
    obra:  registrar,
    /* índice de poesia de um autor: livros e poemas (sem o texto) */
    poemas: function (pac) {
      pac.poemas.forEach(function (p, k) {
        var l = p.livro >= 0 ? pac.livros[p.livro] : null;
        registrar({
          id: p.id, autor: pac.autor, titulo: p.titulo, genero: 'Poesia', poema: true,
          forma: p.forma, n: p.n || '', secao: p.secao || '', subtitulo: p.subtitulo || '',
          ano: p.ano || (l && l.ano) || null, versos: p.versos, lingua: p.lingua || '',
          traducao: p.traducao || null,
          coletanea: l ? { id: pac.autor + '/' + l.id, titulo: l.titulo, ano: l.ano || '', ordem: k, seq: p.livro } : null,
          ordem: k,
          divisao: { singular: 'parte', plural: 'partes' },
          partes: (p.partes || [{}]).map(function (x) { return { n: '', titulo: x.titulo || '' }; }),
          arquivo: pac.arquivo
        });
      });
    },
    /* texto dos poemas de um autor (arquivo carregado sob demanda) */
    textos: function (mapa) {
      Object.keys(mapa).forEach(function (id) {
        var o = dados.porId[id], e = mapa[id];
        if (!o) return;
        e.t.forEach(function (t, i) {
          if (!o.partes[i]) o.partes[i] = { n: '', titulo: '' };
          o.partes[i].texto = t;
          if (e.o) o.partes[i].original = e.o[i];
        });
        if (e.e) o.edicao = e.e;
        o.carregada = true;
      });
    }
  };

  /* Carrega (uma vez) o arquivo com o texto de uma obra; cb(true) quando pronto, cb(false) se falhar.
     Usa <script>, que funciona também abrindo o index.html direto do disco. */
  var pendentes = {};
  function carregar(o, cb) {
    if (!o.arquivo || o.carregada) return cb(true);
    var arq = o.arquivo;
    if (pendentes[arq]) { pendentes[arq].push(cb); return; }
    pendentes[arq] = [cb];
    var s = document.createElement('script');
    function fim(ok) {
      var l = pendentes[arq] || [];
      delete pendentes[arq];
      if (!ok) s.remove();
      l.forEach(function (f) { f(ok && !!o.carregada); });
    }
    s.src = arq;
    s.onload = function () { fim(true); };
    s.onerror = function () { fim(false); };
    document.head.appendChild(s);
  }

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

  /* Marcação mínima dos textos: _itálico_ e **negrito**; {Ms A 45v} marca a folha do manuscrito */
  function inline(s) {
    return esc(s)
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/_([^_]+)_/g, '<em>$1</em>')
      .replace(/\s*\{Ms ([A-C]) (\d+)([rv]?)\}\s*/g, function (m, ms, f, l) {
        return ' <span class="folha-ms" title="Manuscrito ' + ms + ', folha ' + f + (l === 'r' ? ' recto' : l === 'v' ? ' verso' : '') + '">' + ms + ' ' + f + l + '</span> ';
      }).replace(/^ | $/g, '');
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
      /* teatro: "## Cena 2" (título de cena) e "@ JOANA, _timidamente_." (quem fala) */
      if (/^## /.test(b)) return '<p class="cena">' + inline(b.slice(3).trim()) + '</p>';
      if (/^@ /.test(b)) return '<p class="fala">' + inline(b.slice(2).trim()) + '</p>';
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

  /* ----------------------------- poemas e textos em paralelo ----------------------------- */

  /* Poema -> blocos: estrofes ({versos: [...]}) e marcas ({marca, valor}); "sep" diz se o bloco
     vem depois de uma linha em branco (uma fala colada à estrofe não abre espaço).
     Um verso por linha, estrofes separadas por linha em branco, marcas em linhas "::chave valor". */
  function blocosPoema(texto) {
    var blocos = [], estrofe = null, branco = true;
    String(texto || '').split('\n').forEach(function (l) {
      if (!l.trim()) { estrofe = null; branco = true; return; }
      var m = /^::(\w+)\s?(.*)$/.exec(l);
      if (m) { blocos.push({ marca: m[1], valor: m[2].trim(), sep: branco }); estrofe = null; branco = false; return; }
      if (!estrofe) { estrofe = { versos: [], sep: branco }; blocos.push(estrofe); }
      estrofe.versos.push(l);
      branco = false;
    });
    return blocos;
  }

  var SEPARADORES = { 'filete': '<span class="fio"></span>', 'fio horizontal': '<span class="fio"></span>',
    'linha de pontos': '. . . . . . . . . . .' };
  function htmlMarca(b) {
    var v = b.valor;
    switch (b.marca) {
      case 'epigrafe': return v.split(/\s+\/\s+/).map(inline).join('<br>');
      case 'separador': return SEPARADORES[v] || esc(v || '*');
      case 'lacuna': return '. . . . . . . . . . .';
      case 'pagina': return '';
      default: return inline(v);
    }
  }

  /* Linhas do texto em paralelo: cada linha é um verso, uma marca ou um parágrafo.
     Com dois textos, as linhas se casam estrofe com estrofe e verso com verso (poema) ou
     parágrafo com parágrafo (prosa); o que sobra de um lado fica vazio do outro. */
  /* blocos -> [{sep, linhas: [{cls, html}]}] */
  function linhasPoema(texto) {
    return blocosPoema(texto).map(function (b) {
      if (b.marca) return { sep: b.sep, linhas: [{ cls: 'm m-' + b.marca, html: htmlMarca(b) }] };
      return { sep: b.sep, linhas: b.versos.map(function (v) { return { cls: 'v', html: inline(v) }; }) };
    });
  }
  function linhasProsa(texto) {
    var todos = String(texto || '').trim().split(/\n\s*\n/).filter(Boolean);
    var corpo = todos.filter(function (b) { return !/^¤ /.test(b); });
    var notas = todos.filter(function (b) { return /^¤ /.test(b); });
    var linhas = corpo.map(function (b) { return { sep: false, linhas: [{ cls: 'p', html: paragrafos([b]) }] }; });
    if (notas.length) {
      linhas.push({ sep: false, linhas: [{ cls: 'p nota-do-autor', html: '<p class="rotulo">' + (notas.length > 1 ? 'Notas do autor' : 'Nota do autor') + '</p>' +
        paragrafos(notas.map(function (b) { return b.replace(/^¤ /, ''); })) }] });
    }
    return linhas;
  }

  /* HTML da grade: células .orig e .trad alternadas, com data-i comum a cada par (âncora da rolagem).
     "ini" marca o começo de estrofe ou de bloco, nas duas células do par, para que a linha
     tenha a mesma altura dos dois lados. */
  function grade(ladoTrad, ladoOrig, lingua) {
    var n = Math.max(ladoTrad.length, ladoOrig ? ladoOrig.length : 0), html = '', i = 0;
    for (var b = 0; b < n; b++) {
      var bt = ladoTrad[b] || { linhas: [] }, bo = ladoOrig ? ladoOrig[b] || { linhas: [] } : { linhas: [] };
      var m = Math.max(bt.linhas.length, bo.linhas.length);
      var sep = b > 0 && (bt.sep || bo.sep) ? ' ini' : '';
      for (var j = 0; j < m; j++, i++) {
        var ini = j === 0 ? sep : '';
        if (ladoOrig) html += celula('orig', bo.linhas[j], ini, i, lingua);
        html += celula('trad', bt.linhas[j], ini, i, '');
      }
    }
    return html;
  }
  function celula(lado, l, ini, i, lingua) {
    if (!l) return '<div class="' + lado + ' vazio' + ini + '" data-i="' + i + '"></div>';
    return '<div class="' + lado + ' ' + l.cls + ini + '" data-i="' + i + '"' + (lingua ? ' lang="' + lingua + '"' : '') + '>' + l.html + '</div>';
  }

  /* Texto de uma parte: poema ou prosa, com ou sem original ao lado */
  function textoParte(o, p) {
    var poema = !!o.poema;
    var linhas = poema ? linhasPoema : linhasProsa;
    var orig = p.original !== undefined && p.original !== null;
    var lingua = orig && o.traducao ? o.traducao.codigo || '' : '';
    var cls = 'paralelo ' + (poema ? 'poema' : 'prosa');
    var attr = o.lingua && !orig ? ' lang="' + esc(o.lingua) + '"' : '';
    if (!orig && !poema) return '<div class="texto">' + blocos(p.texto) + '</div>';
    return '<div class="texto"><div class="' + cls + '"' + attr + '>' +
      grade(linhas(p.texto), orig ? linhas(p.original) : null, lingua) + '</div></div>';
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
  var GENEROS = ['Romance', 'Novela', 'Contos', 'Autobiografia', 'Poesia', 'Teatro', 'Cartas', 'Orações',
    'Crônica', 'Crítica', 'Tradução'];
  var PLURAIS = { 'Romance': 'Romances', 'Novela': 'Novelas', 'Contos': 'Contos', 'Poesia': 'Poesia',
    'Teatro': 'Teatro', 'Crônica': 'Crônicas', 'Crítica': 'Crítica', 'Tradução': 'Traduções',
    'Autobiografia': 'Autobiografia', 'Cartas': 'Cartas', 'Orações': 'Orações' };

  /* Áreas da capa: cada autor pertence a uma (campo "area"; sem ele, Literatura) */
  var AREAS = [{ id: 'literatura', nome: 'Literatura' }, { id: 'catolicismo', nome: 'Catolicismo' }];
  function areaDe(a) { return a.area || 'literatura'; }
  function acharArea(id) { return AREAS.filter(function (x) { return x.id === id; })[0] || null; }

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

  /* "1899 · 148 capítulos · 66.998 palavras"; num conto: "13 capítulos · 18.034 palavras";
     num poema: "5 partes · 2.001 versos" */
  function fichaObra(o) {
    var d = o.divisao || { singular: 'parte', plural: 'partes' };
    if (o.poema) {
      return [o.partes.length > 1 ? plural(o.partes.length, d.singular, d.plural) : '',
        o.versos === 1 ? '1 verso' : milhar(o.versos) + ' versos'].filter(Boolean).join(' · ');
    }
    if (o.coletanea) {
      return [o.partes.length > 1 ? plural(numeradas(o), d.singular, d.plural) : '',
        milhar(palavras(o)) + ' palavras'].filter(Boolean).join(' · ');
    }
    /* "datas": período de composição, quando a obra não tem um ano só ("1895–1897") */
    return [o.datas || (o.ano ? String(o.ano) : ''), plural(numeradas(o), d.singular, d.plural),
      milhar(palavras(o)) + ' palavras'].filter(Boolean).join(' · ');
  }

  /* ----------------------------- contos em coletânea ----------------------------- */

  /* um conto sem capítulos (ou um poema sem partes) abre direto no texto */
  function linkObra(o) { return '#/o/' + o.id + ((o.coletanea || o.poema) && o.partes.length === 1 ? '/1' : ''); }
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
  /* [{titulo, ano, obras}]: obras avulsas num grupo sem título, coletâneas pelo ano;
     poemas: livros na ordem de publicação do autor (seq), os avulsos por último */
  function porColetanea(obras) {
    var grupos = [], idx = {};
    obras.forEach(function (o) {
      var k = o.coletanea ? o.coletanea.id : '';
      if (!(k in idx)) {
        idx[k] = grupos.length;
        grupos.push({ titulo: o.coletanea ? o.coletanea.titulo : '', ano: o.coletanea ? o.coletanea.ano : o.ano,
          seq: o.poema ? (o.coletanea ? o.coletanea.seq : 1e6) : null, obras: [] });
      }
      grupos[idx[k]].obras.push(o);
    });
    grupos.forEach(function (g) {
      g.obras.sort(function (a, b) {
        if (a.poema && b.poema) return a.ordem - b.ordem;
        return a.coletanea && b.coletanea ? a.coletanea.ordem - b.coletanea.ordem : 0;
      });
    });
    return grupos.sort(function (a, b) {
      if (a.seq !== null && b.seq !== null) return a.seq - b.seq;
      return (a.ano || 0) - (b.ano || 0);
    });
  }

  /* ----------------------------- poesia: pastas por forma ----------------------------- */

  var FORMAS = [
    { id: 'sonetos', nome: 'Sonetos' },
    { id: 'apologos', nome: 'Apólogos' },
    { id: 'liras', nome: 'Liras' },
    { id: 'odes', nome: 'Odes' },
    { id: 'verso-livre', nome: 'Verso livre' },
    { id: 'outras', nome: 'Outras formas' }
  ];
  function acharForma(id) { return FORMAS.filter(function (f) { return f.id === id; })[0] || null; }
  /* pastas com poemas do autor: [{forma, obras}] na ordem de FORMAS */
  function pastasDe(obras) {
    return FORMAS.map(function (f) {
      return { forma: f, obras: obras.filter(function (o) { return (o.forma || 'outras') === f.id; }) };
    }).filter(function (x) { return x.obras.length; });
  }
  function poesiaDe(autorId) {
    return dados.obras.filter(function (o) { return o.autor === autorId && o.genero === 'Poesia'; });
  }
  /* autor só de poesia: a página do autor mostra direto as pastas */
  function soPoesia(autorId) {
    var g = generosDe(autorId);
    return g.length === 1 && g[0].genero === 'Poesia';
  }
  function hrefPoesia(a) { return '#/a/' + a.id + (soPoesia(a.id) ? '' : '/poesia'); }
  function hrefPasta(a, forma) { return '#/a/' + a.id + '/poesia/' + forma; }
  /* trilha até a pasta de um poema: Autor › (Poesia ›) Sonetos */
  function trilhaPasta(a, o) {
    var f = acharForma(o.forma || 'outras'), itens = [{ txt: a.nome, href: '#/a/' + a.id }];
    if (!soPoesia(a.id)) itens.push({ txt: 'Poesia', href: '#/a/' + a.id + '/poesia' });
    if (pastasDe(poesiaDe(a.id)).length > 1) itens.push({ txt: f.nome, href: hrefPasta(a, f.id) });
    return itens;
  }
  /* índice da pasta a que o poema pertence (ou da poesia do autor, se só há uma pasta) */
  function hrefIndicePoema(a, o) {
    return pastasDe(poesiaDe(a.id)).length > 1 ? hrefPasta(a, o.forma || 'outras') : hrefPoesia(a);
  }
  /* poemas da mesma pasta, na ordem da lista (livro a livro): para "Anterior" e "Seguinte" */
  function vizinhosPoema(o) {
    var lista = [];
    porColetanea(poesiaDe(o.autor).filter(function (x) { return (x.forma || 'outras') === (o.forma || 'outras'); }))
      .forEach(function (g) { lista = lista.concat(g.obras); });
    return lista;
  }

  /* ----------------------------- consultas ----------------------------- */

  function acharAutor(id) {
    for (var i = 0; i < dados.autores.length; i++) if (dados.autores[i].id === id) return dados.autores[i];
    return null;
  }
  function acharObra(id) {
    return Object.prototype.hasOwnProperty.call(dados.porId, id) ? dados.porId[id] : null;
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
    /* partes com sigla própria ("LT 12", "PN 17"): a sigla; partes agrupadas sob uma sigla
       ("Ms A"): o título */
    if (obra.divisao && obra.divisao.rotulo === 'n') return parte.n;
    if (obra.divisao && obra.divisao.rotulo === 'nome') return String(parte.titulo || parte.n).replace(/[_*]/g, '');
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

  /* A trilha começa pela área do autor: Catolicismo › Santa Teresinha › ... */
  function autorDoItem(it) {
    var m = it.href && /^#\/a\/([^/]+)$/.exec(it.href);
    if (m) return acharAutor(m[1]);
    if (!it.href) for (var i = 0; i < dados.autores.length; i++) if (dados.autores[i].nome === it.txt) return dados.autores[i];
    return null;
  }
  function definirTrilha(itens) {
    var a = itens.length ? autorDoItem(itens[0]) : null, ar = a && acharArea(areaDe(a));
    if (ar) itens = [{ txt: ar.nome, href: '#/s/' + ar.id }].concat(itens);
    trilha.innerHTML = itens.map(function (it) {
      return it.href ? '<a href="' + it.href + '">' + esc(it.txt) + '</a>' : '<span>' + esc(it.txt) + '</span>';
    }).join('<span class="sep">›</span>');
  }

  function definirProgresso(frac) {
    if (frac === null) { progresso.hidden = true; return; }
    progresso.hidden = false;
    progresso.firstChild.style.width = (Math.max(0, Math.min(1, frac)) * 100).toFixed(2) + '%';
  }

  /* obra da página de leitura anterior: a escolha de original/tradução só dura enquanto se passa
     de uma parte a outra da mesma obra; ao abrir o texto de novo, volta a tradução sozinha */
  var obraNaTela = null, obraAnterior = null;

  function render(html, titulo) {
    obraAnterior = obraNaTela;
    obraNaTela = null;
    document.getElementById('idiomas').hidden = true;   /* a página bilíngue a mostra de novo */
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

    /* as pastas: uma por área, com o número de autores e os gêneros que há nela */
    html += '<p class="secao-titulo">Acervo</p>';
    AREAS.forEach(function (ar) {
      var autores = autoresDaArea(ar.id);
      var generos = [];
      autores.forEach(function (a) {
        generosDe(a.id).forEach(function (x) { if (generos.indexOf(x.genero) < 0) generos.push(x.genero); });
      });
      generos.sort(function (x, y) { return GENEROS.indexOf(x) - GENEROS.indexOf(y); });
      html += '<a class="cartao pasta area" href="#/s/' + ar.id + '">' +
        '<span class="cartao-titulo">' + esc(ar.nome) + '</span>' +
        '<span class="cartao-meta">' + (autores.length ? plural(autores.length, 'autor', 'autores') : 'em preparação') + '</span>' +
        (generos.length ? '<span class="cartao-texto">' + generos.map(function (g) { return esc(nomeGenero(g)); }).join(' · ') + '</span>' : '') +
        '</a>';
    });
    html += '</div>';
    render(html, '');
  }

  function autoresDaArea(id) {
    return autoresOrdenados().filter(function (a) { return areaDe(a) === id; });
  }

  /* Autores de uma área: #/s/<area> */
  function paginaArea(id) {
    var ar = acharArea(id);
    if (!ar) return naoAchei();
    definirTrilha([{ txt: ar.nome }]);
    definirProgresso(null);
    var html = '<div class="folha"><header class="cabeca"><h1>' + esc(ar.nome) + '</h1></header>' +
      '<p class="secao-titulo">Autores</p>';
    autoresDaArea(ar.id).forEach(function (a) {
      var obras = obrasDe(a.id);
      var prosa = obras.filter(function (o) { return !o.poema; }), versos = obras.length - prosa.length;
      /* "6 obras · 26 poemas"; num poeta, só os poemas */
      var conta = [prosa.length ? plural(livros(prosa), 'obra', 'obras') : '',
        versos ? plural(versos, 'poema', 'poemas') : ''].filter(Boolean).join(' · ') || '0 obras';
      html += '<a class="cartao" href="#/a/' + a.id + '">' +
        '<span class="cartao-titulo">' + esc(a.nome) + '</span>' +
        '<span class="cartao-meta">' + esc(a.vida || '') + (a.vida ? ' · ' : '') + conta + '</span>' +
        (obras.length ? '<span class="cartao-texto">' + generosDe(a.id).map(function (x) { return esc(nomeGenero(x.genero)); }).join(' · ') + '</span>' : '') +
        '</a>';
    });
    html += '</div>';
    render(html, ar.nome);
  }

  function cabecaAutor(a) {
    return '<header class="cabeca">' +
      '<h1>' + esc(a.nome) + '</h1>' +
      '<p class="meta">' + esc([a.nomeCompleto, a.vida].filter(Boolean).join(' · ')) + '</p>' +
      (a.nota ? '<p class="nota-autor">' + inline(a.nota) + '</p>' : '') +
      '</header>';
  }

  /* Poesia do autor: uma pasta por forma (sonetos, apólogos...); com uma pasta só, a lista */
  function htmlPastas(a, obras) {
    var pastas = pastasDe(obras);
    if (pastas.length === 1) return htmlListaPoemas(pastas[0].obras);
    var html = '<p class="secao-titulo">Formas</p>';
    pastas.forEach(function (x) {
      var titulos = [];
      porColetanea(x.obras).forEach(function (g) { if (g.titulo && titulos.indexOf(g.titulo) < 0) titulos.push(g.titulo); });
      html += '<a class="cartao pasta" href="' + hrefPasta(a, x.forma.id) + '">' +
        '<span class="cartao-titulo">' + esc(x.forma.nome) + '</span>' +
        '<span class="cartao-meta">' + plural(x.obras.length, 'poema', 'poemas') + '</span>' +
        (titulos.length ? '<span class="cartao-texto">' + titulos.map(function (t) { return '<em>' + esc(t) + '</em>'; }).join(', ') + '</span>' : '') +
        '</a>';
    });
    return html;
  }

  /* Lista de poemas, livro a livro: número no livro (quando há) e título */
  function htmlListaPoemas(obras) {
    var grupos = porColetanea(obras), html = '';
    grupos.forEach(function (g) {
      var titulo = g.titulo || (grupos.length > 1 ? 'Avulsos' : '');
      if (titulo) html += '<p class="secao-titulo">' + (g.titulo ? '<em>' + esc(titulo) + '</em>' : esc(titulo)) + (g.ano ? ' · ' + g.ano : '') + '</p>';
      var comNum = g.obras.some(function (o) { return o.n; });
      html += '<ol class="indice poemas' + (comNum ? '' : ' sem-num') + '">';
      g.obras.forEach(function (o) {
        var extra = o.traducao ? '<span class="orig-tit" lang="' + esc(o.traducao.codigo || '') + '">' + esc(o.traducao.titulo) + '</span>' :
          o.partes.length > 1 ? '<span class="orig-tit">' + esc(fichaObra(o)) + '</span>' : '';
        html += '<li><a href="' + linkObra(o) + '">' +
          (comNum ? '<span class="num">' + esc(o.n) + '</span>' : '') +
          '<span class="tit"' + (o.lingua ? ' lang="' + esc(o.lingua) + '"' : '') + '>' + esc(o.titulo) + extra + '</span>' +
          '</a></li>';
      });
      html += '</ol>';
    });
    return html;
  }

  /* Poemas de uma forma: #/a/<autor>/poesia/<forma> */
  function paginaPasta(id, formaId) {
    var a = acharAutor(id), f = acharForma(formaId);
    if (!a || !f) return naoAchei();
    var obras = poesiaDe(a.id).filter(function (o) { return (o.forma || 'outras') === f.id; });
    if (!obras.length) return naoAchei();
    var itens = [{ txt: a.nome, href: '#/a/' + a.id }];
    if (!soPoesia(a.id)) itens.push({ txt: 'Poesia', href: '#/a/' + a.id + '/poesia' });
    definirTrilha(itens.concat({ txt: f.nome }));
    definirProgresso(null);
    var html = '<div class="folha">' +
      '<header class="cabeca"><h1>' + esc(f.nome) + '</h1><p class="meta">' + esc(a.nome) + ' · ' + plural(obras.length, 'poema', 'poemas') + '</p></header>' +
      htmlListaPoemas(obras) + '</div>';
    render(html, f.nome + ' — ' + a.nome);
  }

  /* Página do autor: escolha do gênero (num poeta, direto as pastas de poesia) */
  function paginaAutor(id) {
    var a = acharAutor(id);
    if (!a) return naoAchei();
    definirTrilha([{ txt: a.nome }]);
    definirProgresso(null);
    if (soPoesia(a.id)) {
      render('<div class="folha">' + cabecaAutor(a) + htmlPastas(a, poesiaDe(a.id)) + '</div>', a.nome);
      return;
    }
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
    if (x.genero === 'Poesia') {
      render(html + htmlPastas(a, x.obras) + '</div>', 'Poesia — ' + a.nome);
      return;
    }
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
    definirTrilha((o.poema ? trilhaPasta(a, o) : [{ txt: a.nome, href: '#/a/' + a.id }, trilhaGenero(a, o.genero || 'Outros')])
      .concat({ txt: o.titulo }));
    definirProgresso(null);

    var pos = posicaoSalva(o);
    var html = '<div class="folha">' +
      '<header class="rosto">' +
      '<p class="rosto-autor">' + esc(a.nome) + '</p>' +
      '<h1>' + esc(o.titulo) + '</h1>' +
      (o.subtitulo ? '<p class="subtitulo-obra">' + inline(o.subtitulo) + '</p>' : '') +
      '<p class="meta">' + (o.coletanea && o.coletanea.titulo !== o.titulo ? '<em>' + esc(o.coletanea.titulo) + '</em>' + (o.coletanea.ano ? ', ' + esc(o.coletanea.ano) : '') + ' · ' :
        o.poema && o.ano ? esc(o.ano) + ' · ' : '') + esc(fichaObra(o)) + '</p>' +
      (o.publicacao ? '<p class="publicacao">' + inline(textoPublicacao(o)) + '</p>' : '') +
      (o.traducao && !o.poema ? '<p class="publicacao">Tradução do ' + esc(o.traducao.lingua) +
        (o.traducao.titulo ? ' (<em lang="' + esc(o.traducao.codigo || '') + '">' + esc(o.traducao.titulo) + '</em>)' : '') + '</p>' : '') +
      (o.descricao ? '<p class="descricao">' + inline(o.descricao) + '</p>' : '') +
      '<p class="acoes">' +
      '<a class="botao" href="#/o/' + o.id + '/' + (pos || 1) + '">' + (pos && pos > 1 ? 'Continuar: ' + esc(rotuloParte(o, o.partes[pos - 1])) : 'Começar a ler') + '</a>' +
      (o.edicao ? ' <a class="botao secundario" href="#/o/' + o.id + '/sobre">' + esc(tituloSobre(o)) + '</a>' : '') +
      '</p>' +
      '</header>' +
      '<p class="secao-titulo">' + esc(d.plural.charAt(0).toUpperCase() + d.plural.slice(1)) + '</p>' +
      '<ol class="indice">';
    /* nos diários, o ano só aparece no índice quando muda; o mesmo com "agrupar" (Ms A, Ms B...) */
    var agrupa = o.divisao && (o.divisao.rotulo === 'titulo' || o.divisao.agrupar);
    o.partes.forEach(function (p, i) {
      var num = agrupa && i && o.partes[i - 1].n === p.n ? '' : p.n;
      html += '<li' + (pos === i + 1 ? ' class="atual"' : '') + '><a href="#/o/' + o.id + '/' + (i + 1) + '">' +
        '<span class="num">' + esc(num) + '</span>' +
        '<span class="tit">' + (p.titulo ? inline(p.titulo) : '<span class="inc">' + incipit(p.texto, 60) + '</span>') +
        (p.folhas ? '<span class="folhas">' + esc(p.folhas) + '</span>' : '') + '</span>' +
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
    var poema = !!o.poema;
    var conto = !!o.coletanea || poema;
    var bilingue = p.original !== undefined && p.original !== null;
    var passos;
    if (poema) {
      passos = trilhaPasta(a, o).concat(total > 1 ?
        [{ txt: o.titulo, href: '#/o/' + o.id }, { txt: rotuloParte(o, p) }] : [{ txt: o.titulo }]);
    } else {
      passos = [
        { txt: a.nome, href: '#/a/' + a.id },
        { txt: o.titulo, href: '#/o/' + o.id },
        { txt: rotuloParte(o, p) }
      ];
      if (conto) {
        passos.splice(1, 0, trilhaGenero(a, o.genero || 'Outros'));
        if (total === 1) passos = passos.slice(0, 2).concat({ txt: o.titulo });
      }
    }
    definirTrilha(passos);
    definirProgresso(i / total);

    /* vizinhos: a parte anterior e a seguinte; nas pontas de um conto, o texto vizinho da coletânea;
       nas de um poema, o poema vizinho da mesma pasta */
    function passo(cls, rel, dir, href, alvo) {
      return '<a class="passo ' + cls + '" href="' + href + '" rel="' + rel + '"><span class="dir">' + dir + '</span><span class="alvo">' + alvo + '</span></a>';
    }
    function indice(href, alvo) {
      return '<a class="passo seg" href="' + href + '"><span class="dir">Índice</span><span class="alvo">' + esc(alvo) + '</span></a>';
    }
    var navAnt = '<span class="passo vazio"></span>', navSeg;
    var irmaos = poema ? vizinhosPoema(o) : conto ? daColetanea(o) : [], k = irmaos.indexOf(o);
    if (i > 1) navAnt = passo('ant', 'prev', '← Anterior', '#/o/' + o.id + '/' + (i - 1), rotuloPasso(o.partes[i - 2]));
    else if (k > 0) navAnt = passo('ant', 'prev', '← Anterior', '#/o/' + irmaos[k - 1].id + '/' + irmaos[k - 1].partes.length, esc(irmaos[k - 1].titulo));
    if (i < total) navSeg = passo('seg', 'next', 'Seguinte →', '#/o/' + o.id + '/' + (i + 1), rotuloPasso(o.partes[i]));
    else if (k >= 0 && k < irmaos.length - 1) navSeg = passo('seg', 'next', 'Seguinte →', '#/o/' + irmaos[k + 1].id + '/1', esc(irmaos[k + 1].titulo));
    else if (poema) navSeg = indice(hrefIndicePoema(a, o), pastasDe(poesiaDe(a.id)).length > 1 ? acharForma(o.forma || 'outras').nome : 'Poesia');
    else if (conto) navSeg = indice('#/a/' + a.id + '/' + slugGenero(o.genero), nomeGenero(o.genero));
    else navSeg = indice('#/o/' + o.id, o.titulo);

    /* título: nas traduções, o original e o traduzido, cada um sobre o seu texto */
    function titulo(tag, cls, trad, orig) {
      var h = '<' + tag + (cls ? ' class="' + cls + '"' : '') + '>';
      if (!bilingue || !orig) return h + inline(trad) + '</' + tag + '>';
      var lingua = o.traducao ? o.traducao.codigo || '' : '';
      return '<div class="paralelo titulos">' +
        '<div class="orig" data-i="t"' + (lingua ? ' lang="' + esc(lingua) + '"' : '') + '>' + h + inline(orig) + '</' + tag + '></div>' +
        '<div class="trad" data-i="t">' + h + inline(trad) + '</' + tag + '></div></div>';
    }

    var cabeca;
    if (conto) {
      /* o conto (ou o poema) se apresenta na 1ª parte; as seguintes só com número e título */
      var livro = [o.coletanea ? '<em>' + esc(o.coletanea.titulo) + '</em>' : '', o.secao ? esc(o.secao) : ''].filter(Boolean).join(' · ');
      cabeca = (i === 1 ?
        (livro ? '<p class="coletanea-parte">' + livro + '</p>' : '') +
        (poema && o.n ? '<p class="num-parte">' + esc(o.n) + '</p>' : '') +
        titulo('h1', 'titulo-conto', o.titulo, o.traducao && o.traducao.titulo) +
        (o.subtitulo ? '<p class="subtitulo-obra">' + inline(o.subtitulo) + '</p>' : '') +
        (o.traducao ? '<p class="publicacao">Tradução do ' + esc(o.traducao.lingua) + '</p>' : '') +
        (o.publicacao ? '<p class="publicacao">' + inline(textoPublicacao(o)) + '</p>' : '') : '') +
        (total > 1 ? (p.n ? '<p class="num-parte">' + esc(p.n) + '</p>' : '') + (p.titulo ? titulo('h2', '', p.titulo, p.tituloOriginal) : '') : '');
    } else {
      cabeca = (p.n ? '<p class="num-parte">' + esc(p.n) + '</p>' : '') +
        (p.titulo ? titulo('h1', '', p.titulo, p.tituloOriginal) : '');
    }

    var html = '<article class="folha leitura' + (poema ? ' de-poema' : '') + (bilingue ? ' bilingue ver-trad' : '') + '">' +
      '<header class="cabeca-parte' + (conto && i === 1 ? ' conto' : '') + '">' + cabeca + '</header>' +
      textoParte(o, p) +
      (i < total || poema ? '' : '<p class="fim">Fim</p>') +
      '<nav class="passos" aria-label="Navegação entre ' + esc(poema && total === 1 ? 'poemas' : o.divisao ? o.divisao.plural : 'partes') + '">' +
      navAnt + navSeg + '</nav>' +
      (total > 1 ? '<p class="posicao">' + i + ' de ' + total + ' · <a href="#/o/' + o.id + '">índice</a></p>' : '') +
      (conto && o.edicao && i === total ? '<p class="posicao"><a href="#/o/' + o.id + '/sobre">' + esc(tituloSobre(o)) + '</a></p>' : '') +
      '</article>';
    render(html, (p.titulo && p.titulo !== o.titulo ? p.titulo + ' — ' : '') + o.titulo);
    obraNaTela = o.id;
    if (bilingue) ativarIdiomas(o);
    registrarLeitura(o, i);
  }

  function tituloSobre(o) { return (o.edicao && o.edicao.titulo) || 'Sobre esta edição'; }

  /* ----------------------------- original e tradução ----------------------------- */

  /* Estado dos dois botões: todo texto abre só com a tradução; a escolha segue de parte em parte
     da mesma obra. "ultimo" é o último lado ligado: em tela estreita, com os dois ligados, é ele
     que aparece. */
  var idiomas = { obra: null, orig: false, trad: true, ultimo: 'trad' };
  var ESTREITO = window.matchMedia ? window.matchMedia('(max-width: 760px)') : { matches: false };

  function verAtual() {
    if (idiomas.orig && idiomas.trad) return ESTREITO.matches ? idiomas.ultimo : 'ambos';
    return idiomas.orig ? 'orig' : 'trad';
  }

  function ativarIdiomas(o) {
    if (idiomas.obra !== o.id || obraAnterior !== o.id) idiomas = { obra: o.id, orig: false, trad: true, ultimo: 'trad' };
    var barra = document.getElementById('idiomas');
    var nome = o.traducao && o.traducao.lingua ? o.traducao.lingua : 'original';
    var bo = barra.querySelector('[data-lado="orig"]');
    bo.textContent = nome.charAt(0).toUpperCase() + nome.slice(1);
    bo.title = 'Mostrar ou esconder o original' + (o.traducao && o.traducao.lingua ? ' em ' + o.traducao.lingua : '');
    barra.hidden = false;
    aplicarIdiomas(false);
  }

  function aplicarIdiomas(manter) {
    var art = app.querySelector('.bilingue');
    if (!art) return;
    var ancora = manter ? pegarAncora(art) : null;
    var v = verAtual();
    /* a classe diz o que está ligado; em tela estreita, o CSS mostra só o "ultimo" dos dois
       (assim a troca de largura não depende de evento nenhum) */
    art.classList.remove('ver-orig', 'ver-trad', 'ver-ambos', 'ultimo-orig', 'ultimo-trad');
    art.classList.add(idiomas.orig && idiomas.trad ? 'ver-ambos' : 'ver-' + v, 'ultimo-' + idiomas.ultimo);
    Array.prototype.forEach.call(document.querySelectorAll('#idiomas [data-lado]'), function (b) {
      var lado = b.getAttribute('data-lado');
      b.setAttribute('aria-pressed', String(v === 'ambos' || v === lado));
    });
    if (ancora) soltarAncora(art, ancora);
  }

  /* Pelo menos um texto fica sempre visível; em tela estreita, um de cada vez */
  function clicarIdioma(lado) {
    var v = verAtual(), outro = lado === 'orig' ? 'trad' : 'orig';
    if (ESTREITO.matches) {
      if (v === lado) return;
      idiomas[lado] = true; idiomas[outro] = false;
    } else if (v === 'ambos') {
      idiomas[lado] = false;
    } else if (v === lado) {
      return;                          /* é o único ligado: fica */
    } else {
      idiomas[lado] = true;
    }
    if (idiomas[lado]) idiomas.ultimo = lado;
    else idiomas.ultimo = outro;
    aplicarIdiomas(true);
  }

  /* Âncora da rolagem: a primeira linha visível sob o topo e a sua distância ao topo;
     depois da troca, a mesma linha (o mesmo verso ou parágrafo, do outro lado) volta ao mesmo lugar */
  function alturaTopo() {
    var t = document.querySelector('.topo');
    return t ? t.getBoundingClientRect().bottom : 0;
  }
  function pegarAncora(art) {
    if (window.scrollY < 4) return null;
    var topo = alturaTopo(), cels = art.querySelectorAll('[data-i]');
    for (var j = 0; j < cels.length; j++) {
      var c = cels[j];
      if (!c.offsetParent) continue;
      var r = c.getBoundingClientRect();
      if (r.bottom > topo + 2) return { i: c.getAttribute('data-i'), dy: r.top - topo };
    }
    return null;
  }
  function soltarAncora(art, a) {
    var cels = art.querySelectorAll('[data-i="' + a.i + '"]');
    for (var j = 0; j < cels.length; j++) {
      if (!cels[j].offsetParent) continue;
      var r = cels[j].getBoundingClientRect();
      window.scrollBy(0, r.top - alturaTopo() - a.dy);
      return;
    }
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
    var tit = tituloSobre(o);
    definirTrilha((o.poema ? trilhaPasta(a, o) : [{ txt: a.nome, href: '#/a/' + a.id }, trilhaGenero(a, o.genero || 'Outros')])
      .concat({ txt: o.titulo, href: linkObra(o) }, { txt: tit }));
    definirProgresso(null);

    var html = '<article class="folha sobre">' +
      '<header class="cabeca"><h1>' + esc(tit) + '</h1><p class="meta">' +
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
    html += '<p class="posicao"><a href="' + linkObra(o) + '">' + ((o.coletanea || o.poema) && o.partes.length === 1 ? 'Voltar ao texto' : 'Voltar ao índice') + '</a></p></article>';
    render(html, tit + ' — ' + o.titulo);
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
    if (p[0] === 's' && p[1]) return paginaArea(p[1]);
    if (p[0] === 'a' && p[1]) {
      if (p[2] === 'poesia' && p[3]) return paginaPasta(p[1], p[3]);
      return p[2] ? paginaGenero(p[1], p[2]) : paginaAutor(p[1]);
    }
    if (p[0] === 'o' && p[1]) {
      /* obra cujo texto ainda não chegou (poemas): carrega e volta aqui */
      var o = acharObra(p[1]);
      if (o && o.arquivo && !o.carregada) {
        var alvo = location.hash;
        render('<div class="folha cabeca"><p class="meta carregando">Carregando…</p></div>', o.titulo);
        carregar(o, function (ok) {
          if (location.hash !== alvo) return;
          if (ok) rota();
          else render('<div class="folha cabeca"><h1>Não foi possível abrir o texto</h1><p><a href="' + esc(alvo) + '" onclick="location.reload()">Tentar de novo</a></p></div>', 'Erro');
        });
        return;
      }
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
    Array.prototype.forEach.call(document.querySelectorAll('#idiomas [data-lado]'), function (b) {
      b.addEventListener('click', function () { clicarIdioma(b.getAttribute('data-lado')); });
    });
    /* ao passar de tela larga para estreita (ou o contrário), um texto ou os dois;
       o "resize" cobre os navegadores que não avisam a mudança da consulta de mídia */
    var eraEstreito = ESTREITO.matches;
    function mudouLargura() {
      if (ESTREITO.matches === eraEstreito) return;
      eraEstreito = ESTREITO.matches;
      aplicarIdiomas(true);
    }
    if (ESTREITO.addEventListener) ESTREITO.addEventListener('change', mudouLargura);
    else if (ESTREITO.addListener) ESTREITO.addListener(mudouLargura);
    window.addEventListener('resize', mudouLargura);
    window.addEventListener('hashchange', rota);
    document.addEventListener('keydown', teclado);
    rota();
  });
})();
