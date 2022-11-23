import json
import random
import copy


def append_json(name: str, sg, tapuz, hamal, siur, kka, mitbah, restingHours, mitbahCD, isHamal, isPtorMitbah, isPtorShmira, isSevevMp, division):
    # this function updates the json with the data by adding a dict to it.
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
    # this function finds the person with the highest rated string. it does it by making a list of
    # everyone with that data type, then reversign it and returing the first object.
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


def doShmira(data, type, highestShmira):
    """Works exactly the same as doHamal"""
    options = []
    for i in data:
        if (i["Resting Hours:"] <= 0) and (i["IsPtorShmira"] == "No"):
            # this section makes it linear. the more difference there is between the current soldier and the soldier
            # with the highest mitbah value the more likely it is to pick them.
            for n in range(i[type], highestShmira+1):
                options.append(i)
    return random.choice(options), data


def doHamal(data):
    """One of the generic functions. This function (and also shmirot) is very simple.
    psudo-randomly pick people for the hamal. what does that mean?
    Essentialy, this function looks at the highest value of a chosen mission
    (say hamal) and then checks to see who is available and is a hamalist.
    after it finds such an individual it adds him to a list for as many times as there
    is a gap between his hamal and the highest hamal. E.g. the highest hamal is 27 and Shmulik has 20 hamals.
    he will be added to the list 7 times. After the function does that to every individual it than randomly
    selects an individual. I.e psudo-random."""
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

        case 2:
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
    """This function decides which people get selected to be KKA based on their amount of kka recorded.
    This function is a bit more complicated (like the siur function) because it's essential that kka
    will be organic and thus only people from the same division get placed together."""
    divisions = seperate_to_divisions(data)
    div1, div2, div3, div4 = [], [], [], []
    try:
        highest1 = highest(divisions[0], "Kaf Kaf A:")
    except IndexError:
        pass
    try:
        highest2 = highest(divisions[1], "Kaf Kaf A:")
    except IndexError:
        pass
    try:
        highest3 = highest(divisions[2], "Kaf Kaf A:")
    except IndexError:
        pass
    try:
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
    for l in range(len(soldiers)):
        for i in soldiers:
            if len(i) < amountOfKKA:
                soldiers.remove(i)
    r = random.choice(soldiers)
    return r, data


def return_score(data, soldiers):
    """This function is very very important to the code.
    it lets us control the random shavtzaks the program makes by rating them to our choosing.
    by controling the score deduction the program will try to avoid a low number. hence why
    4/8 is rated -30 and 4/12 is rated -10. because we want the program to avoid placing people in 4/8
    as much as it possibly can."""
    list_sg = []
    list_tapuz = []
    list_hamal = []
    list_siur = []
    list_kka = []
    list_mitbah = []
    for i in soldiers:
        if i[1] == "SG": list_sg.append(i[0])
        elif i[1] == "Tapuz": list_tapuz.append(i[0])
        elif i[1] == "Siur": list_siur.append(i[0])
        elif i[1] == "Hamal": list_hamal.append(i[0])
        elif i[1] == "Kaf Kaf A": list_kka.append(i[0])
        elif i[1] == "Mitbah": list_mitbah.append(i[0])
        else: pass
    all_soldiers = list_sg + list_tapuz
    score = 0
    for i in range(len(all_soldiers)):
        if all_soldiers[i] == "ERROR":
            score -= 999
        #   4/8
        elif (i + 3 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+3]):
            score -= 25
        #   4/12
        elif (i + 4 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+4]):
            score -= 10
        #   4/16
        elif (i + 5 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i + 5]):
            score -= 5
        #   4/20
        elif (i + 6 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i + 6]):
            score -= 3
        #   4/8
        elif (i + 9 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+9]):
            score -= 25
        #   4/12
        elif (i + 10 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+10]):
            score -= 10
        #   4/16
        elif (i + 11 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i+11]):
            score -= 5
        #   4/20
        elif (i + 12 < len(all_soldiers)) and (all_soldiers[i] == all_soldiers[i + 12]):
            score -= 3
        elif all_soldiers[i] in list_hamal or all_soldiers[i] in list_siur:
            score -= 20
        else: score += 10
    if (list_hamal[0] or list_siur[0] == [all_soldiers[5]]) or (list_hamal[0] or list_siur[0] == [all_soldiers[10]]):
        score -= 35
    if (list_hamal[0] or list_siur[0] == [all_soldiers[6]]) or (list_hamal[0] or list_siur[0] == [all_soldiers[11]]):
        score -= 50
    for i in range(len(list_hamal)):
        if (i + 2 < len(list_hamal)) and (list_hamal[i] == list_hamal[i+2]):
            score -= 50
    for i in range(len(list_siur)):
        if (i + 2 < len(list_siur)) and (list_siur[i] == list_siur[i+2]):
            score -= 50
    for i in list_siur:
        if i in list_hamal:
            score -= 50
    for i in data:
        if i["Name:"] not in soldiers:
            score -= 1
        else: pass
    for i in list_kka:
        if i in list_mitbah:
            score -= 999
    return score


