algoritmo "LogiFast"
// Disciplina   : [Algoritmos e Programação] 
// Professor   : Andre Olimpio
// ============================================================
// LogiFast - Sistema Inteligente de Gerenciamento de Entregas
// Desafio 1 - Algoritmos e Programacao (UNIVAP)
//
// FLUXO: Problema -> Analise -> Estruturas de dados -> Algoritmo
//        -> Modularizacao -> Validacao -> Testes -> Resultado
//
// ESCOPO:
//  - GLOBAIS: entregas, qtdEntregas, matriz, percurso, qtdPercurso,
//    contRegiao. Sao dados compartilhados por varias sub-rotinas e o
//    VisuAlg nao permite passar vetores/matrizes como parametro.
//  - LOCAIS: contadores, acumuladores, indices e leituras temporarias
//    (i, j, soma, cod...). Existem so dentro da sub-rotina que os usa.
//  - PARAMETROS: valores simples (codigo, posicao, distancia, peso...)
//    sao passados por valor, pois a sub-rotina apenas os consulta.
//
// OBS: os tamanhos dos vetores/matriz nas declaracoes sao literais
// (30, 5, 10) porque o VisuAlg nao aceita constantes ali. Devem
// coincidir com MAX_ENTREGAS, MAX_REGIOES e MAX_PERCURSO.
// ============================================================

const
   // capacidades do sistema
   MAX_ENTREGAS = 30
   MAX_REGIOES = 5
   MAX_PERCURSO = 10
   // prioridades
   URGENTE = 1
   PRIORITARIA = 2
   NORMAL = 3
   // status
   AGUARDANDO = 1
   EM_TRANSPORTE = 2
   ENTREGUE = 3
   // custo
   VALOR_KM = 2.50
   PESO_LIM_1 = 5
   PESO_LIM_2 = 20
   PESO_LIM_3 = 50
   ACRESC_PESO_2 = 0.10
   ACRESC_PESO_3 = 0.20
   ACRESC_PESO_4 = 0.35
   ACRESC_PRIORITARIA = 0.15
   ACRESC_URGENTE = 0.30
   // menu
   OPCAO_SAIR = 10

tipo
   Entrega = registro
      codigo: inteiro
      destinatario: caractere
      origem: inteiro
      destino: inteiro
      peso: real
      valorMercadoria: real
      prioridade: inteiro
      distancia: inteiro
      status: inteiro
      custo: real
   fimregistro

var
   // ---------- variaveis globais ----------
   entregas: vetor[1..30] de Entrega
   qtdEntregas: inteiro
   matriz: vetor[1..5,1..5] de inteiro
   nomeRegiao: vetor[1..5] de caractere
   percurso: vetor[1..10] de inteiro
   qtdPercurso: inteiro
   contRegiao: vetor[1..5] de inteiro
   opcao: inteiro

// ============================================================
// INICIALIZACAO
// ============================================================
procedimento inicializarMatriz
inicio
   nomeRegiao[1] <- "Centro"
   nomeRegiao[2] <- "Norte"
   nomeRegiao[3] <- "Sul"
   nomeRegiao[4] <- "Leste"
   nomeRegiao[5] <- "Oeste"

   matriz[1,1] <- 0
   matriz[1,2] <- 12
   matriz[1,3] <- 15
   matriz[1,4] <- 10
   matriz[1,5] <- 14

   matriz[2,1] <- 12
   matriz[2,2] <- 0
   matriz[2,3] <- 25
   matriz[2,4] <- 18
   matriz[2,5] <- 20

   matriz[3,1] <- 15
   matriz[3,2] <- 25
   matriz[3,3] <- 0
   matriz[3,4] <- 16
   matriz[3,5] <- 19

   matriz[4,1] <- 10
   matriz[4,2] <- 18
   matriz[4,3] <- 16
   matriz[4,4] <- 0
   matriz[4,5] <- 22

   matriz[5,1] <- 14
   matriz[5,2] <- 20
   matriz[5,3] <- 19
   matriz[5,4] <- 22
   matriz[5,5] <- 0
fimprocedimento

// ============================================================
// FUNCOES AUXILIARES DE TEXTO
// ============================================================
funcao textoPrioridade(p: inteiro): caractere
var
   t: caractere
inicio
   se p = URGENTE entao
      t <- "Urgente"
   senao
      se p = PRIORITARIA entao
         t <- "Prioritaria"
      senao
         t <- "Normal"
      fimse
   fimse
   retorne t
