/* ---------------------------------------------------------------
   Biblioteca — aplicação de leitura
   Autor → obra → parte (capítulo, canto, ato... conforme a obra).

   Rotas (usam # para funcionar em qualquer hospedagem estática
   e também abrindo o index.html direto do disco):
     #/                      capa: autores e "continuar a leitura"
     #/a/<autor>             obras do autor
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

  /* Parágrafos separados por linha em branco; linhas com "| " formam versos */
  function blocos(texto) {
    return String(texto).trim().split(/\n\s*\n/).map(function (b) {
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

  /* Ordem dos gêneros na página do autor e o título de cada grupo */
  var GENEROS = ['Romance', 'Novela', 'Contos', 'Poesia', 'Teatro', 'Crônica', 'Crítica', 'Tradução'];
  var PLURAIS = { 'Romance': 'Romances', 'Novela': 'Novelas', 'Contos': 'Contos', 'Poesia': 'Poesia',
    'Teatro': 'Teatro', 'Crônica': 'Crônicas', 'Crítica': 'Crítica', 'Tradução': 'Traduções' };

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
  function autoresOrdenados() {
    return dados.autores.slice().sort(function (a, b) {
      return (a.ordem || a.nome).localeCompare(b.ordem || b.nome, 'pt');
    });
  }

  /* Rótulo de uma parte: "Capítulo XII" (numeral da obra) */
  function rotuloParte(obra, parte) {
    if (!parte.n) return String(parte.titulo || '').replace(/[_*]/g, '');   /* contos, poemas: o título */
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
      html += '<a class="retomar" href="#/o/' + r.obra.id + '/' + r.i + '">' +
        '<span class="rot">Continuar a leitura</span>' +
        '<span class="alvo">' + esc(r.obra.titulo) + ' — ' + esc(rotuloParte(r.obra, r.parte)) +
        (r.parte.titulo ? ': ' + inline(r.parte.titulo) : '') + '</span></a>';
    }

    html += '<p class="secao-titulo">Autores</p>';
    autoresOrdenados().forEach(function (a) {
      var obras = obrasDe(a.id);
      html += '<a class="cartao" href="#/a/' + a.id + '">' +
        '<span class="cartao-titulo">' + esc(a.nome) + '</span>' +
        '<span class="cartao-meta">' + esc(a.vida || '') + (a.vida ? ' · ' : '') + plural(obras.length, 'obra', 'obras') + '</span>' +
        (obras.length ? '<span class="cartao-texto">' + obras.map(function (o) { return '<em>' + esc(o.titulo) + '</em>'; }).join(', ') + '</span>' : '') +
        '</a>';
    });
    html += '</div>';
    render(html, '');
  }

  function paginaAutor(id) {
    var a = acharAutor(id);
    if (!a) return naoAchei();
    definirTrilha([{ txt: a.nome }]);
    definirProgresso(null);
    var obras = obrasDe(a.id);
    var html = '<div class="folha">' +
      '<header class="cabeca">' +
      '<h1>' + esc(a.nome) + '</h1>' +
      '<p class="meta">' + esc([a.nomeCompleto, a.vida].filter(Boolean).join(' · ')) + '</p>' +
      (a.nota ? '<p class="nota-autor">' + inline(a.nota) + '</p>' : '') +
      '</header>';
    /* obras agrupadas por gênero, na ordem de GENEROS; dentro do grupo, por ano */
    var grupos = {};
    obras.forEach(function (o) {
      var g = o.genero || 'Outros';
      (grupos[g] = grupos[g] || []).push(o);
    });
    var ordem = GENEROS.filter(function (g) { return grupos[g]; })
      .concat(Object.keys(grupos).filter(function (g) { return GENEROS.indexOf(g) < 0; }).sort());
    ordem.forEach(function (g) {
      html += '<p class="secao-titulo">' + esc(PLURAIS[g] || g) + '</p>';
      grupos[g].forEach(function (o) {
        var d = o.divisao || { singular: 'parte', plural: 'partes' };
        html += '<a class="cartao" href="#/o/' + o.id + '">' +
          '<span class="cartao-titulo"><em>' + esc(o.titulo) + '</em></span>' +
          '<span class="cartao-meta">' + esc(String(o.ano || '')) + (o.ano ? ' · ' : '') + plural(o.partes.length, d.singular, d.plural) + '</span>' +
          (o.descricao ? '<span class="cartao-texto">' + inline(o.descricao) + '</span>' : '') +
          '</a>';
      });
    });
    html += '</div>';
    render(html, a.nome);
  }

  function paginaObra(id) {
    var o = acharObra(id);
    if (!o) return naoAchei();
    var a = acharAutor(o.autor) || { nome: o.autor, id: o.autor };
    var d = o.divisao || { singular: 'parte', plural: 'partes' };
    definirTrilha([{ txt: a.nome, href: '#/a/' + a.id }, { txt: o.titulo }]);
    definirProgresso(null);

    var pos = posicaoSalva(o);
    var html = '<div class="folha">' +
      '<header class="rosto">' +
      '<p class="rosto-autor">' + esc(a.nome) + '</p>' +
      '<h1>' + esc(o.titulo) + '</h1>' +
      '<p class="meta">' + esc([o.genero, o.ano].filter(Boolean).join(' · ')) + '</p>' +
      (o.descricao ? '<p class="descricao">' + inline(o.descricao) + '</p>' : '') +
      '<p class="acoes">' +
      '<a class="botao" href="#/o/' + o.id + '/' + (pos || 1) + '">' + (pos && pos > 1 ? 'Continuar: ' + esc(rotuloParte(o, o.partes[pos - 1])) : 'Começar a ler') + '</a>' +
      (o.edicao ? ' <a class="botao secundario" href="#/o/' + o.id + '/sobre">Sobre esta edição</a>' : '') +
      '</p>' +
      '</header>' +
      '<p class="secao-titulo">' + esc(d.plural.charAt(0).toUpperCase() + d.plural.slice(1)) + '</p>' +
      '<ol class="indice">';
    o.partes.forEach(function (p, i) {
      html += '<li' + (pos === i + 1 ? ' class="atual"' : '') + '><a href="#/o/' + o.id + '/' + (i + 1) + '">' +
        '<span class="num">' + esc(p.n) + '</span>' +
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
    definirTrilha([
      { txt: a.nome, href: '#/a/' + a.id },
      { txt: o.titulo, href: '#/o/' + o.id },
      { txt: rotuloParte(o, p) }
    ]);
    definirProgresso(i / total);

    var ant = i > 1 ? o.partes[i - 2] : null;
    var seg = i < total ? o.partes[i] : null;

    var html = '<article class="folha leitura">' +
      '<header class="cabeca-parte">' +
      '<p class="num-parte">' + esc(p.n) + '</p>' +
      (p.titulo ? '<h1>' + inline(p.titulo) + '</h1>' : '') +
      '</header>' +
      '<div class="texto">' + blocos(p.texto) + '</div>' +
      (seg ? '' : '<p class="fim">Fim</p>') +
      '<nav class="passos" aria-label="Navegação entre ' + esc(o.divisao ? o.divisao.plural : 'partes') + '">' +
      (ant ? '<a class="passo ant" href="#/o/' + o.id + '/' + (i - 1) + '" rel="prev"><span class="dir">← Anterior</span><span class="alvo">' + esc(ant.n) + (ant.titulo ? ' · ' + inline(ant.titulo) : '') + '</span></a>' : '<span class="passo vazio"></span>') +
      (seg ? '<a class="passo seg" href="#/o/' + o.id + '/' + (i + 1) + '" rel="next"><span class="dir">Seguinte →</span><span class="alvo">' + esc(seg.n) + (seg.titulo ? ' · ' + inline(seg.titulo) : '') + '</span></a>' : '<a class="passo seg" href="#/o/' + o.id + '"><span class="dir">Índice</span><span class="alvo">' + esc(o.titulo) + '</span></a>') +
      '</nav>' +
      '<p class="posicao">' + i + ' de ' + total + ' · <a href="#/o/' + o.id + '">índice</a></p>' +
      '</article>';
    render(html, (p.titulo ? p.titulo + ' — ' : '') + o.titulo);
    registrarLeitura(o, i);
  }

  function listaVariantes(itens, rotDe, rotPara, rotParte) {
    return '<table class="variantes"><thead><tr><th>' + esc(rotParte) + '</th><th>' + rotDe + '</th><th>' + rotPara + '</th></tr></thead><tbody>' +
      itens.map(function (v) {
        return '<tr><td class="cap">' + esc(v.cap) + '</td><td>' + esc(v.de) + '</td><td>' + esc(v.para) + '</td></tr>';
      }).join('') + '</tbody></table>';
  }

  function paginaSobre(id) {
    var o = acharObra(id);
    if (!o || !o.edicao) return naoAchei();
    var a = acharAutor(o.autor) || { nome: o.autor, id: o.autor };
    var e = o.edicao;
    var d = o.divisao || { singular: 'parte' };
    var rotParte = d.singular.charAt(0).toUpperCase() + d.singular.slice(1);
    var rotBase = e.base || '1ª edição';
    definirTrilha([
      { txt: a.nome, href: '#/a/' + a.id },
      { txt: o.titulo, href: '#/o/' + o.id },
      { txt: 'Sobre esta edição' }
    ]);
    definirProgresso(null);

    var html = '<article class="folha sobre">' +
      '<header class="cabeca"><h1>Sobre esta edição</h1><p class="meta"><em>' + esc(o.titulo) + '</em> · ' + esc(a.nome) + '</p></header>' +
      '<div class="texto">' + blocos(e.apresentacao || '') + '</div>';

    if (e.erros && e.erros.length) {
      html += '<h2>Erros tipográficos da 1ª edição corrigidos</h2>' +
        '<p class="explica">Grafia da 1ª edição nas duas colunas. ' + e.erros.length + ' correções.</p>' +
        listaVariantes(e.erros, rotBase, 'Corrigido', rotParte);
    }
    if (e.tradicao && e.tradicao.length) {
      html += '<h2>Lições da 2ª edição adotadas</h2>' +
        '<p class="explica">Leituras em que todas as edições posteriores concordam contra a 1ª. Grafia da 1ª edição.</p>' +
        listaVariantes(e.tradicao, rotBase, 'Adotado', rotParte);
    }
    if (e.pontuacao && e.pontuacao.length) {
      html += '<h2>Pontuação da 2ª edição adotada</h2>' +
        '<p class="explica">Mesmo critério: só onde toda a tradição posterior concorda. Grafia atualizada.</p>' +
        listaVariantes(e.pontuacao, rotBase, 'Adotado', rotParte);
    }
    if (e.mantidas && e.mantidas.length) {
      html += '<h2>Leituras da 1ª edição mantidas</h2>' +
        '<p class="explica">Pontos em que parte das edições modernas lê diferente.</p>' +
        '<table class="variantes"><thead><tr><th>' + esc(rotParte) + '</th><th>Este texto</th><th>Outras edições</th></tr></thead><tbody>' +
        e.mantidas.map(function (v) {
          return '<tr><td class="cap">' + esc(v.cap) + '</td><td>' + esc(v.texto) + '</td><td>' + esc(v.variante) +
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
    html += '<p class="posicao"><a href="#/o/' + o.id + '">Voltar ao índice</a></p></article>';
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
    if (p[0] === 'a' && p[1]) return paginaAutor(p[1]);
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
