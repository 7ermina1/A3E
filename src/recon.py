import nmap

class Recon:
    def __init__(self):
        # nmap.PortScanner() requires nmap to be installed on the system path
        try:
            self.nm = nmap.PortScanner()
            self.available = True
        except nmap.PortScannerError:
            print("[-] Nmap not found. Ensure nmap is installed and in your PATH.")
            self.available = False
        except Exception as e:
            print(f"[-] Error initializing nmap: {e}")
            self.available = False

    def scan(self, target):
        if not self.available:
            return None
            
        print(f"[*] Scanning target: {target} for ports 21, 445...")
        try:
            # -Pn: Treat all hosts as online -- skip host discovery
            self.nm.scan(target, arguments='-p 21,445 -Pn')
            if target in self.nm.all_hosts():
                return self.nm[target]
            else:
                print("[-] Target not found or down.")
                return None
        except Exception as e:
            print(f"[-] Scan failed: {e}")
            return None
