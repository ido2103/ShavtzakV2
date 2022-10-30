import json
import random

def append_json(name: str, sg, tapuz, hamal, siur, mitbah, restingHours, mitbahCD, isHamal, isPtorMitbah, isPtorShmira, isSevevMp, division):
    temp_dict = {"Name:": name, "S.G:": sg, "Tapuz:": tapuz, "Hamal:": hamal, "Siur:": siur, "Mitbah:": mitbah,  "Resting Hours:": restingHours,
            "Mitbah Cooldown:": mitbahCD,
            "IsHamal": isHamal,
            "IsPtorMitbah": isPtorMitbah,
            "IsPtorShmira": isPtorShmira,
            "IsSevevMP": isSevevMp,
            "Division": division}
    with open("soldiers.json", "r+") as f:
        data = json.load(f)
        data.append(temp_dict)
        f.seek(0)
        json.dump(data, f, indent=6)
    return data


def seperate_to_divisions(json):
    # returns a list with everyone from all the divisions
    divs = [[],[],[],[],[]]
    for x in json:
        div = x["Division"]
        divs[div-1].append(x)
    return divs


def highest(data, string):
    high = sorted(data, key=lambda d: d[string], reverse=True)
    return high[0][string]


def doMitbah(data):
    # selects 2 soldiers to go to the kitchen.
    chosen = []
    options = []
    # get the soldier with the highest mitbah
    highestMit = highest(data, "Mitbah:")
    # adding only people who can go to the kitchen
    for i in data:
        if (i["Resting Hours:"] <= 0) and (i["Mitbah Cooldown:"] <= 0) and (i["Mitbah:"] <= highestMit)\
                and (i["IsPtorMitbah"] == "False"):
            # this section makes it linear. the more difference there is between the current soldier and the soldier
            # with the highest mitbah value the more likely it is to pick them.
            for n in range(i["Mitbah:"], highestMit):
                options.append(i)
    # select 2 random soldiers out of the list
    while len(chosen) < 2:
        a = random.choice(options)
        if a not in chosen: chosen.append(a)
    return chosen, data


def doShmira(data, type):
    options = []
    highestShmira = highest(data, type)
    for i in data:
        if (i["Resting Hours:"] <= 0) and (i[type] <= highestShmira):
            # this section makes it linear. the more difference there is between the current soldier and the soldier
            # with the highest mitbah value the more likely it is to pick them.
            for n in range(i[type], highestShmira):
                options.append(i)
    return random.choice(options), data


def doHamal(data):
    options = []
    highestHamal = highest(data, "Hamal:")
    for i in data:
        if (i["Resting Hours:"] <= 0) and (i["Hamal:"] <= highestHamal) and (i["IsHamal"] == "True"):
            for n in range(i["Hamal:"], highestHamal):
                options.append(i)
    return random.choice(options), data


def doSiur(data, amountOfSoldiers):
    # this function is the most complicated one since siurim have to be from the same division. first we get the
    # highest number of siurim from every division
    divisions = seperate_to_divisions(data)
    div1, div2, div3, div4 = [], [], [], []
    highest1 = highest(divisions[0], "Siur:")
    highest2 = highest(divisions[1], "Siur:")
    highest3 = highest(divisions[2], "Siur:")
    highest4 = highest(divisions[3], "Siur:")
    # separating everyone into their divisions
    for i in data:
        match i["Division"]:
            case 1:
                if (i["Siur:"] <= highest1) and (i["Resting Hours:"] <= 0):
                    for n in range(i["Siur:"], highest1):
                        div1.append(i)
                pass
            case 2:
                if (i["Siur:"] <= highest2) and (i["Resting Hours:"] <= 0):
                    for n in range(i["Siur:"], highest2):
                        div2.append(i)
                pass
            case 3:
                if (i["Siur:"] <= highest3) and (i["Resting Hours:"] <= 0):
                    for n in range(i["Siur:"], highest3):
                        div3.append(i)
                pass
            case 4:
                if (i["Siur:"] <= highest4) and (i["Resting Hours:"] <= 0):
                    for n in range(i["Siur:"], highest4):
                        div4.append(i)
                pass
            case _:
                pass
    match amountOfSoldiers:
        # setting up the soldiers to the same amount it was set to
        case 1:
            if div1: div1 = random.choice(div1)
            if div2: div2 = random.choice(div2)
            if div3: div3 = random.choice(div3)
            if div4: div4 = random.choice(div4)

        case 2:
            if div1:
                temp = [random.choice(div1)]
                while len(temp) < 2:
                    a = random.choice(div1)
                    if a not in temp: temp.append(a)
                div1 = temp
            if div2:
                temp = [random.choice(div2)]
                while len(temp) < 2:
                    a = random.choice(div2)
                    if a not in temp: temp.append(a)
                div2 = temp
            if div3:
                temp = [random.choice(div3)]
                while len(temp) < 2:
                    a = random.choice(div3)
                    if a not in temp: temp.append(a)
                div3 = temp
            if div4:
                temp = [random.choice(div4)]
                while len(temp) < 2:
                    a = random.choice(div3)
                    if a not in temp: temp.append(a)
                div4 = temp
        case _:
            raise ValueError
    soldiers = [div1, div2, div3, div4]
    a = random.choice(soldiers)
    if amountOfSoldiers == 1:
        return [a], data
    return a, data


def printAllFuncs(data):
    doMitbah(data)
    doHamal(data)
    doShmira(data, "Tapuz:")
    doShmira(data, "S.G:")
    doSiur(data, 2)


def cycle(data, amountOfSoldiers, amountOfSiurim, debug):
    soldiers = []
    # First thing's first, doing the mitbah and giving them a 24 hour break from doing missions.
    for i in data:
        if i["Mitbah Cooldown:"] > 0:
            i["Mitbah Cooldown:"] -= 1
    mitbah, data = doMitbah(data)
    for i in mitbah:
        i["Mitbah:"] += 1
        i["Mitbah Cooldown:"] = 2
        i["Resting Hours:"] = 24
    # then, we need to do the hamal.
    hamal, data = doHamal(data)
    hamal["Hamal:"] += 1
    hamal["Resting Hours:"] = 16
    # then, siur.
    siur, data = doSiur(data, amountOfSoldiers)
    for i in siur:
        i["Siur:"] += 1
        i["Resting Hours:"] = 16
    # finally, smirot.
    tapuz, data = doShmira(data, "Tapuz:")
    tapuz["Tapuz:"] += 1
    tapuz["Resting Hours:"] = 12
    sg, data = doShmira(data, "S.G:")
    sg["S.G:"] += 1
    sg["Resting Hours:"] = 12
    # lastly, resave the database with our brand new edited data.
    for i in mitbah:
        soldiers.append(i)
    soldiers.append(hamal)
    for i in siur:
        soldiers.append(i)
    soldiers.append(tapuz)
    soldiers.append(sg)
    for i in soldiers:
        i["Resting Hours:"] -= 4

    with open("soldiers.json", "w") as f:
        f.seek(0)
        json.dump(data, f, indent=6)
    return soldiers


