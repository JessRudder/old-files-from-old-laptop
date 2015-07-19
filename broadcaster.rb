require 'socket'
chat_socket = UDPSocket.new
 
# tell the OS we mean to broadcast
chat_socket.setsockopt(:SOCKET, :SO_BROADCAST, 1)
 
print "# Sending messages to everyone port 31337\n< "
while message = gets
  chat_socket.send message, 0, '255.255.255.255', 31337
  print "< "
end