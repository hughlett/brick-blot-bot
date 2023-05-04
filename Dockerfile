FROM python:3
COPY . /brick_blot_bot
WORKDIR /brick_blot_bot
RUN pip install -r requirements.txt
RUN ["chmod", "+x", "./wait-for-it.sh"]
CMD ["python3", "brick_blot_bot.py"]