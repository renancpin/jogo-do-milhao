import random

#variáveis globais:
tamanhoTela = 70
premioTotal = 1000000
pontuação = 100
pulosMax = 3
nQuest = 0
pontos = 0

def regras(inicio = True):
    if inicio:
        t = 'BOAS VINDAS AO JOGO DO MILHÃO!!!'
    else:
        t = '**** DA RULES ****'
    
    regras = 'Cada pergunta deste jogo tem quatro alternativas, e apenas uma é a correta.' \
             f'\nA cada resposta correta, você ganhará {pontuação} pontos. Ao errar uma pergunta, ' \
             'o jogo acaba e sua pontuação final será mostrada. '\
             '\n\nPorém, o jogador possui algumas *CHANCES* de evitar perder tudo: ' \
             '\n\n *** É possível PULAR para a próxima questão sem responder a questão atual, ' \
             'ao digitar \"pular\" (sem aspas) no lugar da resposta. Você terá *TRÊS CHANCES* de pular sem responder. ' \
             '\n *** É possível CONSULTAR as regras do jogo sempre que precisar, ' \
             'basta digitar \"ajuda\" (sem aspas) no lugar da resposta. ' \
             '\n *** É possível ENCERRAR o jogo a qualquer momento, digitando \"fim\" (sem aspas) no lugar da resposta. ' \
             'Nesse caso, sua pontuação final será mostrada mas você não ganhará nenhum prêmio.' \
             '\n\nAo final do jogo, seu PRÊMIO será calculado de acordo com sua pontuação, e você poderá entrar para o top 5! ' \
             f'Se conseguir responder todas as questões sem pular, você ganha 1 MILHÃO DE REAIS!!'

    print('')
    print('-'*tamanhoTela)
    print(f'{t}'.center(len(t)+4).center(tamanhoTela,'$'))
    print('-'*tamanhoTela)
    print('')
    print('-'*tamanhoTela)
    print('*'*tamanhoTela)
    
    #A função abaixo formata o texto a ser exibido dentro de um tamanho fixado para a tela
    print(ajustarTextoNaTela(regras))
    print('')
    print('*'*tamanhoTela)
    print('-'*tamanhoTela)
    
    
def ajustarTextoNaTela(texto):
    #A cada iteração, é identificado o espaço em branco
    #mais próximo e anterior ao limite da tela
    #então, é inserida uma quebra de linha no lugar deste espaço
    i = 0
    z = tamanhoTela
    while z < len(texto):
        while (texto.find(' ', i) <= z and texto.find(' ', i) != -1):
            if texto.find('\n', i) != -1 and (texto.find(' ', i) > texto.find('\n', i)):
                i = texto.find('\n', i) + 1
                break
            else:
                i = texto.find(' ', i) + 1
        texto = texto[:i-1] + '\n' + texto[i:]
        z = i + tamanhoTela
    return texto

def carregarPerguntas(arquivo):
    arq = open(arquivo,'r')
    linhas = arq.readlines()
    
    perguntas = []
    for i in range(0, len(linhas), 5):
        #   O arquivo .txt está disposto como segue:
        
        #   linhas[0] = "PERGUNTA 1";
        #   linhas[1] = "resposta A",
        #   linhas[2] = "resposta B",
        #   linhas[3] = "resposta C",
        #   linhas[4] = "resposta D"
        #   ...etc
        
        perguntas.append(  [ linhas[i] , linhas[i+1:i+5] ]  )
        
        #   cada pergunta fica em perguntas[i] e possui o seguinte formato:
        #       pergunta = ["Texto da pergunta?", alternativas]
        #       alternativas = ["a", "b", "c", "d"]
        
        #   portanto, o formato geral de perguntas é:
        #       perguntas = [ ["Pergunta 1?", ["a", "b", "c", "d"], ["Pergunta 2?", ["a", "b", "c", "d"], ..., ["Pergunta N?", ["a", "b", "c", "d"] ]

        #   cada pergunta fica em perguntas[i]
        #   o texto da pergunta fica em perguntas[i][0]
        #   a lista de itens  fica em perguntas[i][1]
        #   o texto de cada item, portanto, fica em perguntas[i][1][n]
        #   (obs:    i = número da pergunta;
        #            n = número do item (0 = a, 1 = b, ... etc.))
        
    embaralharTudo(perguntas)
    return perguntas


