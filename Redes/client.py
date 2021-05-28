#!/usr/bin/python

import socket
import os
from colorama import Fore, Back, Style

address = ("localhost", 30000)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(address)

class Game_board():
    def __init__(self, piece):
        self.piece = piece
        self.max_jogadas = 9
        
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        if(self.piece == "X"):
            self.enemy_piece = "O"
        else:
            self.enemy_piece = "X"

    def instruction(self):
        os.system("clear")
        print("\n\n\t\t"+ Fore.GREEN + "### Bem-Vindo ao Jogo da Velha Bolado ###\n\n\n" + Fore.RESET)
        print(Fore.YELLOW + "Instruções do Jogo:\n")
        print("1) Indique o valor da LINHA que deseja jogar")
        print("2) Indique o valor da COLUNA que deseja jogar")
        print("2) Pressione Enter" + Fore.RESET)
        print("\nAs posições do board estão distribuídas da seguinte forma:\n\n")
        print("\t\t    0   1   2")
        print("\t\t0:  " + self.board[0][0] + " | " + self.board[0][1] + " | " + self.board[0][2])
        print("\t\t   -----------")
        print("\t\t1:  " + self.board[1][0] + " | " + self.board[1][1] + " | " + self.board[1][2])
        print("\t\t   -----------")
        print("\t\t2:  " + self.board[2][0] + " | " + self.board[2][1] + " | " + self.board[2][2])
        print("\n\nPara iniciar, pressione qualquer tecla...")
        input()
        os.system("clear")

    def screen(self, round):

        os.system("clear")
        if(self.piece == "X"):
            print("\nNúmero da Jogada: " + Fore.GREEN + str(round) + Fore.RESET)
        else:    
            print("\nNúmero da Jogada: " + Fore.GREEN + str(round-1) + Fore.RESET)
        print("\n\n\t\t    0   1   2")
        print("\t\t0:  " + self.board[0][0] + " | " + self.board[0][1] + " | " + self.board[0][2])
        print("\t\t   -----------")
        print("\t\t1:  " + self.board[1][0] + " | " + self.board[1][1] + " | " + self.board[1][2])
        print("\t\t   -----------")
        print("\t\t2:  " + self.board[2][0] + " | " + self.board[2][1] + " | " + self.board[2][2])
    
    def action(self, linha, coluna, piece):
        self.board[linha][coluna] = piece

