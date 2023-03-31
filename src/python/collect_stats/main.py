import argparse
import sys

from src.python.collect_stats.net import netstat

# TODO (ticket: as-1234): this impl is explicitly for netstat but should support numerous sampling methods
def main(args: argparse.Namespace):

  # handle arguments
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "-i",
    "--interval",
    dest="interval",
    default=1000,
    help="sampling interval in miliseconds",
  )
  args = parser.parse_args()

  # actual execution
  # TODO (ticket: as-2345): try+except shutdown signal for clean monitoring/metric routing
  sample_sleep_time_seconds = args.interval / 1000.0
  # TODO (ticket: as-3456): sleeping, and actual sampling should be in a separate file.
  #                       : sampling should latch (to a multiple of the interval) and minimize skew
  while True:
    if count != -1 and count > 0:
      if count == 0:
        return
      count -= 1
    time.sleep(sample_sleep_time_seconds)
    output = netstat.run_once()
    parsed_output = netstat.parse_output(output)
    print(netstat.get_queues(parsed_output))


if __name__ == "__main__":
  main()
