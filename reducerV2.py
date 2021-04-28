#!/usr/bin/python

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
cont_palavras = 0
vetor_palavras_mais_usadas = []

for line in sys.stdin:
    line = line.strip()

    word, count = line.split('\t', 1)

    try:
        count = int(count)
    except ValueError:
        continue

    #sinal boleano para saber se contem somente letras ou nao na palavra
    somenteLetras = 0
    
    if current_word != None:
        #verifica se existe somente letras na palavra
        for i in range(len(current_word)):
            if (not ((ord(current_word[i]) >= 65) & (ord(current_word[i]) <= 90))) & (not ((ord(current_word[i]) >= 97) & (ord(current_word[i]) <= 122))):
                somenteLetras = 1
  
    if  current_word == word:
        current_count += count
    else:
        if current_word != None:
            if somenteLetras == 0:
                print('%s\t%s' % (current_word,current_count))
                vetor_palavras_mais_usadas.append([current_word,current_count])
                cont_palavras = cont_palavras + 1
        current_count = count
        current_word = word

somenteLetras = 0

#verifica se existe somente letras na ultima palavra do texto
for i in range(len(current_word)):
    if (not ((ord(current_word[i]) >= 65) & (ord(current_word[i]) <= 90))) & (not ((ord(current_word[i]) >= 97) & (ord(current_word[i]) <= 122))):
        somenteLetras = 1

if current_word == word:
    if somenteLetras == 0:
        print('%s\t%s' % (current_word,current_count))
        vetor_palavras_mais_usadas.append([current_word,current_count])
        cont_palavras = cont_palavras + 1

print('\nQuantidade de Palavras distintas: %s' %cont_palavras)

#Ordenando o vetor de palavras para saber quais as dez palavras mais usadas
i=0
for vetor in vetor_palavras_mais_usadas:
    j=0
    for vetor2 in vetor_palavras_mais_usadas:
        if vetor[1] > vetor2[1]:
            vetor_aux = vetor_palavras_mais_usadas[i]
            vetor_palavras_mais_usadas[i] = vetor_palavras_mais_usadas[j]
            vetor_palavras_mais_usadas[j] = vetor_aux
        j=j+1
    i=i+1
#FIM ---

print('\nAs dez palavras mais usadas são:\n')
for i in range(10):
    print('%s\t%s' % (vetor_palavras_mais_usadas[i][0], vetor_palavras_mais_usadas[i][1]))
#FIM

#Criando as Classes do Histograma no vetor
max = vetor_palavras_mais_usadas[0][1]
classes = []

#caso seja menor que 10 os valores das classes serão em decimal.
if max >= 10:
    valorClasse  = round(max/10)
    valorInicial = 1
else:
    valorClasse  = (max/10)
    valorInicial = 0.1

#criando as classes
valorFinal= valorClasse
for i in range(10):
    #colocando os valores das classes para dentro do vetor
    
    if i == 9:
        classes.append([valorInicial, max, 0])
    else:
        classes.append([valorInicial, valorFinal, 0])

    valorInicial = valorInicial + valorClasse
    valorInicial = round(valorInicial,2)

    valorFinal   = valorFinal   + valorClasse 
    valorFinal   = round(valorFinal,2)

#Faz a contagem de palavras de cada classe
for palavras in vetor_palavras_mais_usadas:
    qtde = palavras[1]

    #verifica se pertence a classe
    for i in range(10):
        if ((qtde >= classes[i][0]) & (qtde <= classes[i][1])): 
            #somando na terceira posicao do vetor que contem a quantidade da classe
            classes[i][2] =  classes[i][2] + 1 

print('\nHistograma de Classes\n')
#listando o histograma pronto
for i in range(10):
    print('%s ~ %s | %s' % (classes[i][0], classes[i][1], classes[i][2]))

   
    

        
