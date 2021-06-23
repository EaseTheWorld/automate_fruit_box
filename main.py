import time
import sys
from canvas_view import CanvasView
from image_process import image_file_to_matrix
from solve import find_move_list

PUZZLE_URL = 'https://en.gamesaien.com/game/fruit_box/'
CANVAS_ID = 'canvas'
PLAY_IMAGE_FILE = 'play.png'
TEMPLATE_FILE_LIST = (
    ('no1.png', 1),
    ('no2.png', 2),
    ('no3.png', 3),
    ('no4.png', 4),
    ('no5.png', 5),
    ('no6.png', 6),
    ('no7.png', 7),
    ('no8.png', 8),
    ('no9.png', 9)
)

def main(input_image_file):

    v = None
    if not input_image_file:
        v = CanvasView(PUZZLE_URL, CANVAS_ID)
        print('page loaded.')

        if not v.click_image_with_timeout(PLAY_IMAGE_FILE, 10):
            print('Error :', PLAY_IMAGE_FILE, 'not matched.')
            sys.exit(1)
        print('play clicked.')

        time.sleep(1) # wait for loading

        input_image_file = 'canvas.png'
        v.save_screenshot_file(input_image_file)
        print(input_image_file, 'saved.')

    number_matrix, rect_matrix = image_file_to_matrix(input_image_file, TEMPLATE_FILE_LIST)
    print('converted to number matrix')

    move_list = find_move_list(number_matrix)
    total_move = len(move_list)
    total_score = sum(move.score for move in move_list)
    result_msg = f'total_move={total_move} total_score={total_score}'
    print(result_msg)

    if v:
        v.popup(result_msg)
        time.sleep(2)
        for move in move_list:
            v.drag_and_drop(
                rect_matrix[move.r1][move.c1][1],
                rect_matrix[move.r1][move.c1][0],
                rect_matrix[move.r2][move.c2][3],
                rect_matrix[move.r2][move.c2][2]
            )
    '''
    while True:
        score, next_move, next_number_matrix = find_best_move(number_matrix)
        move_count += 1
        if next_move:
            total_score += score
            number_matrix = next_number_matrix
            print(f'\n[{move_count}] ---------- {next_move} : {total_score}')
            dump(number_matrix)
            if v:
                r1, c1, r2, c2 = next_move
                v.drag_and_drop(rect_matrix[r1][c1][1], rect_matrix[r1][c1][0],
                    rect_matrix[r2][c2][3], rect_matrix[r2][c2][2])
        else:
            break
    '''

input_image_file = None
if len(sys.argv) > 1:
    input_image_file = sys.argv[1]

main(input_image_file)
