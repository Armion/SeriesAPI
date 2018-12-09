
import app as api
import unittest
import requests


class FlaskrTestCase(unittest.TestCase):

    def test_getToken(self):
        self.assertIsInstance(api.getToken(), str)

    def test_getThumbNail(self):
        #particular case, can change if the TV API change
        self.assertEqual(api.getThumbnail(298566), "https://www.thetvdb.com/banners/_cache/posters/298566-2.jpg")

    def test_getSerie(self):
        self.assertEqual(api.getSerieById(133742), {"Error": "ID: 298566854 not found"}.json())



if __name__ == '__main__':
    unittest.main()