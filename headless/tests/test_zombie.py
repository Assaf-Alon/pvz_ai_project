from tests.testing_utils import *

class TestSunflower(unittest.TestCase):
    def test_zombie1(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("1", "zombie")
        
        action_list = [
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)
        
    
    def test_zombie2(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("2", "zombie")
        
        action_list = [
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

    def test_zombie3(self):
        env, EXPECTED_FILE, ACTUAL_FILE, LEVEL_JSON = setup_test("3", "zombie")
        
        action_list = [
        ]
        
        play_game(env, action_list)
            
        passed = compare_results(EXPECTED_FILE, ACTUAL_FILE)
        self.assertTrue(passed)

