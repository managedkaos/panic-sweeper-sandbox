sweep clean upload shell ping put: tag
	./scripts/$(@).sh

panic: tag
	-sudo varnishadm debug.panic.worker &

status:
	sudo systemctl status varnish

tag:
	@echo "IMAGE_TAG=$(IMAGE_TAG)"

sync:
	rsync -avz -e ssh Makefile ./scripts ${LAB_USER}@${LAB_SERVER}:~
