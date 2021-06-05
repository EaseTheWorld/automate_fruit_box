import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from image_process import find_image

class CanvasView:

    def __init__(self, url, canvas_id):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10) # seconds
        self.driver.get(url)
        self.canvas = self.driver.find_element_by_id(canvas_id)

    def __click(self, x, y):
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.canvas, x, y)
        action.click()
        action.perform()

    def click_image(self, image_file, wait_timeout = 10):
        # if os display scale is not 100%, normalize it
        canvas_size = (int(self.canvas.size['width']), int(self.canvas.size['height']))
        for i in range(wait_timeout):
            rect = find_image(self.canvas.screenshot_as_png, image_file, canvas_size)
            if rect:
                self.__click((rect[0]+rect[2])//2, (rect[1]+rect[3])//2)
                return True
            time.sleep(1)
        return False

    def drag_and_drop(self, x1, y1, x2, y2):
        True
