import requests
import time
from mcstatus import MinecraftServer

lists = ["normal", "prio"]


def createFiles():
    for fileName in lists:
        try:
            open(f"{fileName}.txt", "r").close()
        except FileNotFoundError:
            open(f"{fileName}.txt", "w").close()


def sort(array):
    a = {}
    for ln in array:
        s = ln.split(" ")
        a[s[0]] = s[1]
    return a


def add(name, fileName):
    print(f"{name} joined using {fileName} queue")
    file = open(f"{fileName}.txt", "r+")
    lt = sort(file.readlines())

    if name in lt:
        return
    file.write(f"{name} {round(time.time())}\n")
    file.close()

    ind = 0
    if lists.index(fileName) == ind:
        ind = 1

    f = open(f"{lists[ind]}.txt", "r")
    ls = sort(f.readlines())
    f.close()

    if name in ls:
        remove(name, lists[ind], ls)


def remove(name, fileName, lst):
    del lst[name]
    file = open(f"{fileName}.txt", "w")
    for dt in lst:
        file.write(f"{dt} {lst[dt]}")
    file.close()


createFiles()
oldQueuePlayerList = requests.get("https://2bqueue.info/players").json()["queue"]["players"]
oldMainPlayerList = requests.get("https://2bqueue.info/players").json()["server"]["players"]

online = 0
while True:
    upd = False

    try:
        online = MinecraftServer.lookup("2b2t.org").status().players.online
    except:
        online = 0
    print(online)

    while online < 300:
        upd = True
        try:
            online = MinecraftServer.lookup("2b2t.org").status().players.online
        except:
            online = 0
        print(online)
        time.sleep(2)

    fl = open(f"{lists[1]}.txt", "r")
    plist = sort(fl.readlines())
    fl.close()
    for data in plist.copy():
        if (round(time.time()) - float(plist[data])) > (86400 * 30):
            remove(data, lists[1], plist)

    try:
        if upd:
            oldQueuePlayerList = requests.get("https://2bqueue.info/players").json()["queue"]["players"]
            oldMainPlayerList = requests.get("https://2bqueue.info/players").json()["server"]["players"]

        time.sleep(4)

        newQueuePlayerList = requests.get("https://2bqueue.info/players").json()["queue"]["players"]
        newMainPlayerList = requests.get("https://2bqueue.info/players").json()["server"]["players"]

        for line in newMainPlayerList:
            if line not in oldMainPlayerList:
                if line in oldQueuePlayerList:
                    add(line, lists[0])
                else:
                    add(line, lists[1])

        for line in newQueuePlayerList:
            if line not in oldQueuePlayerList:
                add(line, lists[0])

        oldMainPlayerList = newMainPlayerList
        oldQueuePlayerList = newQueuePlayerList
    except:
        print("something scary happened")
        time.sleep(4)

    online = 0
