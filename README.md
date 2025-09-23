# python-container-template

A template repo for container-ized Python applications.

## Development Setup

This template includes pre-commit hooks for code quality and security checks. To set up the development environment:

1. Install development dependencies:

   ```bash
   make development-requirements
   ```

2. Install pre-commit hooks:

   ```bash
   make pre-commit-install
   ```

3. Run pre-commit on all files (optional):

   ```bash
   make pre-commit-run
   ```

## Pre-commit Hooks

The following hooks are configured to run automatically on commit:

- **Black**: Code formatting with consistent style
- **isort**: Import sorting and organization
- **flake8**: Linting for code quality
- **bandit**: Security vulnerability scanning
- **detect-secrets**: Secret detection in code
- **Various checks includings**:
  - Merge conflict detection
  - YAML/JSON validation
  - Large file detection
  - Trailing whitespace removal
  - End-of-file fixes

## Available Make Targets

- `make development-requirements` - Install development dependencies
- `make pre-commit-install` - Install pre-commit hooks
- `make pre-commit-run` - Run pre-commit on all files
- `make pre-commit-clean` - Remove pre-commit hooks
- `make lint` - Run linting tools manually
- `make fmt` - Format code with black and isort


https://stackoverflow.com/questions/72829097/is-there-a-way-to-know-the-status-of-a-systemctl-process-running-in-the-host-fro


```bash
docker run -it --rm \
  -v /bin/systemctl:/bin/systemctl:ro \
  -v /run/systemd/system:/run/systemd/system:ro \
  -v /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket:ro \
  -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
  ghcr.io/managedkaos/panic-sweeper-sandbox:main \
  systemctl --no-pager status varnish
```

```Makefile
test: pull
	docker run  --network=host --interactive --tty --rm \
		-v /var/lib/varnish:/var/lib/varnish:ro \
		-v /usr/bin/coredumpctl:/usr/bin/coredumpctl:ro \
		-v /var/lib/systemd/coredump:/var/lib/systemd/coredump:ro \
		-v /bin/systemctl:/bin/systemctl:ro \
		-v /run/systemd/system:/run/systemd/system:ro \
		-v /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket:ro \
		-v /sys/fs/cgroup:/sys/fs/cgroup:ro \
		-v $(PWD):/work \
		ghcr.io/managedkaos/panic-sweeper-sandbox:main

new: pull
	docker run  --network=host --interactive --tty --rm \
		-v /var/lib/varnish:/var/lib/varnish:ro \
		-v /var/lib/systemd/coredump:/var/lib/systemd/coredump:ro \
	    -v /var/log/journal:/var/log/journal:ro \
	    -v /run/log/journal:/run/log/journal:ro \
	    -v /bin/systemctl:/bin/systemctl:ro \
	    -v /usr/bin/coredumpctl:/usr/bin/coredumpctl:ro \
	    -v /run/systemd/system:/run/systemd/system:ro \
	    -v /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket:ro \
	    -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
	    -v $(PWD):/work \
	    ghcr.io/managedkaos/panic-sweeper-sandbox:main
c:
	docker run  --network=host --interactive --tty --rm \
		-v /var/lib/varnish:/var/lib/varnish \
		-v /var/lib/systemd/coredump:/var/lib/systemd/coredump \
		-v /bin/systemctl:/bin/systemctl:ro \
		-v /run/systemd/system:/run/systemd/system:ro \
		-v /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket:ro \
		-v /sys/fs/cgroup:/sys/fs/cgroup:ro \
		ghcr.io/managedkaos/panic-sweeper-sandbox:main bash
pull:
	docker pull ghcr.io/managedkaos/panic-sweeper-sandbox:main
```
