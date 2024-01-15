import selenium
import unittest
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class LocationResponseTest(unittest.TestCase):

    def setUp(self):
        # create a WebDriver that is used to interact with the Weather-aap website
        self.driver = selenium.webdriver.Firefox()


    def tearDown(self):
        # Close the WebDriver instance
        self.driver.close()

    def test_positive_location_response(self):
        # open app home page
        self.driver.get('http://localhost:5000')
        # find the location input field and enter valid
        location_input = self.driver.find_element("id","location")
        location_input.send_keys('London')
        # submit the form
        location_input.send_keys(Keys.ENTER)
        time.sleep(10)
        # check if the weather information is displayed
        weather_info = self.driver.find_element(By.TAG_NAME, "table")
        self.assertTrue(weather_info.is_displayed())

    def test_negative_location_response(self):
        # open app home page
        self.driver.get('http://localhost:5000')
        # find the location input field and enter valid
        location_input = self.driver.find_element("id", "location")
        location_input.send_keys('Invalid City')
        # submit the form
        location_input.send_keys(Keys.ENTER)
        time.sleep(10)
        # check if the weather information is displayed
        weather_info = self.driver.find_element(By.TAG_NAME, "p")
        self.assertTrue(weather_info.is_displayed())
        time.sleep(10)



if __name__ == '__main__':
    unittest.main()