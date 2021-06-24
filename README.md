# Goal
automate https://en.gamesaien.com/game/fruit_box/

# Dependencies
- cv2, numpy : image processing
- selenium : browser automation
- [ChromeDriver](https://chromedriver.chromium.org)(download and unzip the executable in PATH)

# Usage
- `python main.py` will do these automatically.
  - open Chrome
  - click 'Play' button
  - convert the image to number matrix
  - save the image to canvas.png
  - find the best moves
  - drag and drop
- `python main.py canvas.png`
  - solve it without browser(for algorithm purpose)
  - more png files in sample directory.
