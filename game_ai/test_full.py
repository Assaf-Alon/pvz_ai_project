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
        SUN_COOLDOWN = int(7.5 * DEFAULT_FPS)
        new_sunflower = cpp_level.Action(cpp_level.SUNFLOWER, 1, 1)
        
        while level.frame < SUN_COOLDOWN + 1:
            self.assertFalse(level.is_action_legal(new_sunflower))
            level.step()
        self.assertEqual(level.frame, SUN_COOLDOWN + 1)
        self.assertEqual(level.suns, 50)
        level.step(new_sunflower)
        self.assertEqual(level.suns, 0)
        second_sun_summon_frame = level.frame
        while level.frame < 6 * DEFAULT_FPS + 2:
            level.step()
        
        
        while level.frame < 150 * DEFAULT_FPS:
            gain_from_sky = int((level.frame - 2) // frames_til_sun) - 1
            gain_from_flower1 = int((level.frame + 18 * DEFAULT_FPS) // frames_til_sunflower) - 1
            gain_from_flower2 = int((level.frame + 18 * DEFAULT_FPS + 2 - second_sun_summon_frame) // frames_til_sunflower)
            
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

class TestZombies(unittest.TestCase):
    def test_zombie_speed1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(48, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        while not level.done:
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (10 * 4.7 + 1)))
    
    def test_zombie_speed2(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(49, 0, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        while not level.done:
            level.step()
        
        self.assertTrue(level.done)
        self.assertFalse(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (10 * 4.7 + 49)))
    
    def test_conehead_speed(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "conehead"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(49, 0, "conehead"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        while not level.done:
            level.step()
        
        self.assertTrue(level.done)
        self.assertFalse(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (10 * 4.7 + 49)))
    
    def test_flagzombie_speed(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "flag"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        while not level.done:
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (10 * 3.7 + 1)))

    def test_newspaperzombie_speed1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "newspaper"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        while not level.done:
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (10 * 4.7 + 1)))
                
    def test_newspaperzombie_speed2(self):
        # Init level
        seconds_until_spawn = 16
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(seconds_until_spawn, 0, "newspaper"))
        level = cpp_level.Level(5, 10, 10, level_data, [cpp_level.PEASHOOTER])
        
        while level.frame < (seconds_until_spawn - 2) * 10:
            level.step()
        
        self.assertTrue(level.is_action_legal(cpp_level.PEASHOOTER, 0, 0))
        level.step(cpp_level.PEASHOOTER, 0, 7)
        
        # 331 -> 181
        while not level.done:
            level.step()
        self.assertTrue(level.done)
        self.assertTrue(level.win)
        
        frames_until_spawn = 10 * seconds_until_spawn
        no_newspaper_speed = int(1.8 * 10)
        newspaper_speed = int(4.7 * 10)
        frames_with_newspaper = int(1.4 * 8 * 10) # Peashooter speed * the amount of shots to reduce HP enough (331-181)=150
        frames_attacking = 3 * 10
        distance_with_newspaper = frames_with_newspaper // newspaper_speed
        frames_with_newspaper = distance_with_newspaper * newspaper_speed
        distance_without_newspaper = 10 - distance_with_newspaper
        frames_without_newspaper = no_newspaper_speed * distance_without_newspaper
        self.assertEqual(level.frame, frames_until_spawn + frames_with_newspaper + frames_without_newspaper + frames_attacking)

    def test_pole_speed1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "pole"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        while not level.done:
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (10 * 2.5 + 1)))
    
    def test_pole_speed2(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "pole"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(30, 0, "pole"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        while level.frame < 30 * DEFAULT_FPS:
            level.step()
        
        self.assertTrue(level.is_action_legal(cpp_level.PEASHOOTER, 0, 7))
        level.step(cpp_level.Action(cpp_level.PEASHOOTER, 0, 7))
        # 9 --> 7 in 5 seconds [50 frames]
        # 7 --> 6 in 1 second  [10 frames] (Attacking)
        # 6 --> 0 32.9 seconds [329 frames]
        
        while not level.done:
            level.step()
        
        self.assertTrue(level.done)
        self.assertFalse(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (30 + 5 + 1 + 7 * 4.7)))
    
    def test_football_speed(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(1, 0, "football"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        while not level.done:
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (10 * 2.5 + 1)))
    
    def test_zombie_hp(self):
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
    
    def test_conezombie_hp(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(20, 0, "conehead"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER])
        
        ZOMBIE_HP = 551
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

    def test_bucketzombie_hp1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(30, 0, "buckethead"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER, cpp_level.WALLNUT])
        
        ZOMBIE_HP = 1281
        ZOMBIE_SPAWN_FRAME = 30 * DEFAULT_FPS
        PLANT_SHOOT_SPEED = round(1.425 * DEFAULT_FPS)
        PLANT_DAMAGE = 20
        
        while not level.is_action_legal(cpp_level.PEASHOOTER, 0, 0):
            level.step()
        level.step(cpp_level.PEASHOOTER, 0, 0)
        self.assertEqual(level.frame, DEFAULT_FPS * 12 + 3)
        self.assertEqual(level.suns, 0)
        
        while not level.is_action_legal(cpp_level.WALLNUT, 0, 5):
            level.step()
        self.assertEqual(level.frame, DEFAULT_FPS * 24 + 2)
        level.step(cpp_level.WALLNUT, 0, 5)
        
        while not level.done:
            level.step()
            if level.is_action_legal(cpp_level.WALLNUT, 0, 3):
                level.step(cpp_level.WALLNUT, 0, 3)
        self.assertTrue(level.lawnmowers[0])
        self.assertTrue(level.win)
        self.assertLessEqual(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED)))   # It should be dead now
        self.assertGreater(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - 2 - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED))) # It should be alive in the previous frame

    def test_bucketzombie_hp2(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(30, 0, "buckethead"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER, cpp_level.WALLNUT])
        
        while not level.is_action_legal(cpp_level.PEASHOOTER, 0, 0):
            level.step()
        level.step(cpp_level.PEASHOOTER, 0, 0)
        self.assertEqual(level.frame, DEFAULT_FPS * 12 + 3)
        self.assertEqual(level.suns, 0)
        
        while not level.is_action_legal(cpp_level.WALLNUT, 0, 5):
            level.step()
        self.assertEqual(level.frame, DEFAULT_FPS * 24 + 2)
        level.step(cpp_level.WALLNUT, 0, 5)
        
        while not level.done:
            level.step()

        self.assertFalse(level.lawnmowers[0])
        self.assertTrue(level.win)
        self.assertEqual(level.frame, DEFAULT_FPS * (30 + 40 + 3 + 47))

    def test_polezombie_hp1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(30, 0, "pole"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER, cpp_level.WALLNUT])
        
        ZOMBIE_HP = 335
        ZOMBIE_SPAWN_FRAME = 30 * DEFAULT_FPS
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
    
    def test_polezombie_hp2(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(30, 0, "pole"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER, cpp_level.WALLNUT])
        
        ZOMBIE_HP = 335
        ZOMBIE_SPAWN_FRAME = 30 * DEFAULT_FPS
        PLANT_SHOOT_SPEED = round(1.425 * DEFAULT_FPS)
        PLANT_DAMAGE = 20
        
        while not level.is_action_legal(cpp_level.PEASHOOTER, 0, 0):
            level.step()
        level.step(cpp_level.PEASHOOTER, 0, 0)
        self.assertEqual(level.frame, DEFAULT_FPS * 12 + 3)
        self.assertEqual(level.suns, 0)
        
        while not level.is_action_legal(cpp_level.WALLNUT, 0, 3):
            level.step()
        self.assertEqual(level.frame, DEFAULT_FPS * 24 + 2)
        level.step(cpp_level.WALLNUT, 0, 3)
        
        while not level.done:
            level.step()
        self.assertTrue(level.lawnmowers[0])
        self.assertTrue(level.win)
        self.assertLessEqual(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED)))   # It should be dead now
        self.assertGreater(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - 2 - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED))) # It should be alive in the previous frame
    
    def test_flagzombie_hp(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(30, 0, "flag"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER, cpp_level.WALLNUT])
        
        ZOMBIE_HP = 181
        ZOMBIE_SPAWN_FRAME = 30 * DEFAULT_FPS
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
    
    def test_newspaperzombie_hp(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(30, 0, "pole"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER, cpp_level.WALLNUT])
        
        ZOMBIE_HP = 331
        ZOMBIE_SPAWN_FRAME = 30 * DEFAULT_FPS
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

    
    def test_football_hp1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(30, 0, "football"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER, cpp_level.WALLNUT])
        
        while not level.is_action_legal(cpp_level.PEASHOOTER, 0, 0):
            level.step()
        level.step(cpp_level.PEASHOOTER, 0, 0)
        self.assertEqual(level.frame, DEFAULT_FPS * 12 + 3)
        self.assertEqual(level.suns, 0)
        
        while not level.is_action_legal(cpp_level.WALLNUT, 0, 5):
            level.step()
        self.assertEqual(level.frame, DEFAULT_FPS * 24 + 2)
        level.step(cpp_level.WALLNUT, 0, 5)
        
        while not level.done:
            level.step()

        self.assertFalse(level.lawnmowers[0])
        self.assertTrue(level.win)
        self.assertEqual(level.frame, DEFAULT_FPS * (30 + 40 + 3 + 25))
    
    def test_football_hp2(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(30, 0, "football"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.PEASHOOTER, cpp_level.WALLNUT])
        
        ZOMBIE_HP = 1581
        ZOMBIE_SPAWN_FRAME = 30 * DEFAULT_FPS
        PLANT_SHOOT_SPEED = round(1.425 * DEFAULT_FPS)
        PLANT_DAMAGE = 20
        
        while not level.is_action_legal(cpp_level.PEASHOOTER, 0, 0):
            level.step()
        level.step(cpp_level.PEASHOOTER, 0, 0)
        self.assertEqual(level.frame, DEFAULT_FPS * 12 + 3)
        self.assertEqual(level.suns, 0)
        
        while not level.is_action_legal(cpp_level.WALLNUT, 0, 5):
            level.step()
        self.assertEqual(level.frame, DEFAULT_FPS * 24 + 2)
        level.step(cpp_level.WALLNUT, 0, 5)
        
        while not level.done:
            level.step()
            if level.is_action_legal(cpp_level.WALLNUT, 0, 3):
                level.step(cpp_level.WALLNUT, 0, 3)
        self.assertTrue(level.lawnmowers[0])
        self.assertTrue(level.win)
        self.assertLessEqual(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED)))   # It should be dead now
        self.assertGreater(ZOMBIE_HP, PLANT_DAMAGE * (1 + ((level.frame - 2 - ZOMBIE_SPAWN_FRAME) // PLANT_SHOOT_SPEED))) # It should be alive in the previous frame


  
class TestPotatoMine(unittest.TestCase):
    # Basic
    def test_potatoemine1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(5, 0, "zombie"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.POTATOMINE])
        
        self.assertTrue(level.is_action_legal(cpp_level.POTATOMINE, 0, 0))
        level.step(cpp_level.POTATOMINE, 0, 0)
        self.assertEqual(level.suns, 25)
        
        while not level.done:
            level.step()

        self.assertTrue(level.lawnmowers[0])
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (5 + 9 * 4.7)))

    # Much HP
    def test_potatomine2(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(5, 0, "football"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.POTATOMINE])
        
        self.assertTrue(level.is_action_legal(cpp_level.POTATOMINE, 0, 0))
        level.step(cpp_level.POTATOMINE, 0, 0)
        self.assertEqual(level.suns, 25)
        
        while not level.done:
            level.step()

        self.assertTrue(level.lawnmowers[0])
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (5 + 9 * 2.5)))
    
    # Don't give it enough time to arm
    def test_potatoemine3(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(5, 3, "football"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.POTATOMINE])
        
        self.assertTrue(level.is_action_legal(cpp_level.POTATOMINE, 3, 0))
        level.step(cpp_level.POTATOMINE, 3, 8)
        self.assertEqual(level.suns, 25)
        
        while not level.done:
            level.step()

        self.assertFalse(level.lawnmowers[3])
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (5 + 3 + 10 * 2.5)))
    
    # Multiple zombies at same tile
    def test_potatoemine4(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(5, 1, "football"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(5, 1, "football"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.POTATOMINE])
        
        self.assertTrue(level.is_action_legal(cpp_level.POTATOMINE, 1, 0))
        level.step(cpp_level.POTATOMINE, 1, 0)
        self.assertEqual(level.suns, 25)
        
        while not level.done:
            level.step()

        self.assertTrue(level.lawnmowers[1])
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (5 + 9 * 2.5)))

    # Multiple zombies at same tile
    def test_potatoemine5(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(5, 1, "football"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(6, 1, "football"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.POTATOMINE])
        
        self.assertTrue(level.is_action_legal(cpp_level.POTATOMINE, 1, 0))
        level.step(cpp_level.POTATOMINE, 1, 0)
        self.assertEqual(level.suns, 25)
        
        while not level.done:
            level.step()

        self.assertFalse(level.lawnmowers[1])
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (6 + 10 * 2.5)))
    
