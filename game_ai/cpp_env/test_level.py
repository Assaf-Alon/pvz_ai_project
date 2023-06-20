import unittest
import level as cpp_level


SUN_INTERVAL = 6

class TestLevel(unittest.TestCase):
    def test_suns_fps_10(self):
        FPS = 10
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(FPS*100, 0, "normal"))
        level = cpp_level.Level(5, 10, FPS, level_data, [])
        self.assertFalse(level.done, "No more zombies to be spawned")
        self.assertFalse(level.win)
        self.assertEqual(level.frame, 1)
        self.assertEqual(level.suns, 50)
        
        frames_til_sun = SUN_INTERVAL * FPS
        
        for i in range(frames_til_sun):
            level.step(level.no_action)
            self.assertEqual(level.frame, i + 2)
        self.assertEqual(level.suns, 50)
        level.step()
        self.assertEqual(level.suns, 75)
        
        for _ in range(frames_til_sun - 1):
            level.step()
        self.assertEqual(level.suns, 75)
        level.step()
        self.assertEqual(level.suns, 100)
    
    def test_suns_fps_30(self):
        FPS = 30
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(FPS*100, 0, "normal"))
        level = cpp_level.Level(5, 10, FPS, level_data, [])
        self.assertFalse(level.done, "No more zombies to be spawned")
        self.assertFalse(level.win)
        self.assertEqual(level.frame, 1)
        self.assertEqual(level.suns, 50)
        
        frames_til_sun = SUN_INTERVAL * FPS
        
        for i in range(frames_til_sun):
            level.step(level.no_action)
            self.assertEqual(level.frame, i + 2)
        self.assertEqual(level.suns, 50)
        level.step()
        self.assertEqual(level.suns, 75)
        
        for _ in range(frames_til_sun - 1):
            level.step()
        self.assertEqual(level.suns, 75)
        level.step()
        self.assertEqual(level.suns, 100)
        
    def test_lawnmower1(self):
        FPS = 10
        ZOMBIE_SPEED = 4.7
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(100 * FPS, 0, "normal"))
        level = cpp_level.Level(5, 10, FPS, level_data, [])
        
        frames_to_reach_house = int(ZOMBIE_SPEED * 10 * FPS)
        
        for i in range(frames_to_reach_house + FPS - 1):
            print(f"frame {level.frame}")
            level.step()
            self.assertTrue(level.lawnmowers[0])
        level.step()
        self.assertFalse(level.lawnmowers[0])
    
    
if __name__ == '__main__':
    unittest.main()
