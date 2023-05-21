load("@rules_cc//cc:defs.bzl", "cc_binary", "cc_library")

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "hello-greet",
    srcs = ["hello-greet.cpp"],
    hdrs = ["hello-greet.hpp"],
)

cc_binary(
    name = "hello-world",
    srcs = ["hello-world.cpp"],
    deps = [
        ":hello-greet",
        "//src/lib:hello-time",
        # "@boost//:process"
    ],
)

sh_binary(
    name = "run",
    srcs = ["run.sh"],
)