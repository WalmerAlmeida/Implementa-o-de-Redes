import socket
from threading import*
import os
from colorama import Fore, Back, Style

address = ("localhost", 30000)
threadCount = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(address)

server_socket.listen()

class Game_board_server():
    def __init__(self, round):
        self.round_server = round
        self.max_jogadas = 9
        
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
    def verify_winner(self, client1, client2, piece_client1, piece_client2):

        if(self.board[0][0] == "X" and self.board[0][1] == "X" and self.board[0][2] == "X"):
            self.round_server = 11
        if(self.board[1][0] == "X" and self.board[1][1] == "X" and self.board[1][2] == "X"):
            self.round_server = 11
        if(self.board[2][0] == "X" and self.board[2][1] == "X" and self.board[2][2] == "X"):
            self.round_server = 11
        if(self.board[0][0] == "X" and self.board[1][0] == "X" and self.board[2][0] == "X"):
            self.round_server = 11
        if(self.board[0][1] == "X" and self.board[1][1] == "X" and self.board[2][1] == "X"):
            self.round_server = 11
        if(self.board[0][2] == "X" and self.board[1][2] == "X" and self.board[2][2] == "X"):
            self.round_server = 11
        if(self.board[0][0] == "X" and self.board[1][1] == "X" and self.board[2][2] == "X"):
            self.round_server = 11
        if(self.board[0][2] == "X" and self.board[1][1] == "X" and self.board[2][0] == "X"):
            self.round_server = 11
        if(self.board[0][0] == "O" and self.board[0][1] == "O" and self.board[0][2] == "O"):
            self.round_server = 12
        if(self.board[1][0] == "O" and self.board[1][1] == "O" and self.board[1][2] == "O"):
            self.round_server = 12
        if(self.board[2][0] == "O" and self.board[2][1] == "O" and self.board[2][2] == "O"):
            self.round_server = 12
        if(self.board[0][0] == "O" and self.board[1][0] == "O" and self.board[2][0] == "O"):
            self.round_server = 12
        if(self.board[0][1] == "O" and self.board[1][1] == "O" and self.board[2][1] == "O"):
            self.round_server = 12
        if(self.board[0][2] == "O" and self.board[1][2] == "O" and self.board[2][2] == "O"):
            self.round_server = 12
        if(self.board[0][0] == "O" and self.board[1][1] == "O" and self.board[2][2] == "O"):
            self.round_server = 12
        if(self.board[0][2] == "O" and self.board[1][1] == "O" and self.board[2][0] == "O"):
            self.round_server = 12
        
        if(self.round_server == 11 or self.round_server == 12 or self.round_server >= 9):
            print("\n\t\t" + Fore.RED + " Fim de Jogo!")
            if(self.round_server == 11):
                print("\n\t" + Fore.YELLOW + "\tO JOGADOR > X < É O VENCEDOR!!\n" + Fore.RESET)
                
                client2.send(str.encode("800"))
                client1.send(str.encode("700"))
            elif(self.round_server == 12):
                print("\n\t" + Fore.YELLOW + "\tO JOGADOR > O < É O VENCEDOR!!\n" + Fore.RESET)
                
                client2.send(str.encode("700"))
                client1.send(str.encode("800"))
                
            elif(self.round_server >= 9):
                print("\n\t" + Fore.YELLOW + "** OPS, PARECE QUE DEU VELHA **" + Fore.RESET)
                client2.send(str.encode("900"))
                client1.send(str.encode("900"))
            return "game over"
            
        client2.send(str.encode("999"))
        client1.send(str.encode("999"))

    def action(self, linha, coluna, piece):
        self.board[linha][coluna] = piece

def client_thread(client1, client2, threadCount1, threadCount2):

    piece_client1 = "X"
    piece_client2 = "O"
    client1.sendall(str.encode("X"))
    client2.sendall(str.encode("O"))
    try:
        while True:
            client1_response = client1.recv(1024)
            client1_response = client1_response.rstrip()
            client2_response = client2.recv(1024)
            client2_response = client2_response.rstrip()

            if(client1_response.decode() == "JOGAR" and client2_response.decode() == "JOGAR"):
                
                client1.sendall(str.encode("100"))
                client2.sendall(str.encode("100"))

                board_server = Game_board_server(1)

                while True:

                    while True:
                        client1_response = client1.recv(1024)
                        client1_response = client1_response.rstrip()
                        command = client1_response.decode().split("#")[0]
                        position = client1_response.decode().split("#")[1]
                        linha = int(position.split("/")[0])
                        coluna = int(position.split("/")[1])

                        if(command == "INSERIR"):
                            print(command + "#" + str(linha) + "/" + str(coluna))
                            
                            if(board_server.board[linha][coluna] == " "):
                                board_server.action(linha, coluna, piece_client1)
                                client2.sendall(str.encode(str(linha) + "/" + str(coluna)))
                                client1.sendall(str.encode("500"))
                                if(board_server.verify_winner(client1, client2, piece_client1, piece_client2) == "game over"):
                                    return
                                board_server.round_server += 1
                                break
                            else:
                                client1.sendall(str.encode("600"))
                                continue
                        else:
                            print(Fore.RED + "Erro inesperado1" + Fore.RESET)
                            break

                    while True:
                        client2_response = client2.recv(1024)
                        client2_response = client2_response.rstrip()
                        command = client2_response.decode().split("#")[0]
                        position = client2_response.decode().split("#")[1]
                        linha = int(position.split("/")[0])
                        coluna = int(position.split("/")[1])

                        if(command == "INSERIR"):
                            print(command + "#" + str(linha) + "/" + str(coluna))
                            
                            if(board_server.board[linha][coluna] == " "):
                                
                                board_server.action(linha, coluna, piece_client2)
                                
                                client2.sendall(str.encode("500"))
                                
                                client1.sendall(str.encode(str(linha) + "/" + str(coluna)))
                                
                                if(board_server.verify_winner(client1, client2, piece_client1, piece_client2) == "game over"):
                                    return
                                board_server.round_server += 1
                                break
                            else:
                                client2.sendall(str.encode("600"))
                                continue
                        else:
                            print(Fore.RED + "Erro inesperado1" + Fore.RESET)
                            break
                    
                
            elif(client1_response.decode() == "SAIR" or client2_response.decode() == "SAIR"):
                client1.sendall(str.encode("200"))
                client2.sendall(str.encode("200"))
                break
            else:
                print(Fore.RED + "Erro inesperado5" + Fore.RESET)
                client1.sendall(str.encode("300"))
                client2.sendall(str.encode("300"))
                break
    except:
        print(Fore.RED + "Erro inesperado6" + Fore.RESET)
        return
    finally:
        client1.close()
        client2.close()
        print("Player", threadCount1, "Offline")
        print("Player", threadCount2, "Offline")


while True:
    try:
        client1, address1 = server_socket.accept()
        client2, address2 = server_socket.accept()

        print("Nova conexao recebida do IP: ", address1[0], "e PORTA: ", address1[1])
        print("Nova conexao recebida do IP: ", address2[0], "e PORTA: ", address2[1])

        client1.sendall(str.encode(str(threadCount + 2)))
        client2.sendall(str.encode(str(threadCount + 1)))
        
        thread = Thread(target=client_thread, args=(client1, client2, threadCount + 1, threadCount + 2))
        thread.start()
        threadCount = threadCount + 2
    except:
        break
    
server_socket.close()