#Leonardo Chaves Duarte
#Enzo Matheus Paganini
#Osmar Andre Bassi
#Vinicius Massao Dziewulski
import os
import math
import nltk
import re
import stanfordnlp
from sly import Lexer, Parser
from collections import Counter
#nltk.download('punkt')
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

jogos = [
        ['call of duty black ops 2', 'tiro em primeira pessoa', 109.99, False],
        ['call of duty modern warfare', 'tiro em primeira pessoa', 199.90, True],
        ['fifa 20', 'esporte', 249.90, True],
        ['pro evolution soccer 2020', 'esporte', 119.90, True],
        ['left for dead 2', 'acao', 20.69, False]
    ]

frame = [
        ['know the game', None,'Do you know the game you want to rent?'],
        ['game', None, 'Which game do you want to rent?'],
        ['time', None, 'How long do you want to rent?'],
        ['payment method', None,'What would be your payment method?']
    ]

metodos_pagamentos = ['money', 'card', 'cash']
afirmativas = ['ye', 'yeah', 'positiv']
negativas = ['no', 'dont know', 'negativ']
perguntas = ['rent', 'do not know']

#Tokenizar
def TokenizeInput( texto):
    palavras_tokenize = tokenize.word_tokenize(texto, language = 'english')
    #print(palavras_tokenize)
    return palavras_tokenize

#Stemm
def StemmerNLTK( palavra, lista):
    #nltk.download('rslp')
    stemmer = nltk.stem.RSLPStemmer()
    lista.append(stemmer.stem(palavra))

#Remocao de Stopwords
def RemocaoStopWords( palavra, lista):
    #nltk.download('stopwords')
    if palavra not in set(stopwords.words('english')):
        lista.append(palavra)

#funcao que pega digramas de um lista
def getGramas (palavra):
    #lista de n-gramas da palavra
    par = list()
    array = list()
    for i in range(len(palavra)):
        ind = palavra[i]
        for j in range(len(ind) - 1):
            array.append(ind[j:2+j])
            #print (ind[j:2+j] + " - i-> ", i , " - j-> ", j)
        par.append(array)
        array = list()
    return par

#funcao que pega digramas de um palavra unica
def getGramasPalavraUnica(palavra):
    array = list()
    for i in range(len(palavra)-1):
        array.append(palavra[i:2+i])
    return array

#calcula a similaridade entre duas palavras
def checaSimilaridade(listaGramas, ngramasInput):
    #print("ngramas - ",ngramasInput)
    inputSet = set(ngramasInput)
    palavraSet = set(listaGramas)
    c = comparaNGramas(inputSet, palavraSet)
    a = len(inputSet)
    b = len(palavraSet)
    return (2*c)/(a+b)

#funçao para verificar digramas iguais
def comparaNGramas(listaA, listaB):
    matches = 0
    for a in listaA:
        for b in listaB:
            if a == b:
                matches += 1            
    return matches

#funcao para a retornar o ranking
def comparePalavras(lex, ngramasInput, dicionario):
    #print("ngramas - ",ngramasInput)
    lista = list()
    rank = list()
    index = 0
    #print("------------------------------")
    #print("    Palavras : Similaridade")
    #print("------------------------------")
    for palavra in lex:
        ngramasPalavra = dicionario[index]
        s = checaSimilaridade(ngramasPalavra, ngramasInput)
        #print(index+1, ') ', palavra, ': ', round(s,4))
        lista.append(palavra)
        lista.append(round(s,4))
        rank.append(lista)
        lista = list()
        index += 1
    return rank

#funcao para dar um sort no ranking
def mySort(lista):
    for i in range(len(lista)):
        if i == len(lista):
            break
        else:
            j = i+1
            for j in range(len(lista)):
                if lista[i][1] > lista[j][1]:
                    aux = lista[i]
                    lista[i] = lista[j]
                    lista[j] = aux
    return lista

#printar o rank
def printRank(rank):
    print("------------------------------")
    print("           RANK               ")
    print("------------------------------")
    for i in range(len(rank)):
        index = i+1
        print(index, ") " + rank[i][0] + " -> ", rank[i][1])