class TestWallnut(unittest.TestCase):
    # Basic
    def test_wallnut1(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(10, 1, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.WALLNUT])
        
        self.assertTrue(level.is_action_legal(cpp_level.WALLNUT, 1, 0))
        level.step(cpp_level.WALLNUT, 1, 0)
        self.assertEqual(level.suns, 0)
        
        while not level.done:
            level.step()

        self.assertFalse(level.lawnmowers[1])
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (10 + 40 + 10 * 4.7)))
    
    # Lots of zombies at once
    def test_wallnut2(self):
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(10, 1, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(10, 1, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(10, 1, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(10, 1, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.WALLNUT])
        
        self.assertTrue(level.is_action_legal(cpp_level.WALLNUT, 1, 0))
        level.step(cpp_level.WALLNUT, 1, 0)
        self.assertEqual(level.suns, 0)
        
        while not level.done:
            level.step()

        self.assertFalse(level.lawnmowers[1])
        self.assertTrue(level.win)
        self.assertEqual(level.frame, int(DEFAULT_FPS * (10 + 10 + 10 * 4.7)))
    
class TestCherryBomb(unittest.TestCase):
    # One zombie
    def test_cherrybomb1(self):
        ZOMBIE_SPAWN_SECOND = 10
        ZOMBIE_SPEED = 4.7
        TIME_TO_EXPLODE = 1.2
        
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND, 1, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.CHERRYBOMB])
        
        level.suns = 1000
        
        # self.assertFalse(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 0))
        while level.frame < int(DEFAULT_FPS * (10 + ZOMBIE_SPEED * 4) + 1):
            level.step()
        
        self.assertTrue(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 5))
        level.step(cpp_level.CHERRYBOMB, 1, 4)
        for i in range(int(DEFAULT_FPS * TIME_TO_EXPLODE)):
            self.assertFalse(level.done, msg=f"Game is over too soon at frame {level.frame}. Iteration {i} out of {int(DEFAULT_FPS * TIME_TO_EXPLODE + 10)}")
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.lawnmowers[1])
        self.assertTrue(level.win)
    
    def test_cherrybomb2(self):
        ZOMBIE_SPAWN_SECOND = 10
        ZOMBIE_SPEED = 4.7
        TIME_TO_EXPLODE = 1.2
        
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND, 1, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.CHERRYBOMB])
        
        level.suns = 1000
        
        # self.assertFalse(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 0))
        while level.frame < int(DEFAULT_FPS * (10 + ZOMBIE_SPEED * 4) + 1):
            level.step()
        
        self.assertTrue(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 5))
        level.step(cpp_level.CHERRYBOMB, 0, 4)
        for i in range(int(DEFAULT_FPS * TIME_TO_EXPLODE)):
            self.assertFalse(level.done, msg=f"Game is over too soon at frame {level.frame}. Iteration {i} out of {int(DEFAULT_FPS * TIME_TO_EXPLODE + 10)}")
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.lawnmowers[1])
        self.assertTrue(level.win)
    
    def test_cherrybomb3(self):
        ZOMBIE_SPAWN_SECOND = 10
        ZOMBIE_SPEED = 4.7
        TIME_TO_EXPLODE = 1.2
        
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND, 1, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.CHERRYBOMB])
        
        level.suns = 1000
        
        # self.assertFalse(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 0))
        while level.frame < int(DEFAULT_FPS * (10 + ZOMBIE_SPEED * 4) + 1):
            level.step()
        
        self.assertTrue(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 5))
        level.step(cpp_level.CHERRYBOMB, 2, 4)
        for i in range(int(DEFAULT_FPS * TIME_TO_EXPLODE)):
            self.assertFalse(level.done, msg=f"Game is over too soon at frame {level.frame}. Iteration {i} out of {int(DEFAULT_FPS * TIME_TO_EXPLODE + 10)}")
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.lawnmowers[1])
        self.assertTrue(level.win)
    
    def test_cherrybomb4(self):
        ZOMBIE_SPAWN_SECOND = 10
        ZOMBIE_SPEED = 4.7
        TIME_TO_EXPLODE = 1.2
        
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND, 1, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.CHERRYBOMB])
        
        level.suns = 1000
        
        # self.assertFalse(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 0))
        while level.frame < int(DEFAULT_FPS * (10 + ZOMBIE_SPEED * 4) + 1):
            level.step()
        
        self.assertTrue(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 5))
        level.step(cpp_level.CHERRYBOMB, 1, 5)
        for i in range(int(DEFAULT_FPS * TIME_TO_EXPLODE)):
            self.assertFalse(level.done, msg=f"Game is over too soon at frame {level.frame}. Iteration {i} out of {int(DEFAULT_FPS * TIME_TO_EXPLODE + 10)}")
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.lawnmowers[1])
        self.assertTrue(level.win)
        
    def test_cherrybomb5(self):
        ZOMBIE_SPAWN_SECOND = 10
        ZOMBIE_SPEED = 4.7
        TIME_TO_EXPLODE = 1.2
        
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND, 1, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.CHERRYBOMB])
        
        level.suns = 1000
        
        # self.assertFalse(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 0))
        while level.frame < int(DEFAULT_FPS * (10 + ZOMBIE_SPEED * 4) + 1):
            level.step()
        
        self.assertTrue(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 5))
        level.step(cpp_level.CHERRYBOMB, 2, 5)
        for i in range(int(DEFAULT_FPS * TIME_TO_EXPLODE)):
            self.assertFalse(level.done, msg=f"Game is over too soon at frame {level.frame}. Iteration {i} out of {int(DEFAULT_FPS * TIME_TO_EXPLODE + 10)}")
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.lawnmowers[1])
        self.assertTrue(level.win)
    
    def test_cherrybomb6(self):
        ZOMBIE_SPAWN_SECOND = 10
        ZOMBIE_SPEED = 4.7
        TIME_TO_EXPLODE = 1.2
        
        # Init level
        level_data = cpp_level.ZombieQueue()
        level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND, 1, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.CHERRYBOMB])
        
        level.suns = 1000
        
        # self.assertFalse(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 0))
        while level.frame < int(DEFAULT_FPS * (10 + ZOMBIE_SPEED * 4) + 1):
            level.step()
        
        self.assertTrue(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 5))
        level.step(cpp_level.CHERRYBOMB, 1, 6)
        for i in range(int(DEFAULT_FPS * TIME_TO_EXPLODE)):
            self.assertFalse(level.done, msg=f"Game is over too soon at frame {level.frame}. Iteration {i} out of {int(DEFAULT_FPS * TIME_TO_EXPLODE + 10)}")
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.lawnmowers[1])

    def test_cherrybomb7(self):
        ZOMBIE_SPAWN_SECOND = 10
        ZOMBIE_SPEED = 4.7
        TIME_TO_EXPLODE = 1.2
        
        # Init level
        level_data = cpp_level.ZombieQueue()
        # level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND - 4, 0, "normal"))
        # level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND - 4, 1, "normal"))
        # level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND - 4, 2, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND, 0, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND, 1, "normal"))
        level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND, 2, "normal"))
        # level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND + 5, 0, "normal"))
        # level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND + 5, 1, "normal"))
        # level_data.push_back(cpp_level.ZombieSpawnTemplate(ZOMBIE_SPAWN_SECOND + 5, 2, "normal"))
        level = cpp_level.Level(5, 10, DEFAULT_FPS, level_data, [cpp_level.CHERRYBOMB])
        
        level.suns = 1000
        
        # self.assertFalse(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 0))
        while level.frame < int(DEFAULT_FPS * (10 + ZOMBIE_SPEED * 4) + 5):
            # expected_tile = 9 - ((level.frame - ZOMBIE_SPAWN_SECOND * DEFAULT_FPS) // int(DEFAULT_FPS * ZOMBIE_SPEED))
            # print(f"[{level.frame}] Expected zombie tile: {expected_tile}")
            level.step()
        
        self.assertTrue(level.is_action_legal(cpp_level.CHERRYBOMB, 1, 5))
        level.step(cpp_level.CHERRYBOMB, 1, 5)
        for i in range(int(DEFAULT_FPS * TIME_TO_EXPLODE)):
            # expected_tile = 9 - ((level.frame - ZOMBIE_SPAWN_SECOND * DEFAULT_FPS) // int(DEFAULT_FPS * ZOMBIE_SPEED))
            # print(f"[{level.frame}] * Expected zombie tile: {expected_tile}")
            self.assertFalse(level.done, msg=f"Game is over too soon at frame {level.frame}. Iteration {i} out of {int(DEFAULT_FPS * TIME_TO_EXPLODE + 10)}")
            level.step()
        
        self.assertTrue(level.done)
        self.assertTrue(level.lawnmowers[1])
        self.assertTrue(level.win)


# TODO
# Chomper
# Jalapeno
# Repeater
# SnowPea
# Squash
# Threepeater

if __name__ == '__main__':
    unittest.main()
