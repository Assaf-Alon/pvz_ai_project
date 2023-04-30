from tests.testing_utils import *

class TestSunflower(unittest.TestCase):
    def test_sunflower1(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1", "sunflower")
        
        action_list = [
            ["plant", "sunflower", 0, 0]
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
        
    
    def test_sunflower2(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2", "sunflower")
        
        action_list = [
            ["plant", "sunflower", 4, 4],
            ["plant", "sunflower", 1, 1],
            ["plant", "sunflower", 1, 0],
            ["plant", "sunflower", 2, 1]
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    def test_sunflower3(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("3", "sunflower")
        
        action_list = [
            ["plant", "sunflower", 3, 4],
            ["plant", "sunflower", 3, 1],
            ["plant", "sunflower", 3, 0],
            ["plant", "sunflower", 3, 2],
            ["plant", "sunflower", 3, 5],
            ["plant", "sunflower", 3, 4],
            ["plant", "sunflower", 3, 3],
            ["plant", "sunflower", 3, 2],
            ["plant", "sunflower", 3, 1],
            ["plant", "sunflower", 3, 0],
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

