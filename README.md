# Game of Life - Streami

사용언어: Python 3.7.2


python을 이용한 game of life



### 주요 프로세스

- 초기 셋팅

    - **[def initialize(filename, genenration)](https://github.com/navill/streami_homework/blob/faf90be54fe9fbe9217b022853c2d9d38e248bf6/game_of_life/game_of_life.py#L13)**

        - 사용자가 입력한 설정에 따라 초기값 설정한다.

            - **\$ python game_of_life.py:** random board state 로 시작하고 여러 generation 에 걸쳐 board 가 바뀌는 것을 visualize 한다.(random board state 구현중)
            - **\$ python game_of_life.py plus.txt:** plus.txt 에 주어진 state 로 시작해서 generation 에 걸쳐 board 가 바뀌는 것을 visualize 한다.

            - **\$ python game_of_life.py plus.txt 10:** plus.txt 에 주어진 state 로 시작해서 10 generation 후의 board state 을 txt 파일로 dump 한다.

- 세포의 세대별 변화 처리

    - **[def create_grid(size, init_cell)](https://github.com/navill/streami_homework/blob/faf90be54fe9fbe9217b022853c2d9d38e248bf6/game_of_life/game_of_life.py#L66)**
        - 0세대 셀이 적용된 grid(MAIN_GRID & CONTAINER_GRID)를 생성한다.
        - 전체 표의 크기는 size에 의해 정해진다.
    - **[def check_live_neighbor(cell_row, cell_col)](https://github.com/navill/streami_homework/blob/faf90be54fe9fbe9217b022853c2d9d38e248bf6/game_of_life/game_of_life.py#L85)**
        - 셀을 중심으로 주변에 살아있는 셀을 개수를 파악한다.

    - **[def change_generation()](https://github.com/navill/streami_homework/blob/faf90be54fe9fbe9217b022853c2d9d38e248bf6/game_of_life/game_of_life.py#L121)**
      - Game of Life의 게임 규칙에 맞게 셀을 활성화하거나 비활성화 한다.

- 화면 출력
    
    - **def visualize()**
        - 셀의 변화를 시각화하기 위한 함수(작성중)
    
- 메인 함수

    - **def main()**
        - Game of Life 게임을 실행하고, 모든 세대의 순환이 완료될 때 세대별 세포 배열을 txt파일로 저장(작성중)

