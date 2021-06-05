import sys
import canvas_view
#from image_process import image_file_to_matrix
#import solve

PUZZLE_URL = 'https://en.gamesaien.com/game/fruit_box/'
CANVAS_ID = 'canvas'
PLAY_IMAGE_FILE = 'play_text.png'
TEMP_SCREENSHOT_FILE = 'canvas.png'
SOLVE_DEPTH = 1


v = CanvasView(PUZZLE_URL, CANVAS_ID)
sys.exit()
v.click_image(PLAY_IMAGE_FILE)
v.screenshot(TEMP_SCREENSHOT_FILE)

number_matrix, offset_matrix = image_file_to_matrix(TEMP_SCREENSHOT_FILE)

while True:
    score, move = solve.find_best_move(number_matrix, SOLVE_DEPTH)
    if move:
        solve.apply_move(number_matrix, move)
        r1, c1, r2, c2 = move
        v.drag_and_drop(offset_matrix[r1][c1][0], offset_matrix[r1][c1][1],
            offset_matrix[r2][c2][0], offset_matrix[r2][c2][1])
    else:
        break
