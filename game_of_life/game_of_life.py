import os
import sys
from os import system
from copy import deepcopy
from time import sleep
import random

##################
# MAIN_GRID: 화면에 뿌려질때 사용될 grid 변수
MAIN_GRID = []
# CONTAINER_GRID: 이전 세대 grid를 잠시 담고 있을 변수. 조건 연산에 사용됨
CONTAINER_GRID = []
write, flush = sys.stdout.write, sys.stdout.flush


##################


def initialize(filename=None):
    """
    :param <str> filename: 사용될 파일 이름(plus.txt)
    """

    # 초기화된 셀들을 저장할 리스트
    list_init_cell = []

    # 파일이 있을 경우 -> 파일을 기반으로 초기화
    if filename:
        try:
            with open(filename) as file_object:
                contents = file_object.readlines()
                contents = (content.split('\n')[0].split(' ') for content in contents)
                # grid 높이 & 넓이
                c_row, c_col = next(contents)
                row, col = int(c_row), int(c_col)
                # 셀의 개수는 건너뜀
                next(contents)

                # 파일에 포함된 초기 세포 좌표
                for content in contents:
                    if content != ['']:
                        cell_row, cell_col = content
                        # 초기 셀 생성
                        list_init_cell.append((int(cell_row), int(cell_col)))
        except OSError:
            write('입력하신 파일을 찾을 수 없습니다.\n')
            sys.exit()
    # 파일이 없을 경우 -> random으로 초기화
    else:
        # 랜덤한 게임의 크기
        col = 80 + 3 * random.randint(1, 20)  # col 최대 크기: 140
        row = 40 + 3 * random.randint(1, 20)  # row 최대 크기: 100

        # 최대 row & col의 난수 생성
        arry_rand_col = list(random.randint(20, col - 20) for _ in range(100))
        arry_rand_row = list(random.randint(10, row - 10) for _ in range(100))

        list_init_cell = list(zip(arry_rand_row, arry_rand_col))

    return [row, col], list_init_cell


def create_grid(grid_size, list_init_cell):
    """
    :param <list> grid_size: 화면에 표시될 테이블의 크기(<int>width, <int>height)
    :param <list> list_init_cell: 세포들의('■') 위치가 들어있는 리스트
    """
    global CONTAINER_GRID

    for _ in range(grid_size[0]):
        MAIN_GRID.append([''.join(chr(9633))] * grid_size[1])

    CONTAINER_GRID = deepcopy(MAIN_GRID)

    for x, y in list_init_cell:
        MAIN_GRID[x][y] = '■'  # chr(9632)
        CONTAINER_GRID[x][y] = '■'  # chr(9632)


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
            except IndexError as e:
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


def change_generation(do_save):
    """
    :param <boolean> do_save: 현재 세대에서 살아있는 셀을 저장할지 여부 판단
    """
    global CONTAINER_GRID

    old_grid = CONTAINER_GRID
    live_cells_row_col = []

    num_gen_cell = 0  # 순환문을 돌며 살아있는 셀 카운트

    # row부터 진행 -> cache hit 유도
    for row in range(len(old_grid)):
        for col, cell in enumerate(old_grid[row]):
            cells_in_loop = False

            # 주변 살아있는 셀 개수 체크
            live_neighbor_cell_num = check_live_neighbor(row, col)

            # 살아있는 셀
            if '■' == cell:
                if live_neighbor_cell_num == 1 or live_neighbor_cell_num == 0:  # 조건1
                    MAIN_GRID[row][col] = '□'  # die
                elif live_neighbor_cell_num > 3:  # 조건2
                    MAIN_GRID[row][col] = '□'  # die
                else:
                    num_gen_cell += 1
                    cells_in_loop = True
            # 죽어있는 셀
            else:
                if live_neighbor_cell_num == 3:  # 조건4
                    MAIN_GRID[row][col] = '■'  # resurrection
                    cells_in_loop = True
                    num_gen_cell += 1
            # 마지막 세대에서(do_save=True) 세포가 살아있을 경우(cells_in_loop=True)
            if do_save and cells_in_loop:
                live_cells_row_col.append([row, col])

    CONTAINER_GRID = deepcopy(MAIN_GRID)

    return live_cells_row_col, num_gen_cell  # 셀들의 행렬, 살아있는 셀 수