fimfuncao

funcao textoStatus(s: inteiro): caractere
var
   t: caractere
inicio
   se s = AGUARDANDO entao
      t <- "Aguardando"
   senao
      se s = EM_TRANSPORTE entao
         t <- "Em transporte"
      senao
         t <- "Entregue"
      fimse
   fimse
   retorne t
fimfuncao

procedimento mostrarRegioes
var
   i: inteiro
inicio
   para i de 1 ate MAX_REGIOES faca
      escreval("   ", i, " - ", nomeRegiao[i])
   fimpara
fimprocedimento

// ============================================================
// REGRAS DE NEGOCIO
// ============================================================

// Calcula o custo: base (distancia x valor/km) + acrescimos de peso e prioridade
funcao calcularCusto(dist: inteiro; pesoCarga: real; prio: inteiro): real
var
   custoBase, acrescPeso, acrescPrio: real
inicio
   custoBase <- dist * VALOR_KM

   se pesoCarga <= PESO_LIM_1 entao
      acrescPeso <- 0
   senao
      se (pesoCarga > PESO_LIM_1) e (pesoCarga <= PESO_LIM_2) entao
         acrescPeso <- ACRESC_PESO_2
      senao
         se (pesoCarga > PESO_LIM_2) e (pesoCarga <= PESO_LIM_3) entao
            acrescPeso <- ACRESC_PESO_3
         senao
            acrescPeso <- ACRESC_PESO_4
         fimse
      fimse
   fimse

   se prio = URGENTE entao
      acrescPrio <- ACRESC_URGENTE
   senao
      se prio = PRIORITARIA entao
         acrescPrio <- ACRESC_PRIORITARIA
      senao
         acrescPrio <- 0
      fimse
   fimse

   // acrescimos calculados sobre o custo-base e somados a ele
   retorne custoBase + (custoBase * acrescPeso) + (custoBase * acrescPrio)
fimfuncao

// Busca linear pelo codigo. Retorna a posicao no vetor ou 0 se nao achar.
funcao localizarEntrega(cod: inteiro): inteiro
var
   i, indice: inteiro
inicio
   indice <- 0
   i <- 1
   enquanto (i <= qtdEntregas) e (indice = 0) faca
      se entregas[i].codigo = cod entao
         indice <- i
      fimse
      i <- i + 1
   fimenquanto
   retorne indice
fimfuncao

// Sequencia obrigatoria: AGUARDANDO -> EM_TRANSPORTE -> ENTREGUE
funcao transicaoValida(atual: inteiro; novo: inteiro): logico
inicio
   retorne ((atual = AGUARDANDO) e (novo = EM_TRANSPORTE)) ou ((atual = EM_TRANSPORTE) e (novo = ENTREGUE))
fimfuncao

// ============================================================
// SAIDA
// ============================================================
procedimento exibirEntrega(indice: inteiro)
inicio
   escreval("----------------------------------------")
   escreval("Codigo       : ", entregas[indice].codigo)
   escreval("Destinatario : ", entregas[indice].destinatario)
   escreval("Origem       : ", nomeRegiao[entregas[indice].origem])
   escreval("Destino      : ", nomeRegiao[entregas[indice].destino])
   escreval("Peso (kg)    : ", entregas[indice].peso:8:2)
   escreval("Valor (R$)   : ", entregas[indice].valorMercadoria:10:2)
   escreval("Prioridade   : ", textoPrioridade(entregas[indice].prioridade))
   escreval("Distancia(km): ", entregas[indice].distancia)
   escreval("Status       : ", textoStatus(entregas[indice].status))
   escreval("Custo (R$)   : ", entregas[indice].custo:10:2)
fimprocedimento

procedimento listarEntregas
var
   i: inteiro
inicio
   se qtdEntregas = 0 entao
      escreval("Nenhuma entrega cadastrada.")
   senao
      para i de 1 ate qtdEntregas faca
         exibirEntrega(i)
      fimpara
   fimse
fimprocedimento

// ============================================================
// CADASTRO (entrada -> validacao -> processamento)
// ============================================================
procedimento cadastrarEntrega
var
   cod, orig, dest, prio: inteiro
   nome: caractere
   pesoCarga, valor: real
   valido: logico
