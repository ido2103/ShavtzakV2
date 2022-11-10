import json
import random
import copy


def append_json(name: str, sg, tapuz, hamal, siur, kka, mitbah, restingHours, mitbahCD, isHamal, isPtorMitbah, isPtorShmira, isSevevMp, division):
    temp_dict = {"Name:": name, "S.G:": sg, "Tapuz:": tapuz, "Hamal:": hamal, "Siur:": siur, "Mitbah:": mitbah,
            "Kaf Kaf A:": kka,
            "Resting Hours:": restingHours,
            "Mitbah Cooldown:": mitbahCD,
            "IsHamal": isHamal,
            "IsPtorMitbah": isPtorMitbah,
            "IsPtorShmira": isPtorShmira,
            "Sevev": isSevevMp,
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
                and (i["IsPtorMitbah"] == "No"):
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
        if (i["Resting Hours:"] <= 0) and (i[type] <= highestShmira) and(i["IsPtorShmira"] == "No"):
            # this section makes it linear. the more difference there is between the current soldier and the soldier
            # with the highest mitbah value the more likely it is to pick them.
            for n in range(i[type], highestShmira+1):
                options.append(i)
    return random.choice(options), data


def doHamal(data):
    options = []
    highestHamal = highest(data, "Hamal:")
    for i in data:
        if (i["Resting Hours:"] <= 0) and (i["Hamal:"] <= highestHamal) and (i["IsHamal"] == "Yes"):
            for n in range(i["Hamal:"], highestHamal+1):
                options.append(i)
    try:
        a = random.choice(options)
    except Exception:
        return {
            "Name:": "ERROR",
            "S.G:": 10,
            "Tapuz:": 18,
            "Hamal:": 0,
            "Siur:": 0,
            "Mitbah:": 7,
            "Kaf Kaf A:": 0,
            "Resting Hours:": 8,
            "Mitbah Cooldown:": 0,
            "IsHamal": "No",
            "IsPtorMitbah": "No",
            "IsPtorShmira": "No",
            "Sevev": "MP",
            "Division": 999
      }, data
    return a, data


def doSiur(data, amountOfSoldiers):
    # this function is the most complicated one since siurim have to be from the same division. first we get the
    # highest number of siurim from every division
    divisions = seperate_to_divisions(data)
    div1, div2, div3, div4 = [], [], [], []
    try:
        highest1 = highest(divisions[0], "Siur:")
    except Exception:
        pass
    try:
        highest2 = highest(divisions[1], "Siur:")
    except Exception:
        pass
    try:
        highest3 = highest(divisions[2], "Siur:")
    except Exception:
        pass
    try:
        highest4 = highest(divisions[3], "Siur:")
    except Exception:
        pass

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
                while len(temp) < amountOfSoldiers and count < 20:
                    a = random.choice(div1)
                    if a not in temp: temp.append(a)
                    count += 1
                div1 = temp

            if div2:
                temp = [random.choice(div2)]
                count = 0
                while len(temp) < amountOfSoldiers and count < 20:
                    a = random.choice(div2)
                    if a not in temp: temp.append(a)
                    count += 1
                div2 = temp
            if div3:
                temp = [random.choice(div3)]
                count = 0
                while len(temp) < amountOfSoldiers and count < 20:
                    a = random.choice(div3)
                    if a not in temp: temp.append(a)
                    count += 1
                div3 = temp
            if div4:
                temp = [random.choice(div4)]
                count = 0
                while len(temp) < amountOfSoldiers and count < 20:
                    a = random.choice(div4)
                    if a not in temp: temp.append(a)
                    count += 1
                div4 = temp
        case _:
            raise ValueError
    soldiers = []
    soldiers.append(div1)
    soldiers.append(div2)
    soldiers.append(div3)
    soldiers.append(div4)
    for j in soldiers:
        for i in soldiers:
            if not i:
                soldiers.remove(i)
    a = random.choice(soldiers)
    if amountOfSoldiers == 1:
        return [a], data
    return a, data


def KafKafA(data, amountOfKKA):
    divisions = seperate_to_divisions(data)
    div1, div2, div3, div4 = [], [], [], []
    try:
        highest1 = highest(divisions[0], "Kaf Kaf A:")
        highest2 = highest(divisions[1],"Kaf Kaf A:")
        highest3 = highest(divisions[2], "Kaf Kaf A:")
        highest4 = highest(divisions[3], "Kaf Kaf A:")
    except IndexError:
        pass
    if amountOfKKA == 1:
        return [random.choice(data)], data
    for i in data:
        match i["Division"]:
            case 1:
                if i["Kaf Kaf A:"] <= highest1 and i["Resting Hours:"] <= 0:
                    for j in range(i["Kaf Kaf A:"], highest1+1):
                        div1.append(i)
            case 2:
                if i["Kaf Kaf A:"] <= highest2 and i["Resting Hours:"] <= 0:
                    for j in range(i["Kaf Kaf A:"], highest2 + 1):
                        div2.append(i)
            case 3:
                if i["Kaf Kaf A:"] <= highest3 and i["Resting Hours:"] <= 0:
                    for j in range(i["Kaf Kaf A:"], highest3 + 1):
                        div3.append(i)
            case 4:
                if i["Kaf Kaf A:"] <= highest4 and i["Resting Hours:"] <= 0:
                    for j in range(i["Kaf Kaf A:"], highest4 + 1):
                        div4.append(i)
            case _:
                pass
    if div1:
        temp = [random.choice(div1)]
        count = 0
        while len(temp) < amountOfKKA and count <= 20:
            a = random.choice(div1)
            if a not in temp: temp.append(a)
            count += 1
        div1 = temp
    if div2:
        temp = [random.choice(div2)]
        count = 0
        while len(temp) < amountOfKKA and count <= 20:
            a = random.choice(div2)
            if a not in temp: temp.append(a)
            count += 1
        div2 = temp
    if div3:
        temp = [random.choice(div3)]
        count = 0
        while len(temp) < amountOfKKA and count <= 20:
            a = random.choice(div3)
            if a not in temp: temp.append(a)
            count += 1
        div3 = temp
    if div4:
        temp = [random.choice(div4)]
        count = 0
        while len(temp) < amountOfKKA and count <= 20:
            a = random.choice(div4)
            if a not in temp: temp.append(a)
            count += 1
        div4 = temp
    soldiers = [div1, div2, div3, div4]
    r = random.choice(soldiers)
    return r, data


def return_score(data, soldiers):
    list_sg = []
    list_tapuz = []
    list_hamal = []
    list_siur = []
    for i in soldiers:
        if i[1] == "SG": list_sg.append(i[0])
        elif i[1] == "Tapuz": list_tapuz.append(i[0])
        elif i[1] == "Siur": list_siur.append(i[0])
        elif i[1] == "Hamal": list_hamal.append(i[0])
        else: pass
    all_soldiers = list_sg + list_tapuz + list_hamal + list_siur
    score = 0
    for i in range(len(all_soldiers)):
        if all_soldiers[i] == "ERROR":
            score -= 999
        if (i + 2 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+2]):
            if i > 12: score -= 15
            else: score -= 15
        elif (i + 3 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+3]):
            if i > 12: score -= 10
            else: score -= 5
        elif (i + 4 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+4]):
            score -= 3
        elif (i + 5 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i + 5]):
            score -= 3
        elif (i + 11 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+11]):
            score -= 15
        elif (i + 10 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i + 10]):
            score -= 10
        elif (i + 4 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+4]):
            if i > 12: score -= 10
            else: score -= 3
        else: score += 10
    for i in data:
        if i["Name:"] not in soldiers:
            score -= 1
        else: pass
    return score


