from copy import deepcopy

##################
# MAIN_GRID: 화면에 뿌려질때 사용될 grid 변수
MAIN_GRID = []
# CONTAINER_GRID: 이전 세대 grid를 잠시 담고 있을 변수. 조건 연산에 사용됨
CONTAINER_GRID = []
# default
SIZE = [40, 80]
##################


def initialize(filename=None, gen=None):
    """
        파일과 세대는 주어질 수 있다.
        :param <str> filename: 사용될 파일 이름(plus.txt)
        :param <int> gen: 사용자가 입력할 세대의 수
    """
    # default size
    # height, width = SIZE
    init_cell = []
    # 파일이 있을 경우 -> 파일을 기반으로 초기화
    if filename:
        with open(filename) as file_object:
            contents = file_object.readlines()
            contents = (content.split('\n')[0].split(' ') for content in contents)
            # grid 높이 & 넓이
            height, width = next(contents)

            # 세대값이 없을 경우 -> plus.txt에서 값을 불러온다.
            if gen is None:
                gen = int(''.join(next(contents)))
            # input값이 있을 경우 -> plus.txt의 값을 무시하고 input 값을 받아온다.
            else:
                next(contents)
            # 파일에 포함된 초기 세포 좌표
            for content in contents:
                if content != ['']:
                    row, col = content
                    # 초기 셀 생성
                    init_cell.append((int(row), int(col)))

    # 파일이 없을 경우 -> random으로 초기화
    else:
        import random
        import itertools
        """
        임의 설정(진행중)
        """
        # 랜덤한 게임의 크기 - 최대 110x80
        width = 80 + 10 * random.randint(0, 3)
        height = 40 + 10 * random.randint(0, 4)
        # 랜덤으로 생성할 셀 수 - 최대 전체 크기 1/2
        num_rand_cell = random.randint(1, (width * height) // 2)
        # 랜덤 세대 수(무한 반복?)
        gen = random.randint(1, 30)

        # 생성 가능한 좌표의 리스트 - [19,19] ~ [21,21]  // 3x3=9칸에 임의로 세포 생성
        init_cell = list(itertools.product(range(19, 22), repeat=2))
        random.shuffle(init_cell)
        init_cell = init_cell[:num_rand_cell]

    return [int(width), int(height)], gen, init_cell


def create_grid(grid_size, init_cell):
    """
    :param <list> size: 화면에 표시될 테이블의 크기(<int>width, <int>height)
    :param <list> init_cell: 세포들의('■') 위치가 들어있는 리스트
    """
    global CONTAINER_GRID

    for _ in range(grid_size[0]):
        MAIN_GRID.append([''.join(chr(9633))] * grid_size[1])
    CONTAINER_GRID = deepcopy(MAIN_GRID)

    for x, y in init_cell:
        MAIN_GRID[x][y] = '■'  # chr(9632)
        CONTAINER_GRID[x][y] = '■'  # chr(9632)

    return init_cell


# 주변에 몇 개의 세포가 살아있는지 카운팅
def check_live_neighbor(cell_row, cell_col):
    """
    :param <int> cell_row: 체크하고자 하는 셀의 행
    :param <int> cell_col: 체크하고자 하는 셀의 열
    """
    live_cell_num = 0
    # 이웃 셀 좌표 생성
    for row in [cell_row - 1, cell_row, cell_row + 1]:
        for col in [cell_col - 1, cell_col, cell_col + 1]:
            # 대상 셀은 제외
            if col == cell_col and row == cell_row:
                continue
            try:
                # 주변에 살아있는 세포가 있을 경우
                if CONTAINER_GRID[row][col] == '■':
                    live_cell_num += 1
            # size를 벗어나는 index는 무시
            except Exception as e:
                # print(f'{e}: 검색이 배열의 범위를 벗어났습니다.')
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

    # row부터 진행 -> cache hit 유도
    for row in range(len(old_grid)):
        for col, cell in enumerate(old_grid[row]):
            # 주변 살아있는 셀 개수
            live_neighbor_cell_num = check_live_neighbor(row, col)
            # 살아있는 셀
            if '■' == cell:
                if live_neighbor_cell_num == 1 or live_neighbor_cell_num == 0:  # 조건1
                    MAIN_GRID[row][col] = '□'  # die
                elif live_neighbor_cell_num > 3:  # 조건2
                    MAIN_GRID[row][col] = '□'  # die
            # 죽어있는 셀
            else:
                if live_neighbor_cell_num == 3:  # 조건4
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
    grid_size, g, init_cell_list = initialize('plus.txt')  # 사용자가 값을 입력하지 않을 경우

    # 초기 그리드 생성
    create_grid(grid_size, init_cell_list)
    test_result = []
    for i in MAIN_GRID:
        test_result.append(''.join(i))
    print(test_result)
    # 세포의 세대별 변화 출력
    for _ in range(8):
        change_generation()
        test_result = []
        for i in MAIN_GRID:
            test_result.append(''.join(i))
        print(test_result)
