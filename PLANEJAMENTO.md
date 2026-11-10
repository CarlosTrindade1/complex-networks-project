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

- [~] Usar a maior componente fracamente conexa como recorte principal. O
  recorte foi validado com 20.099 vertices e 31.545 arestas e ainda deve ser
  incorporado ao notebook.
- [~] Executar Louvain com modularidade e `resolution=1`. Uma execucao de
  viabilidade encontrou 133 comunidades e modularidade 0,796999.
- [~] Executar Leiden com `metric="modularity"` e `resolution=1`. Uma execucao
  de viabilidade encontrou 110 comunidades e modularidade 0,806612.
- [ ] Gerar 100 particoes independentes para cada algoritmo.
- [ ] Construir uma matriz de consenso separada para Louvain e Leiden.
- [ ] Usar `tau=0.5` como limiar principal e `tau=0.3` e `tau=0.7` na analise
  de sensibilidade.
- [ ] Reaplicar o algoritmo ao grafo ponderado de consenso ate convergencia.
- [ ] Comparar as particoes consensuais de Louvain e Leiden por NMI, ARI,
  modularidade e distribuicao dos tamanhos.
- [ ] Caracterizar cada comunidade por estrutura e campos de conhecimento.

## 4. Propagacao deterministica de influencia

- [ ] Adotar probabilidade `p=1` para todas as arestas.
- [ ] Interpretar a propagacao como alcancabilidade na rede dirigida.
- [ ] Construir o DAG de condensacao das componentes fortemente conexas.
- [ ] Medir, para cada comunidade, alcance interno, alcance externo, fracao da
  componente atingida, outras comunidades atingidas e profundidade da
  propagacao.
- [ ] Avaliar a comunidade inteira como conjunto de sementes.
- [ ] Avaliar orcamentos comparaveis de `k=1`, `k=5` e `k=10` sementes.
- [ ] Selecionar sementes por greedy/CELF deterministico e comparar com a
  selecao por maior grau de saida.
- [ ] Produzir rankings de alcance total, alcance externo e eficiencia por
  semente.

## 5. Resultados e entrega final

- [ ] Gerar tabelas reproduziveis de comunidades e propagacao.
- [ ] Produzir graficos de consenso, estabilidade e alcance.
- [ ] Interpretar as comunidades mais influentes como candidatas a escolas de
  pensamento.
- [ ] Documentar as componentes fora da maior componente em um apendice.
- [ ] Atualizar objetivos e metodologia, removendo a analise temporal.
- [ ] Registrar como limitacao que as arestas representam influencia direta
  observada, enquanto a propagacao transitiva e uma hipotese do modelo.
- [ ] Manter o algoritmo preliminar do mestrado como extensao opcional.
