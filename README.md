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
- `/search + ____` Search for keywords and return 5 highest results
- `/remilia` Random Remilia-Scarlet artworks 

## Using Instructions

#### To run the bot

1. Required environments
   - Linux/Windows/Mac-OSX system
   - Python 3.x installed
   - [Python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot#installing) installed
   - Gigabytes of disk space (auto-cache cleaning to be developed soon)
   
2. To run
  
   - Leave your bot token in a file named `token` in project directory
   - Leave your pixiv.net cookie in a file named `cookie` in project directory
   - Open Terminal at folder
   - `$ python PiperPixivBot.py`
   
3. To maintain

   - Come back occasionally and try cleaning database folder (`./db/`) by deleting some files on your own preference

## Versions

#### 0.5.0

**beta5.0**

- New feature: `/remilia`
- Restructured in-memory data mechanism to incread efficiency 

#### 0.4.0

**beta4.0**

- New feature: `/search`
- Re-structure code to improve flexibility
- Cookies needed for searcher crawler

####0.3.2

**beta3.2**

- New feature: use `/downpid` to download the original size of artworks of PixivID
- Combine pictures of same PixivID to one message

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

- bug fix: `/help` msg spaces

####Back End

- Auto cache cleaning, based on LRU
- Multithreading
- MySQL

