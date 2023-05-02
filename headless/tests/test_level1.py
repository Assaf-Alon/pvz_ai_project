from tests.testing_utils import *

class TestLevel1(unittest.TestCase):
    def test_level1(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1")
        
        action_list = [
            ["plant", "Sunflower", 0, 0],
            ["plant", "Sunflower", 1, 0],
            ["plant", "Peashooter", 1, 1],
            ["plant", "Peashooter", 2, 1]
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
    
    def test_level2(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2")
        
        action_list = [
            ["plant", "Sunflower", 0, 0],
            ["plant", "Sunflower", 1, 0],
            ["plant", "Peashooter", 1, 1],
            ["plant", "Peashooter", 2, 1]
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
    
    def test_level3(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("3")
        
        action_list = [
            ["plant", "Sunflower", 0, 0],
            ["plant", "Sunflower", 1, 0],
            ["plant", "Peashooter", 1, 1],
            ["plant", "Peashooter", 2, 1]
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    
# if __name__ == "__main__":