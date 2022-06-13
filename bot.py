from encodings import utf_8
import discord
from discord.ext import commands
import json
from bs4 import BeautifulSoup
import requests
import random 

bot = commands.Bot(command_prefix="J!")

with open("setting.json", "r", encoding="utf-8") as jfile:
    jdata = json.load(jfile)


@bot.event
async def on_ready():
    print(">> start")


@bot.command()
async def HI(ctx):
    await ctx.send("HI")


@bot.command()
async def ping(ctx):
    dcping = str(round(bot.latency * 1000)) + "(ms)"
    await ctx.send(dcping)


@bot.command()
async def ptt(ctx):
    url = "https://www.ptt.cc/bbs/movie/index.html"
    my_header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }
    res = requests.get(url, headers=my_header)
    soup = BeautifulSoup(res.text, "html.parser")
    title_list = soup.find_all("div", {"class": "title"})

    list = []
    for title in title_list:
        if title.a != None:
            list.append(title.a.string)

    link_soup = BeautifulSoup(str(title_list), "html.parser")
    title_link = link_soup.find_all("a")

    link_list = []
    for link in title_link:
        link = "https://www.ptt.cc" + link["href"]
        link_list.append(link)

    for post in range(0, len(list)):
        print(list[post] + ">>" + link_list[post])
        await ctx.send(list[post] + ">>" + link_list[post])


@bot.command()
async def daily(ctx):
    url = "https://fs1.app/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    day_new = soup.find_all("h6", {"class": "title"}, limit=8)
    # print(res.status_code)
    # print(day_new)

    link_list = []
    for link in day_new:
        link_list.append(link.a["href"])
    # print(link_list)

    with open ("url.json","r",encoding="utf8")as f:
        data = json.load(f)

    for i in range(0,len(link_list)):
        n = 0
        for j in range(0,len(data["url"])):
    
            if link_list[i] == data["url"][j]:
                n = n+1
        if n == 0:
            data["url"] = data["url"]+[link_list[i]]
            print("新增一筆至.json")
    with open ("url.json","w",encoding="utf8")as f:
        json.dump(data,f)

    for post in range(0, len(link_list)):
        print(link_list[post])
        await ctx.send(link_list[post])


@bot.command()
async def hot(ctx):
    url = "https://fs1.app/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    day_new = soup.find_all("div", {"class": "img-box cover-md"}, limit=8)

    link_list = []
    for link in day_new:
        link_list.append(link.a["href"])
    # print(link_list)

    with open ("url.json","r",encoding="utf8")as f:
        data = json.load(f)

    for i in range(0,len(link_list)):
        n = 0
        for j in range(0,len(data["url"])):
    
            if link_list[i] == data["url"][j]:
                n = n+1
        if n == 0:
            data["url"] = data["url"]+[link_list[i]]
            print("新增一筆至.json")
    with open ("url.json","w",encoding="utf8")as f:
        json.dump(data,f)

    for post in range(0, len(link_list)):
        print(link_list[post])
        await ctx.send(link_list[post])


@bot.command()
async def all(ctx):
    url = "https://fs1.app/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    day_new = soup.find_all("div", {"class": "img-box"})

    link_list = []
    for link in day_new:
        link_list.append(link.a["href"])
    # print(link_list)
    with open ("url.json","r",encoding="utf8")as f:
        data = json.load(f)

    for i in range(0,len(link_list)):
        n = 0
        for j in range(0,len(data["url"])):
    
            if link_list[i] == data["url"][j]:
                n = n+1
        if n == 0:
            data["url"] = data["url"]+[link_list[i]]
            print("新增一筆至.json")
    with open ("url.json","w",encoding="utf8")as f:
        json.dump(data,f)

    for post in range(0, len(link_list)):
        print(link_list[post])
        await ctx.send(link_list[post])

