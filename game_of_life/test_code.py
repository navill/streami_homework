from game_of_life import *

# ------------------------------------------------------------
# *********** 초기화 ***********
# size, gen, init_cell = initialize()  # 사용자가 값을 입력하지 않을 경우
"""
:Result

([40, 80], 6, [(19, 20), (21, 19), (20, 21), (19, 19)])

"""
# print(initialize('plus.txt'))  # 파일 이름과 세대를 입력할 경우
# ------------------------------------------------------------


# ------------------------------------------------------------
# ***********그리드 생성***********

# size, gen, init_cell = initialize()
# result = create_grid(size, init_cell)
# print(f'row length:{len(result[0])}, col length:{len(result)}')
# print("'*'이 위치한 좌표:")
# for idx, value in enumerate(result):
#     if '*' in value:
#         print(f"x:{value.index('*')}, y:{idx}")
"""
:Result

row length:40, col length:80
'*'이 위치한 좌표:
x:20, y:20
x:19, y:21
"""
# ------------------------------------------------------------