#printar as tabela de jogos com os valores
def printTabelas():
    #imprime lista de jogos no catalogo
    #imprime valores
    frame[0][1] = False
    print('========================================')
    print('                GAMES')
    print('========================================')
    print('          GAME  -  DAILY PRICE')
    for i in jogos:
        valor = 0.0
        if(i[3]):
            valor = i[2]*0.08
        else:
            valor = i[2]*0.04
        print(i[0] +' - R$',round(valor,4))
        print('----------------------------------------')


def frameConhecimentoDoJogo():
    if not frame[0][1]:
        print('I am going to help you, here these are our games...')
        printTabelas()


def frameTempoAluguel():
    inteiro = r'[0-9]+'
    print(frame[2][2])
    tempo = input('Voce: ')
    dialogo = tempo
    lista_token = TokenizeInput(dialogo)
    print(lista_token)
    lista_stemm = list()
    for i in lista_token:
        StemmerNLTK(i, lista_stemm)
    print(lista_stemm)
    lista_stopwords = list()
    for i in lista_stemm:
        RemocaoStopWords(i, lista_stopwords)
    print(lista_stopwords)
    lista_dialogo = lista_stopwords
    for i in lista_dialogo:
        if re.match(inteiro, i):
            tempo = int(i)
    frame[1][1] = tempo
    print('Alugando')

