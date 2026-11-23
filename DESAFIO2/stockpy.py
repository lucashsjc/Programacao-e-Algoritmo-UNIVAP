"""
StockPy - Sistema de Gerenciamento de Estoque e Vendas
Desafio 2 - Lógica de Programação - Tema 3 (Etapas 1 e 2)


# ==========================================================
# VARIÁVEIS GLOBAIS (dados do sistema)
# ==========================================================

# Lista de produtos. Cada produto é um dicionário:
# {"codigo", "nome", "categoria", "preco", "quantidade", "minimo", "vendidos"}
produtos = []

# Lista de vendas (histórico). Cada venda é um dicionário:
# {"codigo", "nome", "categoria", "quantidade", "preco", "valor", "periodo"}
vendas = []

# Totalizadores globais atualizados a cada venda (Requisito 06)
faturamento_total = 0.0
total_operacoes = 0
total_unidades_vendidas = 0

# Nomes dos períodos comerciais (índice 0 = manhã ... índice 3 = madrugada)
PERIODOS = ["Manhã", "Tarde", "Noite", "Madrugada"]

LINHA = "=" * 40


# ==========================================================
# FUNÇÕES AUXILIARES DE ENTRADA E FORMATAÇÃO
# ==========================================================

def formatar_moeda(valor):
    """Recebe um número e retorna uma string no formato R$ 1.234,56."""
    texto = f"{valor:,.2f}"                       # ex.: 1,234.56
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


def ler_texto(mensagem):
    """Lê um texto obrigatório (não aceita vazio). Retorna o texto lido."""
    texto = input(mensagem).strip()
    while texto == "":
        print("Erro: este campo é obrigatório.")
        texto = input(mensagem).strip()
    return texto


def ler_inteiro(mensagem):
    """Lê um número inteiro. Repete enquanto o valor digitado não for inteiro."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Erro: digite um número inteiro válido.")


def ler_inteiro_minimo(mensagem, minimo):
    """Lê um inteiro maior ou igual a 'minimo'. Repete até ser válido."""
    valor = ler_inteiro(mensagem)
    while valor < minimo:
        print(f"Erro: o valor deve ser maior ou igual a {minimo}.")
        valor = ler_inteiro(mensagem)
    return valor


def ler_preco(mensagem):
    """Lê um preço (aceita vírgula ou ponto) que deve ser maior que zero."""
    while True:
        try:
            preco = float(input(mensagem).replace(",", "."))
            if preco > 0:
                return preco
            print("Erro: o preço deve ser maior que zero.")
        except ValueError:
            print("Erro: digite um valor numérico válido.")


# ==========================================================
# ETAPA 1
# ==========================================================

def exibir_menu():
    """Mostra o menu principal e retorna a opção digitada (string)."""
    print("\n" + LINHA)
    print("STOCKPY | MENU PRINCIPAL")
    print(LINHA)
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Consultar produto")
    print("4 - Registrar entrada no estoque")
    print("5 - Registrar venda")
    print("6 - Consultar produtos com estoque baixo")
    print("7 - Consultar resumo de vendas")
    print("8 - Alterar cadastro de produto")
    print("9 - Excluir produto")
    print("10 - Visualizar matriz de vendas")
    print("11 - Consultar análise estatística")
    print("12 - Consultar ranking de produtos")
    print("13 - Realizar busca recursiva")
    print("14 - Calcular valor do estoque por recursão")
    print("15 - Gerar relatório consolidado")
    print("0 - Encerrar aplicação")
    return input("Informe a opção desejada: ").strip()


def buscar_produto(lista, codigo):
    """
    Busca convencional (com for) de um produto pelo código.
    Parâmetros: lista de produtos e código procurado.
    Retorna o dicionário do produto ou None se não encontrar.
    """
    for produto in lista:
        if produto["codigo"] == codigo:
            return produto
    return None


def verificar_estoque(produto):
    """Retorna a situação do estoque do produto recebido como parâmetro."""
    if produto["quantidade"] == 0:
        return "Sem estoque"
    elif produto["quantidade"] <= produto["minimo"]:
        return "Estoque baixo"
    else:
        return "Estoque adequado"


