import sys
from os import system
from copy import deepcopy
from time import sleep
import random
import itertools

##################
# MAIN_GRID: 화면에 뿌려질때 사용될 grid 변수
MAIN_GRID = []
# CONTAINER_GRID: 이전 세대 grid를 잠시 담고 있을 변수. 조건 연산에 사용됨
CONTAINER_GRID = []
GENERATION_NUMBER = 0
write, flush = sys.stdout.write, sys.stdout.flush


##################


def initialize(filename=None, gen=None):
    """
    파일과 세대는 사용자가 선택할 수 있다.
    :param <str> filename: 사용될 파일 이름(plus.txt)
    :param <int> gen: 파일에 있는 세대수를 사용할지 여부 판단
    """

    # default 크기
    init_cell = []
    gen_number = gen
    # 파일이 있을 경우 -> 파일을 기반으로 초기화
    if filename:
        try:
            with open(filename) as file_object:
                contents = file_object.readlines()
                contents = (content.split('\n')[0].split(' ') for content in contents)
                # grid 높이 & 넓이
                row, col = next(contents)

                # 만일 파일이 있는데 gen_number가 None일 경우 - 파일에 있는 세대 수 할당
                if gen_number is None:
                    # 세대값을 파일에서 받아온다.
                    gen_number = int(next(contents).pop())
                # 만일 파일이 있는데 gen_number가 입력되었을 경우 - 무시
                else:
                    next(contents)

                # 파일에 포함된 초기 세포 좌표
                for content in contents:
                    if content != ['']:
                        cell_row, cell_col = content
                        # 초기 셀 생성
                        init_cell.append((int(cell_row), int(cell_col)))
        except OSError:
            write('입력하신 파일을 찾을 수 없습니다.\n')
            sys.exit()
    # 파일이 없을 경우 -> random으로 초기화
    else:
        """
        임의 설정(진행중)
        """
        # 랜덤한 게임의 크기 - 최대 110x80
        col = 80  # + 10 * random.randint(0, 3)
        row = 40  # + 10 * random.randint(0, 4)
        # 랜덤으로 생성할 셀 수 - 최대 전체 크기 1/2
        num_rand_cell = random.randint(1, (col * row) // 2)

        # 생성 가능한 좌표의 리스트 - [19,19] ~ [21,21]  // 3x3=9칸에 임의로 세포 생성
        init_cell = list(itertools.product(range(19, 22), repeat=2))
        random.shuffle(init_cell)
        init_cell = init_cell[:num_rand_cell]
    return [int(row), int(col)], gen_number, init_cell


def create_grid(grid_size, init_cell):
    """
    :param <list> grid_size: 화면에 표시될 테이블의 크기(<int>width, <int>height)
    :param <list> init_cell: 세포들의('■') 위치가 들어있는 리스트
    """
    global CONTAINER_GRID

    print(MAIN_GRID)
    for _ in range(grid_size[0]):
        MAIN_GRID.append([''.join(chr(9633))] * grid_size[1])

    CONTAINER_GRID = deepcopy(MAIN_GRID)

    for x, y in init_cell:
        print(x, y)
        MAIN_GRID[x][y] = '■'  # chr(9632)
        CONTAINER_GRID[x][y] = '■'  # chr(9632)

    return init_cell


# 주변에 몇 개의 세포가 살아있는지 카운팅
def check_live_neighbor(cell_row, cell_col):
    """
    :param <int> cell_row: 체크하고자 하는 셀의 행
    :param <int> cell_col: 체크하고자 하는 셀의 열
    """
    count_live_cell = 0
    # 이웃 셀 좌표 생성
    for row in [cell_row - 1, cell_row, cell_row + 1]:
        for col in [cell_col - 1, cell_col, cell_col + 1]:
            # 대상 셀은 제외
            if col == cell_col and row == cell_row:
                continue
            try:
                # 주변에 살아있는 세포가 있을 경우
                if CONTAINER_GRID[row][col] == '■':
                    count_live_cell += 1
            # size를 벗어나는 index는 무시
            except Exception as e:
                # print(f'{e}: 검색이 배열의 범위를 벗어났습니다.')
                pass

    return count_live_cell


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
    is_live = False

    # row부터 진행 -> cache hit 유도
    for row in range(len(old_grid)):
        for col, cell in enumerate(old_grid[row]):
            # 주변 살아있는 셀 개수 체크
            live_neighbor_cell_num = check_live_neighbor(row, col)
            # 살아있는 셀
            if '■' == cell:
                # 전체 셀에서 세포가 하나라도 살아있을 경우 True, 그렇지 않을 경우 False
                is_live = True
                if live_neighbor_cell_num == 1 or live_neighbor_cell_num == 0:  # 조건1
                    MAIN_GRID[row][col] = '□'  # die
                elif live_neighbor_cell_num > 3:  # 조건2
                    MAIN_GRID[row][col] = '□'  # die
            # 죽어있는 셀
            else:
                if live_neighbor_cell_num == 3:  # 조건4
                    MAIN_GRID[row][col] = '■'  # resurrection

    CONTAINER_GRID = deepcopy(MAIN_GRID)
    return is_live


def visualize(gen):
    """
    :param <int> gen: 진행할 세대의 수
    """
    global GENERATION_NUMBER

    # 0세대 세포로 시작
    gen_number = GENERATION_NUMBER
    zero_generation = '\n'.join([''.join(i) for i in MAIN_GRID])
    write(zero_generation)
    write(f'\nGame of Life를 시작합니다. 현재 {gen_number} 세대 세포입니다.\n')
    flush()

    # 초기화면 2초 대기
    sleep(2)

    while True:
        # 순환문이 시작될 때 남은 빈 배열이 출력되는 문제 -> flush + system('clear')로 해결
        flush()  # 버퍼에 남아있을 수 있는 모든 요소 배출
        system('clear')  # 화면 정리

        # 세대 진행 수
        gen_number += 1
        # 세포 변화 시작
        is_live = change_generation()
        generations = '\n'.join([''.join(i) for i in MAIN_GRID])

        write(generations)
        write(f'\n{gen_number} - 세대\n')
        GENERATION_NUMBER = gen_number

        # 사용자가 쉘에서 파일명을 입력하지 않을 경우 gen은 None
        # => 첫 번째 조건이 False가 되면서 break 라인까지 도달하지 않는다. -> 무한 루프
        # => 어떤 형태로든 int형의 gen이 입력되고(1) 한 개의 셀이라도 살아있으며(2) 그 수 만큼 반복할 때 까지(3) 진행
        # 위 조건을 벗어날 경우 무한 루프
        if (gen.__class__ is int) and (is_live is True) and (gen <= gen_number):
            break

        # 화면에 출력 후 대기
        sleep(1)


def main(sys_args):
    """
    :param <list> sys_args: 쉘에서 입력된 인자값
    """
    global GENERATION_NUMBER

    filename = None
    gen = None

    # 입력값이 0 ~ 3개일 경우
    if len(sys_args) < 4:
        try:
            filename = sys_args[1]
            gen = int(sys_args[2])
        except ValueError:
            # 세대 수가 숫자가 아닐 경우
            write('세대 수는 int형을 입력해주세요.\n')
            return None
        except IndexError:
            # 파일이름과 세대수는 있을수도 없을수도 있다.
            # 있을경우 변수에 할당, 없을 경우 무시(None 유지)
            pass

    # 입력값이 4개 이상일 경우
    else:
        write(f'입력하실 수 있는 변수의 개수가 초가되었습니다.\n')
        return None

    # 초기화
    grid_size, gen_number, init_cell_list = initialize(filename, gen)
    # 초기 그리드 생성
    create_grid(grid_size, init_cell_list)

    # 화면 표시 - 세대 수만큼 진행
    try:
        # gen_number: 파일이 없을 경우 None, 파일이 있고 세대 수를 사용자가 인가할경우 정수형 숫자가 인가된다.
        visualize(gen_number)
    except KeyboardInterrupt:
        write('사용자가 게임을 중지하였습니다.\n')
    finally:
        write(f'게임의 마지막 세포는 {GENERATION_NUMBER}세대 세포입니다.\n')
        write(f'Game of life를 종료합니다.\n')


if __name__ == '__main__':
    args = sys.argv
    main(args)
