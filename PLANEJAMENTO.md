# Planejamento do projeto

## Objetivo atual

Identificar comunidades que representem possiveis escolas de pensamento na rede
agregada do DBpedia e mensurar sua capacidade de propagacao deterministica de
influencia. Nao sera realizada divisao por periodos historicos.

## Legenda

- [x] Concluido e validado
- [~] Implementado, mas precisa ser reexecutado ou revisado
- [ ] Pendente

## 1. Dados e construcao da rede

- [x] Filtrar `influenced`, `influencedBy`, `doctoralAdvisor`,
  `doctoralStudent` e `field` do arquivo do DBpedia.
- [x] Representar `field` como atributo dos vertices.
- [x] Padronizar as arestas no sentido fonte da influencia -> receptor.
- [x] Consolidar `influenced` e `influencedBy` como `influenced`.
- [x] Consolidar `doctoralAdvisor` e `doctoralStudent` como
  `doctoralSupervision`.
- [x] Preservar mais de um tipo de relacao no mesmo par por meio do atributo
  `relations`.
- [x] Gerar e validar o GraphML canonico.
- [x] Auditar a rede canonica: 39.019 vertices, 38.958 arestas, 1 laco,
  8.055 vertices com `field`, 11.579 componentes fracamente conexas e maior
  componente fraca com 20.099 vertices.
- [x] Corrigir o nome do arquivo para `dbpedia-network-canonical.graphml` e
  atualizar a referencia no notebook.
- [ ] Remover, depois da validacao final, o arquivo obsoleto
  `dbpedia-network-cannonical.graphml`.

## 2. Metricas da rede canonica - concluida

- [x] Manter as funcoes de metricas basicas e fazer `analyze_network` retornar
  o dicionario de resultados.
- [x] Criar `G_analysis` como copia da rede canonica e remover o unico laco.
- [x] Executar e salvar `results = analyze_network(G_analysis)`.
- [x] Recalcular as metricas dirigidas e nao dirigidas usando exclusivamente a
  rede canonica.
- [x] Recalcular distribuicoes de graus, componentes e coeficientes de
  clusterizacao.
- [x] Registrar separadamente componentes fracas e fortes. A rede possui 38.721
  componentes fortes e a maior delas possui 66 vertices.
- [x] Atualizar as figuras de graus, componentes e clusterizacao.
- [x] Registrar as novas metricas direcionadas: 38.957 arestas sem o laco,
  graus medios de entrada e saida 0,998411, densidade 0,0000255885,
  clustering medio 0,012632, distancia media 5,451049 e diametro 15 na maior
  componente forte.
- [ ] Atualizar as tabelas que serao usadas no relatorio final.
- [ ] Comparar os novos valores com a entrega parcial e explicar as mudancas
  causadas pela canonicalizacao.

## 3. Deteccao de comunidades - etapa atual

- [x] Usar a maior componente fracamente conexa como recorte principal, com
  20.099 vertices e 31.545 arestas.
- [x] Executar o baseline de Louvain com modularidade, `resolution=1` e
  `seed=42`: 133 comunidades, modularidade 0,796999 e maior comunidade com
  2.354 vertices.
- [x] Executar o baseline de Leiden com `metric="modularity"`, `resolution=1`
  e `seed=42`: 110 comunidades, modularidade 0,801381 e maior comunidade com
  1.748 vertices.
- [x] Implementar e validar a conversao de uma particao para um vetor de
  memberships alinhado aos 20.099 vertices.
- [x] Validar o gerador de ensembles em tres execucoes de Louvain, obtendo
  particoes completas e modularidades entre 0,795968 e 0,805715.
- [x] Gerar e validar 100 particoes independentes para cada algoritmo, usando
  as sementes de 0 a 99.
- [x] Persistir as 100 particoes e seus metadados em arquivos `.npz` e `.csv`,
  sem depender dos outputs embutidos no notebook.
- [x] Construir e auditar a matriz de contagens de coocorrencia do Louvain:
  matriz simetrica `20.099 x 20.099`, diagonal igual a 100 e valores em
  `uint8`.
