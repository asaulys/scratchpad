import typing
import unittest
from subprocess import CompletedProcess
from unittest.mock import MagicMock, patch

from scratchpad.src.python.collect_stats.net.netstat import (
    count_queues,
    parse_netstat_output,
    run_command,
)


# Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
NETSTAT_STDOUT_FIXTURE = b"""
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2183/cupsd          
tcp        12      12 127.0.0.1:8001          0.0.0.0:*               LISTEN      45500/kubectl       
tcp        0       24 0.0.0.0:5355            0.0.0.0:*               LISTEN      1852/systemd-resolv 
tcp        13      0  192.168.122.1:53        0.0.0.0:*               LISTEN      2950/dnsmasq        
udp        0       0  192.168.122.1:531       0.0.0.0:*               LISTEN      3950/dnsshark       
"""

COMMAND_OUTPUT_FIXTURE = [
    "",
    "tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2183/cupsd",
    "tcp        12      12 127.0.0.1:8001          0.0.0.0:*               LISTEN      45500/kubectl",
    "tcp        0       24 0.0.0.0:5355            0.0.0.0:*               LISTEN      1852/systemd-resolv",
    "tcp        13      0  192.168.122.1:53        0.0.0.0:*               LISTEN      2950/dnsmasq",
    "udp        0       0  192.168.122.1:531       0.0.0.0:*               LISTEN      3950/dnsshark",
    "",
]

PARSED_OUTPUT_FIXTURE = [
    {
        "proto": "tcp",
        "recvq": "0",
        "sendq": "0",
        "local": "127.0.0.1:631",
        "remote": "0.0.0.0:*",
        "state": "LISTEN",
        "program": "2183/cupsd",
    },
    {
        "proto": "tcp",
        "recvq": "12",
        "sendq": "12",
        "local": "127.0.0.1:8001",
        "remote": "0.0.0.0:*",
        "state": "LISTEN",
        "program": "45500/kubectl",
    },
    {
        "proto": "tcp",
        "recvq": "0",
        "sendq": "24",
        "local": "0.0.0.0:5355",
        "remote": "0.0.0.0:*",
        "state": "LISTEN",
        "program": "1852/systemd-resolv",
    },
    {
        "proto": "tcp",
        "recvq": "13",
        "sendq": "0",
        "local": "192.168.122.1:53",
        "remote": "0.0.0.0:*",
        "state": "LISTEN",
        "program": "2950/dnsmasq",
    },
    {
        "proto": "udp",
        "recvq": "0",
        "sendq": "0",
        "local": "192.168.122.1:531",
        "remote": "0.0.0.0:*",
        "state": "LISTEN",
        "program": "3950/dnsshark",
    },
]

COUNTED_QUEUE_FIXTURE = {"recvq": 25, "sendq": 36}


def yield_output(output):
    for item in output:
        yield item


class TestNetNetstat(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 2000

    @unittest.mock.patch(
        "scratchpad.src.python.collect_stats.net.netstat.subprocess.run"
    )
    def test_run_command_works_with_mock_output(self, mock_run):
        mock_run.return_value = CompletedProcess(
            args=["mock_netstat_command"],
            returncode=0,
            stdout=NETSTAT_STDOUT_FIXTURE,
            stderr="",
        )
        output = run_command()
        # TODO: why is this not indicating called when the test works?
        # self.assertEqual(
        #     mock_run.called,
        #     True,
        #     f"{mock_run._return_value.__dict__= } {mock_run.__dict__ =}, {repr(mock_run)=}",
        # )
        self.assertEqual(
            hasattr(output, "__iter__"),
            True,
            f"expected output to be an iterator. got: {type(output) = }",
        )
        iterated_output = [line for line in output]
        self.assertEqual(
            iterated_output,
            COMMAND_OUTPUT_FIXTURE,
        )

    def test_parse_netstat_output_returns_expected_lines(self) -> None:
        output = parse_netstat_output(yield_output(COMMAND_OUTPUT_FIXTURE))
        self.assertEqual(
            hasattr(output, "__iter__"),
            True,
            f"expected output to be an iterator. got: {type(output) = }",
        )
        iterated_output = [line for line in output]
        first_line = iterated_output[0]
        expected_keys = [
            "proto",
            "recvq",
            "sendq",
            "local",
            "remote",
            "state",
            "program",
        ]
        for k in expected_keys:
            with self.subTest(key=k):
                self.assertIn(
                    k,
                    first_line.keys(),
                )
        self.assertEqual(iterated_output, PARSED_OUTPUT_FIXTURE)

    def test_count_queues_sums_queues_correctly(self):
        output = count_queues(PARSED_OUTPUT_FIXTURE)
        self.assertEqual(output, COUNTED_QUEUE_FIXTURE)


if __name__ == "__main__":
    unittest.main()


# TODO implement and cleanup
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
