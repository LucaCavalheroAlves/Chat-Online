import random
#Essa função retorna o mdc entre dois valores, usando o algoritmo de Euclides

#Porém antes de calcular o algoritmo de Euclides, é feito uma comparação entre os valores entrados para saber qual é o maior valor, coloquei a comparação caso no futuro queira colocar números aleatórios ae. mas acho que não vamos usar. 
def mdc(a,b): 
    maior = a
    menor = b
    menorcopia = menor

    while menor !=0:
        menor = maior % menor
        maior = menorcopia
        menorcopia = menor  
    return maior
    


# A função gera um número aleatório que seja acima de 1 e menor que o conjunto 'n' (que é o tamanho de conjunto das nossas chaves privadas), além disso o número precisa ser co-primo de 'n', por isso é feito um looping para que o numero tenha mdc entre ele e n igual a 1.

# Anotação: Números co-primos são aqueles números, que entre ELES não há divisor comum além de 1 (mdc entre eles é 1).

def chave_publica(n):
    while True:
        e = random.randrange(2,n)
        if mdc(n,e) == 1 and e !=145:
            return e



#O objetivo de implementar o algoritmo estendido de euclides eh obter o valor de "d" para realizar o processo de decifrar a mensagem desejada.
#O algoritmo de euclides estendido serve para realizar o inverso do mdc para descriptografar a mensagem.
def chave_privada(totiente, e):
    d = 0
    while ((d* e) % totiente != 1):
        d+=1
    return d


#A cifragem em RSA, é feita letra a letra pela seguinte equação: lcifra = l ** chavepub % n

#Para realizar a cifragem, temos que ter definido a mensagem, chave publica (que é a de ciptografia) e o conjunto n.
# Tendo isso podemos aplicar a formula acima, porém a lógica por de trás dessa função é: transformamos letra a letra por vez em um número, e após isso combinamos (com exponenciação) com a chave publica, com isso o numero da letra cifrada aumentará muito podendo até passar do conjunto n estabelecido, para resolver esse problema, é necessário pegar o resto da divisão da letra cifrada com o conjunto, por fim temos a letra cifrada dentro do conjunto estabelecido.
def cifrar(mensagem,e,n):
    msg_cifrada = ''
    for letra in mensagem:
        k = (ord(letra) ** e) % n
        msg_cifrada += chr(k)
    return msg_cifrada


#Para decifrar é feito a mesma logíca, e equacação da cifragem, entretanto usamos a chave privada em vez da chave publica
def decifrar(mensagem,n,d):
    msg_decifrada = ''
    for letra in mensagem:
        k = (ord(letra) ** d) % n
        msg_decifrada += chr(k)
    return msg_decifrada



def rsa (msg):
    #Escolhemos a chave privada, quando escolhemos esses numeros primos
    p = 211
    q = 191 
    n = p * q #40301   

    #Este n é o tamanho do nosso conjunto. No site diz que "É necessário termos um conjunto finito de valores para que possamos fazer o caminho inverso ao realizado para cifrar nossa mensagem". Podemos, chamar nosso conjunto de 40301.


    # Daqui para frente é a função totiente, totiente de n (40301)
    # Totiente significa: a quantidade de co-primos de um numero que são menores que ele mesmo.
    # O totiente de dois numeros primos são os dois números escolhidos menos 1 cada, seguido de multiplicação 
    #Φ(x) = (p - 1) * (q - 1)
    
    totiente = (p - 1) * (q - 1)

    #Ao chamar a função de chave publica com o parâmetro de totiente, estamos pedindo que gere um número co-primo aleatório.
    e = chave_publica(totiente)

    print(f'Chave publica: ({e},{n})')
    
    d = chave_privada(totiente,e)
    print(f'Chave privada: ({d},{n})')

    msg_crifada = cifrar(msg,e,n)
    print(f'Mensagem Cifrada: {msg_crifada}')

    msg_decrifada = decifrar(msg,n,d)
    print(f'Mensagem Decifrada: {msg_decrifada}')


if __name__ == '__main__':
    file_main = True
    print('Bem vindo ao nosso código de criptografia!')
    print('[1] - Criptografar')
    print('[2] - Decriptografar')
    decisao = input('Sua escolha: ')

    while decisao.isnumeric() is False or int(decisao) <1 or int(decisao) >2:
        print(f'Atenção, as opções são [1] e [2] ')
        decisao = input(f'''[1] - Criptografar
    [2] - Decriptografar
    Sua escolha: ''')
    decisao = int(decisao)

    if decisao ==1: #se o usuário escolheu cifrar, assim ele terá
        msg = input(f'Digite a mensagem a ser criptografada: ')
        print()
        rsa(msg)

    else: #tem verificação se o que o usuário digitou valores númericos para as chaves númericas e de conjunto n, e também se são positivas.
        #Após isso faz chamadas para a função decifrar com os parâmetros fornecidos, que são: 'mensagem', 'conjunto n' e 'chave privada'.
        msg = input(f'Digite a exata mensagem que deseja descriptografar: ')
        n = input(f'Digite o tamanho exato do conjunto das chaves usadas: ')
        while n.isnumeric() is False or int(n) < 1:
            print('Atenção!')
            n = input(f'Digite o tamanho exato do conjunto das chaves usadas: ')
        n = int(n)

        d = input(f'Digite a exata chave privada: ')
        while d.isnumeric() is False or int(d) <1:
            print('Atenção!')
            d = input(f'Digite a exata chave privada: ')
        d = int(d)
        print()
        print('A mensagem decriptografada é:',decifrar(msg,n,d))
        