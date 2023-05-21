trap "kill 0" EXIT

set -e

if [[ -z "${BUILD_WORKING_DIRECTORY}" ]]; then
    cd ../..
else
    echo $BUILD_WORKING_DIRECTORY
    cd $BUILD_WORKING_DIRECTORY
fi

if [[ -z "${PREBUILT}" ]]; then
    echo "Building Server"
    bazel build //src/server:hello-world
    sleep 1
fi

echo "Starting Server..."
./bazel-bin/src/server/hello-world

wait