- [x] Auditar os limiares do Louvain: 8.922.981 pares em `tau=0,3`,
  5.717.950 em `tau=0,5` e 3.492.859 em `tau=0,7`.
- [x] Construir e auditar a matriz de contagens de coocorrencia do Leiden:
  matriz simetrica `20.099 x 20.099`, diagonal igual a 100 e valores em
  `uint8`.
- [x] Auditar os limiares do Leiden: 7.989.529 pares em `tau=0,3`, 5.496.780
  em `tau=0,5` e 3.611.704 em `tau=0,7`; respectivamente 0, 1 e 45 vertices
  isolados.
- [x] Comprimir o grafo de consenso principal do Louvain (`tau=0,5`) por
  assinaturas de membership: 2.814 grupos, 337.943 arestas incluindo 1.955
  autolacos, e preservacao exata dos 5.717.950 pares e da soma dos pesos.
- [x] Confirmar no procedimento de Lancichinetti e Fortunato (2012) que
  vertices isolados pelo limiar devem ser religados aos vizinhos de maior
  peso; essa correcao nao altera o Louvain em `tau=0,5`, que nao tem isolados.
- [x] Implementar na construcao comprimida a restauracao dos maiores pesos
  para os isolados, conforme Lancichinetti e Fortunato (2012).
- [x] Comprimir o grafo de consenso principal do Leiden (`tau=0,5`): 2.956
  grupos, 303.345 arestas incluindo 1.950 autolacos, com restauracao de 2
  arestas (11 pares) para eliminar o unico isolado produzido pelo limiar.
- [x] Adotar `tau=0,5` como limiar principal dos grafos de consenso.
- [x] Repetir o consenso final com `tau=0,3` e `tau=0,7` para a analise de
  sensibilidade. Todos os cenarios convergiram na segunda iteracao: Louvain
  encontrou 60, 103 e 310 comunidades, e Leiden 60, 96 e 294 comunidades,
  para `tau=0,3`, `0,5` e `0,7`, respectivamente.
- [x] Comparar as particoes da sensibilidade. O limiar principal `tau=0,5`
  apresenta concordancia alta com os limiares adjacentes (NMI/ARI: 0,856534/
  0,734658 e 0,880234/0,745137 para Louvain; 0,864599/0,765871 e
  0,889734/0,779267 para Leiden), enquanto `tau=0,7` fragmenta a rede de
  forma acentuada. Manter `tau=0,5` como escolha principal.
- [x] Implementar a execucao iterativa e retomavel da sensibilidade, com
  persistencia de cada iteracao e restauracao dos isolados conforme o metodo
  de consenso.
- [x] Implementar um gerador de ensembles ponderados para os grafos de
  consenso comprimidos, com memberships independentes dos rotulos e tamanhos
  expressos em vertices originais.
- [x] Validar tres reaplicacoes ponderadas de Louvain e Leiden; ambos geraram
  tres particoes distintas, confirmando que ainda nao houve convergencia.
- [x] Gerar, persistir e validar 100 particoes ponderadas da primeira iteracao:
  9 particoes distintas no Louvain (101 a 103 comunidades) e 25 no Leiden
  (94 a 97 comunidades), portanto ainda sem convergencia.
- [x] Construir diretamente em memoria os grafos da segunda iteracao: 105
  grupos e 107 arestas para Louvain; 103 grupos e 112 arestas para Leiden.
- [x] Executar e persistir as 100 reaplicacoes da segunda iteracao: uma unica
  particao em todas as sementes, com 103 comunidades no Louvain e 96 no
  Leiden.
- [x] Reaplicar cada algoritmo ao seu grafo ponderado de consenso ate a
  convergencia, atingida na segunda iteracao.
- [x] Implementar a comparacao das particoes consensuais por NMI, ARI,
  modularidade na rede original e distribuicao dos tamanhos.
- [x] Executar e validar as tabelas e a figura da comparacao Louvain-Leiden:
  NMI 0,907016, ARI 0,845755 e modularidades 0,806958 (Louvain) e 0,810280
  (Leiden) na rede original.
