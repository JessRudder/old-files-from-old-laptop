require 'socket'
chat_socket = UDPSocket.new
 
# Listen on all IP addresses on port 31337
chat_socket.bind "", 31337
 
puts "# Now listening on port 31337"
while message = chat_socket.gets.chomp
  puts "> " + message
end