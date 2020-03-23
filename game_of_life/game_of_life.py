"""
python을 이용한 game of life

주요 프로세스 - 초안
- 셋팅(initialize)
    - 파일을 읽어오거나 입력값을 처리하는 부분

- 표 생성(create_grid)
    - 최소 width 80, height 40

- 세포의 세대별 변화
    - 세대에 따라 세포의 변화
    - 네 개의 조건을 바탕으로 알고리즘 구현

- 화면 출력
    - 어떻게 화면에 출력할 것인가?
    - 모든 세대가 완료된 후 txt파일로 세포의 변화 저장

main -> initialize -> create_grid -> change_generations -> visualize(Tkinter)
"""


# 파일과 세대는 주어질 수 있다.
# Test => initialize('plus.txt')
def initialize(filename=None, gen=None):
    """
    :param filename: 사용될 파일 이름(plus.txt)
    :param gen: 사용자가 입력할 세대의 수
    """

    # default size
    height, width = 80, 40
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
        # 생성 가능한 좌표의 리스트 - [19,19]~ [21,21]
        init_cell = list(itertools.product(range(19, 22), repeat=2))
        random.shuffle(init_cell)

        init_cell = init_cell[:rand_cell]

    return [int(width), int(height)], gen, init_cell


# Test => size, gen, init_cell = initialize('plus.txt')
# create_grid(size, gen, init_cell)
def create_grid(size, init_cell):
    """
    :param size: 초기화된 grid의 크기
    :param init_cell: 초기화된 cell
    """
    # size에 맞는 빈('_') 리스트 구현
    grid_list = [[''] * size[0] for _ in range(size[1])]
    for row, col in init_cell:
        grid_list[row][col] = '*'
    # default(80x40) 사이즈의 리스트 반환
    return grid_list


def change_generations(prev_cell):
    # 세대에 따라 셀의 변화
    # 네 개의 조건을 바탕으로 알고리즘 구현
    next_cell = []
    return next_cell


def visualize():
    # 화면에 출력
    pass


def main():
    # 게임 실행
    # 게임 완료 후 txt파일로 저장
    pass


if __name__ == '__main__':
    # 초기화
    # initialize()  # 아무 값을 입력하지 않을 경우 -> random state
    # initialize('plus.txt')  # 파일 이름과 세대를 입력할 경우 -> 파일에 정의된 state

    # 초기화
    size, gen, init_cell = initialize()  # 사용자가 값을 입력하지 않을 경우
    # 그리드 생성
    result = create_grid(size, init_cell)  # 배열을 이용해 그리드 생성
