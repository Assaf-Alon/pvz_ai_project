from tests.testing_utils import *
test_plant = "PotatoMine"

class TestPotatoMine(unittest.TestCase):
    def test_PotatoMine1(self):
        test_num = "1"
        zombie_list = json.loads("""{
        "1": [["Normal", 3]]
        }
        """)
        
        allowed_plants = ["PotatoMine"]
        action_list = [
            ["plant", "PotatoMine", 3, 0]
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test(test_num, test_plant, level_data=zombie_list, allowed_plants=allowed_plants)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
    
    def test_PotatoMine2(self):
        test_num = "2"
        zombie_list = json.loads("""{
        "1": [["Normal", 3]],
        "2": [["Normal", 3]]
        }
        """)
        
        allowed_plants = ["PotatoMine"]
        action_list = [
            ["plant", "PotatoMine", 3, 3]
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test(test_num, test_plant, level_data=zombie_list, allowed_plants=allowed_plants)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
    
    def test_PotatoMine3(self):
        test_num = "3"
        zombie_list = json.loads("""{
        "1": [["Normal", 3]],
        "2": [["Normal", 3]],
        "3": [["Normal", 3]]
        }
        """)
        
        allowed_plants = ["PotatoMine"]
        action_list = [
            ["plant", "PotatoMine", 3, 3],
            ["plant", "PotatoMine", 3, 2],
            ["plant", "PotatoMine", 3, 1]
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test(test_num, test_plant, level_data=zombie_list, allowed_plants=allowed_plants)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    def test_PotatoMine4(self):
        test_num = "4"
        zombie_list = json.loads("""{
        "1": [["Normal", 3]],
        "2": [["Normal", 3]],
        "3": [["Normal", 3]]
        }
        """)
        
        allowed_plants = ["PotatoMine"]
        action_list = [
            ["plant", "PotatoMine", 3, 3],
            ["plant", "PotatoMine", 3, 0]
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test(test_num, test_plant, level_data=zombie_list, allowed_plants=allowed_plants)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
