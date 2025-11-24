"""
Servidor HTTP básico em Python usando sockets TCP.
Este servidor recebe requisições HTTP de clientes e envia arquivos solicitados.
"""

from socket import *
import sys  # Necessário para encerrar o programa


def main():
    """
    Função principal que inicializa e executa o servidor HTTP.
    """
    # Cria o socket TCP (orientado à conexão)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    # Prepara o socket do servidor
    # Define o endereço e porta do servidor
    serverPort = 6789
    serverSocket.bind(('', serverPort))
    
    # Coloca o socket em modo de escuta, permitindo até 1 conexão pendente
    serverSocket.listen(1)
    
    while True:
        # Estabelece a conexão
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        
        try:
            # Recebe a mensagem do cliente (requisição HTTP)
            message = connectionSocket.recv(1024).decode()
            
            # Extrai o nome do arquivo da requisição HTTP
            filename = message.split()[1]
            
            # Abre o arquivo solicitado (remove o '/' inicial do caminho)
            f = open(filename[1:])
            
            # Lê o conteúdo completo do arquivo
            outputdata = f.read()
            
            # Fecha o arquivo após a leitura
            f.close()
            
            # Envia a linha de status do cabeçalho HTTP (200 OK)
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            
            # Envia o conteúdo do arquivo ao cliente
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            
            # Fecha a conexão com o cliente
            connectionSocket.close()
            
        except IOError:
            # Envia mensagem de erro 404 se o arquivo não for encontrado
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
            
            # Fecha o socket do cliente
            connectionSocket.close()
    
    # Fecha o socket do servidor (não será alcançado devido ao loop infinito)
    serverSocket.close()
    sys.exit()  # Encerra o programa


if __name__ == "__main__":
    main()

