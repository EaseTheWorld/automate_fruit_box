import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from image_process import find_image
from image_process import save_image_with_size

class CanvasView:

    def __init__(self, url, canvas_id):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10) # seconds
        self.driver.get(url)
        self.canvas = self.driver.find_element_by_id(canvas_id)

    def close(self):
        if self.driver:
            self.driver.close()

    def __click(self, x, y):
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.canvas, x, y)
        action.click()
        action.perform()

    # os display scale is usually not 100%.
    def __canvas_size(self):
        return (int(self.canvas.size['width']), int(self.canvas.size['height']))

    def click_image_with_timeout(self, image_file, timeout):
        for i in range(timeout):
            rect = find_image(self.canvas.screenshot_as_png, image_file, self.__canvas_size())
            if rect:
                self.__click((rect[0]+rect[2])//2, (rect[1]+rect[3])//2)
                return True
            time.sleep(1)
        return False

    def save_screenshot_file(self, image_file_to_save):
        save_image_with_size(self.canvas.screenshot_as_png, self.__canvas_size(), image_file_to_save)

    # wait=2 for Firefox, wait=0 for Chrome
    def drag_and_drop(self, x1, y1, x2, y2, wait=0):
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.canvas, x1, y1)
        action.click_and_hold()
        # wait dragging is applied
        for i in range(wait):
            x = x2 if i % 2 == 0 else x2-1
            action.move_to_element_with_offset(self.canvas, x, y2)
        action.move_to_element_with_offset(self.canvas, x2, y2)
        action.release()
        action.perform()

    def popup(self, msg, timeout=3):
        self.driver.execute_script(f'alert(\'{msg}\');')
        alert = self.driver.switch_to_alert()
        time.sleep(timeout)
        alert.accept()