def embaralharTudo(perguntas):
    #mistura as perguntas entre si:
    random.shuffle(perguntas)
    
    for i in range(len(perguntas)):
        #mistura as alternativas dentro de cada pergunta:
        random.shuffle(perguntas[i][1])

    
def fazPergunta(perguntas, n):
    #Pega uma pergunta da lista que já estará embaralhada
    #o trecho "min(n, len(perguntas))" garante que a pergunta
    #solicitada esteja dentro dos limites da lista e evita erros
    pergunta = perguntas[min(n,len(perguntas))]
    
    #lembrando:
    #   pergunta = ["P: texto?", ['a','b','c','d']]
    
    #como as perguntas foram embaralhadas, é preciso numerá-las dinamicamente em cada chamada:
    texto = '\n' + pergunta[0].replace('P:', f'{n+1} -').strip()

    #assim como a ordem das alternativas:
    itens = ['a','b','c','d']
    itemCerto = -1

    #o item correto é sinalizado com um '*' no .txt
    #como foram embaralhadas, identificar dinamicamente a alternativa certa:
    for n in range(len(pergunta[1])):
        if pergunta[1][n].find('*') != -1:
            itemCerto = n
    
    #o loop irá testar a validade da resposta. se a resposta digitada não existir, perguntar se deseja tentar denovo:
    while True:
        #novamente, ajustando o texto para caber na tela:
        print(ajustarTextoNaTela(texto))
        for n in range(len(pergunta[1])):
            #e mostrar os itens, também organizando dinamicamente (e removendo o '*'):
            print(itens[n] + ') ' + pergunta[1][n].strip().replace('*',''))

        escolha = input('\nQual a resposta correta? ').lower().strip()
        if escolha in itens:
            if itens.index(escolha) == itemCerto:
                return pontuação
            else:
                return 0
        else:
            if escolha == 'pular':
                return -2
            elif escolha == 'fim':
                return -1
            elif escolha == 'ajuda':
                regras(False)
            else:
                if input('\nEscolha inválida!\nVocê deve digitar o item desejado, entre \'a\',\'b\',\'c\' ' \
                         'e \'d\'\n\nDeseja tentar novamente? [S/N]: ').strip().upper() != 'S':
                    return -1
    
def jogo(perguntas):
    #parâmetros do jogo:
    qAtual = 0
    global pontos
    pontos = 0
    pulos = pulosMax
    
    #embaralhar = True se quiser que embaralhe tudo novamente quando errar uma pergunta e recomeçar o jogo:
    embaralhar = True

    #função para mostrar o placar
    def mostrarPontuação(final = False):
        print('-' * tamanhoTela)
        print(f'{int(pontos)} pontos'.center(46).center(tamanhoTela,'$'))
        if final:
            if pulos < pulosMax:
                t = f'Você usou {pulosMax-pulos} pulo(s), e perdeu {int(pontuação/4 * (pulosMax-pulos))} pontos!'
            else:
                t = 'Você não usou nenhum pulo!'
        else:
            if pulos > 0:
                t = f'Você possui {pulos} pulo(s). Tome cuidado!'
            else:
                t = 'Você NÃO POSSUI mais pulos. Tome cuidado!!'
        print(t.center(46).center(tamanhoTela,'*'))
        print('-'*tamanhoTela)
    
    while qAtual < nQuest:
        acerto = fazPergunta(perguntas,qAtual)

        #pulou a pergunta:
        if acerto == -2:
            if pulos > 0:
                pulos -= 1
                pontos -= int(pontuação/4)
                qAtual += 1
                print('\n' + f'VOCÊ PULOU A PERGUNTA e perdeu {int(pontuação/4)} pontos!'.center(tamanhoTela))
                mostrarPontuação()
            else:
                print('\n' + 'VOCÊ NÃO PODE MAIS PULAR!! Responda à pergunta!'.center(tamanhoTela))
                
        #acertou a pergunta:
        elif acerto == pontuação:
            pontos += pontuação
            qAtual += 1
            print('\n' + 'CERTA RESPOSTA!'.center(tamanhoTela))
            
            #verificar se atingiu o fim das questões
            if pontos == pontuação * (nQuest - (pulosMax-pulos)/4):
                mostrarPontuação(True)
                #se não usou nenhum pulo, então ganhou o prêmio máximo
                if pulos == pulosMax:
                    print('')
                    for i in open('premio.txt','r').readlines():
                        x = i.strip()
                        print(x.center(tamanhoTela))
                #se usou, o prêmio será descontado
                else:
                    print('')
                    print('*'*tamanhoTela)
                    print('PARABÉNS, VOCÊ CONSEGUIU TERMINAR!'.center(50).center(tamanhoTela, '$'))
                    print('Mas usou alguns pulos...'.center(50).center(tamanhoTela, '*'))
                    print(f'Portanto terminou com {int(premioTotal*(pontos/(pontuação*nQuest)))} reais!'.center(50).center(tamanhoTela, '$'))
                    print('*'*tamanhoTela)
                return 0
            else:
                mostrarPontuação()
                
        #errou ou pediu para encerrar o jogo:
        else:
            #errou a pergunta:
            if acerto == 0:
                print('\n' + 'VOCÊ ERROU!!'.center(tamanhoTela))
            #pediu para encerrar o jogo
            else:
                print('\n' + 'VOCÊ ENCERROU O JOGO!'.center(tamanhoTela))
            mostrarPontuação(True)
            return 0

    #se o loop alcançar aqui, algo está errado    
    return -1

