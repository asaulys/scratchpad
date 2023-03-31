package(
    default_visibility = [
        "//visibility:__subpackages__",
        "//scratchpad/tests/python/collect_stats:__subpackages__",
    ]
)

py_library(
    name = "net",
    srcs = [
      "net/netstat.py"
    ],
)

py_binary(
    name = "net_netstat",
    main = "net/netstat.py",
    srcs = ["net/netstat.py",],
)

py_binary(
    name = "collect_stats",
    main = "main.py",
    srcs = ["main.py"],
    deps = [
        ":net",  # a py_library
    ],
)
