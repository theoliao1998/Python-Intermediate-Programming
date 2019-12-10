import unittest
import data

class Tests(unittest.TestCase):

    def test_init_db(self):
        res = data.query("SELECT s.name, a.name, a.IATA FROM Airports AS a JOIN States AS s ON a.state_id=s.Id WHERE a.IATA='DTW'")
        self.assertEqual(res,[("Michigan","Detroit Metropolitan Wayne County Airport","DTW",)])
        res = data.query("SELECT s.name, a.name, a.IATA FROM Airports AS a JOIN States AS s ON a.state_id=s.Id WHERE a.IATA='SEA'")
        self.assertEqual(res,[("Washington","Seattle Tacoma International Airport","SEA",)])
        res = data.query("SELECT s.name, a.name, a.IATA FROM Airports AS a JOIN States AS s ON a.state_id=s.Id WHERE a.IATA='JFK'")
        self.assertEqual(res,[("New-York","John F Kennedy International Airport","JFK",)])

    # this is a "test"
    def test_busy_airports(self):
        busy_airports = data.get_busy_airports()
        self.assertTrue('DTW' in busy_airports)
        self.assertTrue('LAX' in busy_airports)
        self.assertTrue('JFK' in busy_airports)
        self.assertTrue('LGA' in busy_airports)
    
    def test_get_state_airport(self):
        res = data.get_airports("Michigan")
        self.assertTrue(("Detroit","DTW\n","Detroit Metropolitan Wayne County Airport") in res)
        res = data.get_airports("California")
        self.assertTrue(("Los Angeles","LAX\n","Los Angeles International Airport") in res)
        res = data.get_airports("New-York")
        self.assertTrue(('New York', 'JFK\n', 'John F. Kennedy International Airport') in res)
        self.assertTrue(('New York', 'LGA\n', 'LaGuardia Airport') in res)
    
    def test_get_loc(self):
        loc = data.get_loc("DTW")
        self.assertEqual(loc,(42.2123985291,-83.3534011841,))
        loc = data.get_loc("LGA")
        self.assertEqual(loc,(40.77719879,-73.87259674,))
        loc = data.get_loc("JFK")
        self.assertEqual(loc,(40.63980103,-73.77890015,))
        loc = data.get_loc("EWR")
        self.assertEqual(loc,(40.6925010681,-74.1687011719,))


if __name__ == "__main__":
    unittest.main()