inicio
   se qtdEntregas >= MAX_ENTREGAS entao
      escreval("ERRO: capacidade maxima de ", MAX_ENTREGAS, " entregas atingida.")
   senao
      // ----- entrada -----
      escreva("Codigo da entrega: ")
      leia(cod)
      escreva("Destinatario: ")
      leia(nome)
      escreval("Regioes disponiveis:")
      mostrarRegioes
      escreva("Regiao de origem (codigo): ")
      leia(orig)
      escreva("Regiao de destino (codigo): ")
      leia(dest)
      escreva("Peso da carga (kg): ")
      leia(pesoCarga)
      escreva("Valor da mercadoria (R$): ")
      leia(valor)
      escreval("Prioridade: 1-Urgente  2-Prioritaria  3-Normal")
      escreva("Prioridade: ")
      leia(prio)

      // ----- validacao (mostra o primeiro problema encontrado) -----
      valido <- verdadeiro
      se cod <= 0 entao
         escreval("ERRO: o codigo deve ser maior que zero.")
         valido <- falso
      fimse
      se valido e (localizarEntrega(cod) <> 0) entao
         escreval("ERRO: codigo duplicado. Ja existe entrega com o codigo ", cod, ".")
         valido <- falso
      fimse
      se valido e ((orig < 1) ou (orig > MAX_REGIOES)) entao
         escreval("ERRO: regiao de origem inexistente.")
         valido <- falso
      fimse
      se valido e ((dest < 1) ou (dest > MAX_REGIOES)) entao
         escreval("ERRO: regiao de destino inexistente.")
         valido <- falso
      fimse
      se valido e (orig = dest) entao
         escreval("ERRO: origem e destino nao podem ser iguais.")
         valido <- falso
      fimse
      se valido e (pesoCarga <= 0) entao
         escreval("ERRO: peso invalido. Deve ser maior que zero.")
         valido <- falso
      fimse
      se valido e (valor < 0) entao
         escreval("ERRO: valor da mercadoria nao pode ser negativo.")
         valido <- falso
      fimse
      se valido e ((prio < URGENTE) ou (prio > NORMAL)) entao
         escreval("ERRO: prioridade inexistente (use 1, 2 ou 3).")
         valido <- falso
      fimse

      // ----- processamento -----
      se valido entao
         qtdEntregas <- qtdEntregas + 1
         entregas[qtdEntregas].codigo <- cod
         entregas[qtdEntregas].destinatario <- nome
         entregas[qtdEntregas].origem <- orig
         entregas[qtdEntregas].destino <- dest
         entregas[qtdEntregas].peso <- pesoCarga
         entregas[qtdEntregas].valorMercadoria <- valor
         entregas[qtdEntregas].prioridade <- prio
         entregas[qtdEntregas].distancia <- matriz[orig,dest]
         entregas[qtdEntregas].status <- AGUARDANDO
         entregas[qtdEntregas].custo <- calcularCusto(matriz[orig,dest], pesoCarga, prio)
         escreval("Entrega cadastrada com sucesso!")
         escreval("Distancia: ", entregas[qtdEntregas].distancia, " km | Custo estimado: R$ ", entregas[qtdEntregas].custo:8:2)
      fimse
   fimse
fimprocedimento

procedimento consultarEntrega
var
   cod, indice: inteiro
inicio
   escreva("Codigo da entrega: ")
   leia(cod)
   indice <- localizarEntrega(cod)
   se indice = 0 entao
      escreval("Entrega nao encontrada.")
   senao
      exibirEntrega(indice)
   fimse
fimprocedimento

// ============================================================
// ORDENACAO (Bubble Sort com 4 criterios)
// ============================================================

// Retorna verdadeiro se a entrega da posicao a deve vir ANTES da posicao b:
// 1) menor numero de prioridade (1 = urgente); 2) maior valor;
// 3) maior peso; 4) menor codigo.
funcao precede(a: inteiro; b: inteiro): logico
var
   resp: logico
inicio
   se entregas[a].prioridade <> entregas[b].prioridade entao
      resp <- entregas[a].prioridade < entregas[b].prioridade
   senao
      se entregas[a].valorMercadoria <> entregas[b].valorMercadoria entao
         resp <- entregas[a].valorMercadoria > entregas[b].valorMercadoria
      senao
         se entregas[a].peso <> entregas[b].peso entao
            resp <- entregas[a].peso > entregas[b].peso
         senao
            resp <- entregas[a].codigo < entregas[b].codigo
         fimse
      fimse
   fimse
   retorne resp
fimfuncao

