# Game of Life - Streami

사용언어: Python 3.7.2


python을 이용한 game of life



### 주요 프로세스

- **초기 셋팅**

    - **[def initialize(filename, genenration)](https://github.com/navill/streami_homework/blob/faf90be54fe9fbe9217b022853c2d9d38e248bf6/game_of_life/game_of_life.py#L13)**

        - 사용자가 입력한 설정에 따라 초기값 설정한다.

            - **\$ python game_of_life.py:** random board state 로 시작하고 여러 generation 에 걸쳐 board 가 바뀌는 것을 visualize 한다.(random board state 진행중)
            - **\$ python game_of_life.py plus.txt:** plus.txt 에 주어진 state 로 시작해서 generation 에 걸쳐 board 가 바뀌는 것을 visualize 한다.

            - **\$ python game_of_life.py plus.txt 10:** plus.txt 에 주어진 state 로 시작해서 10 generation 후의 board state 을 txt 파일로 dump 한다.

- **세포의 세대별 변화 처리**

    - **[def create_grid(grid_size, init_cell)](https://github.com/navill/streami_homework/blob/faf90be54fe9fbe9217b022853c2d9d38e248bf6/game_of_life/game_of_life.py#L66)**

        - 0세대 셀이 적용된 메인 그리드를 생성한다.

        - 전체 표의 크기는 grid_size에 의해 정해진다.

            (사용자가 아무런 값을 입력하지 않을 경우 창은 최대 140x100까지 커질 수 있다.)

    - **[def check_live_neighbor(cell_row, cell_col)](https://github.com/navill/streami_homework/blob/faf90be54fe9fbe9217b022853c2d9d38e248bf6/game_of_life/game_of_life.py#L85)**

        - 한 개의 셀을 중심으로 주변을 순회하면서 살아있는 셀을 개수를 파악한다.

    - **[def change_generation()](https://github.com/navill/streami_homework/blob/faf90be54fe9fbe9217b022853c2d9d38e248bf6/game_of_life/game_of_life.py#L121)**
      - 전체 셀을 순환하며 Game of Life의 게임 규칙에 맞게 셀을 활성화하거나 비활성화 한다.
        - 위 과정 중에 게임의 모든 셀이 죽었는지 판별한다.

- **화면 출력**
    
    - **[def visualize(gen)](https://github.com/navill/streami_homework/blob/edc004894f939302c39b35f70e34e23da53e102b/game_of_life/game_of_life.py#L152)**
        - 셀의 변화를 시각화하기 위해 **sys.stdout.write()**를 이용하여 쉘에 그린다.
        - 세대 수에 맞게 반복문이 동작한다.
    
- **메인 함수**

    - **[def main(sys_args)]()**
        - shell에서 인가된 두 개의 변수(파일 이름과 세대 수)를 이용해 게임을 초기화하고 실행시키기 위한 함수이다.
        - 게임 동작에 필요한 함수를 실행하고, 세대가 입력될 경우 마지막 세대의 상태를 저장하는 기능을 포함한다.
        - 저장될 파일명은 'dump/dump_D00_T00:00:00.txt'로 저장된다.

