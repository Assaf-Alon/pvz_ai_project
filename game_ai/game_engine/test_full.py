import unittest
import level as cpp_level


SUN_INTERVAL = 6
DEFAULT_FPS = 10

class TestLevel(unittest.TestCase):
    def test_suns_fps_10(self):
        FPS = 10
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(100, 0, "normal"))
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
        level_data.push_back(cpp_level.ZombieSpawnTemplate(100, 0, "normal"))
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
        level_data.push_back(cpp_level.ZombieSpawnTemplate(100, 0, "normal"))
        level = cpp_level.Level(5, 10, FPS, level_data, [])
        
        frames_to_reach_house = int(ZOMBIE_SPEED * 10 * FPS)
        
        for i in range(frames_to_reach_house + FPS - 1):
            level.step()
            self.assertTrue(level.lawnmowers[0])
        level.step()
        self.assertFalse(level.lawnmowers[0])
    
    def test_lawnmower2(self):
        FPS = 10
        ZOMBIE_SPEED = 4.7
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(60, 0, "normal"))
        level = cpp_level.Level(5, 10, FPS, level_data, [])
        
        frames_to_reach_house = int(ZOMBIE_SPEED * 10 * FPS)
        
        for i in range(frames_to_reach_house + FPS - 1):
            level.step()
            self.assertTrue(level.lawnmowers[0])
        level.step()
        self.assertFalse(level.lawnmowers[0])   
        
        while level.frame < FPS * (60 + ZOMBIE_SPEED * 10):
            level.step()
            self.assertFalse(level.done)
        level.step()
        self.assertTrue(level.done)
        self.assertFalse(level.win)
    
    def test_legal_plants1(self):
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(2000, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [])
        
        while level.frame <= 1000 * DEFAULT_FPS:
            for plant in range(1, cpp_level.NUM_PLANTS):
                self.assertFalse(level.is_action_legal(plant, 0, 0), msg=f"Managed to plant {plant} in frame {level.frame} even though it's not legal")
            level.step()

    def test_cooldown1(self):
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(2000, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.SUNFLOWER])
        
        SUN_COOLDOWN = 7.5 # TODO - get this from plant data
        
        while level.frame <= 15 * DEFAULT_FPS:
            level.step()
        level.step(cpp_level.SUNFLOWER, 0, 0)
        while not level.is_action_legal(cpp_level.SUNFLOWER, 1, 0):
            level.step()
        
        self.assertEqual(level.frame, DEFAULT_FPS * (15 + SUN_COOLDOWN) + 1)
        level.step(cpp_level.SUNFLOWER, 1, 0)
        self.assertEqual(level.suns, 50)
    
    def test_cooldown2(self):
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(2000, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.POTATOMINE])
        
        MINE_COOLDOWN = 30 # TODO - get this from plant data
        self.assertTrue(level.is_action_legal(cpp_level.POTATOMINE, 0, 0))
        level.step(cpp_level.POTATOMINE, 0, 0)
        while not level.is_action_legal(cpp_level.POTATOMINE, 0, 1):
            level.step()
        self.assertEqual(level.frame, DEFAULT_FPS * MINE_COOLDOWN + 1)
        level.step(cpp_level.POTATOMINE, 0, 1)
    
