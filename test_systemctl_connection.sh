#!/bin/bash -xe

## Coredumps only
docker run --privileged \
  -v /var/lib/systemd/coredump:/var/lib/systemd/coredump \
  -v /run/systemd:/run/systemd \
  ghcr.io/managedkaos/panic-sweeper-sandbox:main

## More restrictive
docker run --cap-add=SYS_ADMIN \
  -v /var/lib/systemd/coredump:/var/lib/systemd/coredump:ro \
  -v /run/systemd:/run/systemd:ro \
  ghcr.io/managedkaos/panic-sweeper-sandbox:main