def sevev_json(sevev, list_to_remove):
    with open("soldiers.json", "r") as f:
        data_to_iter = json.load(f)
        for i in data_to_iter:
            for n in i:
                try:
                    i[n] = int(i[n])
                except ValueError:
                    pass
    for j in range(len(list_to_remove)):
        for i in data_to_iter: # TEST IT
            if i["Name:"] in list_to_remove:
                try:
                    data_to_iter.remove(i)
                except Exception as exc:
                    print(exc)

    if sevev == "מפ":
        for j in range(len(data_to_iter)):
            for i in data_to_iter:
                if i["Sevev"] != "MP":
                    data_to_iter.remove(i)

    if sevev == "סמפ":
        for j in range(len(data_to_iter)):
            for i in data_to_iter:
                if i["Sevev"] != "SMP":
                    data_to_iter.remove(i)


    with open("json_to_iter.json", "w") as f:
        json.dump(data_to_iter, f, indent=2)


def cycle(data, amountOfSoldiers, amountOfSiurim, amountOfKKA, num):
    soldiers = []
    # First thing's first, doing the mitbah and giving them a 24 hour break from doing missions.
    if num == 1:
        for i in data:
            if i["Mitbah Cooldown:"] > 0:
                i["Mitbah Cooldown:"] -= 1
        mitbah, data = doMitbah(data)
        for i in mitbah:
            i["Mitbah:"] += 1
            i["Mitbah Cooldown:"] = 2
            i["Resting Hours:"] = 24
            soldiers.append((i, "Mitbah"))
        kafkafa, data = KafKafA(data, amountOfKKA)
        for i in kafkafa:
            for j in data:
                if i["Name:"] == j["Name:"]:
                    j["Kaf Kaf A:"] += 1
                    j["Resting Hours:"] = 28
            soldiers.append((i, "Kaf Kaf A"))
    # then, we need to do the hamal.
    if num % 2 == 1:
        hamal, data = doHamal(data)
        hamal["Hamal:"] += 1
        hamal["Resting Hours:"] = 16
        soldiers.append((hamal, "Hamal"))
    # then, siur.
    if num == 1 or (num == 3 and amountOfSiurim > 1) or (num == 5 and amountOfSiurim > 2):
        siur, data = doSiur(data, amountOfSoldiers)
        for i in siur:
            i["Siur:"] += 1
            i["Resting Hours:"] = 16
            soldiers.append((i, "Siur"))
    # finally, smirot.
    tapuz, data = doShmira(data, "Tapuz:")
    tapuz["Tapuz:"] += 1
    tapuz["Resting Hours:"] = 12
    sg, data = doShmira(data, "S.G:")
    sg["S.G:"] += 1
    sg["Resting Hours:"] = 12
    soldiers.append((tapuz, "Tapuz"))
    soldiers.append((sg, "SG"))
    for i in data:
        if i["Resting Hours:"] > 0:
            i["Resting Hours:"] -= 4
    return soldiers, data


def computeList(amountOfSoldiers, amountOfSiurim, amountOfKKA, attempts, sevev, inactive):
    best_score = -999
    sevev_json(sevev, inactive)
    for j in range(attempts):
        with open("json_to_iter.json", "r") as f:
            data_to_iter = json.load(f)
        soldiers = []
        for i in range(1, 7):
            try:
                temp, data_to_iter = (cycle(data_to_iter, amountOfSoldiers, amountOfSiurim, amountOfKKA, i))
            except TypeError:
                pass
            for key in temp:
                soldiers.append((key[0]["Name:"], key[1]))
        temp_score = return_score(data_to_iter, soldiers)
        if temp_score > best_score:
            best_soldiers = soldiers
            best_score = temp_score
            best_data = copy.deepcopy(data_to_iter)
        if j % 100 == 0: print(j)
    # replace the values of the soldiers in soldiers.json with the ones we just iterated through
    with open("soldiers.json", "r") as f:
        all_data = json.load(f)

    for i in all_data:
        for j in best_data:
            if i["Name:"] == j["Name:"]:
                i = j
                best_data.remove(j)

    with open("soldiers.json", "w") as f:
        f.seek(0)
        json.dump(all_data, f, indent=6)
    print(best_score)
    return best_soldiers