class TestSunflower(unittest.TestCase):
    def test_sunflower1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(200, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.SUNFLOWER])
        
        # Place Sunflower
        self.assertEqual(level.suns, 50)
        cpp_action = cpp_level.Action(cpp_level.SUNFLOWER, 2, 2)
        self.assertTrue(level.is_action_legal(cpp_action))
        level.step(cpp_action)
        self.assertEqual(level.suns, 0)
        self.assertEqual(level.frame, 2)
        
        frames_til_sun = int(SUN_INTERVAL * DEFAULT_FPS)
        frames_til_sunflower = int(24.25 * DEFAULT_FPS) # TODO - Take this from plant data

        while level.frame < 150 * DEFAULT_FPS:
            gain_from_sky = int((level.frame - 2) // frames_til_sun)
            gain_from_flower = int((level.frame + 18 * DEFAULT_FPS) // frames_til_sunflower)
            expected_suns = 25 *(gain_from_flower + gain_from_sky)
            self.assertEqual(level.suns, expected_suns, msg=f"Frame: {level.frame}, suns: {level.suns}, expected: {expected_suns}.   {gain_from_flower} from sunflower, and {gain_from_sky} from sky.")
            level.step()
    
    def test_sunflower2(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(200, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.SUNFLOWER])
        
        # Place Sunflower
        self.assertEqual(level.suns, 50)
        level.step(cpp_level.SUNFLOWER, 2, 2)
        self.assertEqual(level.suns, 0)
        self.assertEqual(level.frame, 2)
        
        frames_til_sun = int(SUN_INTERVAL * DEFAULT_FPS)
        frames_til_sunflower = int(24.25 * DEFAULT_FPS) # TODO - Take this from plant data

        while level.frame < 6 * DEFAULT_FPS + 2:
            level.step()
        
        self.assertEqual(level.suns, 50)
        level.step(cpp_level.SUNFLOWER, 1, 1)
        
        while level.frame < 150 * DEFAULT_FPS:
            gain_from_sky = int((level.frame - 2) // frames_til_sun)
            gain_from_flower1 = int((level.frame + 18 * DEFAULT_FPS) // frames_til_sunflower)
            gain_from_flower2 = int((level.frame + 18 * DEFAULT_FPS - 62) // frames_til_sunflower)
            
            expected_suns = 25 *(gain_from_flower1 + gain_from_flower2 + gain_from_sky)
            self.assertEqual(level.suns, expected_suns, msg=f"Frame: {level.frame}, suns: {level.suns}, expected: {expected_suns}.   {gain_from_sky, gain_from_flower1, gain_from_flower2}")
            level.step()

class TestPeaShooter(unittest.TestCase):
    def test_peashooter1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(200, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        while not level.is_action_legal(cpp_level.PEASHOOTER, 0, 0):
            level.step()
        level.step(cpp_level.PEASHOOTER, 0, 0)
        self.assertEqual(level.frame, DEFAULT_FPS * 12 + 3)
        self.assertEqual(level.suns, 0)

    def test_peashooter2(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(20, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        ZOMBIE_HP = 181
        ZOMBIE_SPAWN_FRAME = 20 * DEFAULT_FPS
        PLANT_SHOOT_SPEED = round(1.425 * DEFAULT_FPS)
        PLANT_DAMAGE = 20
        
        while not level.is_action_legal(cpp_level.PEASHOOTER, 0, 0):
            level.step()
        level.step(cpp_level.PEASHOOTER, 0, 0)
        self.assertEqual(level.frame, DEFAULT_FPS * 12 + 3)
        self.assertEqual(level.suns, 0)
        
        while not level.done:
            level.step()
        self.assertTrue(level.lawnmowers[0])
        self.assertTrue(level.win)
        self.assertLessEqual(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED)))   # It should be dead now
        self.assertGreater(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - 2 - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED))) # It should be alive in the previous frame
    
    def test_peashooter3(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(70, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        ZOMBIE_HP = 181
        ZOMBIE_SPAWN_FRAME = 70 * DEFAULT_FPS
        PLANT_SHOOT_SPEED = round(1.425 * DEFAULT_FPS)
        PLANT_DAMAGE = 40
        
        while level.frame <= DEFAULT_FPS * 30:
            level.step()
        self.assertTrue(level.is_action_legal(cpp_level.PEASHOOTER, 0, 0))
        level.step(cpp_level.PEASHOOTER, 0, 0)
        
        while level.frame <= DEFAULT_FPS * 50:
            level.step()
            
        self.assertTrue(level.is_action_legal(cpp_level.PEASHOOTER, 0, 1))
        level.step(cpp_level.PEASHOOTER, 0, 1)
        
        while not level.done:
            level.step()
        self.assertTrue(level.lawnmowers[0])
        self.assertTrue(level.win)
        self.assertLessEqual(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED)))   # It should be dead now
        self.assertGreater(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - 2 - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED))) # It should be alive in the previous frame



if __name__ == '__main__':
    unittest.main()
