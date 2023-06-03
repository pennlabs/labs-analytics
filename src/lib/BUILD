load("@rules_cc//cc:defs.bzl", "cc_library")

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "hello-time",
    srcs = ["hello-time.cpp"],
    hdrs = ["hello-time.hpp"],
)

cc_library(
    name = "file_client",
    srcs = ["file_client.cpp"],
    hdrs = ["file_client.hpp"],
    deps = [
        ":file_serializer",
    ],
    data = ["//logs:logs"]
)

cc_library(
    name = "file_serializer",
    srcs = ["file_serializer.cpp"],
    hdrs = ["file_serializer.hpp"],
    data = ["//logs:logs"]
)