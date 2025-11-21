#!/bin/bash -xe
sudo docker run --interactive --tty --rm --privileged --pid=host \
  -e HOST=${HOSTNAME} \
  -v ${PWD}:/work \
  -v /usr/bin/coredumpctl:/usr/bin/coredumpctl:ro \
  -v /usr/bin/varnishadm:/usr/bin/varnishadm:ro \
  -v /var/lib/varnish:/var/lib/varnish:ro \
  -v /usr/lib64/libvarnishapi.so.3:/usr/lib64/libvarnishapi.so.3:ro \
  -v /etc/varnish/secret:/etc/varnish/secret:ro \
  -v /bin/systemctl:/bin/systemctl:ro \
  -v /run/systemd/system:/run/systemd/system:ro \
  -v /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket:ro \
  -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
  -v /var/log/journal:/var/log/journal:ro \
  -v /run/log/journal:/run/log/journal:ro \
  -v /var/lib/systemd/coredump:/var/lib/systemd/coredump:ro \
  --entrypoint /bin/bash \
  ghcr.io/managedkaos/panic-sweeper-sandbox:main clean
  yum-dss.bamtech.co/hulu-docker/mediadistribution/panic-sweeper/panic-sweeper:${IMAGE_TAG:-feature_containerize-27} ping
  yum-dss.bamtech.co/hulu-docker/mediadistribution/panic-sweeper/panic-sweeper:${IMAGE_TAG:-feature_containerize-27}
