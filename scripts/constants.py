# required constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = 32, 32


knight_heath = 20
knight_speed = 5
knight_power_jump = 15
knight_attack_power = 5
knight_cooldown_anim = 100

goblin_heath = 10
goblin_speed = 3
goblin_attack_power = 3
goblin_cooldown_anim = 75
goblin_range_player = 150

skeleton_heath = 15
skeleton_speed = 2
skeleton_attack_power = 7
skeleton_cooldown_anim = 100
skeleton_range_player = 200

flying_eye_heath = 10
flying_eye_speed = 2
flying_eye_attack_power = 2.5
flying_eye_cooldown_anim = 50
flying_eye_range_player = 0

mushroom_heath = 15
mushroom_speed = 4
mushroom_attack_power = 5
mushroom_cooldown_anim = 75
mushroom_range_player = 1000

fire_anim = 75
quantity_fire = 3

enemy_specifications = {0: {'heath': goblin_heath,
                            'speed': goblin_speed,
                            'attack': goblin_attack_power,
                            'anim': goblin_cooldown_anim,
                            'range': goblin_range_player,
                            'list_sheet': [('Goblin/Idle.png', 4),
                                           ('Goblin/Run.png', 8),
                                           ('Goblin/Attack.png', 8),
                                           ('Goblin/Death.png', 4),
                                           ('Goblin/Take Hit.png', 4)]},
                        1: {'heath': skeleton_heath,
                            'speed': skeleton_speed,
                            'attack': skeleton_attack_power,
                            'anim': skeleton_cooldown_anim,
                            'range': skeleton_range_player,
                            'list_sheet': [('Skeleton/Idle.png', 4),
                                           ('Skeleton/Walk.png', 4),
                                           ('Skeleton/Attack.png', 8),
                                           ('Skeleton/Death.png', 4),
                                           ('Skeleton/Take Hit.png', 4)]},
                        2: {'heath': flying_eye_heath,
                            'speed': flying_eye_speed,
                            'attack': flying_eye_attack_power,
                            'anim': flying_eye_cooldown_anim,
                            'range': flying_eye_range_player,
                            'list_sheet': [('FlyingEye/Flight.png', 8),
                                           ('FlyingEye/Flight.png', 8),
                                           ('FlyingEye/Attack.png', 8),
                                           ('FlyingEye/Death.png', 4),
                                           ('FlyingEye/Take Hit.png', 4)]},
                        3: {'heath': mushroom_heath,
                            'speed': mushroom_speed,
                            'attack': mushroom_attack_power,
                            'anim': mushroom_cooldown_anim,
                            'range': mushroom_range_player,
                            'list_sheet': [('Mushroom/Idle.png', 4),
                                           ('Mushroom/Run.png', 8),
                                           ('Mushroom/Attack.png', 8),
                                           ('Mushroom/Death.png', 4),
                                           ('Mushroom/Take Hit.png', 4)]}}