// Troca dois registros campo a campo
procedimento trocarEntregas(a: inteiro; b: inteiro)
var
   auxCod, auxOrig, auxDest, auxPrio, auxDist, auxStatus: inteiro
   auxNome: caractere
   auxPeso, auxValor, auxCusto: real
inicio
   auxCod <- entregas[a].codigo
   auxNome <- entregas[a].destinatario
   auxOrig <- entregas[a].origem
   auxDest <- entregas[a].destino
   auxPeso <- entregas[a].peso
   auxValor <- entregas[a].valorMercadoria
   auxPrio <- entregas[a].prioridade
   auxDist <- entregas[a].distancia
   auxStatus <- entregas[a].status
   auxCusto <- entregas[a].custo

   entregas[a].codigo <- entregas[b].codigo
   entregas[a].destinatario <- entregas[b].destinatario
   entregas[a].origem <- entregas[b].origem
   entregas[a].destino <- entregas[b].destino
   entregas[a].peso <- entregas[b].peso
   entregas[a].valorMercadoria <- entregas[b].valorMercadoria
   entregas[a].prioridade <- entregas[b].prioridade
   entregas[a].distancia <- entregas[b].distancia
   entregas[a].status <- entregas[b].status
   entregas[a].custo <- entregas[b].custo

   entregas[b].codigo <- auxCod
   entregas[b].destinatario <- auxNome
   entregas[b].origem <- auxOrig
   entregas[b].destino <- auxDest
   entregas[b].peso <- auxPeso
   entregas[b].valorMercadoria <- auxValor
   entregas[b].prioridade <- auxPrio
   entregas[b].distancia <- auxDist
   entregas[b].status <- auxStatus
   entregas[b].custo <- auxCusto
fimprocedimento

procedimento ordenarEntregas
var
   i, j: inteiro
inicio
   para i de 1 ate qtdEntregas - 1 faca
      para j de 1 ate qtdEntregas - i faca
         se precede(j + 1, j) entao
            trocarEntregas(j, j + 1)
         fimse
      fimpara
   fimpara
fimprocedimento

procedimento exibirFilaDespacho
var
   i, posicao: inteiro
inicio
   ordenarEntregas
   posicao <- 0
   escreval("=== FILA DE DESPACHO (entregas aguardando) ===")
   para i de 1 ate qtdEntregas faca
      se entregas[i].status = AGUARDANDO entao
         posicao <- posicao + 1
         escreval(posicao, "o | Cod ", entregas[i].codigo, " | ", textoPrioridade(entregas[i].prioridade), " | Valor R$ ", entregas[i].valorMercadoria:9:2, " | Peso ", entregas[i].peso:6:2, " kg | ", nomeRegiao[entregas[i].origem], " -> ", nomeRegiao[entregas[i].destino])
      fimse
   fimpara
   se posicao = 0 entao
      escreval("Nenhuma entrega aguardando transporte.")
   fimse
fimprocedimento

// ============================================================
// ALTERACAO DE STATUS
// ============================================================
procedimento iniciarTransporte
var
   cod, indice: inteiro
inicio
   escreva("Codigo da entrega: ")
   leia(cod)
   indice <- localizarEntrega(cod)
   se indice = 0 entao
      escreval("Entrega nao encontrada.")
   senao
      se entregas[indice].status = ENTREGUE entao
         escreval("ERRO: entrega ja concluida, nao pode ser modificada.")
      senao
         se entregas[indice].status = EM_TRANSPORTE entao
            escreval("ERRO: entrega ja foi enviada (esta em transporte).")
         senao
            se transicaoValida(entregas[indice].status, EM_TRANSPORTE) entao
               entregas[indice].status <- EM_TRANSPORTE
               escreval("Transporte iniciado para a entrega ", cod, ".")
            fimse
         fimse
      fimse
   fimse
fimprocedimento

procedimento finalizarEntrega
var
   cod, indice: inteiro
inicio
   escreva("Codigo da entrega: ")
   leia(cod)
   indice <- localizarEntrega(cod)
   se indice = 0 entao
      escreval("Entrega nao encontrada.")
   senao
      se entregas[indice].status = ENTREGUE entao
         escreval("ERRO: entrega ja concluida, nao pode ser modificada.")
      senao
         se entregas[indice].status = AGUARDANDO entao
            escreval("ERRO: entrega ainda esta aguardando. Inicie o transporte antes de finalizar.")
         senao
            se transicaoValida(entregas[indice].status, ENTREGUE) entao
               entregas[indice].status <- ENTREGUE
               escreval("Entrega ", cod, " finalizada com sucesso.")
            fimse
         fimse
      fimse
   fimse