@bot.command()
async def rand(ctx):
    with open("url.json", "r", encoding="utf8")as f:
        data = json.load(f)
    JB_random = random.choice(data["url"])
    print(JB_random)
    print("已隨機挑選")
    #await ctx.send(JB_random)

    res = requests.get(JB_random)
    soup = BeautifulSoup(res.text, "html.parser")
    girl_img = soup.find("a", {"class": "model"})
    JB_title = soup.find("div", {"class":"header-left"})
    background_img = soup.find("meta", {"property": "og:image"})
    detail_html = soup.find_all("span", {"class": "mr-3"})
    detail_html_2 = soup.find("span", {"class": "count"})
    JB_time = detail_html[0].string
    JB_look = detail_html[1].string
    JB_like = detail_html_2.string
    background_link = background_img["content"]
    title_name = JB_title.h4.string
    girl_link = girl_img["href"]
    try:
        img_link = girl_img.img["src"]
        girl_name = girl_img.img["title"]
    except:
        girl_name = girl_img.span["title"]
        img_link = "https://assets.fs1.app/assets/images/logo.png"
    print(background_link,title_name,girl_link,img_link,girl_name,JB_time,JB_look,JB_like)

    embed=discord.Embed(title=title_name, url=JB_random, color=0xec416c)
    embed.set_author(name=girl_name, url=girl_link, icon_url=img_link)
    embed.set_thumbnail(url=background_link)
    embed.add_field(name="發行時間", value=JB_time, inline=False)
    embed.add_field(name="觀看人數", value=JB_look, inline=False)
    embed.add_field(name="按讚人數", value=JB_like, inline=False)
    await ctx.send(embed=embed)



@bot.command()
async def nowData(ctx):
    with open("url.json", "r", encoding="utf8")as f:
        data = json.load(f)
    print("目前資料共",len(data["url"]),"筆")
    await ctx.send("目前資料共"+str(len(data["url"]))+"筆")

@bot.command()
async def LoadData(ctx):
    for i in range(0,3):
        with open("url.json", "r", encoding="utf8")as f:
            data = json.load(f)
        JB_random = random.choice(data["url"])
        print(JB_random)

        url = JB_random
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        day_new = soup.find_all("div", {"class": "img-box"})

        link_list = []
        for link in day_new:
            link_list.append(link.a["href"])

        for post in range(0, len(link_list)):
            print(link_list[post])

        with open ("url.json","r",encoding="utf8")as f:
            data = json.load(f)
            print(len(data["url"]))

    a = 0
    for i in range(0,len(link_list)):
        n = 0
        for j in range(0,len(data["url"])):
        
            if link_list[i] == data["url"][j]:
                n = n+1
        if n == 0:
            data["url"] = data["url"]+[link_list[i]]
            print("已新增一筆至json")
            a = a+1
    print("共新增",a,"筆資料")
    print(data["url"])
    print("目前資料共",len(data["url"]),"筆")
    with open ("url.json","w",encoding="utf8")as f:
        json.dump(data,f)
    await ctx.send("共新增"+str(a)+"筆資料  目前資料共"+str(len(data["url"]))+"筆")





@bot.command()
async def search(ctx,*,msg):
    print("search "+msg)
    #await ctx.send("search "+item)
    url = "https://fs1.app//search/"+msg+"/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    day_new = soup.find_all("div", {"class": "img-box cover-md"})
    link_list = []
    for link in day_new:
        link_list.append(link.a["href"])
    # print(link_list)

    with open ("url.json","r",encoding="utf8")as f:
        data = json.load(f)

    for i in range(0,len(link_list)):
        n = 0
        for j in range(0,len(data["url"])):
    
            if link_list[i] == data["url"][j]:
                n = n+1
        if n == 0:
            data["url"] = data["url"]+[link_list[i]]
            print("新增一筆至.json")
    with open ("url.json","w",encoding="utf8")as f:
        json.dump(data,f)

    for post in range(0, len(link_list)):
        print(link_list[post])
        await ctx.send(link_list[post])

@bot.command()
async def i_want_cowcow(ctx):
    embed=discord.Embed(title="Jable bot helper", color=0xffd500)
    embed.set_author(name="I LOVE COWCOW", icon_url="https://assets.fs1.app/assets/icon/favicon.ico")
    embed.add_field(name="和 JABLE 說 HI", value="J!HI", inline=False)
    embed.add_field(name="搜尋", value="J!search", inline=False)
    embed.add_field(name="今日新片(8部)", value="J!daily", inline=False)
    embed.add_field(name="熱門(8部)", value="J!hot", inline=False)
    embed.add_field(name="所有影片", value="J!all", inline=False)
    embed.add_field(name="隨機選片", value="J!rand", inline=False)
    embed.add_field(name="顯示隨機庫數量", value="J!nowData", inline=False)
    embed.add_field(name="增加資料", value="J!LoadData", inline=False)
    await ctx.send(embed=embed)





bot.run(jdata["Token"])
