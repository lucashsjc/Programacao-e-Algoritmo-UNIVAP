# Algoritmos e Programação – UNIVAP

Repositório com os desafios da disciplina de **Algoritmos e Programação** da FEAU – UNIVAP.

- **Aluno:** Lucas Henrique da Silva
- **Professor:** Andre Olimpio

---

## 📁 Estrutura

```
DESAFIO1/
  ├── LogiFast.alg         → código do Desafio 1 (VisuAlg)
  └── LINK DO VIDEO.txt    → link do vídeo explicativo
DESAFIO2/
  ├── StockPy.py           → código do Desafio 2 (Python)
  └── LINK DO VIDEO.txt    → link do vídeo explicativo
```

---

## 🚚 Desafio 1 – LogiFast

**Sistema Inteligente de Gerenciamento de Entregas**, desenvolvido em **VisuAlg**.

Controla as entregas de uma transportadora entre cinco regiões da cidade (Centro, Norte, Sul, Leste e Oeste).

**Funcionalidades**
- Cadastro de entregas com validação (código duplicado, regiões inválidas, peso, valor e prioridade)
- Distância obtida automaticamente por uma **matriz de distâncias**
- Cálculo do custo com acréscimos por peso e prioridade
- Fila de despacho ordenada com **Bubble Sort** usando 4 critérios
- Controle de status: Aguardando → Em transporte → Entregue
- Estatísticas gerais e análise da matriz
- Cálculo **recursivo** da distância de um percurso

**Conceitos aplicados:** constantes, registro, vetor de registros, matriz, procedimentos, funções, passagem de parâmetros, variáveis locais e globais, ordenação e recursividade.

**Como executar:** abra o arquivo `LogiFast.alg` no VisuAlg e pressione **F9**.

---

## 📦 Desafio 2 – StockPy

**Sistema de Gerenciamento de Estoque e Vendas**, desenvolvido em **Python**.

Gerencia os produtos, o estoque e as vendas de uma loja de informática e acessórios.

**Funcionalidades**
- Cadastro, consulta, alteração e exclusão de produtos
- Entrada no estoque e registro de vendas com comprovante
- Alerta de produtos com estoque baixo
- **Matriz de vendas** por produto e período (manhã, tarde, noite e madrugada)
- Análise estatística e relatório gerencial consolidado
- Ranking dos produtos mais vendidos com ordenação própria (**Insertion Sort**)
- **Busca recursiva** de produtos e **cálculo recursivo** do valor do estoque

**Conceitos aplicados:** listas, dicionários, matriz (listas aninhadas), `match ... case`, laços `for` e `while`, funções com parâmetros e retorno, variáveis locais e globais, validação com `try/except`, ordenação e recursividade.

**Como executar** (requer **Python 3.10 ou superior**):

```bash
python DESAFIO2/StockPy.py
```

---

## 🎥 Vídeos

Os links dos vídeos explicativos estão no arquivo `LINK DO VIDEO.txt` de cada pasta.
