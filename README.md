# Brick-Blot-Bot

## Description

Python program that scrapes data from [North Carolina State University campus police reports](https://safety2.oit.ncsu.edu/newblotter.asp) and posts the reports to [Twitter](https://twitter.com/brickblotbot).

## Requirements

- Either:
  - Windows install of Chrome installed under `C:\Program Files\Google\`.
  - Instance of [Selenium's standalone Chrome browser](https://github.com/SeleniumHQ/docker-selenium) on `localhost:4444`.
- Twitter API and Access tokens inside `.env`. See [the sample .env file](.env.sample) for an example of how the tokens should be added.

## Usage

1. `git clone https://github.com/drewrh/brick-blot-bot.git`
2. `cd ./brick-blot-bot`
3. `pip install -r requirements.txt`
4. `python3 ./brick_blot_bot.py`