fimprocedimento

// ============================================================
// MATRIZ E ANALISE REGIONAL (lacos aninhados)
// ============================================================
procedimento analisarMatriz
var
   i, j, maior, menor, soma, cont: inteiro
   media: real
inicio
   escreval("=== MATRIZ DE DISTANCIAS (km) ===")
   escreva("          ")
   para j de 1 ate MAX_REGIOES faca
      escreva(nomeRegiao[j]:8)
   fimpara
   escreval("")

   maior <- matriz[1,2]
   menor <- matriz[1,2]
   soma <- 0
   cont <- 0
   para i de 1 ate MAX_REGIOES faca
      escreva(nomeRegiao[i]:10)
      para j de 1 ate MAX_REGIOES faca
         escreva(matriz[i,j]:8)
         se matriz[i,j] > maior entao
            maior <- matriz[i,j]
         fimse
         // a diagonal principal (i = j) e ignorada em menor e media
         se i <> j entao
            se matriz[i,j] < menor entao
               menor <- matriz[i,j]
            fimse
            soma <- soma + matriz[i,j]
            cont <- cont + 1
         fimse
      fimpara
      escreval("")
   fimpara

   media <- soma / cont
   escreval("Maior distancia existente     : ", maior, " km")
   escreval("Menor distancia (diferente 0) : ", menor, " km")
   escreval("Media das distancias          : ", media:6:2, " km")
fimprocedimento

// ============================================================
// ESTATISTICAS
// ============================================================
procedimento exibirEstatisticas
var
   i, cAguard, cTransp, cEntr, cUrg, cPrio, cNorm: inteiro
   iMaxValor, iMaxPeso, iMaxDist, regMax: inteiro
   somaPeso, somaValor, somaCusto: real
inicio
   se qtdEntregas = 0 entao
      escreval("Nenhuma entrega cadastrada para gerar estatisticas.")
   senao
      cAguard <- 0
      cTransp <- 0
      cEntr <- 0
      cUrg <- 0
      cPrio <- 0
      cNorm <- 0
      somaPeso <- 0
      somaValor <- 0
      somaCusto <- 0
      iMaxValor <- 1
      iMaxPeso <- 1
      iMaxDist <- 1
      para i de 1 ate MAX_REGIOES faca
         contRegiao[i] <- 0
      fimpara

      para i de 1 ate qtdEntregas faca
         // contagem por status
         se entregas[i].status = AGUARDANDO entao
            cAguard <- cAguard + 1
         senao
            se entregas[i].status = EM_TRANSPORTE entao
               cTransp <- cTransp + 1
            senao
               cEntr <- cEntr + 1
            fimse
         fimse
         // contagem por prioridade
         se entregas[i].prioridade = URGENTE entao
            cUrg <- cUrg + 1
         senao
            se entregas[i].prioridade = PRIORITARIA entao
               cPrio <- cPrio + 1
            senao
               cNorm <- cNorm + 1
            fimse
         fimse
         // acumuladores
         somaPeso <- somaPeso + entregas[i].peso
         somaValor <- somaValor + entregas[i].valorMercadoria
         somaCusto <- somaCusto + entregas[i].custo
         // maiores
         se entregas[i].valorMercadoria > entregas[iMaxValor].valorMercadoria entao
            iMaxValor <- i
         fimse
         se entregas[i].peso > entregas[iMaxPeso].peso entao
            iMaxPeso <- i
         fimse
         se entregas[i].distancia > entregas[iMaxDist].distancia entao
            iMaxDist <- i
         fimse
         // regiao de destino (quem recebeu a entrega)
         contRegiao[entregas[i].destino] <- contRegiao[entregas[i].destino] + 1
      fimpara

      regMax <- 1
      para i de 2 ate MAX_REGIOES faca
         se contRegiao[i] > contRegiao[regMax] entao
            regMax <- i
         fimse
      fimpara

      escreval("=== ESTATISTICAS ===")
      escreval("Total de entregas       : ", qtdEntregas)
      escreval("Aguardando              : ", cAguard)
      escreval("Em transporte           : ", cTransp)
      escreval("Entregues               : ", cEntr)
      escreval("Urgentes                : ", cUrg)
      escreval("Prioritarias            : ", cPrio)
      escreval("Normais                 : ", cNorm)
      escreval("Peso total (kg)         : ", somaPeso:10:2)
      escreval("Peso medio (kg)         : ", (somaPeso / qtdEntregas):10:2)
      escreval("Valor total (R$)        : ", somaValor:10:2)
      escreval("Valor medio (R$)        : ", (somaValor / qtdEntregas):10:2)
      escreval("Custo total (R$)        : ", somaCusto:10:2)
      escreval("Custo medio (R$)        : ", (somaCusto / qtdEntregas):10:2)
      escreval("Entrega de maior valor  : cod ", entregas[iMaxValor].codigo, " (R$ ", entregas[iMaxValor].valorMercadoria:8:2, ")")
      escreval("Entrega de maior peso   : cod ", entregas[iMaxPeso].codigo, " (", entregas[iMaxPeso].peso:6:2, " kg)")
      escreval("Entrega de maior dist.  : cod ", entregas[iMaxDist].codigo, " (", entregas[iMaxDist].distancia, " km)")
      escreval("Regiao que mais recebeu : ", nomeRegiao[regMax], " (", contRegiao[regMax], " entregas)")
   fimse
