from tests.testing_utils import *

MAX_FRAME = 2000

class TestSunflower(unittest.TestCase):
    def test_Peashooter1(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1", "Peashooter")
        
        action_list = [
            ["plant", "Peashooter", 0, 0],
            ["plant", "Peashooter", 1, 0],
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
        
    
    def test_Peashooter2(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2", "Peashooter")
        
        action_list = [
            ["plant", "Peashooter", 0, 0],
            ["plant", "Peashooter", 0, 1],
            ["plant", "Peashooter", 0, 2],
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    def test_Peashooter3(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("3", "Peashooter")
        
        action_list = [
            ["plant", "Sunflower", 0, 2],
            ["plant", "Sunflower", 1, 2],
            ["plant", "Sunflower", 2, 2],
            ["plant", "Peashooter", 0, 0],
            ["plant", "Peashooter", 1, 0],
            ["plant", "Peashooter", 2, 0],
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

