import argparse
import logging
import re
import subprocess
import typing

from dataclasses import dataclass


logger = logging.getLogger("scratchpad.src.python.collect_stats.net.netstat")
logger.setLevel(logging.DEBUG)

NETSTAT_COMMAND = [
    "netstat",
    "-tupn",
]
# TODO - this is a trivial parsing implementation. We should use something like 'jc' if we call
# netstat directly or just use a library to provide this data.
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


def run_command(**kwargs: typing.Dict[str, typing.Any]) -> typing.Generator[str, None, None]:
    """run_command executes the netstat command to obtain data.

    OPTIONAL key-word arguments:
      capture_output (bool): True - whether to pass back stdout and stderr
      timeout (float): time to allow the process to run

    yields strings representing the captured output lines
    """
    # set up subprocess
    options: typing.Dict[typing.Any, typing.Any] = {
        "capture_output": kwargs.get("capture_output", True),
        "timeout": float(kwargs.get("timeout", 1.0)),  # type: ignore
    }
    # prepare to run command
    logger.debug(f"running {NETSTAT_COMMAND = } with {options = }")
    process = subprocess.run(NETSTAT_COMMAND, **options)
    # TODO: we could handle exceptions and|or stderr
    for line in process.stdout.decode().split("\n"):
        logger.debug(f"yielding {line = }")
        yield (line.rstrip())


def parse_netstat_output(
    output: typing.Iterable[str],
) -> typing.Optional[typing.Generator[dict, None, None]]:
    """parse_netstat_output() - iterates over lines of output from netstat and attempts to create
       a dictionary via regex pattern match

     output: a list of strings representing lines from netstat. e.g.:
     tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2183/cupsd
     tcp        12     0 127.0.0.1:10001         0.0.0.0:*               LISTEN      46500/tumadre

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
        logger.debug(f"trying match for {line = }. got {result =}")
        if result:
            logger.debug(f"yielding {result.groupdict()= }")
            yield result.groupdict()
        else:
            logger.debug("no resulting match")
    return None


def count_queues(fields: typing.List[dict]) -> typing.Dict[str, int]:
    """count_queues() - discretely sums the receive and transmit queues. We expect these to be
    fields in a dictionary.

    Returns a dictionary with keys 'recvq' and 'sendq'
    """
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
    """helper used to execute this program when this file is called directly"""
    # generators
    output = run_command()
    fields = parse_netstat_output(output)
    # this terminates the generator sequence
    queues = count_queues(fields)
    return queues


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sums receive and transmit queues as reported by netstat"
    )
    parser.parse_args()
    print(process())
