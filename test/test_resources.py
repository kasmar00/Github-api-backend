import unittest
import json

import app.resources as resources


def loadJson():
    with open("test/data.json") as f:
        data = json.loads(f.read())
    return data


class Test(unittest.TestCase):

    def test_extraction(self):
        self.assertEqual([{"name": "akubra",  "stars": 79}, {
                         "name": "allegro-api",  "stars": 132}], resources.github.extractData(loadJson()))
        self.assertEqual([], resources.github.extractData([]))

    def test_download(self):
        # check if a list is returned
        self.assertIsInstance(resources.github.getUrl("allegro"), list)
        # check if wrong username returns a list
        self.assertRaisesRegex(Exception, "User not found", resources.github.getUrl,
                               "vioreikaithae3vah3miu5lie6YooRahnohdii")
        # check empty username
        self.assertRaisesRegex(Exception, "Bad username",
                               resources.github.getUrl,  "")
        self.assertRaisesRegex(Exception, "Bad username",
                               resources.github.getUrl,  "dshfdhadfhfh asdrfygaedhthte")
        self.assertRaisesRegex(Exception, "Bad username",
                               resources.github.getUrl,  "aafadsfdaf/asdgsdgafdsgaf")

        self.assertTrue(True in [({"name": "linux"}.items() <= i.items())
                        for i in resources.github.getUrl("torvalds")])

    def test_sumStar(self):
        self.assertEqual(211, resources.Stars.starSum([{"name": "akubra",  "stars": 79}, {
                         "name": "allegro-api",  "stars": 132}]))


if __name__ == '__main__':
    unittest.main()