def visualize(gen=None):
    """
    :param <int> gen: 진행할 세대의 수
    """
    # ex: gen = 10(입력받은 셀이 10일 경우)
    # 진행중인 세대 수
    count_gen_num = 0
    zero_generation = '\n'.join([''.join(i) for i in MAIN_GRID])
    write(zero_generation)
    text = '\nGame of Life를 시작합니다. 현재 {0} 세대 세포입니다.\n'.format(count_gen_num)
    write(text)
    flush()

    # 초기화면 2초 대기
    sleep(2)

    while True:
        count_gen_num += 1
        # int형 세대수가 아닐경우(사용자가 세대 수를 입력하지 않을 경우)
        # => 무한 루프
        # 초기 세대수(0)가 입력받은 세대 수와 같아질때까지 반복
        # => do_save=True(셀 행렬 저장 실행)
        do_save = True if gen == count_gen_num else False

        # 세포 변화 시작 -> 살아있는 셀 리스트 반환
        live_cells_row_col, num_live_cell = change_generation(do_save)

        flush()  # 버퍼에 남아있을 수 있는 모든 요소 배출
        system('cls' if os.name == 'nt' else 'clear')
        # system('cls')  # 화면 정리

        generations = '\n'.join([''.join(i) for i in MAIN_GRID])
        write(generations)
        # 세포가 하나라도 살아있을 경우
        if num_live_cell:
            write('\n{0} - 세대\n'.format(count_gen_num))
        # 모두 죽어있을 경우 종료
        else:
            write('\n모든 세포가 죽어있습니다.\n')
            count_gen_num -= 1
            break

        # 사용자가 쉘에서 파일명을 입력하지 않을 경우 gen은 None
        # => 첫 번째 조건이 False가 되면서 break 라인까지 도달하지 않는다. -> 무한 루프
        # => int형의 gen이 입력되고 그 수 만큼 반복할 때 까지 진행
        # 위 조건을 벗어날 경우 무한 루프
        if gen.__class__ is int and gen <= count_gen_num:
            break

        # 화면에 출력 후 대기
        sleep(1)
    return count_gen_num, live_cells_row_col


def main(sys_args):
    """
    :param <list> sys_args: 쉘에서 입력된 인자값
    """
    filename = None
    gen = None

    # 입력값이 0 ~ 3개일 경우
    if len(sys_args) < 4:
        try:
            filename = sys_args[1]
            gen = int(sys_args[2])
            if gen == 0:
                write('세대 수는 0보다 큰 값을 입력해주세요.\n')
                return None
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
        write('입력하실 수 있는 변수의 개수가 초가되었습니다.\n')
        return None

    # 초기화: 창의 크기, 초기 셀의 행렬
    grid_size, init_cell_list = initialize(filename)
    # 초기 그리드 생성
    create_grid(grid_size, init_cell_list)
    try:
        # gen: 세대 수를 사용자가 인가할 경우 정수형 숫자가 인가/그렇지 않을 경우 None
        last_gen, live_cells_row_col = visualize(gen)  # 마지막 세대의 수, 살아남은 셀 좌표를 반환
        live_cells_num = len(live_cells_row_col)

        # 살아있는 셀이 한개라도 있을 경우
        if live_cells_num >= 1:
            import datetime
            now = datetime.datetime.now().strftime('D%m_%d_T%H:%M:%S')
            # 마지막 세대 상태 저장
            with open('dump/dump_{0}.txt', 'w+'.format(now)) as file_object:
                # size: grid_size from initialize()
                # gen: gen from sys.argv
                # survive_cell: live_cells_row_col from visualize()
                size = '{0} {1}.\n'.format(grid_size[0], grid_size[1])
                # grid 크기
                file_object.write(size)
                # 셀 개수
                file_object.write('{0}\n'.format(live_cells_num))
                # 셀 행렬 저장
                for row, col in live_cells_row_col:
                    file_object.write('{0} {1}\n'.format(row, col))
                file_object.write('\n')

    except KeyboardInterrupt:
        write('사용자에 의해 게임이 종료되었습니다.\n')
    else:
        write('게임이 {0}세대까지 진행되었습니다.\n'.format(last_gen))
        write('Game of life를 종료합니다.\n')


if __name__ == '__main__':
    args = sys.argv
    main(args)
