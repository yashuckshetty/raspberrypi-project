

import socket
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sever_address=('192.168.0.3',999)
print('starting up on{} port{}'.format(*server_address))
sock.bind(server_address)
sock.listen(1)
	while True:
		print('waiting for a connection')
		connection ,client_address=sock.accpet()
			try:
				print('connection from',client_address)
			while True:
				data = connection recv(16)
				print('received {!r}'.format(data))
					if data:
						print('sending data back to the client')
						connection.sendall(data)
					else:
						print('no data from',client_address)
					break
			finally:
				print("closing current connection")
				connection.close()