- [x] Caracterizar as comunidades Leiden como candidatas a escolas de
  pensamento. Para cada comunidade, combinar: (i) campos de conhecimento
  distintivos em relacao ao restante da rede, e nao somente o campo dominante;
  (ii) vertices representativos por alcance e centralidade; (iii) relacoes
  internas de influencia e de orientacao; e (iv) quando necessario,
  enriquecimento semantico externo (resumos, categorias, ocupacoes e
  movimentos). Registrar rotulo interpretativo, evidencias e nivel de
  confianca; usar "agrupamento tematico" quando a evidencia for insuficiente
  para afirmar uma escola de pensamento.
- [x] Persistir a caracterizacao das 96 comunidades em tabelas e relatorio
  reproduziveis. A classificacao final encontrou 12 escolas candidatas, 18
  tradicoes intelectuais, 38 linhagens cientificas, 14 agrupamentos tematicos
  e 14 agrupamentos mistos.
- [x] Tratar a esparsidade de `field` explicitamente: somente 473 dos 20.099
  vertices do recorte possuem o atributo. Calcular enriquecimento em relacao
  aos vertices anotados da rede e aceitar um campo como evidencia apoiada
  apenas com pelo menos duas ocorrencias e cobertura comunitaria de 5%.
- [x] Verificar semanticamente as 12 escolas candidatas em fontes academicas
  ou institucionais e rebaixar abordagens profissionais, linhagens autorais e
  tradicoes amplas que nao sustentam o status de escola.

## 4. Propagacao deterministica de influencia

- [x] Adotar probabilidade `p=1` para todas as arestas.
- [x] Interpretar a propagacao como alcancabilidade na rede dirigida.
- [x] Construir o DAG de condensacao das componentes fortemente conexas: 19.808
  SCCs e 29.010 arestas para 20.099 vertices e 31.545 arestas da rede de
  influencia; a maior SCC possui 66 vertices.
- [x] Medir, para cada comunidade Leiden, alcance interno, alcance externo,
  fracao da rede atingida, outras comunidades atingidas e profundidade da
  propagacao. Apenas 7 SCCs cruzam comunidades.
- [x] Avaliar a comunidade inteira como conjunto de sementes. Os maiores
  alcances externos sao das comunidades 26 (9.646 vertices), 15 (9.133), 27
  (9.086), 57 (9.011, apesar de conter somente 4 vertices) e 77 (8.678, com
  13 vertices).
- [x] Avaliar orcamentos comparaveis de `k=1`, `k=5` e `k=10` sementes.
  Sob propagacao deterministica, greedy/CELF alcanca respectivamente 49,1%,
  60,3% e 63,9% da rede; a referencia por grau de saida alcanca 28,3%,
  48,6% e 48,6%.
- [x] Selecionar sementes por greedy/CELF deterministico e comparar com a
  selecao por maior grau de saida. Usar SCCs para evitar candidatos
  equivalentes e desempate pelo identificador do no; persistir sementes,
  ganhos marginais, tabela por orcamento e figura em
  `community_results/influence/seed_selection/`.
- [~] Caracterizar as comunidades que fornecem as sementes, reunindo para
  cada semente sua comunidade Leiden, rotulo interpretativo, tipo e confianca
  da caracterizacao, perfil de `field` e metricas de propagacao comunitaria.
- [x] Persistir rankings de alcance total, alcance externo e eficiencia por
  semente, incluindo as comunidades e seus vertices representativos, em
  `community_results/influence/`.

## 5. Resultados e entrega final

- [ ] Gerar tabelas reproduziveis de comunidades e propagacao.
- [ ] Produzir graficos de consenso, estabilidade e alcance.
- [x] Interpretar as comunidades mais influentes como candidatas a escolas de
  pensamento.
- [ ] Documentar as componentes fora da maior componente em um apendice.
- [ ] Atualizar objetivos e metodologia, removendo a analise temporal.
- [ ] Registrar como limitacao que as arestas representam influencia direta
  observada, enquanto a propagacao transitiva e uma hipotese do modelo.
- [ ] Manter o algoritmo preliminar do mestrado como extensao opcional.
