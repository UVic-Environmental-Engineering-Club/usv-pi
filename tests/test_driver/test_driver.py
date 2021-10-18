import unittest

from src.data_classes.sensor.data_in import GpsCoord
from src.driver.driver import add_gps_coord

class TestDriver(unittest.TestCase):

    ###########################
    ## add_gps_coord() Tests ##
    ###########################

    def test_addGPSCoordNotNone(self):
        """Ensure function does not return none"""
        coord1 = GpsCoord(1, 2.00, 3.00)
        coord2 = GpsCoord(2, 4.00, 6.00)
        route = [coord1, coord2]
        self.assertIsNotNone( add_gps_coord(route, coord1) )


    def test_addGPSCoordEmptyRoute(self):
        """Ensure adding a coordinate to an empty route is successful"""
        emptyRoute = []
        coord = GpsCoord(1, 2.00, 3.00)
        result = [coord]
        self.assertEqual(result, add_gps_coord(emptyRoute, coord))


    def test_addGPSCoordNormalRoute(self):
        """Ensure adding a coordinate to a non-empty route is successful"""
        coord1 = GpsCoord(1, 2.00, 3.00)
        coord2 = GpsCoord(2, 4.00, 6.00)
        coord3 = GpsCoord(3, 6.00, 8.00)
        route = [coord1, coord2]
        result = [coord1, coord2, coord3]
        self.assertEqual(result, add_gps_coord(route, coord3))


    def test_addGPSCoordDoesNotChangeList(self):
        """Ensure the original route is not altered by adding a coordinate"""
        coord1 = GpsCoord(1, 2.00, 3.00)
        coord2 = GpsCoord(2, 4.00, 6.00)
        coord3 = GpsCoord(3, 6.00, 8.00)
        route = [coord1, coord2]
        result = [coord1, coord2]
        add_gps_coord(route, coord3)
        self.assertEqual(route, result)



    ##############################
    ## remove_gps_coord() Tests ##
    ##############################


if __name__ == '__main__':
    unittest.main()
    