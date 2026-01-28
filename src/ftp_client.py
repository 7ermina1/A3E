import ftplib

class FTPClient:
    def __init__(self, target):
        self.target = target

    def check_anonymous(self):
        print(f"[*] Checking FTP Anonymous access on {self.target}...")
        try:
            ftp = ftplib.FTP(self.target, timeout=10)
            ftp.login() # Anonymous by default
            welcome = ftp.getwelcome()
            ftp.quit()
            return True, f"Anonymous login successful. Banner: {welcome}"
        except Exception as e:
            return False, str(e)
