#!/bin/bash -e

return_code=$1
build_dir=$2

print_progress() {
    for i in $(seq 1 5); do
        echo "Build in progress..."
        if [ "$i" -eq 3 ]; then
            >&2 echo "Warning..."
        fi
        if [ "$i" -eq 4 ]; then
            printf "package-installer\x1b[0;32m [100%%]\x1b[0m\n"
        fi
        sleep 0.1
    done
}

echo "[$(date +"%H:%M:%S")] Begin $build_dir"

echo "[$(date +"%H:%M:%S")] Begin $build_dir/stage0"
sleep 0.1
echo "[$(date +"%H:%M:%S")] End $build_dir/stage0"

echo "[$(date +"%H:%M:%S")] Begin $build_dir/stage1"
sleep 0.1
echo "[$(date +"%H:%M:%S")] End $build_dir/stage1"

echo "[$(date +"%H:%M:%S")] Begin $build_dir/stage2"


print_progress

if [ "$return_code" -eq 0 ]; then
    echo "[$(date +"%H:%M:%S")] End $build_dir/stage2"
    echo "Build finished"

    if [ $# -ge 2 ]; then
        mkdir -p "$build_dir"/deploy
        touch "$build_dir"/deploy/image_"$(date +'%Y-%m-%d')"-test-target-lite.img.xz
    fi
else
    >&2 echo "Build failed"
    exit "$return_code"
fi

echo "[$(date +"%H:%M:%S")] End $build_dir"

exit "$return_code"