def sevev_json(sevev, list_to_remove):
    """This function creates a new json file to iterate through with the computeList function.
    This new json is without the inactive people (gimelim/sevev)"""
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
                    print(exc, 2)

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


def custom_mission(data, amount_of_people):
    """This function gets called whenever you add a custom mission.
    It will allocate the specified amount_of_people to the mission."""
    available_soldiers = []
    chosen_soldiers = []
    for i in data:
        if i["Resting Hours:"] <= 0:
            available_soldiers.append(i)
    for i in range(amount_of_people):
        rnd = random.choice(available_soldiers)
        chosen_soldiers.append(rnd)
        available_soldiers.remove(rnd)


    return data, chosen_soldiers


def cycle(data, amountOfSoldiers, amountOfSiurim, amountOfKKA, num, custom_name, custom_num):
    """This function is the core of the program. this function gets called 6 times.
    each time it is being called it operates differently based on the num value.
    it is responsible for calling the relevant functions in order to place the
    soldiers in the relevant functions."""
    soldiers = []
    # firstly we add all the stuff that are 1 time only such as mitbah, kka, and any custom missions.
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
            i["Kaf Kaf A:"] += 1
            i["Resting Hours:"] = 28
            soldiers.append((i, "Kaf Kaf A"))
        if custom_name != "":
            data, custom_soldiers = custom_mission(data, custom_num)
            for i in custom_soldiers:
                i["Resting Hours:"] = 24
                soldiers.append((i, "Custom"))
    # then, all the things that happend every other iteration (that take 8 hours) such as hamal, siur.
    if num % 2 == 1:
        hamal, data = doHamal(data)
        hamal["Hamal:"] += 1
        hamal["Resting Hours:"] = 16
        soldiers.append((hamal, "Hamal"))
    # siur is a bit more odd since there might be a need for only 1/2/3 siurim but hamal always has 3.
    if num == 1 or (num == 3 and amountOfSiurim > 1) or (num == 5 and amountOfSiurim > 2):
        siur, data = doSiur(data, amountOfSoldiers)
        for i in siur:
            i["Siur:"] += 1
            i["Resting Hours:"] = 16
            soldiers.append((i, "Siur"))
    # then, regardless of the num we do shmirot.
    highestShmira = highest(data, "Tapuz:")
    tapuz, data = doShmira(data, "Tapuz:", highestShmira)
    tapuz["Tapuz:"] += 1
    tapuz["Resting Hours:"] = 12
    highestShmira = highest(data, "S.G:")
    sg, data = doShmira(data, "S.G:", highestShmira)
    sg["S.G:"] += 1
    sg["Resting Hours:"] = 12
    soldiers.append((tapuz, "Tapuz"))
    soldiers.append((sg, "SG"))
    # after everyone has their new role for this cycle we remove 4 hours from everyone. this is
    # done to stimulate time passing.
    for i in data:
        if i["Resting Hours:"] > 0:
            i["Resting Hours:"] -= 4
    return soldiers, data


def computeList(amountOfSoldiers, amountOfSiurim, amountOfKKA, attempts, sevev, inactive, custom_name, custom_num):
    """This is the main function. This function is responsible for calling the cycle function for as many times
    as needed, rating it and keeping the best score. After it's done with that this function uploads the best
    shavtzak to the shavtzak.json file which is read in the GUI to construct the visible, user friendly
    shavtzak."""
    best_score = -999
    # make a json to iter through. this removes inactive people and considers only people from the chosen sevev.
    sevev_json(sevev, inactive)
    for j in range(attempts):
        # after testing, i've found that opening a json file is faster than using copy.deepcopy().
        with open("json_to_iter.json", "r") as f:
            data_to_iter = json.load(f)
        soldiers = []
        for i in range(1, 7):
            temp, data_to_iter = cycle(data_to_iter, amountOfSoldiers, amountOfSiurim, amountOfKKA, i,
                                            custom_name, custom_num)
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
    list_to_update = []
    for i in all_data:
        list_to_update.append(i)
    for i in range(len(all_data)):
        for j in range(len(best_data)):
            if all_data[i]["Name:"] == best_data[j]["Name:"]:
                list_to_update[i] = best_data[j]
    # finally dumps the information of the people not included in the shavtzak with the ones that are. that
    # happens in order to prevent data being deleted for someone because you didn't include them.
    return best_soldiers, best_score, list_to_update
