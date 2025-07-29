#! /usr/bin/env bash

function test_bluer_objects_gif() {
    local options=$1

    local source_object_name=test_bluer_objects_clone-$(bluer_ai_string_timestamp_short)

    python3 -m bluer_objects.testing \
        create_test_asset \
        --object_name $source_object_name
    [[ $? -ne 0 ]] && return 1

    bluer_objects_gif \
        ~upload,$options \
        $source_object_name \
        --frame_duration 200 \
        --output_filename test.gif \
        --scale 2 \
        --suffix .png
}
