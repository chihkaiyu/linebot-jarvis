rm:
	docker-compose down
run:
	docker-compose up -d
in:
	docker exec -ti linebotjarvis_bot_1 /bin/bash
build:
	docker build -t linebot ./bot
upgrade:
	make rm
	docker rmi linebot
	make build
	make run
logs:
	docker logs linebotjarvis_bot_1