fimprocedimento

// ============================================================
// RECURSIVIDADE - DISTANCIA DE UM PERCURSO
// ============================================================
// distanciaTotal(indice) = dist(percurso[indice], percurso[indice+1]) + distanciaTotal(indice+1)
// CASO-BASE: indice >= qtdPercurso (ultima regiao, nao ha proximo trecho) -> 0
funcao distanciaTotal(indice: inteiro): inteiro
var
   resultado: inteiro
inicio
   se indice >= qtdPercurso entao
      resultado <- 0
   senao
      resultado <- matriz[percurso[indice], percurso[indice + 1]] + distanciaTotal(indice + 1)
   fimse
   retorne resultado
fimfuncao

procedimento calcularPercurso
var
   i, reg: inteiro
inicio
   repita
      escreva("Quantas regioes tem o percurso (2 a ", MAX_PERCURSO, ")? ")
      leia(qtdPercurso)
      se (qtdPercurso < 2) ou (qtdPercurso > MAX_PERCURSO) entao
         escreval("ERRO: informe um valor entre 2 e ", MAX_PERCURSO, ".")
      fimse
   ate (qtdPercurso >= 2) e (qtdPercurso <= MAX_PERCURSO)

   escreval("Regioes disponiveis:")
   mostrarRegioes
   para i de 1 ate qtdPercurso faca
      repita
         escreva("Regiao ", i, " do percurso (codigo): ")
         leia(reg)
         se (reg < 1) ou (reg > MAX_REGIOES) entao
            escreval("ERRO: regiao inexistente.")
         fimse
      ate (reg >= 1) e (reg <= MAX_REGIOES)
      percurso[i] <- reg
   fimpara

   escreva("Percurso: ")
   para i de 1 ate qtdPercurso faca
      escreva(nomeRegiao[percurso[i]])
      se i < qtdPercurso entao
         escreva(" -> ")
      fimse
   fimpara
   escreval("")
   escreval("Distancia total: ", distanciaTotal(1), " km")
fimprocedimento

// ============================================================
// PROGRAMA PRINCIPAL (apenas menu e chamadas)
// ============================================================
inicio
   qtdEntregas <- 0
   inicializarMatriz

   repita
      escreval("")
      escreval("LOGIFAST - SISTEMA DE GERENCIAMENTO DE ENTREGAS")
      escreval("1. Cadastrar entrega")
      escreval("2. Listar entregas")
      escreval("3. Consultar entrega")
      escreval("4. Exibir fila de despacho")
      escreval("5. Iniciar transporte")
      escreval("6. Finalizar entrega")
      escreval("7. Exibir matriz de distancias")
      escreval("8. Exibir estatisticas")
      escreval("9. Calcular percurso recursivamente")
      escreval("10. Encerrar sistema")
      escreva("Opcao: ")
      leia(opcao)
      escreval("")

      escolha opcao
         caso 1
            cadastrarEntrega
         caso 2
            listarEntregas
         caso 3
            consultarEntrega
         caso 4
            exibirFilaDespacho
         caso 5
            iniciarTransporte
         caso 6
            finalizarEntrega
         caso 7
            analisarMatriz
         caso 8
            exibirEstatisticas
         caso 9
            calcularPercurso
         caso 10
            escreval("Sistema encerrado.")
         outrocaso
            escreval("ERRO: opcao invalida. Escolha de 1 a 10.")
      fimescolha
   ate opcao = OPCAO_SAIR
fimalgoritmo
