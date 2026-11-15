# Caracterização das comunidades propagadoras do GRASP

## Método

As 60 execuções geraram 31 conjuntos de vértices distintos. Os IDs 0–29 correspondem às sementes 0–29 com `γ` mediano; o ID 30 é a variante adicional da semente 23 com `γ` no percentil 25. Conjuntos repetidos são caracterizados uma vez, com todas as ocorrências registradas na tabela. Cada conjunto é fracamente conexo e satisfaz o CPM da configuração em que ocorreu.

A caracterização segue o protocolo Leiden: campos enriquecidos entre os vértices anotados, representantes por alcance e PageRank interno, tipos de relações internas e inspeção substantiva dos vértices e arestas. Acrescenta-se o alcance perdido ao retirar cada integrante, para identificar sua contribuição exclusiva ao alcance coletivo. Os rótulos Leiden aparecem apenas como contexto: a classificação é feita para cada conjunto da heurística.

`field` está ausente em 30 dos 31 conjuntos e aparece em apenas um vértice do conjunto restante. Nenhum campo atinge simultaneamente duas ocorrências e cobertura de 5%; portanto, os rótulos não se apoiam em `field`. Nenhum conjunto foi classificado como escola candidata. As classes `tradição intelectual`, `linhagem científica`, `agrupamento temático` e `agrupamento misto` descrevem a evidência observável, sem afirmar identidade doutrinária.

## Síntese

Foram caracterizados 31 conjuntos distintos: 13 agrupamento misto, 4 agrupamento temático, 8 linhagem científica, 6 tradição intelectual.

| ID | Rótulo | Classe | Confiança | Integrantes | Alcance externo | Leiden |
|---:|---|---|---|---:|---:|---:|
| 23 | Filosofia e matemática em coalizão de alto alcance | agrupamento misto | alta | 24 | 10939 | 5 |
| 30 | Filosofia e matemática em coalizão de alto alcance (γ p25) | agrupamento misto | alta | 26 | 10938 | 5 |
| 10 | Ciências naturais e filosofia em ramos de influência | agrupamento misto | media | 13 | 10337 | 4 |
| 20 | Filosofia, matemática e psicologia em ramos cruzados | agrupamento misto | baixa | 17 | 10190 | 8 |
| 14 | Filosofia antiga e pensamento religioso medieval | tradição intelectual | media | 11 | 9901 | 2 |
| 11 | Filosofia, psicologia e sociologia em rede de recepção | agrupamento misto | media | 13 | 9898 | 5 |
| 29 | Pensamento social, economia e matemática em ramos cruzados | agrupamento misto | baixa | 13 | 9883 | 4 |
| 3 | Filosofia antiga e recepção na crítica social | agrupamento misto | media | 7 | 9881 | 3 |
| 13 | Filosofia grega e retórica romana | tradição intelectual | media | 8 | 9866 | 1 |
| 18 | Recepção de Platão e filosofia clássica | tradição intelectual | media | 8 | 9865 | 1 |
| 28 | Platão e recepção na Antiguidade tardia | tradição intelectual | media | 7 | 9865 | 1 |
| 9 | Antiguidade e astronomia medieval na recepção de Spinoza | agrupamento misto | media | 7 | 9864 | 2 |
| 7 | Antiguidade, astronomia medieval e recepção na psicologia | agrupamento misto | media | 9 | 9863 | 3 |
| 25 | Filosofia antiga e pensamento social moderno | agrupamento misto | media | 9 | 9862 | 3 |
| 0 | Filosofia antiga e recepção na lógica moderna | agrupamento misto | media | 8 | 9861 | 2 |
| 1 | Filosofia clássica e direito natural moderno | tradição intelectual | media | 8 | 9861 | 1 |
| 4 | Geometria antiga e fontes do pensamento de Kant | agrupamento misto | media | 6 | 9860 | 2 |
| 16 | Filosofia antiga e moderna em cadeia de influência | agrupamento misto | media | 6 | 9857 | 3 |
| 27 | Sufismo e recepção no pensamento de Seyyed Hossein Nasr | tradição intelectual | media | 9 | 9373 | 3 |
| 6 | História natural, medicina e química em linhagens acadêmicas | linhagem científica | media | 7 | 8855 | 3 |
| 2 | Linhagem de orientação em matemática europeia | linhagem científica | alta | 9 | 8234 | 1 |
| 22 | Linhagem de matemática e estatística | linhagem científica | alta | 10 | 6806 | 3 |
| 12 | Par de orientação Ettingshausen–von Lang | linhagem científica | alta | 2 | 6568 | 1 |
| 21 | Par de orientação Haase–Rosenmüller | linhagem científica | alta | 2 | 6371 | 1 |
| 8 | Recepção de Kant e Schopenhauer na ética | agrupamento temático | media | 3 | 5789 | 1 |
| 17 | Genealogia da linguagem BASIC | agrupamento temático | alta | 6 | 569 | 1 |
| 26 | Fortran e precursores de DOPE | agrupamento temático | alta | 3 | 564 | 1 |
| 5 | Par de orientação Bourgin–Duffin | linhagem científica | alta | 2 | 65 | 1 |
| 19 | Documentação e organização do conhecimento | agrupamento temático | media | 2 | 35 | 1 |
| 24 | Par de orientação Fischer–Meyer | linhagem científica | alta | 2 | 26 | 1 |
| 15 | Par de orientação Teuber–Richards | linhagem científica | alta | 2 | 18 | 1 |

## Fichas por conjunto

### 0 — Filosofia antiga e recepção na lógica moderna

**Classe:** `agrupamento_misto` · **confiança:** media · **integrantes:** 8 · **alcance externo:** 9861 · **ocorrências:** mediana:00;p25:00.

**Interpretação:** Hesíodo, Tales, Pitágoras e Aristóteles se conectam a Łukasiewicz, Copi e Barton; o grupo une tradições filosóficas e lógica sem delimitar uma escola.

**Composição Leiden:** 7: 5 — Cânone da filosofia antiga à moderna; 14: 3 — Inteligência artificial e computação do MIT.

**Representantes:** Hesiod (alcance ext. individual 9858, PR int. 0.0454, perda exclusiva 1); Aristotle (alcance ext. individual 9730, PR int. 0.177, perda exclusiva 0); Pherecydes of Syros (alcance ext. individual 9858, PR int. 0.084, perda exclusiva 0); Jan Łukasiewicz (alcance ext. individual 1710, PR int. 0.196, perda exclusiva 0); Pythagoras (alcance ext. individual 9855, PR int. 0.155, perda exclusiva 0).

**Relações internas:** 7 de influência e 0 de orientação; densidade dirigida 0.125; 2.6% das arestas incidentes são internas.

