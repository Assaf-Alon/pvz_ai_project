from tests.testing_utils import *

class TestSunflower(unittest.TestCase):
    def test_Sunflower1(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1", "Sunflower")
        
        action_list = [
            ["plant", "Sunflower", 0, 0]
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
        
    
    def test_Sunflower2(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2", "Sunflower")
        
        action_list = [
            ["plant", "Sunflower", 4, 4],
            ["plant", "Sunflower", 1, 1],
            ["plant", "Sunflower", 1, 0],
            ["plant", "Sunflower", 2, 1]
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    def test_Sunflower3(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("3", "Sunflower")
        
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
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

