rm:
	docker-compose down
run:
	docker-compose up -d
in:
	docker exec -ti linebotjarvis_bot_1 /bin/bash
build:
	docker build -t linebot ./bot
	# docker rmi `docker images | grep '^<none>' | awk '{print $$3}'`
upgrade:
	make rm
	make build
	make run
logs:
	docker logs linebotjarvis_bot_1
push:
	git co master
	git push origin master
	git co develop
	git push origin develop