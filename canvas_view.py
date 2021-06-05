from selenium import webdriver

class CanvasView:
    def __init__(self, url, canvas_id):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10) # seconds
        self.driver.get(url)
        self.canvas = self.driver.find_element_by_id(canvas_id)
    def click_image(self, image_png):
        True
    def drag_and_drop(self, x1, y1, x2, y2):
        True
