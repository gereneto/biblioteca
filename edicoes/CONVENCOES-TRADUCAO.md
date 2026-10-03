# Convenções gerais das traduções da Biblioteca (seção Catolicismo)

Vale para toda obra traduzida para a Biblioteca. Cada obra tem, além deste, um guia próprio em
`edicoes/<obra>/CONVENCOES.md` (nomes, tratamento, termos), que prevalece onde for mais específico.
Modelo de referência já pronto: `edicoes/santa-teresinha/CONVENCOES.md`.

## 1. Princípio

Fidelidade ao que o autor escreveu, em português do Brasil correto, natural e literário. Nada de
acréscimos, explicações, glosas ou modernizações de doutrina. Guarde o movimento da frase do autor
(longa ou curta, solene ou viva), as imagens, a ordem das ideias, as repetições de propósito, os
jogos de palavras (quando não passam, registre nas notas a solução e a perda).

## 2. Regras fixas

- **Nunca mesóclise.** Reescreva com próclise, ênclise ou outra construção (*dir-te-ei* → *eu te
  direi*; *far-se-á* → *há de fazer-se*). Antes de entregar:
  ```
  grep -n -E -o "[A-Za-zÀ-ÿ]+-(lo|la|los|las|o|a|os|as|me|te|se|lhe|lhes|nos|vos|no|na)-(ei|as|á|ás|emos|eis|ão|ia|ias|íamos|íeis|iam)\b" <arquivos>
  ```
  Não pode sair nada.
- Colocação pronominal brasileira culta: próclise onde soa natural, ênclise no começo de frase.
- Citações da Escritura: traduza o texto como o autor o cita (de memória, da Vetus Latina, da
  Vulgata, da Septuaginta, da King James...), não copie uma Bíblia portuguesa. Referências no
  formato do autor; se ele não dá referência, não acrescente.
- Nomes bíblicos e de santos na forma portuguesa usual (Moisés, Isaías, Paulo, Ambrósio).
- Aspas: as do português, “...”, com ‘...’ dentro (salvo indicação do guia da obra).
- Itálico: `_assim_`. Palavra estrangeira que fica em outra língua vai em itálico.
- Datas e números como no original, adaptados ao uso brasileiro.

## 3. Formato dos arquivos

- Um arquivo traduzido para cada arquivo-fonte, com o mesmo nome, em `edicoes/<obra>/traducao/`.
- Cabeçalho com linhas `# chave: valor` (pelo menos `# titulo:` traduzido); depois o texto,
  parágrafos separados por uma linha em branco, **um parágrafo traduzido para cada parágrafo do
  original, na mesma ordem**.
- As marcas do original ficam no mesmo lugar, iguais: numeração de capítulo e seção (`[I.1]`,
  `[12]`), colunas de edição (`{PG 26.837}`). Não traduza nem mova as marcas.
- Versos: uma linha por verso, começando com `| `; estrofe = bloco. Versos de hino ou poema
  citado se traduzem pelo método do Versificador (ver `edicoes/santa-teresinha/CONVENCOES.md`, § 7),
  com metro e rima quando o original tem; citação curta de verso, pode ficar em verso livre, com
  registro nas notas.

## 4. Notas do tradutor

Cada tarefa grava `edicoes/<obra>/traducao/notas-<trecho>.md`: nomes e termos novos e como foram
traduzidos; passagens difíceis e a interpretação adotada; variantes do texto-fonte que pesaram;
jogos de palavras e perdas. Não altere os guias: proponha mudanças nas notas.

## 5. Arquivos temporários

Outras traduções correm ao mesmo tempo. Se precisar de arquivos temporários, use só uma pasta
própria: `C:\Users\geren\AppData\Local\Temp\claude\<obra>-<trecho>\`.

## 6. Antes de entregar

1. Um arquivo traduzido para cada arquivo-fonte do trecho; mesmo número de parágrafos.
2. Todas as marcas do original presentes, na ordem.
3. Grep de mesóclise sem resultado.
4. Releitura inteira, de uma vez, procurando sentido trocado, galicismos/latinismos/anglicismos,
   concordância, regência, crase e frases forçadas.