def cadastrar_produto(lista):
    """Cadastra um novo produto na lista recebida, aplicando as regras de negócio."""
    print("\n--- CADASTRO DE PRODUTO ---")
    codigo = ler_inteiro("Código do produto: ")
    if buscar_produto(lista, codigo) is not None:
        print("Erro: já existe um produto com esse código. Cadastro cancelado.")
        return

    produto = {
        "codigo": codigo,
        "nome": ler_texto("Nome do produto: "),
        "categoria": ler_texto("Categoria: "),
        "preco": ler_preco("Preço unitário de venda: "),
        "quantidade": ler_inteiro_minimo("Quantidade inicial em estoque: ", 0),
        "minimo": ler_inteiro_minimo("Quantidade mínima desejada: ", 0),
        "vendidos": 0,      # contador de unidades vendidas começa em zero
    }
    lista.append(produto)
    print(f"Produto '{produto['nome']}' cadastrado com sucesso!")


def listar_produtos(lista):
    """Exibe todos os produtos da lista em forma de tabela."""
    if len(lista) == 0:
        print("Nenhum produto cadastrado.")
        return
    print(f"\n{'Código':<8}{'Nome':<22}{'Categoria':<16}{'Preço':>13}"
          f"{'Qtd':>6}{'Mín':>6}  Situação")
    print("-" * 90)
    for p in lista:
        print(f"{p['codigo']:<8}{p['nome'][:21]:<22}{p['categoria'][:15]:<16}"
              f"{formatar_moeda(p['preco']):>13}{p['quantidade']:>6}"
              f"{p['minimo']:>6}  {verificar_estoque(p)}")


def consultar_produto(lista):
    """Pede um código e mostra todas as informações do produto."""
    codigo = ler_inteiro("Código do produto: ")
    produto = buscar_produto(lista, codigo)
    if produto is None:
        print("Produto não encontrado.")
        return
    exibir_ficha(produto)


def exibir_ficha(p):
    """Mostra a ficha completa de um produto (reutilizada em vários pontos)."""
    print(LINHA)
    print("CONSULTA DE PRODUTO")
    print(LINHA)
    print(f"Código: {p['codigo']}")
    print(f"Produto: {p['nome']}")
    print(f"Categoria: {p['categoria']}")
    print(f"Preço unitário: {formatar_moeda(p['preco'])}")
    print(f"Quantidade atual: {p['quantidade']}")
    print(f"Estoque mínimo: {p['minimo']}")
    print(f"Situação: {verificar_estoque(p).upper()}")
    print(f"Unidades vendidas: {p['vendidos']}")
    print(LINHA)


def registrar_entrada(lista):
    """Adiciona unidades ao estoque de um produto existente."""
    codigo = ler_inteiro("Código do produto: ")
    produto = buscar_produto(lista, codigo)
    if produto is None:
        print("Erro: produto não encontrado.")
        return
    quantidade = ler_inteiro("Quantidade recebida: ")
    if quantidade <= 0:
        print("Erro: a quantidade deve ser um inteiro positivo. Operação rejeitada.")
        return
    anterior = produto["quantidade"]
    produto["quantidade"] = anterior + quantidade
    print(f"Quantidade anterior: {anterior}")
    print(f"Quantidade adicionada: {quantidade}")
    print(f"Novo saldo disponível: {produto['quantidade']}")


def ler_periodo():
    """Pede o período da venda (1 a 4) e retorna o índice da coluna (0 a 3)."""
    print("Períodos: 1-Manhã  2-Tarde  3-Noite  4-Madrugada")
    periodo = ler_inteiro("Período da venda: ")
    while periodo < 1 or periodo > 4:
        print("Erro: escolha um período entre 1 e 4.")
        periodo = ler_inteiro("Período da venda: ")
    return periodo - 1


def registrar_venda(lista):
    """Processa a venda de um produto e atualiza estoque e totalizadores globais."""
    global faturamento_total, total_operacoes, total_unidades_vendidas

    codigo = ler_inteiro("Código do produto: ")
    produto = buscar_produto(lista, codigo)
    if produto is None:
        print("Erro: produto não encontrado. Venda não realizada.")
        return
    quantidade = ler_inteiro("Quantidade a vender: ")
    if quantidade <= 0:
        print("Erro: a quantidade deve ser um inteiro positivo.")
        return
    if quantidade > produto["quantidade"]:
        print(f"Erro: estoque insuficiente (disponível: {produto['quantidade']}).")
        return
    periodo = ler_periodo()

    valor = produto["preco"] * quantidade          # regra 4
    produto["quantidade"] -= quantidade            # regra 5
    produto["vendidos"] += quantidade
    faturamento_total += valor                     # regra 6
    total_unidades_vendidas += quantidade          # regra 7
    total_operacoes += 1                           # regra 8

    # Guarda a operação no histórico (usado pela matriz, estatísticas e ranking)
    vendas.append({
        "codigo": produto["codigo"], "nome": produto["nome"],
        "categoria": produto["categoria"], "quantidade": quantidade,
        "preco": produto["preco"], "valor": valor, "periodo": periodo,
    })

    print(LINHA)
    print("VENDA REALIZADA")
    print(LINHA)
    print(f"Produto: {produto['nome']}")
    print(f"Quantidade: {quantidade}")
    print(f"Preço unitário: {formatar_moeda(produto['preco'])}")
    print(f"Valor total: {formatar_moeda(valor)}")
    print(f"Período: {PERIODOS[periodo]}")
    print(f"Estoque restante: {produto['quantidade']}")
    print(LINHA)


