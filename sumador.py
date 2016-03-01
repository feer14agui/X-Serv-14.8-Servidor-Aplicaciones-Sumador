
import socket


class webApp:
    """Root of a hierarchy of classes implementing web applications
    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print ('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print ('HTTP request received (going to parse and process):')
            request = recvSocket.recv(2048)
            print (request)
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print ('Answering back...')
            recvSocket.send(str.encode("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n"))
            recvSocket.close()

class sumApp(webApp):
	
	def analize(self, request):
		numero = request.split()[1][1:]
		return numero

	def sum(self, num1, num2):
		suma = num1 + num2
		return suma
		
	def parse(self, request):
		try:
			numero = int(request.split()[1][1:])	
			valido = True	
		except ValueError:
			numero = 0
			valido = False
		return numero,valido

	def process(self,parsedRequest):

		numero,valido = parsedRequest  #parsedRequest es una tupla

		if not valido:
			return ("200 OK", "<html><body><h1>Solo quiero numeros</h1></body></html>")
		if self.primero:
			self.guardado = numero
			self.primero = False
			return ("200 OK", "<html><body><h1>Dame otro numero</h1></body></html>")
		else:
			Resultado = self.guardado + numero
			self.primero = True
			return ("200 OK", "<html><body><h1>Resultado: " + str(Resultado) +" </h1></body></html>") 

	def __init__(self, hostname, port):
		self.primero = True
		#super(,self).__init__() #esto hace que se arranque el init de arriba
		super(sumApp, self).__init__(hostname, port) #esto hace que se arranque el init de arriba en python3
	

if __name__ == "__main__":
    testWebApp = sumApp("localhost", 1234)
