from tests.testing_utils import *

class TestZombie(unittest.TestCase):
    def test_zombie1(self):
        zombie_list = json.loads("""{
        "10": [["Normal", 1]]
        }
        """)
        
        action_list = [
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1", "zombie", level_data=zombie_list)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
        
    
    def test_zombie2(self):
        zombie_list = json.loads("""{
        "50": [["Normal", 0], ["Normal", 1], ["Normal", 2], ["Normal", 3], ["Normal", 4]]
        }
        """)
        
        action_list = [
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2", "zombie", level_data=zombie_list)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    def test_zombie3(self):
        zombie_list = json.loads("""{
        "10": [["Normal", 0], ["Normal", 1], ["Normal", 2], ["Normal", 3], ["Normal", 4]],
        "20": [["Normal", 0], ["Normal", 1], ["Normal", 2], ["Normal", 3], ["Normal", 4]],
        "30": [["Normal", 0], ["Normal", 1], ["Normal", 2], ["Normal", 3], ["Normal", 4]],
        "40": [["Normal", 0], ["Normal", 1], ["Normal", 2], ["Normal", 3], ["Normal", 4]],
        "50": [["Normal", 0], ["Normal", 1], ["Normal", 2], ["Normal", 3], ["Normal", 4]],
        "60": [["Normal", 0], ["Normal", 1], ["Normal", 2], ["Normal", 3], ["Normal", 4]],
        "70": [["Normal", 0], ["Normal", 1], ["Normal", 2], ["Normal", 3], ["Normal", 4]]
        }
        """)
        
        action_list = [
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("3", "zombie", level_data=zombie_list)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

