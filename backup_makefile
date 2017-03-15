build:
	docker rmi linebot:latest
	docker build -t linebot .
run:
	docker run -d -p 443:443 --name linebot linebot
stop:
	docker stop linebot
	docker rm linebot
rm:
	docker rm linebot
in:
	docker exec -ti linebot_bot_1 /bin/bash
log:
	docker logs linebot
upgrade:
	make stop
	make build
	make run
