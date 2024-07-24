# required constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = 32, 32

SIZE_BUTTON = (SCREEN_WIDTH // 4, 75)

enemy_spawn_x = [-125, SCREEN_WIDTH - 70]
enemy_spawn_y = [SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 700]

money = int(open('data/txt_files/saves.txt', 'r', encoding='utf-8').readline().split()[-1])  # no constants

statue_hp = 30

knight_heath = 25
knight_speed = 4
knight_power_jump = 17
knight_attack_power = 5
knight_cooldown_anim = 100
update_first_ability = 3000
update_second_ability = 15000

alexander_heath = 20
alexander_speed = 5
alexander_power_jump = 17
alexander_attack_power = 6
alexander_cooldown_anim = 75
alexander_update_first_ability = 10000
alexander_update_second_ability = 7500

samurai_heath = 15
samurai_speed = 6
samurai_power_jump = 19
samurai_attack_power = 5
samurai_cooldown_anim = 50
samurai_update_first_ability = 1000
samurai_update_second_ability = 7500

goblin_heath = 12.5
goblin_speed = 3
goblin_attack_power = 3
goblin_cooldown_anim = 75
goblin_range_player = 150

skeleton_heath = 17.5
skeleton_speed = 2
skeleton_attack_power = 7
skeleton_cooldown_anim = 100
skeleton_range_player = 200

flying_eye_heath = 12.5
flying_eye_speed = 2
flying_eye_attack_power = 2.5
flying_eye_cooldown_anim = 50
flying_eye_range_player = 0

mushroom_heath = 17.5
mushroom_speed = 4
mushroom_attack_power = 5
mushroom_cooldown_anim = 75
mushroom_range_player = 1000

death_enemy_heath = 75
death_enemy_speed = 3
death_enemy_attack_power = 20
death_enemy_cooldown_anim = 100
death_enemy_range_player = 250

bossSoul_heath = 400
bossSoul_speeds = 3
bossSoul_cooldown_stop_moving = 1500

portal_attack_power = 3

ball_attack_power = 10

fire_anim = 75
quantity_fire = 4
fire_cooldown = 7000

cooldown_enemy_spawn = 3000
cooldown_wave = 4000

character_price = {0: 0,
                   1: 750,
                   2: 2500}

player_sheet_list = {0: [('player_knight/IDLE.png', 3),
                         ('player_knight/WALK.png', 8),
                         ('player_knight/ATTACK.png', 7),
                         ('player_knight/DEATH.png', 10),
                         ('player_knight/HURT.png', 3)],

                     1: [('player_alexander/IDLE.png', 6),
                         ('player_alexander/WALK.png', 8),
                         ('player_alexander/ATTACK.png', 10),
                         ('player_alexander/DEATH.png', 30),
                         ('player_alexander/HURT.png', 5),
                         ('player_alexander/ABILITY.png', 10)],

                     2: [('player_samurai/IDLE.png', 8),
                         ('player_samurai/WALK.png', 8),
                         ('player_samurai/ATTACK.png', 12),
                         ('player_samurai/DEATH.png', 6),
                         ('player_samurai/HURT.png', 4)]
                     }

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
                                           ('Mushroom/Take Hit.png', 4)]},
                        4: {'heath': death_enemy_heath,
                            'speed': death_enemy_speed,
                            'attack': death_enemy_attack_power,
                            'anim': death_enemy_cooldown_anim,
                            'range': death_enemy_range_player,
                            'list_sheet': [('death_enemy/Idle.png', 6),
                                           ('death_enemy/Run.png', 12),
                                           ('death_enemy/Attack.png', 15),
                                           ('death_enemy/Death.png', 22),
                                           ('death_enemy/Take Hit.png', 5)]},
                        }
