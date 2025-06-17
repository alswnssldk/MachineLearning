import os
import json
import numpy as np


def AI(PicherId):
    PicherBreaks = []
    PicherCoordinates = []
    PicherPluse = []

    PichResultCode = []
    PichResult = []
    PichBallType = []

    DirList = os.listdir("Mlb_Playbyplay_Data")
    # print(DirList)

    # target id
    id = PicherId

    for A in DirList:
        FileDir = os.listdir(f"Mlb_Playbyplay_Data/{A}")
        for B in FileDir:
            with open(f"Mlb_Playbyplay_Data/{A}/{B}", "r", encoding="utf-8") as f:
                print(f"{A}에 {B}하는중")
                j = json.load(f)
            EventList = j["body"]
            for Event in EventList:
                if Event["matchup"]["pitcher"]["id"] == id:
                    # print("투수 찾음")
                    PlayEvent = Event["playEvents"]
                    for playevent in PlayEvent:
                        # print(playevent["isPitch"])
                        if playevent["isPitch"] == True:
                            Pich = playevent["pitchData"]
                            breaks_data = Pich.get("breaks")
                            coords_data = Pich.get("coordinates")

                            # breaks가 딕셔너리일 때만 .values() 사용
                            if isinstance(breaks_data, dict) and isinstance(coords_data, dict):
                                PicherBreaks.append(list(breaks_data.values()))
                                PicherCoordinates.append(list(coords_data.values()))

                                Extension = Pich.get("extension", 0)

                                PicherPluse.append([
                                    Pich["endSpeed"],
                                    Extension,
                                    Pich["plateTime"],
                                    Pich["startSpeed"],
                                    Pich["strikeZoneBottom"],
                                    Pich["strikeZoneTop"],
                                    Pich["typeConfidence"],
                                    Pich["zone"]
                                ])
                                PichResultCode.append(playevent["details"]["code"])
                                PichResult.append(playevent["details"]["description"])
                                PichBallType.append(playevent["details"]["type"]["code"])
                            else:
                                continue
            print(f"{A} 까지 완료")


    #print(len(PicherBreaks))
    #print(len(PicherCoordinates))
    # print(PicherPluse)
    # print(PichResult)
    # print(PichResultCode)
    # print(len(PichBallType))

    y = []
    PichCB = []
    for A in PichResultCode:
        if A == "C" or A == "S":
            y.append(1)
        else:
            y.append(0)

    for i in range(len(PicherCoordinates)):
        #print(PicherBreaks[i]+PicherCoordinates[i])
        #print(len(PicherBreaks[i]+PicherCoordinates[i]))
        if len(PicherBreaks[i]+PicherCoordinates[i]) == 23:
            PichCB.append(PicherBreaks[i]+PicherCoordinates[i]+PicherPluse[i])
        else:
            del PichBallType[i]
            del y[i]

    y = np.array(y)
    print(len(y))
    # print(PichCB)
    PichCBNp = np.array(PichCB)
    #print(PichCBNp)
    print(PichCBNp.shape)

    #============================================================================
    # Keras 부분
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    # X: 투수 공 피쳐
    # y: 헛스윙 여부 (0 또는 1)
    X = PichCBNp  # 투수 공 피쳐 배열
    y = y  # 헛스윙 라벨 배열

    # 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

    # 스케일링
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 모델 구성
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # 모델 학습
    model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_split=0.2)

    # 평가
    loss, accuracy = model.evaluate(X_test_scaled, y_test)
    print(f'Test Accuracy: {accuracy:.4f}')

    Keras_score = accuracy
    print(Keras_score)
    #====================================================================================================
    # XGBoost 부분

    from xgboost import XGBClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(PichCBNp, y, test_size=0.2, random_state=42)

    # 모델 정의 및 학습
    model = XGBClassifier(
        n_estimators=500,
        learning_rate=0.01,
        max_depth=5,
        min_child_weight=3,
        gamma=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)

    # 예측 및 정확도 출력
    y_pred = model.predict(X_test)
    print("Test Accuracy:", accuracy_score(y_test, y_pred))
    XGBoost_score = accuracy_score(y_test, y_pred)


    return(XGBoost_score, Keras_score)
