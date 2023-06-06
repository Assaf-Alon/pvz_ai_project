from tests.testing_utils import *
test_plant = "WallNut"

class TestWallNut(unittest.TestCase):
    def test_WallNut1(self):
        test_num = "1"
        zombie_list = json.loads("""{
        "1": [["Normal", 3]]
        }
        """)
        
        allowed_plants = ["WallNut"]
        action_list = [
            ["plant", "WallNut", 3, 0]
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test(test_num, test_plant, level_data=zombie_list, allowed_plants=allowed_plants)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
    
    def test_WallNut2(self):
        test_num = "2"
        zombie_list = json.loads("""{
        "1": [["Normal", 3]],
        "2": [["Normal", 3]]
        }
        """)
        
        allowed_plants = ["WallNut"]
        action_list = [
            ["plant", "WallNut", 3, 3]
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test(test_num, test_plant, level_data=zombie_list, allowed_plants=allowed_plants)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
    
    def test_WallNut3(self):
        test_num = "3"
        zombie_list = json.loads("""{
        "1": [["Normal", 3]],
        "2": [["Normal", 3]],
        "3": [["Normal", 3]]
        }
        """)
        
        allowed_plants = ["WallNut"]
        action_list = [
            ["plant", "WallNut", 3, 3]
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test(test_num, test_plant, level_data=zombie_list, allowed_plants=allowed_plants)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