**Exemplos internos:** Hesiod → Pherecydes of Syros [influenced]; Aristotle → Jan Łukasiewicz [influenced]; Pythagoras → Aristotle [influenced]; Pherecydes of Syros → Pythagoras [influenced]; Jan Łukasiewicz → Robert S. Barton [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Aristotle; Hesiod; Irving Copi; Jan Łukasiewicz; Pherecydes of Syros; Pythagoras; Robert S. Barton; Thales of Miletus.

### 1 — Filosofia clássica e direito natural moderno

**Classe:** `tradicao_intelectual` · **confiança:** media · **integrantes:** 8 · **alcance externo:** 9861 · **ocorrências:** mediana:01;p25:01.

**Interpretação:** O núcleo Gentili–Suárez–Grotius forma um ramo de direito natural ligado por arestas de influência a Aristóteles e aos precursores antigos; a comunidade representa uma recepção ampla.

**Composição Leiden:** 7: 8 — Cânone da filosofia antiga à moderna.

**Representantes:** Aristotle (alcance ext. individual 9730, PR int. 0.161, perda exclusiva 0); Pherecydes of Syros (alcance ext. individual 9858, PR int. 0.0489, perda exclusiva 4); Pythagoras (alcance ext. individual 9855, PR int. 0.132, perda exclusiva 0); Francisco Suárez (alcance ext. individual 9000, PR int. 0.227, perda exclusiva 0); Alonso Rodriguez (alcance ext. individual 9000, PR int. 0.0489, perda exclusiva 1).

**Relações internas:** 7 de influência e 0 de orientação; densidade dirigida 0.125; 2.3% das arestas incidentes são internas.

**Exemplos internos:** Pythagoras → Aristotle [influenced]; Aristotle → Francisco Suárez [influenced]; Pherecydes of Syros → Pythagoras [influenced]; Alonso Rodriguez → Francisco Suárez [influenced]; Thales of Miletus → Pythagoras [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Alberico Gentili; Alonso Rodriguez; Aristotle; Francisco Suárez; Hugo Grotius; Pherecydes of Syros; Pythagoras; Thales of Miletus.

### 2 — Linhagem de orientação em matemática europeia

**Classe:** `linhagem_cientifica` · **confiança:** alta · **integrantes:** 9 · **alcance externo:** 8234 · **ocorrências:** mediana:02;p25:02.

**Interpretação:** As arestas internas são de orientação e conectam Kästner, Bessel, Kummer, Schwarz, Weierstrass e Fejér; a evidência sustenta uma genealogia acadêmica, sem afirmar unidade doutrinária.

**Composição Leiden:** 26: 9 — Matemática alemã dos séculos XIX e XX.

**Representantes:** Abraham Gotthelf Kästner (alcance ext. individual 8204, PR int. 0.0406, perda exclusiva 1425); Ernst Kummer (alcance ext. individual 6779, PR int. 0.159, perda exclusiva 0); Friedrich Bessel (alcance ext. individual 6780, PR int. 0.0406, perda exclusiva 2); Heinrich Scherk (alcance ext. individual 6779, PR int. 0.139, perda exclusiva 0); Hermann Schwarz / Hermann Schwarz / 1 (alcance ext. individual 1462, PR int. 0.21, perda exclusiva 0).

**Relações internas:** 0 de influência e 8 de orientação; densidade dirigida 0.111; 10.0% das arestas incidentes são internas.

**Exemplos internos:** Heinrich Scherk → Ernst Kummer [doctoralSupervision]; Abraham Gotthelf Kästner → Heinrich Wilhelm Brandes [doctoralSupervision]; Ernst Kummer → Hermann Schwarz / Hermann Schwarz / 1 [doctoralSupervision]; Friedrich Bessel → Heinrich Scherk [doctoralSupervision]; Heinrich Wilhelm Brandes → Heinrich Scherk [doctoralSupervision].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Abraham Gotthelf Kästner; Ernst Kummer; Friedrich Bessel; Heinrich Scherk; Heinrich Wilhelm Brandes; Hermann Schwarz / Hermann Schwarz / 1; Karl Weierstrass; Lipót Fejér; Ágoston Scholtz.

### 3 — Filosofia antiga e recepção na crítica social

**Classe:** `agrupamento_misto` · **confiança:** media · **integrantes:** 7 · **alcance externo:** 9881 · **ocorrências:** mediana:03;p25:03.

**Interpretação:** Hesíodo, Homero, Platão e Epicuro se ligam a Stirner e Weitling, com Yang Zhu como outra influência registrada sobre Stirner; são ramos intelectuais distintos.

**Composição Leiden:** 7: 4 — Cânone da filosofia antiga à moderna; 5: 2 — Filosofia continental, idealismo e crítica social; 34: 1 — Pensamento e estética do Leste Asiático.

**Representantes:** Hesiod (alcance ext. individual 9860, PR int. 0.0645, perda exclusiva 33); Epicurus (alcance ext. individual 9537, PR int. 0.213, perda exclusiva 0); Plato (alcance ext. individual 9764, PR int. 0.174, perda exclusiva 0); Homer (alcance ext. individual 9829, PR int. 0.0645, perda exclusiva 2); Max Stirner (alcance ext. individual 5694, PR int. 0.355, perda exclusiva 0).

**Relações internas:** 6 de influência e 0 de orientação; densidade dirigida 0.143; 2.0% das arestas incidentes são internas.

**Exemplos internos:** Hesiod → Plato [influenced]; Plato → Epicurus [influenced]; Homer → Plato [influenced]; Epicurus → Max Stirner [influenced]; Wilhelm Weitling → Max Stirner [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Epicurus; Hesiod; Homer; Max Stirner; Plato; Wilhelm Weitling; Yang Zhu.

### 4 — Geometria antiga e fontes do pensamento de Kant

**Classe:** `agrupamento_misto` · **confiança:** media · **integrantes:** 6 · **alcance externo:** 9860 · **ocorrências:** mediana:04;p25:04.

**Interpretação:** Tales, Hipócrates de Quios e Euclides formam um ramo matemático, enquanto Crusius e Swedenborg convergem para Kant; a ligação estrutural não define uma escola única.

**Composição Leiden:** 7: 3 — Cânone da filosofia antiga à moderna; 5: 3 — Filosofia continental, idealismo e crítica social.

**Representantes:** Euclid (alcance ext. individual 9368, PR int. 0.231, perda exclusiva 0); Christian August Crusius (alcance ext. individual 7739, PR int. 0.0855, perda exclusiva 1); Thales (alcance ext. individual 9860, PR int. 0.0855, perda exclusiva 493); Hippocrates of Chios (alcance ext. individual 9368, PR int. 0.0855, perda exclusiva 1); Emanuel Swedenborg (alcance ext. individual 7739, PR int. 0.0855, perda exclusiva 1).

**Relações internas:** 5 de influência e 0 de orientação; densidade dirigida 0.167; 1.9% das arestas incidentes são internas.

**Exemplos internos:** Thales → Euclid [influenced]; Hippocrates of Chios → Euclid [influenced]; Euclid → Immanuel Kant [influenced]; Christian August Crusius → Immanuel Kant [influenced]; Emanuel Swedenborg → Immanuel Kant [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Christian August Crusius; Emanuel Swedenborg; Euclid; Hippocrates of Chios; Immanuel Kant; Thales.

### 5 — Par de orientação Bourgin–Duffin

**Classe:** `linhagem_cientifica` · **confiança:** alta · **integrantes:** 2 · **alcance externo:** 65 · **ocorrências:** mediana:05;p25:05.

**Interpretação:** A única aresta interna registra orientação de David Bourgin a Richard Duffin; a evidência é genealógica e limitada a dois integrantes.

**Composição Leiden:** 19: 2 — Matemática francesa: análise, geometria e estruturas.

**Representantes:** David Bourgin (alcance ext. individual 65, PR int. 0.351, perda exclusiva 1); Richard Duffin (alcance ext. individual 65, PR int. 0.649, perda exclusiva 0).

**Relações internas:** 0 de influência e 1 de orientação; densidade dirigida 0.500; 25.0% das arestas incidentes são internas.

**Exemplos internos:** David Bourgin → Richard Duffin [doctoralSupervision].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** David Bourgin; Richard Duffin.

### 6 — História natural, medicina e química em linhagens acadêmicas

**Classe:** `linhagem_cientifica` · **confiança:** media · **integrantes:** 7 · **alcance externo:** 8855 · **ocorrências:** mediana:06;p25:06.

**Interpretação:** Relações de influência e orientação ligam Bartram, Lineu, Gmelin, Blumenbach, Baldinger, Vauquelin e Stromeyer; o grupo combina ramos das ciências naturais.

**Composição Leiden:** 27: 5 — Pensamento moderno, cultura e teoria social; 18: 1 — Química alemã e físico-química; 19: 1 — Matemática francesa: análise, geometria e estruturas.

**Representantes:** Carl Linnaeus (alcance ext. individual 8060, PR int. 0.0701, perda exclusiva 10); Johann Friedrich Gmelin (alcance ext. individual 8042, PR int. 0.189, perda exclusiva 0); William Bartram (alcance ext. individual 8090, PR int. 0.0701, perda exclusiva 39); Johann Friedrich Blumenbach (alcance ext. individual 7111, PR int. 0.13, perda exclusiva 0); Ernst Gottfried Baldinger (alcance ext. individual 7193, PR int. 0.0701, perda exclusiva 68).

**Relações internas:** 2 de influência e 4 de orientação; densidade dirigida 0.143; 14.0% das arestas incidentes são internas.

**Exemplos internos:** Carl Linnaeus → Johann Friedrich Gmelin [influenced]; William Bartram → Johann Friedrich Gmelin [influenced]; Johann Friedrich Gmelin → Friedrich Stromeyer [doctoralSupervision]; Ernst Gottfried Baldinger → Johann Friedrich Blumenbach [doctoralSupervision]; Johann Friedrich Blumenbach → Friedrich Stromeyer [doctoralSupervision].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Carl Linnaeus; Ernst Gottfried Baldinger; Friedrich Stromeyer; Johann Friedrich Blumenbach; Johann Friedrich Gmelin; Louis Nicolas Vauquelin; William Bartram.

### 7 — Antiguidade, astronomia medieval e recepção na psicologia

**Classe:** `agrupamento_misto` · **confiança:** media · **integrantes:** 9 · **alcance externo:** 9863 · **ocorrências:** mediana:07;p25:07.

**Interpretação:** Um ramo de Tales e Homero passa por Xenófanes e Spinoza, outro inclui Al-Battani e Ibn Ezra, e Potebnia e Spinoza convergem para Vygotsky.

**Composição Leiden:** 7: 6 — Cânone da filosofia antiga à moderna; 3: 2 — Psicologia do desenvolvimento, social e experimental; 5: 1 — Filosofia continental, idealismo e crítica social.

**Representantes:** Xenophanes (alcance ext. individual 9828, PR int. 0.117, perda exclusiva 0); Abraham bar Hiyya (alcance ext. individual 8975, PR int. 0.08, perda exclusiva 0); Al-Battani (alcance ext. individual 8977, PR int. 0.0433, perda exclusiva 3); Abraham ibn Ezra (alcance ext. individual 8914, PR int. 0.111, perda exclusiva 0); Baruch Spinoza (alcance ext. individual 8914, PR int. 0.237, perda exclusiva 0).

**Relações internas:** 8 de influência e 0 de orientação; densidade dirigida 0.111; 6.4% das arestas incidentes são internas.

**Exemplos internos:** Abraham bar Hiyya → Abraham ibn Ezra [influenced]; Al-Battani → Abraham bar Hiyya [influenced]; Xenophanes → Baruch Spinoza [influenced]; Homer → Xenophanes [influenced]; Thales → Xenophanes [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Abraham bar Hiyya; Abraham ibn Ezra; Al-Battani; Alexander Potebnia; Baruch Spinoza; Homer; Lev Vygotsky; Thales; Xenophanes.

### 8 — Recepção de Kant e Schopenhauer na ética

**Classe:** `agrupamento_tematico` · **confiança:** media · **integrantes:** 3 · **alcance externo:** 5789 · **ocorrências:** mediana:08;p25:08.

**Interpretação:** As duas arestas internas apontam de Kant e Schopenhauer para Claudia Card; três vértices não bastam para identificar uma tradição homogênea.

**Composição Leiden:** 27: 3 — Pensamento moderno, cultura e teoria social.

**Representantes:** Kant (alcance ext. individual 5782, PR int. 0.213, perda exclusiva 84); Claudia Card (alcance ext. individual 2, PR int. 0.574, perda exclusiva 0); Schopenhauer (alcance ext. individual 5706, PR int. 0.213, perda exclusiva 8).

**Relações internas:** 2 de influência e 0 de orientação; densidade dirigida 0.333; 3.0% das arestas incidentes são internas.

**Exemplos internos:** Kant → Claudia Card [influenced]; Schopenhauer → Claudia Card [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Claudia Card; Kant; Schopenhauer.

### 9 — Antiguidade e astronomia medieval na recepção de Spinoza

**Classe:** `agrupamento_misto` · **confiança:** media · **integrantes:** 7 · **alcance externo:** 9864 · **ocorrências:** mediana:09;p25:09.

**Interpretação:** Tales e Homero se ligam a Xenófanes; Al-Battani, Bar Hiyya e Ibn Ezra formam outro ramo que converge, com Xenófanes, para Spinoza.

**Composição Leiden:** 7: 6 — Cânone da filosofia antiga à moderna; 5: 1 — Filosofia continental, idealismo e crítica social.

**Representantes:** Xenophanes (alcance ext. individual 9829, PR int. 0.173, perda exclusiva 0); Homer (alcance ext. individual 9830, PR int. 0.0641, perda exclusiva 2); Abraham bar Hiyya (alcance ext. individual 8976, PR int. 0.119, perda exclusiva 0); Thales (alcance ext. individual 9860, PR int. 0.0641, perda exclusiva 25); Al-Battani (alcance ext. individual 8978, PR int. 0.0641, perda exclusiva 3).

**Relações internas:** 6 de influência e 0 de orientação; densidade dirigida 0.143; 5.8% das arestas incidentes são internas.

**Exemplos internos:** Homer → Xenophanes [influenced]; Thales → Xenophanes [influenced]; Abraham bar Hiyya → Abraham ibn Ezra [influenced]; Al-Battani → Abraham bar Hiyya [influenced]; Xenophanes → Baruch Spinoza [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Abraham bar Hiyya; Abraham ibn Ezra; Al-Battani; Baruch Spinoza; Homer; Thales; Xenophanes.

### 10 — Ciências naturais e filosofia em ramos de influência

**Classe:** `agrupamento_misto` · **confiança:** media · **integrantes:** 13 · **alcance externo:** 10337 · **ocorrências:** mediana:10;p25:10.

**Interpretação:** A solução reúne linhagens médicas e de história natural com um ramo da filosofia antiga e moderna; a composição atravessa quatro comunidades Leiden.

**Composição Leiden:** 27: 6 — Pensamento moderno, cultura e teoria social; 7: 4 — Cânone da filosofia antiga à moderna; 1: 2 — Filosofia analítica e filosofia anglófona do século XX; 24: 1 — Cibernética, teoria de sistemas e comunicação.

**Representantes:** Aristotle (alcance ext. individual 9730, PR int. 0.1, perda exclusiva 0); Alexander von Humboldt (alcance ext. individual 5749, PR int. 0.113, perda exclusiva 0); Pythagoras (alcance ext. individual 9855, PR int. 0.0823, perda exclusiva 0); Ernst Anton Nicolai (alcance ext. individual 7192, PR int. 0.0564, perda exclusiva 0); Ernst Gottfried Baldinger (alcance ext. individual 7192, PR int. 0.0784, perda exclusiva 0).

**Relações internas:** 9 de influência e 3 de orientação; densidade dirigida 0.077; 3.4% das arestas incidentes são internas.

**Exemplos internos:** Pythagoras → Aristotle [influenced]; Johann Friedrich Blumenbach → Alexander von Humboldt [influenced]; Aristotle → Charles Taylor (philosopher) [influenced]; Ernst Anton Nicolai → Ernst Gottfried Baldinger [doctoralSupervision]; Pherecydes of Syros → Pythagoras [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Alexander von Humboldt; Aristotle; Charles Taylor (philosopher); Ernst Anton Nicolai; Ernst Gottfried Baldinger; Gadamer; Johann Friedrich Blumenbach; Johann Heinrich Schulze; Lipovetsky; Michael Polanyi; Pherecydes of Syros; Pythagoras; Thales of Miletus.

### 11 — Filosofia, psicologia e sociologia em rede de recepção

**Classe:** `agrupamento_misto` · **confiança:** media · **integrantes:** 13 · **alcance externo:** 9898 · **ocorrências:** mediana:11;p25:11.

**Interpretação:** Suárez, Leibniz, Wundt, Mead e Blumer conectam ramos de filosofia, psicologia e sociologia a um núcleo de grande alcance da filosofia antiga.

**Composição Leiden:** 7: 7 — Cânone da filosofia antiga à moderna; 3: 2 — Psicologia do desenvolvimento, social e experimental; 11: 2 — Sociologia e antropologia clássicas; 5: 1 — Filosofia continental, idealismo e crítica social; 34: 1 — Pensamento e estética do Leste Asiático.

**Representantes:** Aristotle (alcance ext. individual 9727, PR int. 0.0769, perda exclusiva 0); Alonso Rodriguez (alcance ext. individual 8997, PR int. 0.0233, perda exclusiva 1); Pythagoras (alcance ext. individual 9852, PR int. 0.063, perda exclusiva 0); Francisco Suárez (alcance ext. individual 8997, PR int. 0.0758, perda exclusiva 0); Gottfried Wilhelm Leibniz (alcance ext. individual 8713, PR int. 0.14, perda exclusiva 0).

**Relações internas:** 13 de influência e 0 de orientação; densidade dirigida 0.083; 3.0% das arestas incidentes são internas.

**Exemplos internos:** Pythagoras → Aristotle [influenced]; Aristotle → Francisco Suárez [influenced]; Aristotle → Gottfried Wilhelm Leibniz [influenced]; Alonso Rodriguez → Francisco Suárez [influenced]; Francisco Suárez → Gottfried Wilhelm Leibniz [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Alonso Rodriguez; Aristotle; Charles H. Cooley; Confucius; Francisco Suárez; George Herbert Mead; Gottfried Wilhelm Leibniz; Gustav Theodor Fechner; Herbert Blumer; Pherecydes of Syros; Pythagoras; Thales of Miletus; Wilhelm Wundt.

### 12 — Par de orientação Ettingshausen–von Lang

**Classe:** `linhagem_cientifica` · **confiança:** alta · **integrantes:** 2 · **alcance externo:** 6568 · **ocorrências:** mediana:12;p25:12.

**Interpretação:** A única aresta interna registra orientação de Andreas von Ettingshausen a Viktor von Lang; o grande alcance decorre sobretudo do primeiro integrante.

**Composição Leiden:** 23: 2 — Física matemática, geociências e sistemas complexos.

**Representantes:** Andreas von Ettingshausen (alcance ext. individual 6568, PR int. 0.351, perda exclusiva 6030); Viktor von Lang (alcance ext. individual 539, PR int. 0.649, perda exclusiva 0).

**Relações internas:** 0 de influência e 1 de orientação; densidade dirigida 0.500; 20.0% das arestas incidentes são internas.

**Exemplos internos:** Andreas von Ettingshausen → Viktor von Lang [doctoralSupervision].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Andreas von Ettingshausen; Viktor von Lang.

### 13 — Filosofia grega e retórica romana

**Classe:** `tradicao_intelectual` · **confiança:** media · **integrantes:** 8 · **alcance externo:** 9866 · **ocorrências:** mediana:13;p25:13.

**Interpretação:** Arestas de influência levam de filósofos gregos e de Políbio, Arquias e Apolônio Molon a Cícero; a comunidade representa uma recepção intelectual ampla.

**Composição Leiden:** 7: 8 — Cânone da filosofia antiga à moderna.

**Representantes:** Aristotle (alcance ext. individual 9731, PR int. 0.19, perda exclusiva 0); Pherecydes of Syros (alcance ext. individual 9859, PR int. 0.0577, perda exclusiva 4); Pythagoras (alcance ext. individual 9856, PR int. 0.156, perda exclusiva 0); Apollonius Molon (alcance ext. individual 9519, PR int. 0.0577, perda exclusiva 1); Thales of Miletus (alcance ext. individual 9859, PR int. 0.0577, perda exclusiva 4).

**Relações internas:** 7 de influência e 0 de orientação; densidade dirigida 0.125; 2.3% das arestas incidentes são internas.

**Exemplos internos:** Pythagoras → Aristotle [influenced]; Pherecydes of Syros → Pythagoras [influenced]; Aristotle → Cicero [influenced]; Thales of Miletus → Pythagoras [influenced]; Apollonius Molon → Cicero [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Apollonius Molon; Aristotle; Aulus Licinius Archias; Cicero; Pherecydes of Syros; Polybius; Pythagoras; Thales of Miletus.

### 14 — Filosofia antiga e pensamento religioso medieval

**Classe:** `tradicao_intelectual` · **confiança:** media · **integrantes:** 11 · **alcance externo:** 9901 · **ocorrências:** mediana:14;p25:14.

**Interpretação:** Aristóteles, Tomás de Aquino, Joaquim de Fiore e Arnaldus de Villa Nova aparecem como influências em torno de Ramon Llull e autores posteriores.

**Composição Leiden:** 7: 10 — Cânone da filosofia antiga à moderna; 15: 1 — Tradicionalismo, perenialismo e pensamento sufi.

**Representantes:** Aristotle (alcance ext. individual 9730, PR int. 0.117, perda exclusiva 0); Al-Ghazali (alcance ext. individual 9344, PR int. 0.0355, perda exclusiva 33); Pythagoras (alcance ext. individual 9855, PR int. 0.0959, perda exclusiva 0); Aquinas (alcance ext. individual 9180, PR int. 0.0355, perda exclusiva 1); Pherecydes of Syros (alcance ext. individual 9858, PR int. 0.0355, perda exclusiva 4).

**Relações internas:** 10 de influência e 0 de orientação; densidade dirigida 0.091; 2.8% das arestas incidentes são internas.

**Exemplos internos:** Pythagoras → Aristotle [influenced]; Pherecydes of Syros → Pythagoras [influenced]; Aristotle → Ramon Llull / Ramon Llull / 1 [influenced]; Al-Ghazali → Ramon Llull / Ramon Llull / 1 [influenced]; Thales of Miletus → Pythagoras [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Al-Ghazali; Aquinas; Aristotle; Arnaldus de Villa Nova; Jakob Wimpfeling; Joachim of Fiore; Johannes Trithemius; Pherecydes of Syros; Pythagoras; Ramon Llull / Ramon Llull / 1; Thales of Miletus.

### 15 — Par de orientação Teuber–Richards

**Classe:** `linhagem_cientifica` · **confiança:** alta · **integrantes:** 2 · **alcance externo:** 18 · **ocorrências:** mediana:15;p25:15.

**Interpretação:** A única aresta interna registra orientação de Hans-Lukas Teuber a Whitman Richards; o grupo é uma genealogia acadêmica mínima.

**Composição Leiden:** 3: 2 — Psicologia do desenvolvimento, social e experimental.

**Representantes:** Hans-Lukas Teuber (alcance ext. individual 18, PR int. 0.351, perda exclusiva 3); Whitman Richards (alcance ext. individual 16, PR int. 0.649, perda exclusiva 0).

**Relações internas:** 0 de influência e 1 de orientação; densidade dirigida 0.500; 12.5% das arestas incidentes são internas.

**Exemplos internos:** Hans-Lukas Teuber → Whitman Richards [doctoralSupervision].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Hans-Lukas Teuber; Whitman Richards.

### 16 — Filosofia antiga e moderna em cadeia de influência

**Classe:** `agrupamento_misto` · **confiança:** media · **integrantes:** 6 · **alcance externo:** 9857 · **ocorrências:** mediana:16;p25:16.

**Interpretação:** Anaximandro, Demócrito e Lucrécio formam um ramo que chega a Kant; Kant e A. Loos se ligam a Wittgenstein, combinando tradições distintas.

**Composição Leiden:** 7: 3 — Cânone da filosofia antiga à moderna; 1: 2 — Filosofia analítica e filosofia anglófona do século XX; 5: 1 — Filosofia continental, idealismo e crítica social.

**Representantes:** Democritus (alcance ext. individual 9777, PR int. 0.131, perda exclusiva 0); Anaximander (alcance ext. individual 9857, PR int. 0.0706, perda exclusiva 81); Immanuel Kant (alcance ext. individual 7738, PR int. 0.225, perda exclusiva 0); Lucretius (alcance ext. individual 9529, PR int. 0.182, perda exclusiva 0); A. Loos (alcance ext. individual 3972, PR int. 0.0706, perda exclusiva 1).

**Relações internas:** 5 de influência e 0 de orientação; densidade dirigida 0.167; 1.0% das arestas incidentes são internas.

**Exemplos internos:** Anaximander → Democritus [influenced]; Democritus → Lucretius [influenced]; Lucretius → Immanuel Kant [influenced]; Immanuel Kant → Ludwig Wittgenstein [influenced]; A. Loos → Ludwig Wittgenstein [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** A. Loos; Anaximander; Democritus; Immanuel Kant; Lucretius; Ludwig Wittgenstein.

### 17 — Genealogia da linguagem BASIC

**Classe:** `agrupamento_tematico` · **confiança:** alta · **integrantes:** 6 · **alcance externo:** 569 · **ocorrências:** mediana:17;p25:17.

**Interpretação:** Speedcoding e JOSS influenciam BASIC, que se liga a variantes de Visual Basic e Basic4ppc; os vértices são linguagens de programação, não uma escola de pensamento.

**Composição Leiden:** 0: 6 — Linguagens de programação e genealogia de paradigmas.

**Representantes:** BASIC (alcance ext. individual 374, PR int. 0.198, perda exclusiva 0); JOSS (alcance ext. individual 385, PR int. 0.0733, perda exclusiva 5); Speedcoding (alcance ext. individual 563, PR int. 0.0733, perda exclusiva 183); Visual Basic (classic) / Visual Basic / 1 (alcance ext. individual 7, PR int. 0.241, perda exclusiva 0); Basic4ppc (alcance ext. individual 0, PR int. 0.341, perda exclusiva 0).

**Relações internas:** 5 de influência e 0 de orientação; densidade dirigida 0.167; 9.8% das arestas incidentes são internas.

**Exemplos internos:** JOSS → BASIC [influenced]; Speedcoding → BASIC [influenced]; BASIC → Visual Basic (classic) / Visual Basic / 1 [influenced]; Visual Basic (classic) / Visual Basic / 1 → Basic4ppc [influenced]; Visual Basic → Basic4ppc [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** BASIC; Basic4ppc; JOSS; Speedcoding; Visual Basic; Visual Basic (classic) / Visual Basic / 1.

### 18 — Recepção de Platão e filosofia clássica

**Classe:** `tradicao_intelectual` · **confiança:** media · **integrantes:** 8 · **alcance externo:** 9865 · **ocorrências:** mediana:18;p25:18.

**Interpretação:** Hesíodo, Homero, Crátilo e Diotima aparecem como influências sobre Platão; Gassendi e Locke estendem a rede para a filosofia moderna.

**Composição Leiden:** 7: 8 — Cânone da filosofia antiga à moderna.

**Representantes:** Hesiod (alcance ext. individual 9860, PR int. 0.05, perda exclusiva 33); Cratylus (alcance ext. individual 9764, PR int. 0.05, perda exclusiva 1); Diotima of Mantinea (alcance ext. individual 9793, PR int. 0.05, perda exclusiva 1); Homer (alcance ext. individual 9829, PR int. 0.05, perda exclusiva 2); Plato (alcance ext. individual 9764, PR int. 0.22, perda exclusiva 0).

**Relações internas:** 7 de influência e 0 de orientação; densidade dirigida 0.125; 2.3% das arestas incidentes são internas.

**Exemplos internos:** Hesiod → Plato [influenced]; Cratylus → Plato [influenced]; Diotima of Mantinea → Plato [influenced]; Homer → Plato [influenced]; Plato → Pierre Gassendi [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Cratylus; Diotima of Mantinea; Hesiod; Homer; John Locke; Pierre Gassendi; Plato; Polybius.

### 19 — Documentação e organização do conhecimento

**Classe:** `agrupamento_tematico` · **confiança:** media · **integrantes:** 2 · **alcance externo:** 35 · **ocorrências:** mediana:19;p25:19.

**Interpretação:** A única aresta interna registra influência de Melvil Dewey sobre Paul Otlet; a comunidade é pequena demais para afirmar uma escola autônoma.

**Composição Leiden:** 24: 2 — Cibernética, teoria de sistemas e comunicação.

**Representantes:** Melvil Dewey (alcance ext. individual 35, PR int. 0.351, perda exclusiva 1); Paul Otlet (alcance ext. individual 35, PR int. 0.649, perda exclusiva 0).

**Relações internas:** 1 de influência e 0 de orientação; densidade dirigida 0.500; 5.3% das arestas incidentes são internas.

**Exemplos internos:** Melvil Dewey → Paul Otlet [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Melvil Dewey; Paul Otlet.

### 20 — Filosofia, matemática e psicologia em ramos cruzados

**Classe:** `agrupamento_misto` · **confiança:** baixa · **integrantes:** 17 · **alcance externo:** 10190 · **ocorrências:** mediana:20;p25:20.

**Interpretação:** A solução combina filósofos antigos, Leibniz, Frege, Carnap, Hempel, matemáticos e psicólogos; oito comunidades Leiden contribuem integrantes.

**Composição Leiden:** 1: 5 — Filosofia analítica e filosofia anglófona do século XX; 7: 4 — Cânone da filosofia antiga à moderna; 18: 2 — Química alemã e físico-química; 27: 2 — Pensamento moderno, cultura e teoria social; 3: 1 — Psicologia do desenvolvimento, social e experimental; 5: 1 — Filosofia continental, idealismo e crítica social; 26: 1 — Matemática alemã dos séculos XIX e XX; 34: 1 — Pensamento e estética do Leste Asiático.

**Representantes:** Gottfried Wilhelm Leibniz (alcance ext. individual 8711, PR int. 0.0687, perda exclusiva 0); Abraham Gottlob Werner (alcance ext. individual 6753, PR int. 0.0166, perda exclusiva 44); Plato (alcance ext. individual 9760, PR int. 0.0447, perda exclusiva 0); Alfred Clebsch (alcance ext. individual 4026, PR int. 0.0528, perda exclusiva 0); Confucius (alcance ext. individual 8811, PR int. 0.0166, perda exclusiva 40).

**Relações internas:** 11 de influência e 5 de orientação; densidade dirigida 0.059; 3.7% das arestas incidentes são internas.

**Exemplos internos:** Plato → Gottfried Wilhelm Leibniz [influenced]; Confucius → Gottfried Wilhelm Leibniz [influenced]; Gottfried Wilhelm Leibniz → Gottlob Frege [influenced]; Abraham Gottlob Werner → Christian Samuel Weiss [doctoralSupervision]; Hesiod → Plato [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Abraham Gottlob Werner; Alfred Clebsch; Carl Gustav Hempel; Carl Hempel; Christian Samuel Weiss; Confucius; Ernst Christian Julius Schering; Franz Ernst Neumann; Gottfried Wilhelm Leibniz; Gottlob Frege; Gustav Theodor Fechner; Hermann Lotze; Hesiod; Homer; Jaegwon Kim; Plato; Rudolf Carnap.

### 21 — Par de orientação Haase–Rosenmüller

**Classe:** `linhagem_cientifica` · **confiança:** alta · **integrantes:** 2 · **alcance externo:** 6371 · **ocorrências:** mediana:21;p25:21.

**Interpretação:** A única aresta interna registra orientação de Johann Gottlob Haase a Johann Christian Rosenmüller; a evidência é uma relação genealógica mínima.

**Composição Leiden:** 5: 2 — Filosofia continental, idealismo e crítica social.

**Representantes:** Johann Christian Rosenmüller (alcance ext. individual 6371, PR int. 0.649, perda exclusiva 0); Johann Gottlob Haase (alcance ext. individual 6371, PR int. 0.351, perda exclusiva 1).

**Relações internas:** 0 de influência e 1 de orientação; densidade dirigida 0.500; 50.0% das arestas incidentes são internas.

**Exemplos internos:** Johann Gottlob Haase → Johann Christian Rosenmüller [doctoralSupervision].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Johann Christian Rosenmüller; Johann Gottlob Haase.

### 22 — Linhagem de matemática e estatística

**Classe:** `linhagem_cientifica` · **confiança:** alta · **integrantes:** 10 · **alcance externo:** 6806 · **ocorrências:** mediana:22;p25:22.

**Interpretação:** Orientações ligam Kummer, Schwarz, Fejér, Riesz, Cramér, Wold e Whittle; o grupo combina genealogias de matemática e estatística.

**Composição Leiden:** 26: 5 — Matemática alemã dos séculos XIX e XX; 29: 3 — Estatística matemática e genética quantitativa; 9: 2 — Matemática e física matemática do século XX.

**Representantes:** Ernst Kummer (alcance ext. individual 6775, PR int. 0.0317, perda exclusiva 9); Karl Weierstrass (alcance ext. individual 6778, PR int. 0.0317, perda exclusiva 12); Hermann Schwarz / Hermann Schwarz / 1 (alcance ext. individual 1458, PR int. 0.0856, perda exclusiva 0); Harald Cramér (alcance ext. individual 43, PR int. 0.154, perda exclusiva 0); Herman Wold (alcance ext. individual 11, PR int. 0.162, perda exclusiva 0).

**Relações internas:** 1 de influência e 8 de orientação; densidade dirigida 0.100; 9.3% das arestas incidentes são internas.

**Exemplos internos:** Ernst Kummer → Hermann Schwarz / Hermann Schwarz / 1 [doctoralSupervision]; Karl Weierstrass → Hermann Schwarz / Hermann Schwarz / 1 [doctoralSupervision]; Hermann Schwarz / Hermann Schwarz / 1 → Lipót Fejér [doctoralSupervision]; Harald Cramér → Herman Wold [doctoralSupervision]; Marcel Riesz → Harald Cramér [doctoralSupervision].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Ernst Kummer; Harald Cramér; Herman Wold; Hermann Schwarz / Hermann Schwarz / 1; Karl Weierstrass; Lipót Fejér; Marcel Riesz; Maurice Bartlett; Peter Whittle (mathematician); Ágoston Scholtz.

### 23 — Filosofia e matemática em coalizão de alto alcance

**Classe:** `agrupamento_misto` · **confiança:** alta · **integrantes:** 24 · **alcance externo:** 10939 · **ocorrências:** mediana:23.

**Interpretação:** A solução de maior alcance reúne ramos antigos e medievais da filosofia com genealogias de matemática e física matemática; a conectividade não implica uma escola comum.

**Composição Leiden:** 7: 7 — Cânone da filosofia antiga à moderna; 26: 7 — Matemática alemã dos séculos XIX e XX; 9: 7 — Matemática e física matemática do século XX; 1: 2 — Filosofia analítica e filosofia anglófona do século XX; 24: 1 — Cibernética, teoria de sistemas e comunicação.

**Representantes:** Aristotle (alcance ext. individual 9728, PR int. 0.0382, perda exclusiva 0); Al-Ghazali (alcance ext. individual 9342, PR int. 0.0116, perda exclusiva 33); Pythagoras (alcance ext. individual 9853, PR int. 0.0313, perda exclusiva 0); René Descartes (alcance ext. individual 8963, PR int. 0.0476, perda exclusiva 0); Abraham Gotthelf Kästner (alcance ext. individual 8198, PR int. 0.0116, perda exclusiva 687).

**Relações internas:** 13 de influência e 12 de orientação; densidade dirigida 0.043; 4.6% das arestas incidentes são internas.

**Exemplos internos:** Pythagoras → Aristotle [influenced]; Aristotle → René Descartes [influenced]; Aristotle → Karl Popper [influenced]; Al-Ghazali → René Descartes [influenced]; Anselm of Canterbury → René Descartes [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Abraham Gotthelf Kästner; Al-Ghazali; Anselm of Canterbury; Aristotle; Arthur Cayley; Carl Gustav Jacob Jacobi; Carl Neumann; Donald T. Campbell; Enno Dirksen; Friedrich Julius Richelot; H. F. Baker; J. A. Todd; Johann Tobias Mayer; Karl Bühler; Karl Popper; Michael Atiyah; Pherecydes of Syros; Pythagoras; René Descartes; Roger Penrose; Solomon Lefschetz; Thales of Miletus; W. V. D. Hodge; William Edward Story.

### 24 — Par de orientação Fischer–Meyer

**Classe:** `linhagem_cientifica` · **confiança:** alta · **integrantes:** 2 · **alcance externo:** 26 · **ocorrências:** mediana:24;p25:24.

**Interpretação:** A única aresta interna registra orientação de Patrick C. Fischer a Albert R. Meyer; o rótulo limita-se à relação observada.

**Composição Leiden:** 31: 2 — Escola matemática russa e soviética.

**Representantes:** Albert R. Meyer (alcance ext. individual 26, PR int. 0.649, perda exclusiva 0); Patrick C. Fischer (alcance ext. individual 26, PR int. 0.351, perda exclusiva 1).

**Relações internas:** 0 de influência e 1 de orientação; densidade dirigida 0.500; 9.1% das arestas incidentes são internas.

**Exemplos internos:** Patrick C. Fischer → Albert R. Meyer [doctoralSupervision].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Albert R. Meyer; Patrick C. Fischer.

### 25 — Filosofia antiga e pensamento social moderno

**Classe:** `agrupamento_misto` · **confiança:** media · **integrantes:** 9 · **alcance externo:** 9862 · **ocorrências:** mediana:25;p25:25.

**Interpretação:** O núcleo antigo se liga a Comte e Bachelard, enquanto Saint-Simon e Ibn Khaldun também aparecem como influências de Comte; há várias tradições no mesmo conjunto.

**Composição Leiden:** 7: 6 — Cânone da filosofia antiga à moderna; 5: 2 — Filosofia continental, idealismo e crítica social; 57: 1 — Pensamento social árabe de Ibn Khaldun a al-Jabri.

**Representantes:** Aristotle (alcance ext. individual 9730, PR int. 0.143, perda exclusiva 0); Pythagoras (alcance ext. individual 9855, PR int. 0.117, perda exclusiva 0); Auguste Comte (alcance ext. individual 5746, PR int. 0.239, perda exclusiva 0); Pherecydes of Syros (alcance ext. individual 9858, PR int. 0.0434, perda exclusiva 4); De Saint-Simon (alcance ext. individual 5757, PR int. 0.0434, perda exclusiva 2).

**Relações internas:** 8 de influência e 0 de orientação; densidade dirigida 0.111; 2.3% das arestas incidentes são internas.

**Exemplos internos:** Pythagoras → Aristotle [influenced]; Aristotle → Auguste Comte [influenced]; Pherecydes of Syros → Pythagoras [influenced]; De Saint-Simon → Auguste Comte [influenced]; Ibn Khaldun → Auguste Comte [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Aristotle; Auguste Comte; De Saint-Simon; Gaston Bachelard; Ibn Khaldun; Max Picard; Pherecydes of Syros; Pythagoras; Thales of Miletus.

### 26 — Fortran e precursores de DOPE

**Classe:** `agrupamento_tematico` · **confiança:** alta · **integrantes:** 3 · **alcance externo:** 564 · **ocorrências:** mediana:26;p25:26.

**Interpretação:** Fortran e DARSIMCO aparecem como influências de DOPE; os três vértices são linguagens de programação.

**Composição Leiden:** 0: 3 — Linguagens de programação e genealogia de paradigmas.

**Representantes:** DARSIMCO (alcance ext. individual 20, PR int. 0.213, perda exclusiva 1); Fortran (alcance ext. individual 564, PR int. 0.213, perda exclusiva 545); DOPE (Dartmouth Oversimplified Programming Experiment) (alcance ext. individual 20, PR int. 0.574, perda exclusiva 0).

**Relações internas:** 2 de influência e 0 de orientação; densidade dirigida 0.333; 7.7% das arestas incidentes são internas.

**Exemplos internos:** DARSIMCO → DOPE (Dartmouth Oversimplified Programming Experiment) [influenced]; Fortran → DOPE (Dartmouth Oversimplified Programming Experiment) [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** DARSIMCO; DOPE (Dartmouth Oversimplified Programming Experiment); Fortran.

### 27 — Sufismo e recepção no pensamento de Seyyed Hossein Nasr

**Classe:** `tradicao_intelectual` · **confiança:** media · **integrantes:** 9 · **alcance externo:** 9373 · **ocorrências:** mediana:27;p25:27.

**Interpretação:** Al-Ghazali, Ibn Masarra e Bayazid Bastami se ligam a Ibn Arabi; Hafez, Rumi, Ibn Sina e outros convergem para Nasr. O grupo atravessa vertentes da tradição islâmica.

**Composição Leiden:** 15: 7 — Tradicionalismo, perenialismo e pensamento sufi; 7: 1 — Cânone da filosofia antiga à moderna; 5: 1 — Filosofia continental, idealismo e crítica social.

**Representantes:** Al-Ghazali (alcance ext. individual 9344, PR int. 0.0557, perda exclusiva 108); Ibn Arabi / Ibn ʿArabī / 1 (alcance ext. individual 9175, PR int. 0.198, perda exclusiva 0); Bayazid Bastami (alcance ext. individual 9178, PR int. 0.0557, perda exclusiva 4); Ibn Masarra (alcance ext. individual 9259, PR int. 0.0557, perda exclusiva 23); Hafez (alcance ext. individual 5739, PR int. 0.0557, perda exclusiva 1).

**Relações internas:** 8 de influência e 0 de orientação; densidade dirigida 0.111; 5.9% das arestas incidentes são internas.

**Exemplos internos:** Al-Ghazali → Ibn Arabi / Ibn ʿArabī / 1 [influenced]; Bayazid Bastami → Ibn Arabi / Ibn ʿArabī / 1 [influenced]; Ibn Masarra → Ibn Arabi / Ibn ʿArabī / 1 [influenced]; Ibn Arabi / Ibn ʿArabī / 1 → Seyyed Hossein Nasr [influenced]; Hafez → Seyyed Hossein Nasr [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Al-Ghazali; Allameh Sayyed Abul Hasan Rafiee Qazvini; Bayazid Bastami; Hafez; Ibn Arabi / Ibn ʿArabī / 1; Ibn Masarra; Ibn Sina; Rumi; Seyyed Hossein Nasr.

### 28 — Platão e recepção na Antiguidade tardia

**Classe:** `tradicao_intelectual` · **confiança:** media · **integrantes:** 7 · **alcance externo:** 9865 · **ocorrências:** mediana:28;p25:28.

**Interpretação:** Hesíodo, Homero, Crátilo e Diotima apontam para Platão, enquanto David, o Invencível, e Platão se ligam a João Filopono; o grupo é uma cadeia de recepção ampla.

**Composição Leiden:** 7: 7 — Cânone da filosofia antiga à moderna.

**Representantes:** Cratylus (alcance ext. individual 9765, PR int. 0.0667, perda exclusiva 1); Hesiod (alcance ext. individual 9861, PR int. 0.0667, perda exclusiva 33); Diotima of Mantinea (alcance ext. individual 9794, PR int. 0.0667, perda exclusiva 1); Plato (alcance ext. individual 9765, PR int. 0.294, perda exclusiva 0); Homer (alcance ext. individual 9830, PR int. 0.0667, perda exclusiva 2).

**Relações internas:** 6 de influência e 0 de orientação; densidade dirigida 0.143; 2.7% das arestas incidentes são internas.

**Exemplos internos:** Cratylus → Plato [influenced]; Hesiod → Plato [influenced]; Diotima of Mantinea → Plato [influenced]; Homer → Plato [influenced]; Plato → John Philoponus [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Cratylus; David the Invincible; Diotima of Mantinea; Hesiod; Homer; John Philoponus; Plato.

### 29 — Pensamento social, economia e matemática em ramos cruzados

**Classe:** `agrupamento_misto` · **confiança:** baixa · **integrantes:** 13 · **alcance externo:** 9883 · **ocorrências:** mediana:29;p25:29.

**Interpretação:** A solução reúne autores clássicos, Marx, Fourier, Knapp, Bortkiewicz, Monge, Babbage e Herschel; há relações internas reais, mas não uma tradição única.

**Composição Leiden:** 7: 4 — Cânone da filosofia antiga à moderna; 5: 3 — Filosofia continental, idealismo e crítica social; 12: 3 — História do pensamento econômico; 41: 3 — Genealogia histórica de matemática e física.

**Representantes:** Michel de Montaigne (alcance ext. individual 8988, PR int. 0.0954, perda exclusiva 0); Hesiod (alcance ext. individual 9859, PR int. 0.029, perda exclusiva 33); Charles Babbage (alcance ext. individual 5695, PR int. 0.0782, perda exclusiva 0); Plato (alcance ext. individual 9763, PR int. 0.0782, perda exclusiva 0); Charles Fourier (alcance ext. individual 5708, PR int. 0.029, perda exclusiva 9).

**Relações internas:** 12 de influência e 1 de orientação; densidade dirigida 0.077; 2.1% das arestas incidentes são internas.

**Exemplos internos:** Plato → Michel de Montaigne [influenced]; Hesiod → Plato [influenced]; Gaspard Monge → Charles Babbage [influenced]; Homer → Plato [influenced]; Michel de Montaigne → Karl Marx [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 7.7%.

**Integrantes:** Charles Babbage; Charles Fourier; Ferdinand Lassalle; Gaspard Monge; Georg Friedrich Knapp; Hesiod; Homer; Johann Jakob Bachofen; John Herschel; Karl Marx; Ladislaus Bortkiewicz; Michel de Montaigne; Plato.

### 30 — Filosofia e matemática em coalizão de alto alcance (γ p25)

**Classe:** `agrupamento_misto` · **confiança:** alta · **integrantes:** 26 · **alcance externo:** 10938 · **ocorrências:** p25:23.

**Interpretação:** Variante da semente 23 com Bias de Priene e Heráclito adicionais; mantém os mesmos 24 integrantes da solução com γ mediano e amplia o ramo antigo.

**Composição Leiden:** 7: 9 — Cânone da filosofia antiga à moderna; 26: 7 — Matemática alemã dos séculos XIX e XX; 9: 7 — Matemática e física matemática do século XX; 1: 2 — Filosofia analítica e filosofia anglófona do século XX; 24: 1 — Cibernética, teoria de sistemas e comunicação.

**Representantes:** Aristotle (alcance ext. individual 9728, PR int. 0.0494, perda exclusiva 0); Pythagoras (alcance ext. individual 9852, PR int. 0.0284, perda exclusiva 0); Heraclitus (alcance ext. individual 9821, PR int. 0.0315, perda exclusiva 0); René Descartes (alcance ext. individual 8963, PR int. 0.0494, perda exclusiva 0); Al-Ghazali (alcance ext. individual 9342, PR int. 0.0105, perda exclusiva 33).

**Relações internas:** 16 de influência e 12 de orientação; densidade dirigida 0.042; 4.8% das arestas incidentes são internas.

**Exemplos internos:** Pythagoras → Aristotle [influenced]; Heraclitus → Aristotle [influenced]; Aristotle → René Descartes [influenced]; Pythagoras → Heraclitus [influenced]; Aristotle → Karl Popper [influenced].

**Campos apoiados:** nenhum; cobertura de `field` 0.0%.

**Integrantes:** Abraham Gotthelf Kästner; Al-Ghazali; Anselm of Canterbury; Aristotle; Arthur Cayley; Bias of Priene; Carl Gustav Jacob Jacobi; Carl Neumann; Donald T. Campbell; Enno Dirksen; Friedrich Julius Richelot; H. F. Baker; Heraclitus; J. A. Todd; Johann Tobias Mayer; Karl Bühler; Karl Popper; Michael Atiyah; Pherecydes of Syros; Pythagoras; René Descartes; Roger Penrose; Solomon Lefschetz; Thales of Miletus; W. V. D. Hodge; William Edward Story.

## Limitações

Os grupos foram escolhidos para maximizar alcance sob conectividade fraca e coesão CPM. Por isso, podem atravessar tradições e comunidades Leiden. Arestas de orientação registram genealogia acadêmica e não implicam adesão doutrinária. As relações do DBpedia e a propagação transitiva com `p=1` medem potencial estrutural, não transmissão histórica observada. A ausência quase completa de `field` impede validar os rótulos por enriquecimento temático. Nenhum rótulo desta etapa afirma uma escola candidata; por esse motivo não foi feita uma verificação externa de escolas.
