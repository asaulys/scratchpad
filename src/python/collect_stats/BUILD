py_library(
    name = "net",
    srcs = [
      "net/netstat.py"
    ],
)

py_binary(
    name = "collect_stats",
    main = "main.py",
    srcs = ["main.py"],
    deps = [
        ":net",  # a py_library
    ],
)
