@namespace
class SpriteKind:
    static = SpriteKind.create()

# Create the energy status bar and hide it initially
statusbar = statusbars.create(20, 4, StatusBarKind.energy)
statusbar.set_flag(SpriteFlag.INVISIBLE, True)
# just to thing
# Global variables
laserSpeed = 200
followSpeed = 20
level = 1
enemies = 0
isTimestopEnabled = False
isDrainingEnergy = False
laser: Sprite = None

# Create player sprite
plane = sprites.create(img("""
        ..fffffffffffffffffffff.
        ..2bbbbfbbbbbbbbbbbbbff.
        ..2bbbbfbfeeeeeee444bff.
        ..2bbbbfbeeefeeee444ef..
        ..2bbbbfbbbbbbfbb444ef..
        ..ffffffffffffffb454ef..
        .........f..e..fb44fef..
        ..........f.ee.fbf44ef..
        ..........f..eefb444ef..
        ...........f...fb454ef..
        ............ffffb544ef..
        ...............fbf44ef..
        ...............fb44eef..
        ...............fb444ef..
        ...............fb445ef..
        ...............fbbbbbf..
        """), SpriteKind.player)

plane.x = 140
info.set_life(3)
scene.set_background_color(4)
controller.move_sprite(plane, 0, 100)
plane.set_stay_in_screen(True)

# Function to spawn enemies
def spawnSprites():
    global enemies, level
    randomNum = level * 2 + randint(0, 20)
    for _ in range(randomNum):
        enemy = sprites.create(img("""
                . . . . . . . . . . . . . . . .
                . . . . 3 3 3 3 3 3 3 . . . . .
                . . . 3 3 3 3 3 3 3 3 3 . . . .
                . . 3 3 3 3 3 3 3 3 3 3 3 . . .
                . 3 3 3 3 3 3 3 3 3 3 3 3 3 . .
                . 3 3 3 3 3 3 3 3 3 3 3 3 3 . .
                . 3 3 3 3 3 3 3 3 3 3 3 3 3 . .
                . 3 3 3 3 3 3 3 3 3 3 3 3 3 . .
                . 3 3 3 3 3 3 3 3 3 3 3 3 3 . .
                . 3 3 3 3 3 3 3 3 3 3 3 3 3 . .
                . 3 3 3 3 3 3 3 3 3 3 3 3 3 . .
                . . 3 3 3 3 3 3 3 3 3 3 3 . . .
                . . . 3 3 3 3 3 3 3 3 3 . . . .
                . . . . 3 3 3 3 3 3 3 . . . . .
                . . . . . . . . . . . . . . . .
                . . . . . . . . . . . . . . . .
                """), SpriteKind.enemy)
        enemy.set_position(randint(0, 50), randint(0, 100))
        enemy.follow(plane, followSpeed)
    enemies = randomNum

# Initial spawn
spawnSprites()

# Laser firing function on A press
def on_a_pressed():
    global laser
    music.play(music.create_sound_effect(WaveShape.TRIANGLE,
            2274,
            2186,
            255,
            0,
            500,
            SoundExpressionEffect.WARBLE,
            InterpolationCurve.LINEAR),
        music.PlaybackMode.IN_BACKGROUND)  # This is okay here, as it's a short sound
    laser = sprites.create(img("""
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            """),
        SpriteKind.projectile)
    laser.set_position(plane.x, plane.y)
    laser.vx = 0 - laserSpeed

controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

# On overlap between player and enemy, lose life
def on_on_overlap(sprite2, otherSprite2):
    info.change_life_by(-1)
    music.play(music.create_sound_effect(WaveShape.SQUARE,
            5000,
            0,
            255,
            0,
            500,
            SoundExpressionEffect.NONE,
            InterpolationCurve.LINEAR),
        music.PlaybackMode.UNTIL_DONE)
    if info.life() == 0:
        game.game_over(False)

sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)

