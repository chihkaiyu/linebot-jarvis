rm:
	docker-compose down
run:
	docker-compose up -d
in:
	docker exec -ti linebotjarvis_bot_1 /bin/bash
build:
	docker build -t linebot ./bot
	docker rmi `docker images | grep '^<none>' | awk '{print $$3}'`
upgrade:
	make rm
	make build
	make run
logs:
	docker logs linebotjarvis_bot_1
push:
	git push origin master
	git push origin develop