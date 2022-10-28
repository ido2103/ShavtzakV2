import json


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
    try:
        lst = seperate_to_divisions(data)
        for i in lst:
            print(i, len(i))
        return data
    except Exception as exc:
        print(exc)


def seperate_to_divisions(json):
    # returns a list with everyone from all of the divisions
    divs = [[],[],[],[],[]]
    for d in range(len(json)):
        x = (json[d]["Name:"],json[d]["Division"])
        divs[int(x[1])-1].append(x)
    return divs

