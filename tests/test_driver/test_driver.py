import unittest

from data_classes.sensor.data_in import GpsCoord
from driver.driver import add_gps_coord


class TestDriver(unittest.TestCase):

    def test_Testing(self):
        self.assertEqual(1 + 2 + 3, 6, "Should be 6")


    def test_addGPSCoordNotNone(self):
        coord1 = GpsCoord(1, 2.00, 3.00)
        coord2 = GpsCoord(2, 4.00, 6.00)
        route = [coord1, coord2]
        self.assertIsNotNone( add_gps_coord(route, coord1) )


if __name__ == '__main__':
    unittest.main()