def produtos_em_alerta(lista):
    """Retorna uma nova lista com os produtos cuja quantidade é <= ao mínimo."""
    alerta = []
    for p in lista:
        if p["quantidade"] <= p["minimo"]:
            alerta.append(p)
    return alerta


def listar_estoque_baixo(lista):
    """Exibe os produtos em situação de alerta de estoque."""
    alerta = produtos_em_alerta(lista)
    if len(alerta) == 0:
        print("Não existem produtos em situação de alerta.")
        return
    print(f"\n{'Código':<8}{'Nome':<22}{'Qtd':>6}{'Mín':>6}  Situação")
    print("-" * 60)
    for p in alerta:
        print(f"{p['codigo']:<8}{p['nome'][:21]:<22}{p['quantidade']:>6}"
              f"{p['minimo']:>6}  {verificar_estoque(p)}")


def calcular_ticket_medio(faturamento, operacoes):
    """Retorna faturamento / operações, ou None se não houve vendas (evita divisão por zero)."""
    if operacoes == 0:
        return None
    return faturamento / operacoes


def resumo_vendas(lista):
    """Mostra os indicadores comerciais básicos (Requisito 08)."""
    print(LINHA)
    print("RESUMO DE VENDAS")
    print(LINHA)
    print(f"Total de produtos: {len(lista)}")
    print(f"Total de vendas: {total_operacoes}")
    print(f"Unidades vendidas: {total_unidades_vendidas}")
    print(f"Faturamento: {formatar_moeda(faturamento_total)}")
    ticket = calcular_ticket_medio(faturamento_total, total_operacoes)
    if ticket is None:
        print("Ticket médio: nenhuma venda realizada.")
    else:
        print(f"Ticket médio: {formatar_moeda(ticket)}")
    print(f"Produtos em alerta: {len(produtos_em_alerta(lista))}")
    print(LINHA)


# ==========================================================
# ETAPA 2
# ==========================================================

