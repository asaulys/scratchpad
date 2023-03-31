import logging
import re
import subprocess
import typing

from dataclasses import dataclass
from typing import List


logger = logging.getLogger("collect_stats.net.netstat")
logger.setLevel(logging.DEBUG)

# TODO - this is a trivial parsing implementation. We should use something like 'jc' if we call
# netstat directly or just use a library to provide this data.
# NETSTAT_COMMAND = ["netstat", "-tulpn",]
NETSTAT_COMMAND = [
  "netstat",
  "-tupn",
]
# TODO - opportunities: this doesn't match all possible output formats and could use improvements
# to enhance support.
RE_PATTERN = re.compile(
  r"^(?P<proto>\S{3,})\s+(?P<recvq>\d+)\s+(?P<sendq>\d+)\s+(?P<local>\S+)\s+(?P<remote>\S+)\s+(?P<state>\S+)\s+(?P<program>.*)\s*"
)

# Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
EXPECTED_NETSTAT_IP_OUTPUT = """
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2183/cupsd          
tcp        12      12 127.0.0.1:8001          0.0.0.0:*               LISTEN      45500/kubectl       
tcp        24      0 0.0.0.0:5355            0.0.0.0:*               LISTEN      1852/systemd-resolv 
tcp        0      13 192.168.122.1:53        0.0.0.0:*               LISTEN      2950/dnsmasq        
udp        15     15 172.20.10.202:50314     142.250.190.67:443      ESTABLISHED 7078/brave --type=u  
"""

# @dataclass
# class NetstatIPOutput:
#   proto: str
#   recv-q: int
#   send-q: int
#   local-addr: str
#   remote-addr: str
#   state: str
#   program: str

#   @classmethod
#   def from_string(cls, input: str) -> typing.Optional[netstat_ip_output]:
#     # TODO - this is a trivial parsing implementation. We should use something like 'jc' to handle
#     #        all of the output cases
#     fields = input.rstrip.split()
#     if "Proto" in fields and "Recv-Q" in fields:
#       return
#     if len(fields) == 7 and ("tcp" in field[0] or "udp" in field[0]):
#       return cls(*fields)
#     else:
#       raise NotImplementedError("unhandled input")


def run_command(**kwargs) -> str:
  """input: none
       OPTIONAL: capture_output (bool): True - passed to subprocess.run

  yields strings representing the captured output
  """
  # set up subprocess
  options = {
    "capture_output": kwargs.get("capture_output", True),
    "timeout": kwargs.get("timeout", 1.0)
  }
  # prepare to run command
  logger.debug(f"running {NETSTAT_COMMAND = } with {options = }")
  process = subprocess.run(NETSTAT_COMMAND, **options)
  # TODO: we could handle exceptions and|or stderr
  for line in process.stdout.decode().split("\n"):
    logger.debug(f"yielding {line = }")
    yield (line.rstrip())


def parse_netstat_output(output: str) -> typing.Optional[dict]:
  """output: a line from netstat
   tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2183/cupsd

   yields a dictionary representing parsed output
  {'proto': 'tcp',
   'recvq': '12',
   'sendq': '12',
   'local': '127.0.0.1:8001',
   'remote': '0.0.0.0:*',
   'state': 'LISTEN',
   'program': '45500/kubectl'}
  """

  for line in output:
    result = RE_PATTERN.match(line)
    if not result:
      logger.debug(f"returning None for: {line = }")
      return None
    yield result.groupdict()


def count_queues(fields: List[dict]):
  recvq = 0
  sendq = 0
  for field_group in fields:
    if not field_group:
      continue
    if recvq != 0 or sendq != 0:
      logger.debug(f"non-zero queue found {field_group = }")
    recvq = int(field_group.get("recvq", 0)) + recvq
    sendq = int(field_group.get("sendq", 0)) + sendq
  return {"recvq": recvq, "sendq": sendq}


def process():
  """ helper when this file is called directly
  """
  # generators
  output = run_command()
  fields = parse_netstat_output(output)
  # this terminates the generator sequence
  queues = count_queues(fields)
  return queues


if __name__ == "__main__":
  print(process())