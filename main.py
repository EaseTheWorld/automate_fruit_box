import time
import sys
from canvas_view import CanvasView
from image_process import image_file_to_matrix
from image_process import dump
from solve import find_best_move
from solve import clear_range

# range trim needed
# depth is 2, it leaves last move

PUZZLE_URL = 'https://en.gamesaien.com/game/fruit_box/'
CANVAS_ID = 'canvas'
PLAY_IMAGE_FILE = 'play.png'
TEMP_SCREENSHOT_FILE = 'canvas.png'
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
SOLVE_DEPTH = 1


v = CanvasView(PUZZLE_URL, CANVAS_ID)
print('page loaded.')

if not v.click_image_with_timeout(PLAY_IMAGE_FILE, 10):
    print('Error :', PLAY_IMAGE_FILE, 'not matched.')
    sys.exit(1)
print('play clicked.')

time.sleep(1) # wait for loading
v.save_screenshot_file(TEMP_SCREENSHOT_FILE)
print(TEMP_SCREENSHOT_FILE, 'saved.')

number_matrix, rect_matrix = image_file_to_matrix(TEMP_SCREENSHOT_FILE, TEMPLATE_FILE_LIST)
print('converted to number matrix')
dump(number_matrix)

while True:
    score, move_list = find_best_move(number_matrix, SOLVE_DEPTH)
    if move_list:
        move = move_list[0]
        number_matrix = clear_range(number_matrix, move)
        print('------------', move)
        dump(number_matrix)
        r1, c1, r2, c2 = move
        v.drag_and_drop(rect_matrix[r1][c1][1], rect_matrix[r1][c1][0],
            rect_matrix[r2][c2][3], rect_matrix[r2][c2][2])
    else:
        break
