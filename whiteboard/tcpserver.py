import socketserver,threading

class ThreadTCPserver(socketserver.ThreadingMixIn,socketserver.TCPServer):
    allow_reuse_address=True
    pass

class Handler_TCPServer(socketserver.BaseRequestHandler):

    cur_thread = threading.current_thread()
    print(f"Thread Handle: {cur_thread}")
    def handle(self):
        try:
            print(type(self.client_address))
            while True:
                msg=self.request.recv(1024).decode("utf-8")
                print(f"client rev data:{msg}")
                if msg==" ":
                    break
                send_msg="server received you message."
                send_back=self.request.sendall(send_msg.encode("utf-8"))
        except Exception as e:
            print("Error {}: {}".format(self.client_address[0], e))
        print("Client Disconnet ")

if __name__=="__main__":
    HOST,PORT="127.0.0.1",8001
    tcp_server=ThreadTCPserver((HOST,PORT),Handler_TCPServer)
    tcp_server.serve_forever()


