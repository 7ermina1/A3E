import unittest
import sys
from unittest.mock import MagicMock, patch

# Mock dependencies BEFORE importing src.engine
sys.modules['nmap'] = MagicMock()
sys.modules['pymetasploit3'] = MagicMock()
sys.modules['pymetasploit3.msfrpc'] = MagicMock()

from src.engine import AttackEngine

class TestAttackEngine(unittest.TestCase):
    
    @patch('src.engine.Recon')
    @patch('src.engine.FTPClient')
    @patch('src.engine.MSFClient')
    def test_run_path_b_ftp(self, MockMSF, MockFTP, MockRecon):
        # Setup Mocks
        mock_recon_instance = MockRecon.return_value
        # Simulate open port 21
        mock_recon_instance.scan.return_value = {
            'tcp': {
                21: {'state': 'open'},
                445: {'state': 'closed'}
            }
        }
        
        mock_ftp_instance = MockFTP.return_value
        mock_ftp_instance.check_anonymous.return_value = (True, "Success")
        
        # Init Engine
        engine = AttackEngine("127.0.0.1", "pass", "127.0.0.1")
        engine.run()
        
        # Verify Recon was called
        mock_recon_instance.scan.assert_called_with("127.0.0.1")
        
        # Verify FTP was called
        mock_ftp_instance.check_anonymous.assert_called_once()
        
        # Verify MSF was NOT called (port 445 closed)
        MockMSF.return_value.execute_eternalblue.assert_not_called()

    @patch('src.engine.Recon')
    @patch('src.engine.FTPClient')
    @patch('src.engine.MSFClient')
    def test_run_path_a_eternalblue(self, MockMSF, MockFTP, MockRecon):
        # Setup Mocks
        mock_recon_instance = MockRecon.return_value
        # Simulate open port 445
        mock_recon_instance.scan.return_value = {
            'tcp': {
                21: {'state': 'closed'},
                445: {'state': 'open'}
            }
        }
        
        mock_msf_instance = MockMSF.return_value
        mock_msf_instance.connect.return_value = True
        mock_msf_instance.execute_eternalblue.return_value = "Job started: 123"
        
        # Init Engine
        engine = AttackEngine("192.168.1.10", "pass", "192.168.1.5")
        engine.run()
        
        # Verify MSF connected and executed
        mock_msf_instance.connect.assert_called_once()
        mock_msf_instance.execute_eternalblue.assert_called_once()

if __name__ == '__main__':
    unittest.main()
