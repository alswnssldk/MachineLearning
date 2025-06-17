from Main import AI
import matplotlib.pyplot as plt
import numpy as np


KR = []
XG = []

KR.append(AI(671737)[1])
XG.append(AI(671737)[0])

KR.append(AI(656557)[1])
XG.append(AI(656557)[0])

KR.append(AI(608379)[1])
XG.append(AI(608379)[0])

KR.append(AI(669302)[1])
XG.append(AI(669302)[0])


print(XG)
print(KR)

players = [f'Player {i+1}' for i in range(len(KR))]

x = np.arange(len(KR))  # x축 위치
width = 0.35  # 막대 폭

plt.bar(x - width/2, KR, width, label='Keras')
plt.bar(x + width/2, XG, width, label='XGBoost')

plt.xlabel('Player')
plt.ylabel('Score')
plt.title('Player Score Comparison: Keras vs XGBoost')
plt.xticks(x, players)
plt.ylim(0, 1)  # 정확도 범위
plt.legend()
plt.tight_layout()
plt.show()