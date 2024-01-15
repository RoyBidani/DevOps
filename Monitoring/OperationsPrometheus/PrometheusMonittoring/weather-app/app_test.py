import unittest
import requests

class WebTestReachable(unittest.TestCase):

    def test_web_reachable(self):
        try:
            # Make a GET request to the website
            response = requests.get('http://localhost:8000')
            # Check that the response status code is 200
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.ConnectionError:
            # The website is not reachable
            self.assertFalse('Website is not reachable')


if __name__ == '__main__':
    unittest.main()
