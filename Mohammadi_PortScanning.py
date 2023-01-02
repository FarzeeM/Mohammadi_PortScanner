import socket
from concurrent import futures
from datetime import datetime


# set up sockets
def checking_ports(host, port, timeout):
   port_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   port_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   port_sock.settimeout(timeout)

   try:
       port_sock.connect((host, port))
       return port
   except:
       return

# initailize threadpool
def scan(host, timeout):
   threadPoolSize = 30000
   portsToCheck = 30000

   executor = futures.ThreadPoolExecutor(max_workers=threadPoolSize)
   checking = [
       executor.submit(checking_ports, host, port, timeout)
       for port in range(0, portsToCheck, 1)

   ]

   for response in futures.as_completed(checking):

    if response.result():
        print('Open on port: {}'.format(response.result()))
        try:
            print('Service Name: ' + socket.getservbyport(response.result()))
        except:
            print('Service Name: Unavailable')
        print('Date & Time:' + str(datetime.now()))
        print()


def main():
    targetIp = input("Enter the target IP address: ") # specifies ip address
    timeout = int(input("How long before the connection times out: ")) # input for TTL
    z1 = datetime.now() # scan start
    scan(targetIp, timeout)
    z2 = datetime.now() # scan end
    total = z2 - z1 # calculates scan time
    print()
    print('Scanning Completed In: ' + str(total) + ' Seconds')


if __name__ == "__main__":
   main()
