# Using Ubuntu focal because python:3 was weird with pandas
FROM ubuntu:20.04

COPY . /brick_blot_bot
WORKDIR /brick_blot_bot
RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip install -r requirements.txt
CMD ["./wait-for-it.sh" , "http://chrome:4444" , "--" , "python3", "brick_blot_bot.py"]