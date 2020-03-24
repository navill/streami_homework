from copy import deepcopy

##################
# MAIN_GRID: 화면에 뿌려질때 사용될 grid 변수
MAIN_GRID = []
# CONTAINER_GRID: 이전 세대 grid를 잠시 담고 있을 변수. 조건 연산에 사용됨
CONTAINER_GRID = []
# default
SIZE = [80, 40]
# 중앙 셀을 기준으로 이웃을 검사하기 위해 사용
##################
# size에 맞는 빈('chr(9633 -> □)') 2차 배열 구현
for _ in range(SIZE[1]):
    MAIN_GRID.append([''.join(chr(9633))] * SIZE[0])


for _ in range(SIZE[1]):
    CONTAINER_GRID.append([''.join(chr(9633))] * SIZE[0])


def initialize(filename=None, gen=None):
    """
        파일과 세대는 주어질 수 있다.
        :param <str> filename: 사용될 파일 이름(plus.txt)
        :param <int> gen: 사용자가 입력할 세대의 수
    """
    # default size
    height, width = SIZE
    init_cell = []
    # 파일이 있을 경우 -> 파일을 기반으로 초기화
    if filename:
        with open(filename) as file_object:
            contents = file_object.readlines()
            contents = (content.split('\n')[0].split(' ') for content in contents)
            # grid 높이 & 넓이
            height, width = next(contents)

            # 세대
            # input값이 없을 경우 -> plus.txt에서 값을 불러온다.
            if gen is None:
                gen = int(''.join(next(contents)))
            # input값이 있을 경우 -> plus.txt의 값을 무시하고 input 값을 받아온다.
            else:
                next(contents)
            # 파일에 포함된 초기 세포 좌표
            for i in contents:
                if i != ['']:
                    row, col = i
                    init_cell.append((int(row), int(col)))

    # 파일이 없을 경우 -> random으로 초기화
    else:
        import random
        import itertools
        # 랜덤으로 생성할 좌표의 수
        rand_cell = random.randint(1, 9)
        gen = random.randint(1, 9)
        # 생성 가능한 좌표의 리스트 - [19,19]~ [21,21]  // 3x3=9칸에 임의로 세포 생성
        init_cell = list(itertools.product(range(19, 22), repeat=2))
        random.shuffle(init_cell)

        init_cell = init_cell[:rand_cell]

    return [int(width), int(height)], gen, init_cell


def create_grid(cell_coord_list):
    """
    :param <list> cell_coord_list: 세포들의('■') 좌표가 들어있는 리스트
    """

    for x, y in cell_coord_list:
        MAIN_GRID[x][y] = chr(9632)
        CONTAINER_GRID[x][y] = chr(9632)
        print('create_grid:', x, y)

    return cell_coord_list


def check_live_neighbor(cell_row, cell_col):
    # print('checklive:', cell_row, cell_col)
    """
    살아있는 세포의 주변 세포가 살아있는지 측정(조건 1,2,3)
    :param <int> cell_row: 체크하고자 하는 셀의 행
    :param <int> cell_col: 체크하고자 하는 셀의 열
    """
    live_cell_num = 0
    # 이웃 셀 좌표 생성
    for row in [cell_row - 1, cell_row, cell_row + 1]:
        # print('y:', row)
        for col in [cell_col - 1, cell_col, cell_col + 1]:
            # print('x:', col)
            # 자신을 제외하고 순회
            # print('5,4:', test_grid[cell_row][cell_col], col, row)
            if col == cell_col and row == cell_row:
                continue
                # size를 벗어나는 index는 무시
            try:
                # 주변에 살아있는 세포가 있을 경우
                if CONTAINER_GRID[row][col] == '■':
                    live_cell_num += 1
                    # print(cell_row, cell_col)
                    # print(col, row)
                    # print('------------')
            except:
                pass

    return live_cell_num


"""
네 개의 조건을 바탕으로 알고리즘 구현
공간이 채워져있을 경우
1. 이웃이 하나 혹은 없을 경우 세포는 죽는다.
2. 네 개 이상의 이웃을 가진 셀은 죽는다.
3. 두 개 혹은 세 개의 이웃이있는 셀은 살아남는다.

공간이 비워져 있을 경우
4. 각 셀의 이웃이 세 개일 경우 세포는 살아난다.
"""


def change_generation():
    global CONTAINER_GRID
    old_grid = CONTAINER_GRID
    """
    :param <list> 다음 세대로 변하기 전 살아 있는 세포들의 좌표 리스트
    """
    # 이전 세대 세포가 그려진 표

    # new = old.copy() -> change_generation에서 new를 사용-> old = new

    # col부터 진행 -> cache hit 유도
    for row in range(len(old_grid)):
        for col, cell in enumerate(old_grid[row]):
            live_neighbor_cell_num = check_live_neighbor(row, col)
            if live_neighbor_cell_num != 0:
                print(live_neighbor_cell_num, row, col)
            if '■' == cell:
                if live_neighbor_cell_num == 1 or live_neighbor_cell_num == 0:  # 조건1
                    MAIN_GRID[row][col] = '□'  # die
                    print('condition1-die:', row, col)
                elif live_neighbor_cell_num > 3:  # 조건2
                    MAIN_GRID[row][col] = '□'  # die
                    print('condition2-die:', row, col)

                elif live_neighbor_cell_num == 2 or live_neighbor_cell_num == 3:  # 조건3
                    print('keep:', row, col)
                    continue  # 살아있는 상태 유지
            else:
                if live_neighbor_cell_num == 3:
                    print('resurrection:', row, col)
                    MAIN_GRID[row][col] = '■'  # resurrection

    CONTAINER_GRID = deepcopy(MAIN_GRID)


def visualize():
    # 화면에 출력
    pass


def main():
    # 게임 실행
    # 게임 완료 후 txt파일로 저장
    pass


if __name__ == '__main__':
    # 초기화
    s, g, i = initialize('plus.txt')  # 사용자가 값을 입력하지 않을 경우

    # 그리드 생성
    result = create_grid(i)  # 배열을 이용해 그리드 생성
    first_grid = []
    for i in MAIN_GRID:
        first_grid.append(''.join(i))
    print(first_grid)

    # 세포의 세대별 변화 출력
    for _ in range(7):
        change_generation()
        test_result = []
        for i in MAIN_GRID:
            test_result.append(''.join(i))
        print(test_result)

