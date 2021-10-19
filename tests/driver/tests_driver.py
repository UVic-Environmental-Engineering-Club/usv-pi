import unittest

from src.data_classes.sensor.data_in import GpsCoord
from src.driver.driver import add_gps_coord, remove_gps_coord, reset_route

class TestDriver(unittest.TestCase):

    """
    add_gps_coord() Tests
    """
  
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


    """
    remove_gps_coord() Tests
    """

    def test_removeGPSCoordOnEmptyRoute(self):
        """Ensure an error is not thrown when called to remove a coordinate on an empty list"""
        coord1 = GpsCoord(1, 2.00, 3.00)
        route = []
        remove_gps_coord(route, coord1)
        # A test will fail if any unhandled exception is raised (no assert)


    def test_removeGPSCoordWithOneCoord(self):
        """Ensure the function can successfully remove a coordinate that exists in the route one time"""
        coord1 = GpsCoord(1, 2.00, 3.00)
        coord2 = GpsCoord(2, 4.00, 6.00)
        coord3 = GpsCoord(3, 6.00, 9.00)
        route = [coord1, coord2, coord3]
        result = [coord2, coord3]
        self.assertEqual(result, remove_gps_coord(route, coord1))


    def test_removeGPSCoordWithReoccurringCoord(self):
        """Ensure the function can remove all occurences of a coord in the route"""
        coord1 = GpsCoord(1, 2.00, 3.00)
        coord2 = GpsCoord(2, 4.00, 6.00)
        coord3 = GpsCoord(3, 6.00, 9.00)
        route = [coord2, coord1, coord2, coord3, coord1, coord3]
        result = [coord2, coord2, coord3, coord3]
        self.assertEqual(result, remove_gps_coord(route, coord1))


    def test_removeGPSCoordDoesNotChangeOriginalRoute(self):
        """Ensure function does not change the original route (it returns a new, altered list)"""
        coord1 = GpsCoord(1, 2.00, 3.00)
        coord2 = GpsCoord(2, 4.00, 6.00)
        coord3 = GpsCoord(3, 6.00, 9.00)
        route = [coord2, coord1, coord2, coord3, coord1, coord3]
        result = [coord2, coord1, coord2, coord3, coord1, coord3]
        remove_gps_coord(route, coord1)
        self.assertEqual(route, result)


    def test_removeGPSCoordOnRouteWithBadCoord(self):
        """"Ensure calling the function with a coord not on the route does not change the route"""
        coord1 = GpsCoord(1, 2.00, 3.00)
        coord2 = GpsCoord(2, 4.00, 6.00)
        coord3 = GpsCoord(3, 6.00, 9.00)
        coord4 = GpsCoord(4, 8.00, 12.00)
        route = [coord2, coord1, coord2, coord3, coord1, coord3, coord2]
        result = [coord2, coord1, coord2, coord3, coord1, coord3, coord2]
        self.assertEqual(result, remove_gps_coord(route, coord4))



    """
    reset_route() Tests 
    """
    

    def test_resetRouteIsEmptyList(self):
        """Ensure an empty list is returned"""
        self.assertEqual(0, len(reset_route()) )


    def test_resetRouteCanAddGpsCoord(self):
        """Ensure you can add GpsCoord's to the reset route"""
        route = reset_route()
        coord1 = GpsCoord(1, 2.00, 3.00)
        self.assertEqual([coord1], route + [coord1])



    """
    start_route() Tests
    """


    """
    pause_route() Tests
    """


if __name__ == '__main__':
    unittest.main()
