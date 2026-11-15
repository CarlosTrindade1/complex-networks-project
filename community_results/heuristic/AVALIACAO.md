# Avaliação da heurística com alcance determinístico

## Protocolo e conferência

Foram analisadas as 60 execuções em `exact_reach/`: 30 sementes (0 a 29) para
cada valor de `gamma`, na rede dirigida congelada de 20.099 vértices e 31.545
arcos. Todas as execuções produziram comunidades de pelo menos dois vértices,
fracamente conexas e viáveis segundo o CPM dirigido. As identidades dos
arquivos de entrada e do código conferem com `config.json`. Recalcular o
alcance e a coesão de cada solução a partir da rede reproduziu os valores
salvos. As duas listas elite contêm 20 soluções, conforme o limite de Jaccard
de vértices de 0,5.

O alcance externo conta os vértices atingidos fora da própria comunidade sob
`p=1`. A eficiência é o alcance externo dividido pelo número de integrantes.
Os tempos são as somas de construção e busca local registradas nas execuções;
dependem do computador usado.

| `gamma` | Soluções válidas | Tamanho mediano | Alcance externo mediano | Melhor alcance externo | Tamanho da melhor | Tempo total |
|---|---:|---:|---:|---:|---:|---:|
| Percentil 25: 0,003534 | 30/30 | 7,5 | 9.860,5 | 10.938 | 26 | 20,6 s |
| Mediana: 0,041739 | 30/30 | 7,5 | 9.860,5 | 10.939 | 24 | 19,8 s |

## Efeito de `gamma`

As soluções finais de 29 das 30 sementes são idênticas nos dois valores de
`gamma`. Apenas a semente 23 mudou: com o percentil 25, a solução tem 26
integrantes, 27 arcos internos, densidade 0,041538 e alcance externo de
10.938. Com a mediana, tem 24 integrantes, 24 arcos internos, densidade
0,043478 e alcance externo de 10.939. Os 24 integrantes da segunda solução
estão contidos na primeira. A solução de 26 integrantes fica ligeiramente
abaixo da restrição da mediana. Assim, a mediana tem a vantagem de exigir
maior coesão sem perda observada de alcance neste conjunto de sementes, mas
os resultados não sustentam uma diferença ampla de desempenho entre os dois
valores. No conjunto, há 31 comunidades distintas entre as 60 execuções.

## Comparação com o baseline Leiden

A comunidade Leiden com maior alcance externo é a 26: 694 integrantes e
9.646 vértices externos atingidos. A melhor solução da heurística atinge
10.939 com 24 integrantes, uma diferença de 1.293 vértices externos. Em
17 das 30 execuções de cada `gamma`, o alcance externo supera 9.646; essas
soluções têm entre 6 e 26 integrantes. O maior alcance total de uma
comunidade Leiden é 10.518 (comunidade 7); a melhor heurística atinge
10.963 no total.

Entre as comunidades Leiden com até 24 integrantes, o maior alcance externo
é 9.011, da comunidade 57 com quatro integrantes. Para uma comparação por
tamanho, a fronteira não dominada das soluções da heurística em tamanho
menor e alcance externo maior está em `pareto_size_reach.csv`:

| Integrantes | Alcance externo | Alcance por integrante | Semente |
|---:|---:|---:|---:|
| 2 | 6.568 | 3.284 | 12 |
| 6 | 9.860 | 1.643 | 4 |
| 7 | 9.881 | 1.412 | 3 |
| 11 | 9.901 | 900 | 14 |
| 13 | 10.337 | 795 | 10 |
| 24 | 10.939 | 456 | 23 |

As seis linhas usam as soluções de `gamma` mediano; as cinco primeiras
também aparecem com o percentil 25. A maior eficiência da heurística é
3.284 vértices externos por integrante (semente 12, dois integrantes).
A maior eficiência entre as comunidades Leiden é 2.252,75 (comunidade 57,
quatro integrantes). Leiden foi otimizado para modularidade e cobre a rede
com uma partição; a heurística otimiza propagação e pode selecionar
integrantes de comunidades diferentes. Portanto, a comparação mede o ganho
de alcance dos conjuntos selecionados, não a qualidade de uma partição.

## Diversidade e interpretação

As soluções elite obedecem ao limite de Jaccard de **integrantes**: a mediana
do Jaccard entre seus pares é zero. Apesar disso, a mediana do Jaccard entre
os conjuntos de vértices **atingidos** é 0,953, e 121 dos 190 pares de cada
elite têm sobreposição de alcance acima de 0,9. A diversidade de integrantes
não corresponde, neste caso, a diversidade dos públicos atingidos.

A melhor solução (`gamma` mediano, semente 23) contém integrantes de cinco
comunidades Leiden: sete da matemática alemã dos séculos XIX e XX (26), sete
do cânone da filosofia antiga à moderna (7), sete da matemática e física
matemática do século XX (9), dois da filosofia analítica (1) e um da
cibernética (24). Em 16 das 30 soluções por `gamma`, os integrantes vêm de
mais de uma comunidade Leiden. O resultado é melhor descrito como um
**conjunto conectado de propagadores**: a conectividade e o CPM estão
verificados, mas não estabelecem uma escola de pensamento homogênea.

## Conclusão

A heurística encontra conjuntos pequenos com alcance determinístico elevado.
A mediana de `gamma` é uma escolha principal defensável para o próximo
relato, mantendo o percentil 25 como sensibilidade. Convém mostrar a
fronteira tamanho–alcance e a forte sobreposição entre públicos atingidos,
além do melhor resultado isolado. As inferências continuam condicionadas às
arestas observadas no DBpedia e à hipótese de propagação transitiva com
`p=1`.

A caracterização semântica e relacional das 31 soluções distintas está em
`characterization/characterization.md`, com tabelas reproduzíveis no mesmo
diretório. Ela separa linhagens de orientação, tradições intelectuais,
agrupamentos temáticos e conjuntos mistos; nenhum deles foi classificado
como escola candidata.
