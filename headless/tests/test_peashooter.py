from tests.testing_utils import *

MAX_FRAME = 2000
test_plant = "Peashooter"
class TestPeashooter(unittest.TestCase):
    def test_Peashooter1(self):
        zombie_list = dict()
        zombie_list["50"] = [["Normal", 0]]
        
        action_list = [
            ["plant", "Peashooter", 0, 0],
            ["plant", "Peashooter", 1, 0],
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1", test_plant, zombie_list)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
        
    
    def test_Peashooter2(self):
        zombie_list = json.loads("""{
        "10": [["Normal", 0]],
        "20": [["Normal", 0]],
        "30": [["Normal", 0]],
        "40": [["Normal", 0]],
        "50": [["Normal", 0]],
        "60": [["Normal", 0]]
        }
        """)
        
        action_list = [
            ["plant", "Peashooter", 0, 0],
            ["plant", "Peashooter", 0, 1],
            ["plant", "Peashooter", 0, 2],
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2", test_plant, level_data=zombie_list)
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    def test_Peashooter3(self):
        zombie_list = json.loads("""{
        "30": [["Normal", 0], ["Normal", 1], ["Normal", 2]],
        "32": [["Normal", 0]],
        "34": [["Normal", 0], ["Normal", 1], ["Normal", 2]],
        "36": [["Normal", 0]],
        "38": [["Normal", 0]],
        "40": [["Normal", 0]]
        }
        """)
        action_list = [
            ["plant", "Sunflower", 0, 2],
            ["plant", "Sunflower", 1, 2],
            ["plant", "Sunflower", 2, 2],
            ["plant", "Peashooter", 0, 0],
            ["plant", "Peashooter", 1, 0],
            ["plant", "Peashooter", 2, 0],
        ]
        
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("3", test_plant, level_data=zombie_list)
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

