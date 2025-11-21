#!/bin/bash -xe
sudo /usr/local/bin/aws sts get-caller-identity

sudo /usr/local/bin/aws s3api put-object \
    --bucket panicsweeper-20251118191616480100000001 \
    --key test.txt
    --body "Hello, World!" \
    --content-type text/plain
