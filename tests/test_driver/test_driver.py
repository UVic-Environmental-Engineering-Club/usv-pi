import unittest

from src.data_classes.sensor.data_in import GpsCoord
from src.driver.driver import add_gps_coord

class TestDriver(unittest.TestCase):
    
    ###########################
    ## add_gps_coord() Tests ##
    ###########################

    def test_addGPSCoordNotNone(self):
        """Tests add_grps_route will not return none"""
        coord1 = GpsCoord(1, 2.00, 3.00)
        coord2 = GpsCoord(2, 4.00, 6.00)
        route = [coord1, coord2]
        self.assertIsNotNone( add_gps_coord(route, coord1) )


    # Test you can add a coord to an empty route
    def test_addGPSCoordEmptyList(self):
        pass


    # Check a new new coord was successsfully added
    def test_addGPSCoordSuccessfullyAdded(self):
       pass

    # 

    ##############################
    ## remove_gps_coord() Tests ##
    ##############################


if __name__ == '__main__':
    unittest.main()