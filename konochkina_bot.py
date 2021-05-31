import telebot
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import requests
import json



driver = webdriver.Chrome("/chromedriver")

with open('token.txt') as tk:
    token = tk.read().strip()

bot = telebot.TeleBot(token)

parsed = False


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот по поиску видео в YouTube.\nПереходи к просмотру "
                                      "прямо из Телеграм, сохраняй ссылки на видео в избранное или отправляй друзьям, "
                                      "не выходя из приложения.\nЧтобы найти видео по названию, "
                                      "введи команду /search_videos.\nЧтобы посмотреть тренды YouTube введи /trends."
                                      "\nДля просмотра списка команд введи /help.")


@bot.message_handler(commands=['search_videos'])
def search_videos(message):
    msg = bot.send_message(message.chat.id, "Введите текст, который вы хотите найти в YouTube")
    bot.register_next_step_handler(msg, search)

@bot.message_handler(commands=['trends'])
def trends(message):
    msg = bot.send_message(message.chat.id, "Посмотрим, что сегодня в тренде YouTube")
    search_trends(message)

@bot.message_handler(commands=['help'])
def help(message):
    msg = bot.send_message(message.chat.id, "/start — получение информации о боте\n/search_videos — поиск видео по "
                                            "названию\n/trends — обзор видео в трендах YouTube")

@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, "Ты что-то хотел?")

def search(message):
    bot.send_message(message.chat.id, "Начинаю поиск")
    video_href = "https://www.youtube.com/results?search_query=" + message.text
    driver.get(video_href)
    sleep(2)
    videos = driver.find_elements_by_id("video-title")
    for i in range(len(videos)):
        bot.send_message(message.chat.id, videos[i].get_attribute('href'))
        if i == 2:
            break

def search_trends(message):
    bot.send_message(message.chat.id, "Начинаю поиск трендов")
    video_href = "https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl"
    driver.get(video_href)
    sleep(2)
    videos = driver.find_elements_by_id("video-title")
    for i in range(len(videos)):
        bot.send_message(message.chat.id, videos[i].get_attribute('href'))
        if i == 4:
            break


bot.polling()
