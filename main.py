import argparse
import sys
from src.engine import AttackEngine

def main():
    parser = argparse.ArgumentParser(description="Project A3E: Automated Agentless Adversarial Emulation")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("--msf-pass", help="Metasploit RPC Password", default="password")
    parser.add_argument("--lhost", help="Local Host IP for Reverse Shell (LHOST)", default="127.0.0.1")
    
    args = parser.parse_args()

    print(f"[*] A3E Initialized.")
    print(f"[*] Target: {args.target}")
    
    engine = AttackEngine(args.target, args.msf_pass, args.lhost)
    engine.run()

if __name__ == "__main__":
    main()
