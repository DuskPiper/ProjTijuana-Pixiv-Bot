# ProjTijuana-Pixiv-Bot
A Telegram-based bot that helps browsing pixiv

## Introduction

This is a open-sourced Telegram Bot. This bot utilized Pixiv API to fetch artworks from pixiv.net.

## User Interface

Currently available commands are listed below.

- `/start`  Say hello to bot
- `/help`  Show tips
- `/pid + ____` Download and send you all artworks of a given Pixiv-ID
- `/uid + ____` Download and send you 5 most recent Pixiv-IDs' artworks

## Using Instructions

#### To run the bot

1. Required environments
   - Linux/Windows/Mac-OSX system
   - Python 3.x installed
   - [Python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot#installing) installed
   - Gigabytes of disk space (auto-cache cleaning to be developed soon)
   
2. To run
   
   - Leave your bot token in a file named `token` in project directory
   
   - Open Terminal at folder
   - `python PiperPixivBot.py`
   
3. To maintain

   - Come back occasionally and try cleaning database folder (`./db/`) by deleting some files on your own preference

## Versions

#### 0.3.1

**beta3.1**

- fix bug: crush on first run

#### 0.3.0

**beta3**

- stability improvements 

#### 0.2.0

**beta2**

- new function: `/uid` command
- bug fix

#### 0.1.0

**beta1**

- initial release

## Future Plans / `ToDo` List

#### Front End

- `/search` 
- Original quality artworks

####Back End

- Auto cache cleaning, based on LRU
- Multithreading
- MySQL

