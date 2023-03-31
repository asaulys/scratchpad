import unittest
from subprocess import CompletedProcess
from unittest.mock import patch

import scratchpad.src.python.collect_stats.net.netstat as netstat


# Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
FAKE_NETSTAT_STDOUT = b"""
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2183/cupsd          
tcp        12      12 127.0.0.1:8001          0.0.0.0:*               LISTEN      45500/kubectl       
tcp        24      24 0.0.0.0:5355            0.0.0.0:*               LISTEN      1852/systemd-resolv 
tcp        13      13 192.168.122.1:53        0.0.0.0:*               LISTEN      2950/dnsmasq        
"""
EXPECTED_RUN_COMMAND_LIST = [
    '',
    'tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2183/cupsd',
    'tcp        12      12 127.0.0.1:8001          0.0.0.0:*               LISTEN      45500/kubectl',
    'tcp        24      24 0.0.0.0:5355            0.0.0.0:*               LISTEN      1852/systemd-resolv',
    'tcp        13      13 192.168.122.1:53        0.0.0.0:*               LISTEN      2950/dnsmasq',
    ''
]


class TestNetNetstat(unittest.TestCase):

    @patch("subprocess.run")
    def test_run_command_output_formatted_correctly(self, mock_communicate):
      mock_communicate.return_value = CompletedProcess(
          args = ["mock_netstat_command"],
          returncode = 0,
          stdout=FAKE_NETSTAT_STDOUT,
          stderr="",
      )
      output = netstat.run_command()
      self.assertEqual(
          hasattr(output, "__iter__"),
          True,
          f"expected output to be an iterator. got: {type(output) = }"
      )
      iterated_output = [line for line in output]
      self.assertEqual(
          iterated_output,
          EXPECTED_RUN_COMMAND_LIST, 
      )

#    def test_count_queues_adds_correctly(self):


if __name__ == "__main__":
  unittest.main()









#@patch(subprocess.check_output)
#def test_call_to_main():
##    with patch("subprocess.check_output") as mock_check_output:
#        mock_check_output.return_value(EXPECTED_NETSTAT_NAP_OUTPUT)
        # import pdb
        # pdb.set_trace()
#        main(count=3)

# def run_netstat_nap():
#   #output = subprocess.check_output(NETSTAT_NAP_COMMAND)
#   output = EXPECTED_NETSTAT_NAP_OUTPUT
#   return output
# 
# def parse_netstat_output(output: str):
#     """expected input:
#         tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2183/cupsd          
# 
#         expected output:
#         ['tcp', '0', '0', '127.0.0.1:8001', '0.0.0.0:*', 'LISTEN', '45500/kubectl']
#     """
#     data = []
#     for line in output.split("\n"):
#       data.append(line.rstrip().split())
#     return data
# 
# def count_queues():
#     pass
# 
# def main(count:int = -1):
#     # try+except shutdown signal for clean monitoring/metric routing
#     while True:
#         if count != -1 and count > 0:
#             if count == 0:
#                 return
#             count -= 1
#         time.sleep(.300)
#         output = run_netstat_nap()
#         netstat_output_dict = parse_netstat_output(output)
#         print(count_queues(netstat_output_dict))
