import os
import json
import pandas as pd
import datetime
import requests

#List part#
GameFile_List = []
File_List = []
Game_ID = []
Game_Day = []
Day_Range = []
Box = []
Box1 = []
#List part#



# def part #
def JsonkeyTest(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False

    return True

def dashdel(date):
    if "-" in date:
        date = date.split("-")
        return date[0]+date[1]+date[2]
    else:
        return date[0:4]+"-"+date[4:6]+"-"+date[6:8]
# def part #

# Day Range
Day_Range = pd.date_range('20240321', dashdel(str(datetime.date.today())))
# Day Range


# file name 가져오기
dir = "Mlb_Game_Data"
file = os.listdir(dir)
for A in file:
    File_List.append(A[0:10])
# file name 가져오기


# Mlb_Game_Data 에서 gamePk 긁어오기
for File_Name in File_List:
    with open("Mlb_Game_Data/"+File_Name+".txt", "r", encoding="utf-8") as f:
        #print(File_Name+"읽기")
        j = json.load(f)
        A = j["body"]
        if not JsonkeyTest(A, "0") == False:
            KeyList = list(A.keys())
            KeyList.pop()
            for GameNumber in KeyList:
                GameData = A[str(GameNumber)]
                Box1.append(GameData["gamePk"])
                if not GameData["officialDate"] in Game_Day:
                    GameStatus = GameData["status"]
                    if not GameStatus["detailedState"] == "Postponed":
                        Game_Day.append(GameData["officialDate"])
            Game_ID.append(Box1)
            Box1 = []
        else:
            #print(File_Name+"없음")
            Box.append(File_Name)



for A in Box:
    if os.path.isdir("Mlb_Playbyplay_Data\\"+A) == False:
        os.makedirs("Mlb_Playbyplay_Data\\"+A, exist_ok=True) #내용 없는 애들 날자 파일만 만들어주기
# Mlb_Game_Data 에서 gamePk 긁어오기


for A in Game_Day:
    if os.path.isdir("Mlb_Playbyplay_Data\\"+A) == False:
        os.makedirs("Mlb_Playbyplay_Data\\"+A, exist_ok=True)


#game file name 가져오기
dir = "Mlb_Playbyplay_Data"
file = os.listdir(dir)
for A in file:
    File_List.append(A[0:10])
#game file name 가져오기


# 긁어온 Game ID = gamePk 로 game api 부르기 + 검수 절차도 포함 [[[[[[[[잘못하면 돈 날아간다]]]]]]]]]]
for i in range(len(Game_Day)):
    print(Game_Day[i])
    for gameid in Game_ID[i]:
        if os.path.isfile("Mlb_Playbyplay_Data\\"+Game_Day[i]+"\\"+str(gameid)+".txt") == False:
            url = "https://baseball4.p.rapidapi.com/v1/mlb/games-playbyplay"
            querystring = {"gamePk":gameid}
            headers = {
                "x-rapidapi-key": "비밀^^",
                "x-rapidapi-host": "baseball4.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, params=querystring)
            j = response.json()
            data = json.dumps(j, ensure_ascii=False, indent=3, sort_keys=True)
            with open("Mlb_Playbyplay_Data\\"+Game_Day[i]+"\\"+str(gameid)+".txt", "w", encoding="utf-8") as file:
                file.write(data)
# 긁어온 Game ID = gamePk 로 game api 부르기 + 검수 절차도 포함