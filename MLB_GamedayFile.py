import datetime
import json
import pandas as pd
import requests
import os

## 날짜 하이폰 없는 버전=====##
ToDayH = datetime.date.today()
ToDay = str(ToDayH).split("-")
ToDay = ToDay[0]+ToDay[1]+ToDay[2]
##========================##


## LIST 섹션 ##
Miss_Day_Range = []
Day_Range = []
File_List = []

GameVenueId = []
GameVenueName = []
GameId = []
HomeGameProbablePicherId = []
HomeGameProbablePicherName = []
HomeGameTeamId = []
AwayGameProbablePicherId = []
AwayGameProbablePicherName = []
AwayGameTeamId = []
##------------##

def is_json_key_present(json, key):
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

###================MLB_Game_Data file downloder part=====================###
###================MLB_Game_Data file downloder part=====================###
url = "https://baseball4.p.rapidapi.com/v1/mlb/schedule"


d_list = pd.date_range('20250326', ToDay)
for A in d_list:
    Day_Range.append(str(A)[0:10])
print(Day_Range)


dir = "Mlb_Game_Data"
file = os.listdir(dir)
for A in file:
    File_List.append(A[0:10])
print(File_List)

if File_List == Day_Range:
    None
else:
    for A in Day_Range:
        file = os.listdir(dir)
        for B in file:
            File_List.append(B[0:10])
        if File_List == Day_Range:
            None
        else:
            if A in File_List:
                None
            else:
                print(A+"가 없습니다")
                Miss_Day_Range_timestamp = pd.date_range(dashdel(A), ToDay)
                for B in Miss_Day_Range_timestamp:
                    Miss_Day_Range.append(str(B)[0:10])

                if Miss_Day_Range[0] == ToDayH:
                    print("오늘것만 호출")
                    querystring = {"date":ToDayH}
                    headers = {
                        "x-rapidapi-key": "비밀^^",
                        "x-rapidapi-host": "baseball4.p.rapidapi.com"
                    }
                    response = requests.get(url, headers=headers, params=querystring)
                    j = response.json()
                    data = json.dumps(j, ensure_ascii=False, indent=3, sort_keys=True)
                    with open("Mlb_Game_Data\\"+ToDayH+".txt", "w", encoding="utf-8") as file:
                        file.write(data)
                else:
                    for day in Miss_Day_Range:
                        print(day+" 호출")
                        querystring = {"date":day}
                        headers = {
                            "x-rapidapi-key": "비밀^^",
                            "x-rapidapi-host": "baseball4.p.rapidapi.com"
                        }
                        response = requests.get(url, headers=headers, params=querystring)
                        j = response.json()
                        data = json.dumps(j, ensure_ascii=False, indent=3, sort_keys=True)
                        with open("Mlb_Game_Data\\"+day+".txt", "w", encoding="utf-8") as file:
                            file.write(data)
###================MLB_Game_Data file downloder part=====================###
###================MLB_Game_Data file downloder part====================###

