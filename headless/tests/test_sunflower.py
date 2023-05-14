from tests.testing_utils import *

test_plant = "Sunflower"
class TestSunflower(unittest.TestCase):
    def test_Sunflower1(self):
        
        zombie_list = json.loads("""{
        "50": [["Normal", 3]]
        }
        """)
        
        action_list = [
            ["plant", "Sunflower", 0, 0]
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1", test_plant, level_data=zombie_list)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
        
    def test_Sunflower2(self):
        zombie_list = json.loads("""{
        "10": [["Normal", 3]],
        "20": [["Normal", 3]],
        "30": [["Normal", 3]],
        "60": [["Normal", 3]]
        }
        """)
        action_list = [
            ["plant", "Sunflower", 4, 4],
            ["plant", "Sunflower", 1, 1],
            ["plant", "Sunflower", 1, 0],
            ["plant", "Sunflower", 2, 1]
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2", "Sunflower", level_data=zombie_list)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    def test_Sunflower3(self):
        zombie_list = json.loads("""{
        "10": [["Normal", 3]],
        "20": [["Normal", 3]],
        "30": [["Normal", 3]],
        "60": [["Normal", 3]]
        }
        """)
        
        action_list = [
            ["plant", "Sunflower", 3, 4],
            ["plant", "Sunflower", 3, 1],
            ["plant", "Sunflower", 3, 0],
            ["plant", "Sunflower", 3, 2],
            ["plant", "Sunflower", 3, 5],
            ["plant", "Sunflower", 3, 4],
            ["plant", "Sunflower", 3, 3],
            ["plant", "Sunflower", 3, 2],
            ["plant", "Sunflower", 3, 1],
            ["plant", "Sunflower", 3, 0],
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("3", "Sunflower", level_data=zombie_list)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