# On overlap between projectile and enemy: destroy both and handle level progression
def on_on_overlap2(sprite, otherSprite):
    global enemies, level, laserSpeed, isTimestopEnabled
    sprites.destroy(sprite)
    sprites.destroy(otherSprite)
    enemies -= 1
    music.play(music.create_sound_effect(WaveShape.NOISE,
            1,
            1,
            255,
            0,
            500,
            SoundExpressionEffect.VIBRATO,
            InterpolationCurve.CURVE),
        music.PlaybackMode.IN_BACKGROUND)
    if enemies == 0:
        spawnSprites()
        level += 1
        laserSpeed += 10
        # Special event at level 8
        if level == 8:
            sprite3 = sprites.create(img("""
                ...........................cccccccccc..........................
                .........................ccc11111111ccc........................
                ........................cc111111111111cc.......................
                .......................cc11111111111111cc......................
                ......................cc1111111111111111cc.....................
                ......................c111111111111111111c.....................
                .....................cc111111111111111111cc....................
                .....................cc1111111111111111111c....................
                .....................c11111111111111111111c....................
                ....................cc11111111111111111111cc...................
                ....................cc11111111111111111111cc...................
                ....................cc111111111111111111111c...................
                ....................cc111111111111111111111c...................
                ....................cc111111111111111111111c...................
                ....................cc111111111111bcccc1111c...................
                ....................cc11111111111111ccc1111c...................
                .....................c11bcccc1111111cc11111c...................
                .....................cb111ccc1111111111111cc...................
                .....................cb111cc11111111111111cc...................
                .....................cb1111111111111b111ccccc..................
                ....................ccbb111111111111b11cc111cc.................
                ..................ccc11bb11111b1111b111c11111cc................
                ................cccdd111bb11111bbbb111b1111111ccccc............
                ...............cc111d1111bbb11111111bb1111bb111cc1cc...........
                ..............cc1111dd11111bbbbbbbbbbb1111bb111b111cc..........
                ..............c111111d11111111d11111bbb111bb11bb1111cc.........
                .............cc111111d11111111dd1111bb1b111b11b111111c.........
                ............cc111114441111111111ddddb11bbbb111b111111c.........
                ...........cc11111145411111111111111b11111111bb111111cc........
                ..........cc111111145411111111111111bb1111111bb1111111c........
                .........ccdd111111454111111111111111bb1111111bb111111cc.......
                ........cc111d1111145441111111111111111b1111111bb111111c.......
                .......cc11111d111d45541111111111111111bb1111111bb11111c.......
                .......c111111dd1ddd45411111111111111111bb1111111bbddd1cc......
                ......cc1111bbbbbddd454111111111111111111bb11111111bddd1c......
                ......cc11bbb111bbbd4541111111111111111111bb11111111111dcc.....
                ......cc11bb111bbbbc4541111111111111111111dbc11111111111cc.....
                ......cc11b111bb111bc5411111111111111111111dcc11111111111c.....
                bbbbbbcc111111b11111bc4cc111111111111111111ddcc1111111111c.....
                dddddddcc1111b111111bb11ccbbbbbbbb111111111dddcc11111111cc.....
                ddddddddcc111b1111111bb11cdddddddbbbbbbbbbbbbbccc111111cc......
                ddddddddddcccb11111111bbccbbddddddddddddddddddddccc111ccbbbbbbb
                ddddddddddddccc11111111bc111bbbddddddddddddddddddccccccdddddddd
                dddddddddddddccc1111111cc111111bbbddddddddddddddddddddddddddddd
                ddddddddddddbb11cc1111cc111111111bddddddddddddddddddddddddddddd
                ddddddddddbb11111cccccc111111111bdddddddddddddddddddddddddddddd
                ddddddddddb11111111111111111111bddddddddddddddddddddddddddddddd
                ddddddddddbb111111111111111111bdddddddddddddddddddddddddddddddd
                ddddddddddddbb111111111111111bddddddddddddddddddddddddddddddddd
                ddddddddddddddbb111111111111bdddddddddddddddddddddddddddddddddd
                ddddddddddddddddbb111111111bddddddddddddddddddddddddddddddddddd
                ddddddddddddddddddbb111111bdddddddddddddddddddddddddddddddddddd
                ddddddddddddddddddddbb111bddddddddddddddddddddddddddddddddddddd
                ddddddddddddddddddddddbbbdddddddddddddddddddddddddddddddddddddd
                ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
                """), SpriteKind.static)
            sprite3.set_position(153, 106)
            sprite3.say_text("B")
            sprite3.set_scale(0.5, ScaleAnchor.MIDDLE)
            isTimestopEnabled = True
            sprite3.set_flag(SpriteFlag.INVISIBLE, False)
        if level > 8:
            sprite3.set_flag(SpriteFlag.INVISIBLE, True)
            isTimestopEnabled = True
            statusbar.value = 100

sprites.on_overlap(SpriteKind.projectile, SpriteKind.enemy, on_on_overlap2)

# On overlap energy zero, reset states
def on_status_zero(status):
    global isTimestopEnabled, followSpeed
    isTimestopEnabled = False
    followSpeed = 20
    for enemy in sprites.all_of_kind(SpriteKind.enemy):
        enemy.follow(plane, followSpeed)

statusbars.on_zero(StatusBarKind.energy, on_status_zero)

# Handling B button press: enable timestop and start energy drain
def on_event_pressed():
    global isTimestopEnabled, followSpeed, isDrainingEnergy
    if isTimestopEnabled:
        statusbar.attach_to_sprite(plane)
        statusbar.set_flag(SpriteFlag.INVISIBLE, False)
        followSpeed = 20 // 3
        for enemy in sprites.all_of_kind(SpriteKind.enemy):
            enemy.follow(plane, followSpeed)
        isDrainingEnergy = True  # Start draining energy

# Handling B button release: stop timestop and energy drain
def on_event_released():
    global followSpeed, isDrainingEnergy
    isDrainingEnergy = False  # Stop draining energy
    statusbar.set_flag(SpriteFlag.INVISIBLE, True)
    if isTimestopEnabled:
        followSpeed = 20
        for enemy in sprites.all_of_kind(SpriteKind.enemy):
            enemy.follow(plane, followSpeed)

controller.B.on_event(ControllerButtonEvent.PRESSED, on_event_pressed)
controller.B.on_event(ControllerButtonEvent.RELEASED, on_event_released)

# Energy draining logic in the update loop
def drain_energy_update():
    global isDrainingEnergy
    if isDrainingEnergy:
        if statusbar.value > 0:
            statusbar.value -= 1
        else:
            # Energy depleted, stop timestop effects
            isDrainingEnergy = False
            statusbar.set_flag(SpriteFlag.INVISIBLE, True)
            on_event_released()

game.on_update(drain_energy_update)

# Update score to reflect current level
def on_on_update():
    info.set_score(level)

game.on_update(on_on_update)
