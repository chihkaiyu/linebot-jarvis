rm:
	docker-compose down
run:
	docker-compose up -d
in:
	docker exec -ti lienbotjarvis_bot_1 /bin/bash
build:
	docker build -t linebot_bot .
upgrade:
	make rm
	docker rmi linebot_bot
	make build
	make run
logs:
	docker logs linebotjarvis_bot_1
