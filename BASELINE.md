# Baseline consolidado

## Escopo

Este documento encerra o baseline de detecção de comunidades e propagação de
influência na rede canônica do DBpedia. O baseline combina:

1. detecção estável de comunidades por Louvain e Leiden;
2. consenso de partições e análise de sensibilidade;
3. caracterização semântica das comunidades Leiden;
4. ranqueamento do potencial de propagação das comunidades;
5. seleção de nós-semente com orçamentos comparáveis.

A heurística futura não é definida nem executada nesta etapa.

## Protocolo congelado

- Rede dirigida canônica, após remoção do único laço.
- Recorte principal: maior componente fracamente conexa, com 20.099 nós e
  31.545 arestas.
- Louvain e Leiden com modularidade e resolução 1.
- Cem execuções independentes por algoritmo, com sementes de 0 a 99.
- Consenso principal com limiar `tau=0,5`; sensibilidade em `tau=0,3` e
  `tau=0,7`.
- Partição Leiden consensual como referência de interpretação e influência.
- Propagação determinística dirigida, com `p=1` em todas as arestas.
- Ciclos tratados pela condensação das componentes fortemente conexas em um
  DAG.

Uma comparação futura deverá preservar a mesma rede, o mesmo modelo de
propagação, o mesmo tratamento de SCCs e as mesmas métricas de partição e
influência.

## Detecção e estabilidade

As cem execuções independentes apresentaram os seguintes resultados:

| Algoritmo | Modularidade média | Desvio-padrão | Faixa de comunidades |
|---|---:|---:|---:|
| Louvain | 0,799972 | 0,004554 | 93–142 |
| Leiden | 0,804239 | 0,003858 | 91–155 |

O consenso convergiu na segunda iteração em todos os cenários. Com o limiar
principal `tau=0,5`, foram obtidas 103 comunidades Louvain e 96 comunidades
Leiden. As partições consensuais apresentam NMI 0,907016, ARI 0,845755 e
variação de informação de 0,658876 nats.

Na rede original do recorte, as modularidades das partições finais são
0,806958 para Louvain e 0,810280 para Leiden. A análise de sensibilidade
confirma alta concordância do cenário principal com os limiares adjacentes,
embora `tau=0,7` fragmente a rede em 310 comunidades Louvain e 294 Leiden.

## Caracterização das comunidades Leiden

As 96 comunidades foram classificadas em:

| Classificação | Quantidade |
|---|---:|
| Escola candidata | 12 |
| Tradição intelectual | 18 |
| Linhagem científica | 38 |
| Agrupamento temático | 14 |
| Agrupamento misto | 14 |

Foram atribuídos 48 níveis de confiança alta, 30 média e 18 baixa. A
interpretação combina vértices representativos, relações internas, campos
distintivos e, quando necessário, evidência semântica externa.

O atributo `field` é muito esparso: apenas 473 dos 20.099 nós possuem essa
anotação. Por isso, um campo é tratado como evidência apoiada somente quando
possui pelo menos duas ocorrências e cobertura comunitária mínima de 5%.

## Potencial de influência das comunidades

Cada comunidade foi inicialmente tratada como um conjunto coletivo de
sementes. As comunidades com maior alcance externo são:

| Posição | Comunidade | Alcance externo |
|---:|---:|---:|
| 1 | 26 | 9.646 |
| 2 | 15 | 9.133 |
| 3 | 27 | 9.086 |
| 4 | 57 | 9.011 |
| 5 | 34 | 8.716 |

O resultado mede alcance estrutural potencial. Ele não representa uma
probabilidade empírica de difusão.

## Orçamentos de nós-semente

Para sementes individuais, greedy/CELF foi comparado à seleção por maior grau
de saída:

| Estratégia | `k=1` | `k=5` | `k=10` |
|---|---:|---:|---:|
| Greedy/CELF | 49,1% | 60,3% | 63,9% |
| Maior grau de saída | 28,3% | 48,6% | 48,6% |

As dez sementes greedy/CELF pertencem a dez comunidades diferentes. As dez
sementes de maior grau concentram-se em apenas três comunidades. Essa
diversidade estrutural explica a menor redundância do greedy/CELF e seu maior
alcance acumulado.

## Artefatos reproduzíveis

Todo o código necessário está em `main.ipynb`. Para reproduzir o baseline,
abra o notebook no ambiente Conda `dbpedia-network` e execute as células em
ordem. As últimas células da seção **6. Consolidação reproduzível do
baseline** validam os artefatos anteriores e regeneram a consolidação.

Os arquivos JSON em `community_characterization/` são entradas declarativas
de curadoria semântica, assim como o GraphML é a entrada da rede; eles não
contêm código executável.

Os principais resultados consolidados são:

- `community_results/baseline/baseline_summary.json`: protocolo e resultados
  principais em formato legível por máquina;
- `community_results/baseline/baseline_communities.csv`: caracterização,
  propagação e participação na seleção de sementes para as 96 comunidades;
- `community_results/baseline/baseline_run_stability.csv`: resumo das cem
  execuções por algoritmo;
- `community_results/baseline/baseline_sensitivity.csv`: sensibilidade ao
  limiar com NMI, ARI e variação de informação;
- `community_results/baseline/baseline_artifact_index.csv`: índice e validação
  dos artefatos que compõem o baseline.

## Limitações

- As arestas representam relações diretas observadas no DBpedia.
- A propagação transitiva é uma hipótese estrutural do modelo.
- `p=1` mede alcance potencial, não a chance real de influência.
- A interpretação temática é condicionada pela baixa cobertura de `field`.
- A análise principal exclui os nós fora da maior componente fracamente
  conexa.