def alterar_produto(lista):
    """Permite alterar nome, categoria, preço ou estoque mínimo (código e quantidade não)."""
    codigo = ler_inteiro("Código do produto: ")
    produto = buscar_produto(lista, codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    opcao = ""
    while opcao != "0":
        print(f"\nAlterando: {produto['nome']} (código {produto['codigo']})")
        print("1 - Nome | 2 - Categoria | 3 - Preço | 4 - Estoque mínimo | 0 - Voltar")
        opcao = input("O que deseja alterar? ").strip()
        match opcao:
            case "1":
                produto["nome"] = ler_texto("Novo nome: ")
            case "2":
                produto["categoria"] = ler_texto("Nova categoria: ")
            case "3":
                produto["preco"] = ler_preco("Novo preço: ")
            case "4":
                produto["minimo"] = ler_inteiro_minimo("Novo estoque mínimo: ", 0)
            case "0":
                print("Alteração finalizada.")
            case _:
                print("Opção inválida.")
                continue
        if opcao != "0":
            print("Dado alterado com sucesso.")


def excluir_produto(lista):
    """Exclui um produto sem histórico de vendas, após confirmação."""
    codigo = ler_inteiro("Código do produto: ")
    produto = buscar_produto(lista, codigo)
    if produto is None:
        print("Produto não encontrado.")
        return
    if produto["vendidos"] > 0:
        print("Erro: produto possui histórico de vendas e não pode ser excluído.")
        return
    confirmacao = input(f"Confirma a exclusão de '{produto['nome']}'? (S/N): ").strip().upper()
    if confirmacao == "S":
        lista.remove(produto)
        print("Produto excluído.")
    else:
        print("Exclusão cancelada.")


def gerar_matriz_vendas(lista, historico):
    """
    Monta a matriz de vendas (listas aninhadas) a partir do histórico.
    Linha i = produto lista[i]; coluna j = período j (manhã, tarde, noite, madrugada).
    Retorna a matriz.
    """
    # cria uma linha [0, 0, 0, 0] para cada produto
    matriz = []
    for i in range(len(lista)):
        matriz.append([0, 0, 0, 0])

    # percorre o histórico e soma cada venda na célula [produto][período]
    for venda in historico:
        for i in range(len(lista)):
            if lista[i]["codigo"] == venda["codigo"]:
                matriz[i][venda["periodo"]] += venda["quantidade"]
    return matriz


def totais_por_periodo(matriz):
    """Soma cada coluna da matriz e retorna uma lista com 4 totais."""
    totais = [0, 0, 0, 0]
    for linha in matriz:
        for j in range(4):
            totais[j] += linha[j]
    return totais


def visualizar_matriz(lista):
    """Exibe a matriz de vendas com total por produto (linha) e por período (coluna)."""
    if len(lista) == 0:
        print("Nenhum produto cadastrado.")
        return
    matriz = gerar_matriz_vendas(lista, vendas)
    print(f"\n{'Código':<8}{'Produto':<20}", end="")
    for nome in PERIODOS:
        print(f"{nome:>11}", end="")
    print(f"{'Total':>9}")
    print("-" * 81)
    for i in range(len(lista)):
        print(f"{lista[i]['codigo']:<8}{lista[i]['nome'][:19]:<20}", end="")
        for j in range(4):
            print(f"{matriz[i][j]:>11}", end="")
        print(f"{sum(matriz[i]):>9}")          # total do produto = soma da linha
    print("-" * 81)
    totais = totais_por_periodo(matriz)
    print(f"{'TOTAL POR PERÍODO':<28}", end="")
    for t in totais:
        print(f"{t:>11}", end="")
    print(f"{sum(totais):>9}")


def faturamento_do_produto(codigo):
    """Soma o valor de todas as vendas de um produto (a partir do histórico)."""
    total = 0.0
    for venda in vendas:
        if venda["codigo"] == codigo:
            total += venda["valor"]
    return total


def produto_mais_vendido(lista):
    """Retorna o produto com mais unidades vendidas (empate: ordem alfabética) ou None."""
    melhor = None
    for p in lista:
        if p["vendidos"] > 0:
            if (melhor is None or p["vendidos"] > melhor["vendidos"] or
                    (p["vendidos"] == melhor["vendidos"] and p["nome"].lower() < melhor["nome"].lower())):
                melhor = p
    return melhor


def produto_menos_vendido(lista):
    """Retorna o produto com menos unidades vendidas, entre os que venderam (empate: alfabética)."""
    pior = None
    for p in lista:
        if p["vendidos"] > 0:
            if (pior is None or p["vendidos"] < pior["vendidos"] or
                    (p["vendidos"] == pior["vendidos"] and p["nome"].lower() < pior["nome"].lower())):
                pior = p
    return pior


def calcular_valor_estoque(lista):
    """Valor estimado do estoque (versão com laço): soma de preço x quantidade."""
    total = 0.0
    for p in lista:
        total += p["preco"] * p["quantidade"]
    return total


def analise_estatistica(lista):
    """Exibe os indicadores estatísticos do Requisito 11."""
    print(LINHA)
    print("ANÁLISE ESTATÍSTICA DE VENDAS")
    print(LINHA)
    if len(lista) == 0:
        print("Nenhum produto cadastrado.")
        print(LINHA)
        return
    print(f"Faturamento total: {formatar_moeda(faturamento_total)}")
    print(f"Total de unidades vendidas: {total_unidades_vendidas}")
    print(f"Valor do estoque: {formatar_moeda(calcular_valor_estoque(lista))}")
    if len(vendas) == 0:
        print("Nenhuma venda registrada: demais indicadores indisponíveis.")
        print(LINHA)
        return

    print(f"Ticket médio: {formatar_moeda(calcular_ticket_medio(faturamento_total, total_operacoes))}")
    mais = produto_mais_vendido(lista)
    menos = produto_menos_vendido(lista)
    print(f"Produto mais vendido: {mais['nome']} ({mais['vendidos']} un.)")
    print(f"Produto menos vendido: {menos['nome']} ({menos['vendidos']} un.)")

    # maior e menor venda: percorre o histórico comparando os valores
    maior = vendas[0]
    menor = vendas[0]
    for venda in vendas:
        if venda["valor"] > maior["valor"]:
            maior = venda
        if venda["valor"] < menor["valor"]:
            menor = venda
    print(f"Maior venda: {formatar_moeda(maior['valor'])} ({maior['nome']}, {maior['quantidade']} un.)")
    print(f"Menor venda: {formatar_moeda(menor['valor'])} ({menor['nome']}, {menor['quantidade']} un.)")
    print(LINHA)


def vem_antes(a, b):
    """Critério do ranking: True se 'a' deve ficar antes de 'b'
    (mais unidades vendidas primeiro; empate -> nome em ordem alfabética)."""
    if a["vendidos"] != b["vendidos"]:
        return a["vendidos"] > b["vendidos"]
    return a["nome"].lower() < b["nome"].lower()


def ordenar_ranking(lista):
    """
    Ordenação por inserção (insertion sort) sobre uma CÓPIA da lista,
    para não alterar a ordem original do cadastro. Retorna a lista ordenada.
    """
    ordenada = lista.copy()
    for i in range(1, len(ordenada)):
        atual = ordenada[i]
        j = i - 1
        # empurra para a direita quem deve ficar depois do 'atual'
        while j >= 0 and vem_antes(atual, ordenada[j]):
            ordenada[j + 1] = ordenada[j]
            j -= 1
        ordenada[j + 1] = atual
    return ordenada


def ranking_produtos(lista):
    """Exibe o ranking dos produtos com pelo menos uma unidade vendida."""
    vendidos = []
    for p in lista:
        if p["vendidos"] > 0:
            vendidos.append(p)
    if len(vendidos) == 0:
        print("Nenhum produto vendido ainda.")
        return
    ranking = ordenar_ranking(vendidos)
    print(f"\n{'Pos':<5}{'Código':<8}{'Nome':<22}{'Categoria':<16}{'Vendidos':>9}{'Faturamento':>16}")
    print("-" * 76)
    posicao = 1
    for p in ranking:
        print(f"{posicao:<5}{p['codigo']:<8}{p['nome'][:21]:<22}{p['categoria'][:15]:<16}"
              f"{p['vendidos']:>9}{formatar_moeda(faturamento_do_produto(p['codigo'])):>16}")
        posicao += 1


def buscar_produto_recursivo(lista, codigo, indice):
    """
    Busca recursiva (Requisito 13) - sem for/while.
    Caso-base 1: índice chegou ao fim da lista -> retorna None.
    Caso-base 2: produto do índice atual tem o código -> retorna o produto.
    Passo recursivo: procura a partir do próximo índice.
    """
    if indice >= len(lista):
        return None
    if lista[indice]["codigo"] == codigo:
        return lista[indice]
    return buscar_produto_recursivo(lista, codigo, indice + 1)


def executar_busca_recursiva(lista):
    """Executa a busca recursiva e compara com a busca convencional."""
    codigo = ler_inteiro("Código a buscar: ")
    resultado_rec = buscar_produto_recursivo(lista, codigo, 0)
    resultado_conv = buscar_produto(lista, codigo)

    print(f"Busca recursiva:    {resultado_rec['nome'] if resultado_rec else None}")
    print(f"Busca convencional: {resultado_conv['nome'] if resultado_conv else None}")
    if resultado_rec is resultado_conv:
        print("As duas buscas retornaram o mesmo resultado.")
    else:
        print("Atenção: as buscas retornaram resultados diferentes!")
    if resultado_rec is not None:
        exibir_ficha(resultado_rec)


def calcular_valor_estoque_recursivo(lista, indice):
    """
    Soma recursiva de preço x quantidade (Requisito 14) - sem for/while.
    Caso-base: índice no fim da lista -> 0.
    Passo: valor do produto atual + resultado da chamada para o próximo índice.
    """
    if indice >= len(lista):
        return 0
    produto = lista[indice]
    return produto["preco"] * produto["quantidade"] + calcular_valor_estoque_recursivo(lista, indice + 1)


def exibir_valor_estoque_recursivo(lista):
    """Mostra o valor do estoque calculado por recursão e confere com a versão com laço."""
    if len(lista) == 0:
        print("Nenhum produto cadastrado. Valor do estoque: R$ 0,00")
        return
    valor = calcular_valor_estoque_recursivo(lista, 0)
    print(f"Valor estimado do estoque (recursivo): {formatar_moeda(valor)}")
    print(f"Conferência (com laço):                {formatar_moeda(calcular_valor_estoque(lista))}")


def relatorio_consolidado(lista):
    """Gera o relatório gerencial consolidado (Requisito 15)."""
    print(LINHA)
    print("RELATÓRIO GERENCIAL CONSOLIDADO")
    print(LINHA)

    # categorias distintas e unidades disponíveis
    categorias = []
    unidades_disponiveis = 0
    for p in lista:
        if p["categoria"] not in categorias:
            categorias.append(p["categoria"])
        unidades_disponiveis += p["quantidade"]

    print(f"Produtos cadastrados: {len(lista)}")
    print(f"Categorias existentes: {len(categorias)}")
    print(f"Unidades disponíveis: {unidades_disponiveis}")
    print(f"Unidades vendidas: {total_unidades_vendidas}")
    print(f"Operações de venda: {total_operacoes}")
    print(f"Faturamento acumulado: {formatar_moeda(faturamento_total)}")
    ticket = calcular_ticket_medio(faturamento_total, total_operacoes)
    print(f"Ticket médio: {formatar_moeda(ticket) if ticket is not None else 'nenhuma venda realizada'}")
    print(f"Valor estimado do estoque: {formatar_moeda(calcular_valor_estoque_recursivo(lista, 0))}")
    print(f"Produtos em estoque baixo: {len(produtos_em_alerta(lista))}")

    if len(vendas) == 0:
        print("Sem vendas: indicadores de desempenho indisponíveis.")
        print(LINHA)
        return

    mais = produto_mais_vendido(lista)
    print(f"Produto mais vendido: {mais['nome']} ({mais['vendidos']} un.)")

    # produto com maior faturamento (empate: alfabética)
    melhor = None
    melhor_valor = 0.0
    for p in lista:
        valor = faturamento_do_produto(p["codigo"])
        if valor > 0 and (melhor is None or valor > melhor_valor or
                          (valor == melhor_valor and p["nome"].lower() < melhor["nome"].lower())):
            melhor = p
            melhor_valor = valor
    print(f"Produto com maior faturamento: {melhor['nome']} ({formatar_moeda(melhor_valor)})")

    # faturamento por categoria (dicionário categoria -> valor)
    por_categoria = {}
    for venda in vendas:
        por_categoria[venda["categoria"]] = por_categoria.get(venda["categoria"], 0.0) + venda["valor"]
    melhor_cat = None
    for cat in por_categoria:
        if (melhor_cat is None or por_categoria[cat] > por_categoria[melhor_cat] or
                (por_categoria[cat] == por_categoria[melhor_cat] and cat.lower() < melhor_cat.lower())):
            melhor_cat = cat
    print(f"Categoria com maior faturamento: {melhor_cat} ({formatar_moeda(por_categoria[melhor_cat])})")

    # período com mais unidades: usa '>' estrito, então no empate vence o primeiro (manhã, tarde...)
    totais = totais_por_periodo(gerar_matriz_vendas(lista, vendas))
    melhor_periodo = 0
    for j in range(1, 4):
        if totais[j] > totais[melhor_periodo]:
            melhor_periodo = j
    print(f"Período com mais unidades vendidas: {PERIODOS[melhor_periodo]} ({totais[melhor_periodo]} un.)")
    print(LINHA)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():
    """Laço principal: mostra o menu até o usuário escolher 0."""
    executando = True
    while executando:
        opcao = exibir_menu()
        match opcao:
            case "1":
                cadastrar_produto(produtos)
            case "2":
                listar_produtos(produtos)
            case "3":
                consultar_produto(produtos)
            case "4":
                registrar_entrada(produtos)
            case "5":
                registrar_venda(produtos)
            case "6":
                listar_estoque_baixo(produtos)
            case "7":
                resumo_vendas(produtos)
            case "8":
                alterar_produto(produtos)
            case "9":
                excluir_produto(produtos)
            case "10":
                visualizar_matriz(produtos)
            case "11":
                analise_estatistica(produtos)
            case "12":
                ranking_produtos(produtos)
            case "13":
                executar_busca_recursiva(produtos)
            case "14":
                exibir_valor_estoque_recursivo(produtos)
            case "15":
                relatorio_consolidado(produtos)
            case "0":
                print("Encerrando o StockPy. Até logo!")
                executando = False
            case _:
                print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