#onde tudo funciona
def acao(conversa, verifica):
    engano1 = True
    engano2 = True
    engano3 = True
    engano4 = True
    recibo = True
    verifica2 = -1
    if verifica == 1:
        print("KRONK: "+frame[0][2])
        first = input('You: ')
        dialogo = first.lower()
        lista_token = TokenizeInput(dialogo)
        lista_stemm = list()
        for i in lista_token:
            StemmerNLTK(i, lista_stemm)
        lista_dialogo = lista_stemm
        for i in lista_dialogo:
            if i in afirmativas:
                verifica2 = 1
            elif i in negativas:
                verifica2 = 0
            elif i == 'cancel':
                print("KRONK: Why leaving so soon? Bye :(")
                conversa = False
                return
        while(engano1):
            if verifica2 == 1:
                frame[0][1] = True
            elif verifica2 == 0:
                frame[0][1] = False
                frameConhecimentoDoJogo()
            print("KRONK: "+frame[1][2])
            second = input('You: ')
            second.lower()
            if second == 'cancel':
                recibo = False
                engano1 = False
            else:
                #print(nome_jogos)
                #print("==================================================")
                grama_second = getGramasPalavraUnica(second)
                grama_jogos = getGramas(nome_jogos)
                #ngramasInput = getGramasPalavraUnica(second)
                #print("second - ",second,", digrama second - ",ngramasInput)
                rank = list()
                rank = comparePalavras(nome_jogos,grama_second, grama_jogos)
                rank_sorted = mySort(rank)
                #printRank(rank_sorted)

                while(engano2):
                    if rank_sorted[0][1] == 1:
                        frame[1][1] = rank_sorted[0][0]
                        print("KRONK: You are renting " + frame[1][1])
                        engano1 = False
                        engano2 = False
                    elif rank_sorted[0][1] >= 0.5:
                        print("KRONK: You meant " + rank_sorted[0][0] +"?")
                        second = input('You: ')
                        second = second.lower()
                        if second == 'cancel':
                            recibo = False
                            engano1 = False
                            engano2 = False
                            engano3 = False
                            engano4 = False
                        else:
                            lista_token2 = TokenizeInput(second)
                            lista_stopwords2 = lista_token2
                            #for i in lista_token2:
                                #RemocaoStopWords(i, lista_stopwords2)
                            lista_stemm2 = list()
                            for i in lista_stopwords2:
                                StemmerNLTK(i, lista_stemm2)
                            lista_dialogo2 = lista_stemm2
                            for i in lista_dialogo2:
                                if i in afirmativas:
                                    frame[1][1] = rank_sorted[0][0]
                                    print("KRONK: You are renting " + frame[1][1])
                                    engano1 = False
                                    engano2 = False
                                elif i in negativas:
                                    rank_aux = rank_sorted[1]
                                    rank_sorted[0] = rank_aux

                while(engano3):
                    print("KRONK: Plese do not type number in full")
                    print("KRONK: "+frame[2][2])
                    third = input('You: ')
                    third = third.lower()
                    if 'cancel' in third:
                        recibo = False
                        engano3 = False
                        engano4 = False
                    tempo = None
                    nlp = stanfordnlp.Pipeline()
                    doc = nlp(third)
                    for i in doc.sentences[0].words:
                        if i.dependency_relation == 'nummod':
                            tempo = i.text 
                    if tempo != None:
                        frame[2][1] = tempo
                        engano3 = False
                    else:
                        print("KRONK: I did not understood please try again :)")

                pagamento = ""
                while(engano4):
                    print("KRONK: "+frame[3][2])
                    fourth = input('You: ')
                    fourth = fourth.lower()
                    if 'cancel' in fourth:
                        recibo = False
                        engano4 = False
                    doc2 = nlp(fourth)
                    for i in doc2.sentences[0].words:
                        if i.dependency_relation == 'obl' and i.text in metodos_pagamentos:
                            pagamento = i.text
                            frame[3][1] = pagamento
                            engano4 = False
                        elif i.dependency_relation == 'obl' and i.text not in metodos_pagamentos:
                            print("KRONK: Sorry did not understood, please what is your payment method? We only accept money and creadit card")
                
                if recibo:
                    preco = 0
                    jogo_comprado = frame[1][1]
                    for i in range(len(jogos)):
                        if jogo_comprado == jogos[i][0]:
                            if jogos[i][3]:
                                preco = jogos[i][2]*.08*int(frame[2][1])
                            else:
                                preco = jogos[i][2]*.04*int(frame[2][1])
                    print("======================================================================")
                    print("Game rented: "+frame[1][1]+" ====== Days rented: "+frame[2][1]+" days.")
                    print("Cost $",round(preco, 2),"  ======= Payment method - "+frame[3][1])
                    print("======================================================================")
                    print("KRONK: Do you want to confirm the payment?")
                    final_input = input("You: ")
                    final_input.lower()
                    lista_final = TokenizeInput(final_input)
                    lista_final_stemm = list()
                    for i in lista_final:
                        StemmerNLTK(i, lista_final_stemm)
                    for i in lista_final_stemm:
                        if i in afirmativas:
                            print("KRONK: Your order is done")
                            print("KRONK: Thanks for buying with us. BYEEEeee...:D")
                        elif i in negativas:
                            print("KRONK: You have canceled your order...")
                            print("KRONK: Back where we started :/")
            if not recibo:
                print("KRONK: Back where we started :/")
        
    elif verifica == 0:
        frame[0][1] = False
        frameConhecimentoDoJogo()
        while(engano1):
            frame[0][1] = True
            frameConhecimentoDoJogo()
            print("KRONK: "+frame[1][2])
            second = input('You: ')
            second.lower()
            if second == 'cancel':
                recibo = False
                engano1 = False
            else:
                #print(nome_jogos)
                #print("==================================================")
                grama_second = getGramasPalavraUnica(second)
                grama_jogos = getGramas(nome_jogos)
                #ngramasInput = getGramasPalavraUnica(second)
                #print("second - ",second,", digrama second - ",ngramasInput)
                rank = list()
                rank = comparePalavras(nome_jogos,grama_second, grama_jogos)
                rank_sorted = mySort(rank)
                #printRank(rank_sorted)

                while(engano2):
                    if rank_sorted[0][1] == 1:
                        frame[1][1] = rank_sorted[0][0]
                        print("KRONK: You are renting " + frame[1][1])
                        engano1 = False
                        engano2 = False
                    elif rank_sorted[0][1] >= 0.5:
                        print("KRONK: You meant " + rank_sorted[0][0] +"?")
                        second = input('You: ')
                        second = second.lower()
                        if second == 'cancel':
                            recibo = False
                            engano1 = False
                            engano2 = False
                            engano3 = False
                            engano4 = False
                        else:
                            lista_token2 = TokenizeInput(second)
                            lista_stopwords2 = list()
                            for i in lista_token2:
                                RemocaoStopWords(i, lista_stopwords2)
                            lista_stemm2 = list()
                            for i in lista_stopwords2:
                                StemmerNLTK(i, lista_stemm2)
                            lista_dialogo2 = lista_stemm2
                            for i in lista_dialogo2:
                                if i in afirmativas:
                                    frame[1][1] = rank_sorted[0][0]
                                    print("KRONK: You are renting " + frame[1][1])
                                    engano1 = False
                                    engano2 = False
                                elif i in negativas:
                                    rank_aux = rank_sorted[1]
                                    rank_sorted[0] = rank_aux

                nlp = stanfordnlp.Pipeline()
                while(engano3):
                    print("KRONK: Plese do not type number in full")
                    print("KRONK: "+frame[2][2])
                    third = input('You: ')
                    third = third.lower()
                    if 'cancel' in third:
                        recibo = False
                        engano3 = False
                        engano4 = False
                    tempo = None
                    doc = nlp(third)
                    for i in doc.sentences[0].words:
                        if i.dependency_relation == 'nummod':
                            tempo = i.text 
                    if tempo != None:
                        frame[2][1] = tempo
                        engano3 = False
                    else:
                        print("KRONK: I did not understood please try again :)")

                pagamento = ""
                while(engano4):
                    print("KRONK: "+frame[3][2])
                    fourth = input('You: ')
                    fourth = fourth.lower()
                    if 'cancel' in fourth:
                        recibo = False
                        engano4 = False
                    doc2 = nlp(fourth)
                    for i in doc2.sentences[0].words:
                        if i.dependency_relation == 'obl' and i.text in metodos_pagamentos:
                            pagamento = i.text
                            frame[3][1] = pagamento
                            engano4 = False
                        elif i.dependency_relation == 'obl' and i.text not in metodos_pagamentos:
                            print("KRONK: Sorry did not understood, please what is your payment method? We only accept money and creadit card")
                
                if recibo:
                    preco = 0
                    jogo_comprado = frame[1][1]
                    for i in range(len(jogos)):
                        if jogo_comprado == jogos[i][0]:
                            if jogos[i][3]:
                                preco = jogos[i][2]*.08*int(frame[2][1])
                            else:
                                preco = jogos[i][2]*.04*int(frame[2][1])
                    print("======================================================================")
                    print("Game rented: "+frame[1][1]+" ====== Days rented: "+frame[2][1]+" days.")
                    print("Cost $",round(preco, 2),"  ======= Payment method - "+frame[3][1])
                    print("======================================================================")
                    print("KRONK: Do you want to confirm the payment?")
                    final_input = input("You: ")
                    final_input.lower()
                    lista_final = TokenizeInput(final_input)
                    lista_final_stemm = list()
                    for i in lista_final:
                        StemmerNLTK(i, lista_final_stemm)
                    for i in lista_final_stemm:
                        if i in afirmativas:
                            print("KRONK: Your order is done")
                            print("KRONK: Thanks for buying with us. BYEEEeee...:D")
                        elif i in negativas:
                            print("KRONK: You have canceled your order...")
                            print("KRONK: Back where we started :/")

            if not recibo:
                print("KRONK: Back where we started :/")
    else:
        print('KRONK: Sorry i did not understand')


