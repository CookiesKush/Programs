import sys
import socket
import time
import signal

from timeit import default_timer as timer


class TCPPinger:

    def __init__(self, host:str, port:int):
        """ Initialize Class """

        # Register SIGINT Handler
        signal.signal(signal.SIGINT, self.signal_handler)

        # Set Host and Port
        self.host = host
        self.port = port

        # Max Count counters
        self.maxCount = 10000
        self.count    = 0

        # Pass/Fail counters
        self.passed   = 0
        self.failed   = 0

        # Start Pinger
        self.ping()
        # Output Results if maxCount reached
        self.getResults()

    def getResults(self):
        """ Output Results """

        lRate = 0
        if self.failed != 0:
            lRate = self.failed / (self.count) * 100
            lRate = "%.2f" % lRate

        print(f"--- {self.host} ping statistics ---")
        print(f"\nTCP Ping Results: Connections (Total/Pass/Fail): [{self.count}/{self.passed}/{self.failed}] (Failed: {str(lRate)}%)")

    def signal_handler(self, signal, frame):
        """ Catch Ctrl-C and Exit """
        self.getResults()
        sys.exit(0)

    def ping(self):
        # Loop while less than max count or until Ctrl-C caught
        while self.count < self.maxCount:

            # Increment Counter
            self.count += 1
            self.success = False

            # New Socket
            s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

            # 1sec Timeout
            s.settimeout(1)

            # Start a timer
            s_start = timer()

            # Try to Connect
            try:
                s.connect((host, int(port)))
                s.shutdown(socket.SHUT_RD)
                self.success = True
            
            # Connection Timed Out
            except socket.timeout:
                print("Connection timed out!")
                self.failed += 1
            except OSError as e:
                print("OS Error:", e)
                self.failed += 1

            # Stop Timer
            s_stop = timer()
            s_runtime = "%.2f" % (1000 * (s_stop - s_start))

            if self.success:
                print("Connected to %s[%s]: tcp_seq=%s time=%s ms" % (self.host, self.port, (self.count-1), s_runtime))
                self.passed += 1

            # Sleep for 1sec
            if self.count < self.maxCount:
                time.sleep(1)


if __name__ == "__main__":
    host = str(input("Enter Host: "))
    port = int(input("Enter Port: "))
    TCPPinger(host, port)
