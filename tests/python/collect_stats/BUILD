py_test(
    name = "all",
    srcs = [
      "*.py",
      "net/*.py",
    ],
)

py_test(
    name = "test_net_netstat",
    main = "net/test_netstat.py",
    srcs = ["net/test_netstat.py",],
    deps = [
        "//scratchpad/src/python/collect_stats:net",
    ],
    #visibility = [ 
    #    "//scratchpad/src/python/collect_stats:__pkg__",
    #    "//scratchpad/tests/python/collect_stats:__pkg__",
    #], 
)