def TicTacToe_online():
    try:
        print("\n\n\t\t" + Fore.YELLOW + "### Jogo Da Velha Online ###\n\n\n" + Fore.RESET)

        print("Esperando oponente")

        opponent = client_socket.recv(1024)
        opponent = opponent.rstrip()
        print("Você está jogando contra o " + Fore.GREEN + "palyer " + opponent.decode() + Fore.RESET)

        piece = client_socket.recv(1024)
        piece = piece.rstrip()
        print("Sua peça é " + Fore.GREEN + piece.decode() + Fore.RESET)

        if(piece.decode() == "X"):
            round = 1
        else:
            round = 2

        board = Game_board(piece.decode())

        board.instruction()

        while True:
            text = input("\nDigite " + Fore.GREEN + "'JOGAR'" + Fore.RESET + " se quiser iniciar o jogo ou digite " + Fore.GREEN + "'SAIR'" + Fore.RESET + " para desconectar: ")
            text = text.upper()
                
            
            if(text != "SAIR" and text != "JOGAR"):
                print("Resposta inválida")
                continue

            client_socket.sendall(str.encode(text))

            if (text == "SAIR"):
                return
            elif(text == "JOGAR"):
                break


        print("Esperando resposta do adversário")
        server_response = client_socket.recv(1024)
        server_response = server_response.rstrip()


        if(server_response.decode() == "100"):
            print("Código " + str(server_response.decode()) + ", Os dois jogadores decidiram iniciar o jogo")
            

            while True:
                
                if(round%2):
                    
                    while True:
                        try:
                            board.screen(round)
                            print("\n Sua vez -->" + Fore.GREEN + board.piece + Fore.RESET + "<--\n")
                            linha = int(input("Digite a linha que deseja jogar: "))
                            coluna = int(input("Digite a coluna que deseja jogar: "))

                            if(linha < 0 or linha > 2 or coluna < 0 or coluna > 2): 
                                print("Digite uma posição válida! Pressione Enter para continuar")
                                input()
                                continue
                            elif(board.board[linha][coluna] != " "):
                                linha = 0
                                coluna = 0
                                print("\nEssa posição já está preenchida! Tente novamente. Pressione Enter para continuar\n")
                                input()
                                continue
                            else:
                                position = "INSERIR" + "#" + str(linha) + "/" + str(coluna)
                                client_socket.sendall(str.encode(position))

                                server_response = client_socket.recv(1024)
                                server_response = server_response.rstrip()
                                if(server_response.decode() == "500"):
                

                                    verify_winner_response = client_socket.recv(1024)
                                    verify_winner_response = verify_winner_response.rstrip()
                                    board.action(linha, coluna, board.piece)
                                    board.screen(round)
                                    if(verify_winner_response.decode() == "700"):
                                        print("\n\t\t" + Fore.RED + " Fim de Jogo!")
                                        print("\n\t\t" + Fore.YELLOW + "** PARABÉNS **\n\n\tO JOGADOR > " + board.piece + " < É O VENCEDOR!!\n")
                                        return
                                    elif(verify_winner_response.decode() == "800"):
                                        print("\n\t\t" + Fore.RED + " Fim de Jogo!")
                                        print("\n\t" + Fore.YELLOW + "Você perdeu, Mais sorte na próxima vez :(\n")
                                        return
                                    elif(verify_winner_response.decode() == "900"):
                                        print("\n\t\t" + Fore.RED + " Fim de Jogo!")
                                        print("\n\t" + Fore.YELLOW + "** OPS, PARECE QUE DEU VELHA **")
                                        return
                                    elif(verify_winner_response.decode() == "999"):
                                        print("Ainda sem vencedor")
                                        break
                                    else:
                                        print("Erro1")
                                        return

                                elif(server_response.decode() == "600"):
                                    print("Posição já preenchida")
                                    continue
                                else:
                                    print("Erro2")
                                    return

                        except:
                            print("Valor inválido. Pressione Enter para continuar")
                            input()
                             
                else:
                    print("Esperando jogada do adversário")

                    server_position = client_socket.recv(1024)
                    server_position = server_position.rstrip()
                    
                    linha = int(server_position.decode().split("/")[0])
                    coluna = int(server_position.decode().split("/")[1])

                    board.action(linha, coluna, board.enemy_piece)

                    verify_winner_response = client_socket.recv(1024)
                    verify_winner_response = verify_winner_response.rstrip()

                    board.screen(round)

                    if(verify_winner_response.decode() == "700"):
                        print("\n\t\t" + Fore.RED + " Fim de Jogo!")
                        print("\n\t\t" + Fore.YELLOW + "** PARABÉNS **\n\n\tO JOGADOR > " + board.piece + " < É O VENCEDOR!!\n")
                        return
                    elif(verify_winner_response.decode() == "800"):
                        print("\n\t\t" + Fore.RED + " Fim de Jogo!")
                        print("\n\t" + Fore.YELLOW + "Você perdeu, Mais sorte na próxima vez :(\n")
                        return
                    elif(verify_winner_response.decode() == "900"):
                        print("\n\t\t" + Fore.RED + " Fim de Jogo!")
                        print("\n\t" + Fore.YELLOW + "** OPS, PARECE QUE DEU VELHA **")
                        return
                    elif(verify_winner_response.decode() == "999"):
                        print("Ainda sem vencedor")
                    else:
                        print("Erro3")
                        return

                    
                round += 1
        elif(server_response.decode() == "200"):
            print("Código " + str(server_response.decode()) + ", O seu adversário desistiu")
            return
        elif(server_response.decode() == "300"):
            print("Código " + str(server_response.decode()) + ", Resposta inesperada")
            return
    
    except:
        print(Fore.RED + "Erro inesperado" + Fore.RESET)
        return

TicTacToe_online()
client_socket.close()
print("Conexão com o servidor foi finalizada")