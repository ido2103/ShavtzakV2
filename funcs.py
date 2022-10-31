import json
import random
import copy


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
            for n in range(i["Mitbah:"], highestMit+1):
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
            for n in range(i[type], highestShmira+1):
                options.append(i)
    return random.choice(options), data


def doHamal(data):
    options = []
    highestHamal = highest(data, "Hamal:")
    for i in data:
        if (i["Resting Hours:"] <= 0) and (i["Hamal:"] <= highestHamal) and (i["IsHamal"] == "True"):
            for n in range(i["Hamal:"], highestHamal+1):
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
                    for n in range(i["Siur:"], highest1+1):
                        div1.append(i)
                pass
            case 2:
                if (i["Siur:"] <= highest2) and (i["Resting Hours:"] <= 0):
                    for n in range(i["Siur:"], highest2+1):
                        div2.append(i)
                pass
            case 3:
                if (i["Siur:"] <= highest3) and (i["Resting Hours:"] <= 0):
                    for n in range(i["Siur:"], highest3+1):
                        div3.append(i)
                pass
            case 4:
                if (i["Siur:"] <= highest4) and (i["Resting Hours:"] <= 0):
                    for n in range(i["Siur:"], highest4+1):
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

        case 2: # ADD: IF THEY LITERALLY DON'T HAVE ENOUGH PEOPLE FOR A SIUR THE WHILE LOOP'S STUCK INDEFINETLY.
            if div1:
                temp = [random.choice(div1)]
                count = 0
                while len(temp) < 2 and count < 10:
                    a = random.choice(div1)
                    if a not in temp: temp.append(a)
                    count += 1
                div1 = temp

            if div2:
                temp = [random.choice(div2)]
                count = 0
                while len(temp) < 2 and count < 10:
                    a = random.choice(div2)
                    if a not in temp: temp.append(a)
                    count += 1
                div2 = temp
            if div3:
                temp = [random.choice(div3)]
                count = 0
                while len(temp) < 2:
                    a = random.choice(div3)
                    if a not in temp: temp.append(a)
                    count += 1
                div3 = temp
            if div4:
                temp = [random.choice(div4)]
                count = 0
                while len(temp) < 2:
                    a = random.choice(div3)
                    if a not in temp: temp.append(a)
                    count += 1
                div4 = temp
        case _:
            raise ValueError
    soldiers = [div1, div2, div3, div4]
    for i in soldiers:
        if not i:
            soldiers.remove(i)
    a = random.choice(soldiers)
    if amountOfSoldiers == 1:
        return [a], data
    return a, data


def cycle(data, amountOfSoldiers, amountOfSiurim, debug, num):
    soldiers = []
    # First thing's first, doing the mitbah and giving them a 24 hour break from doing missions.
    if not debug:
        for i in data:
            if i["Mitbah Cooldown:"] > 0:
                i["Mitbah Cooldown:"] -= 1
    if num == 1:
        mitbah, data = doMitbah(data)
        for i in mitbah:
            if not debug:
                i["Mitbah:"] += 1
                i["Mitbah Cooldown:"] = 2
                i["Resting Hours:"] = 24
            soldiers.append((i, "Mitbah"))
    # then, we need to do the hamal.
    if num % 2 == 1:
        hamal, data = doHamal(data)
        if not debug:
            hamal["Hamal:"] += 1
            hamal["Resting Hours:"] = 16
        soldiers.append((hamal, "Hamal"))
    # then, siur.
    if num == 1 or (num == 3 and amountOfSiurim > 1) or (num == 5 and amountOfSiurim > 2):
        siur, data = doSiur(data, amountOfSoldiers)
        for i in siur:
            if not debug:
                i["Siur:"] += 1
                i["Resting Hours:"] = 16
            soldiers.append((i, "Siur"))
    # finally, smirot.
    tapuz, data = doShmira(data, "Tapuz:")
    if not debug:
        tapuz["Tapuz:"] += 1
        tapuz["Resting Hours:"] = 12
    sg, data = doShmira(data, "S.G:")
    if not debug:
        sg["S.G:"] += 1
        sg["Resting Hours:"] = 12
    soldiers.append((tapuz, "Tapuz"))
    soldiers.append((sg, "SG"))
    if not debug:
        for i in data:
            if i["Resting Hours:"] > 0:
                i["Resting Hours:"] -= 4
    return soldiers, data


def computeList(data, amountOfSoldiers, amountOfSiurim, debug):
    happy = "False"
    while happy != "True":
        dataToIter = copy.deepcopy(data)
        soldiers = []
        for i in range(1, 7):
            temp, dataToIter = (cycle(dataToIter, amountOfSoldiers, amountOfSiurim, debug, i))
            for key in temp:
                soldiers.append(key[0]["Name:"] + " " + key[1])
        print("\n".join(soldiers))
        happy = input("Are you happy with the given shavtzak? True/False")
    with open("soldiers.json", "w") as f:
        f.seek(0)
        json.dump(dataToIter, f, indent=6)
    return soldiers
