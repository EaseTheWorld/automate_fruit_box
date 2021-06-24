# Goal
automate https://en.gamesaien.com/game/fruit_box/

# Dependencies
- cv2, numpy : image processing
- selenium : browser automation
- [ChromeDriver](https://chromedriver.chromium.org)(download and unzip the executable in PATH)

# Usage
- `python main.py` : automation mode
  - open Chrome
  - click 'Play' button
  - convert the image to number matrix
  - save the image to canvas.png
  - find the best moves
  - drag and drop to get rid of the fruits!
- `python main.py png_file` : test mode
  - solve the png file without browser
  - more png files in sample directory.
