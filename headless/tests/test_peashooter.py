from tests.testing_utils import *

MAX_FRAME = 2000

class TestSunflower(unittest.TestCase):
    def test_peashooter1(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1", "peashooter")
        
        action_list = [
            ["plant", "peashooter", 0, 0],
            ["plant", "peashooter", 1, 0],
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
        
    
    def test_peashooter2(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2", "peashooter")
        
        action_list = [
            ["plant", "peashooter", 0, 0],
            ["plant", "peashooter", 0, 1],
            ["plant", "peashooter", 0, 2],
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    def test_peashooter3(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("3", "peashooter")
        
        action_list = [
            ["plant", "sunflower", 0, 2],
            ["plant", "sunflower", 1, 2],
            ["plant", "sunflower", 2, 2],
            ["plant", "peashooter", 0, 0],
            ["plant", "peashooter", 1, 0],
            ["plant", "peashooter", 2, 0],
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