def highScore(pontos = 0, nome = ''):
    #criar o arquivo se não existir, depois abrir em modo leitura E escrita:
    open('highscore.txt','a+').close()
    arq = open('highscore.txt','r+')
    saida = []

    #padronizar as linhas
    for i in arq.readlines():
        if i.strip() != '':
            saida.append(i.strip())
    
    if pontos > 0 and nome != '':
        for i in range(0, len(saida), 2):
            if pontos >= int(saida[i]):
                saida.insert(i, str(pontos))
                saida.insert(i+1, nome)
                break
        
        if len(saida) < 10:
            if not (str(pontos) in saida):
                saida.append(str(pontos))
                saida.append(nome)

    #manter apenas os 5 primeiros no arquivo
    while len(saida) > 10:
        saida.pop()

    print('\n' + '$' * tamanhoTela)
    print('\n' + '-' * tamanhoTela)
    print('HIGHSCORE'.center(30).center(tamanhoTela,'*'))
    print('-' * tamanhoTela)
    for i in range(0, len(saida), 2):
        print('\n' + ' ' * 25 + f'{int(i/2)+1}º Lugar:   {saida[i+1]}'.ljust(tamanhoTela-25))
        print(' ' * 25 + f'Pontuação:  {saida[i]}'.ljust(tamanhoTela-25))
    print('\n' + '-' * tamanhoTela)
    print('Fim de jogo!! Até logo!'.center(30).center(tamanhoTela, '*'))
    print('-' * tamanhoTela)
     
    for i in range(len(saida)):
        saida[i] += '\n'

    #salvar de volta no arquivo
    arq.truncate(0)
    arq.seek(0)
    arq.writelines(saida)
    arq.close()

def main():
    #carregar perguntas:
    perguntas = carregarPerguntas('perguntas.txt')
    
    #definir o número de perguntas a ser feito.
    #use nQuest = len(perguntas) para usar todas as perguntas do arquivo:
    global nQuest
    nQuest = 10 #len(perguntas)

    #perguntar se deseja iniciar o jogo:
    while True:
        regras()
        
        #ler o nome do usuário:
        nome = input('\nDigite o seu nome: ')
        print('\n' + '*'*(16+len(nome)))
        print(f'Bem vindo(a), {nome}!')
        print('*'*(16+len(nome)) + '\n')
        
        if input('Você está preparado para começar? [S/N]: ').strip().upper() == 'S':
            print('-'*tamanhoTela)
            result = 1
            while result != 0:
                if result == -1:
                    print('Algo deu errado!')
                    break
                else:
                    result = jogo(perguntas)
                    highScore(pontos,nome)
                    if input('\nDeseja jogar novamente? [S/N]: ').strip().upper() == 'S':
                        print('\n' + '-' * tamanhoTela)
                        print('Iniciando um novo jogo...'.center(30).center(tamanhoTela, '*'))
                        print('-' * tamanhoTela + '\n')
                        result = 1
                    else:
                        print('\n' + '-' * tamanhoTela)
                        print('Obrigado por jogar!'.center(30).center(tamanhoTela, '*'))
                        print('-' * tamanhoTela + '\n')
                    break
        else:
            if input('Você tem certeza disso? [S/N]: ').strip().upper() == 'S':
                print('\n' + '-' * tamanhoTela)
                print('Tudo bem!! Até mais!'.center(30).center(tamanhoTela, '*'))
                print('-' * tamanhoTela)
                break
            else:
                print('-'*tamanhoTela)
        
if __name__=='__main__':
    main()