def chat():
    conversa = True
    os.system('clear')
    print('Hi I am KRONK the chatbot. I was created to help you while you are renting games')
    print('Obs: Please use lower case')
    print('If you want to leave just type cancel :)')
    verifica = -1
    while conversa:
        for i in frame:
            i[1] = None
        #print(frame)
        print("KRONK: How can i help you?")
        input_inicial = input("You: ")
        input_inicial = input_inicial.lower()
        if input_inicial == 'cancel':
            print("KRONK: Leaving... Bye :)")
            conversa=False
            break
        grama_inicial = getGramasPalavraUnica(input_inicial)
        grama_perguntas = getGramas(perguntas)
        rank_perguntas = comparePalavras(perguntas, grama_inicial, grama_perguntas)
        rank_perguntas_sorted = mySort(rank_perguntas)

        if rank_perguntas_sorted[0][0] == perguntas[0]:
            verifica = 1
            acao(conversa, verifica)
        elif rank_perguntas_sorted[0][0] == perguntas[1]:
            verifica = 0
            acao(conversa,verifica)
        else:
            print("KRONK: Sorry i did not understood")
        #print(frame)

if __name__ == '__main__':
    #dicionario de jogos
    nome_jogos = list()
    for i in range(len(jogos)):
        nome_jogos.append(jogos[i][0])
    pares_jogos = getGramas(nome_jogos)
    chat()