# Collect Stats

## Overview
Born out of an interview question and my resulting fumble. Lots to do.

The (currently) primary entry point is actually net/netstat.py. See examples for details.

## Examples
**run netstat sampling**

`bazel run src/python/collect_stats:net_netstat`

**run netstat tests**

`bazel test tests/python/collect_stats:test_net_netstat`

## Known Issues
- Too many *TODO*s
- Bazel configuration requires additional work. should not need to specify 'scratchpad'
- Our puppy **LOVES** to demand attention when I'm on my laptop. This currently blocks all issues. (jk)
