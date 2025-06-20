namespace SpriteKind {
    export const static = SpriteKind.create()
}

let statusbar = statusbars.create(20, 4, StatusBarKind.Energy)
statusbar.setFlag(SpriteFlag.Invisible, true)
controller.A.onEvent(ControllerButtonEvent.Pressed, function on_a_pressed() {
    
    music.play(music.createSoundEffect(WaveShape.Triangle, 2274, 2186, 255, 0, 500, SoundExpressionEffect.Warble, InterpolationCurve.Linear), music.PlaybackMode.InBackground)
    laser = sprites.create(img`
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
            `, SpriteKind.Projectile)
    laser.setPosition(plane.x, plane.y)
    laser.vx = 0 - laserSpeed
})
let followSpeed = 20
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_on_overlap(sprite2: Sprite, otherSprite2: Sprite) {
    info.changeLifeBy(-1)
    music.play(music.createSoundEffect(WaveShape.Square, 5000, 0, 255, 0, 500, SoundExpressionEffect.None, InterpolationCurve.Linear), music.PlaybackMode.UntilDone)
    if (info.life() == 0) {
        game.gameOver(false)
    }
    
})
let isTimestopEnabled = false
function spawnSprites() {
    let enemy: Sprite;
    
    randomNum = level * 2 + randint(0, 20)
    for (let index = 0; index < randomNum; index++) {
        enemy = sprites.create(img`
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
                `, SpriteKind.Enemy)
        enemy.setPosition(randint(0, 50), randint(0, 100))
        enemy.follow(plane, followSpeed)
    }
    enemies = randomNum
}

statusbars.onZero(StatusBarKind.Energy, function on_status_zero(status: StatusBarSprite) {
    let isTimestopEnabled = false
    let followSpeed = 20
    for (let enemy of sprites.allOfKind(SpriteKind.Enemy)) {
        enemy.follow(plane, followSpeed)
    }
})
controller.B.onEvent(ControllerButtonEvent.Pressed, function on_event_pressed() {
    
    
    if (isTimestopEnabled) {
        statusbar.attachToSprite(plane)
        statusbar.setFlag(SpriteFlag.Invisible, false)
        followSpeed = 20 / 3
        for (let enemy of sprites.allOfKind(SpriteKind.Enemy)) {
            enemy.follow(plane, followSpeed)
        }
        for (let i = 0; i < 100; i++) {
            statusbar.value -= 1
            pause(100)
        }
    }
    
})
controller.B.onEvent(ControllerButtonEvent.Released, function on_event_released() {
    statusbar.setFlag(SpriteFlag.Invisible, true)
    
    if (isTimestopEnabled) {
        followSpeed = 20
        for (let enemy of sprites.allOfKind(SpriteKind.Enemy)) {
            enemy.follow(plane, followSpeed)
        }
    }
    
})
sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Enemy, function on_on_overlap2(sprite: Sprite, otherSprite: Sprite) {
    let sprite3: Sprite;
    
    sprites.destroy(sprite)
    sprites.destroy(otherSprite)
    enemies += 0 - 1
    music.play(music.createSoundEffect(WaveShape.Noise, 1, 1, 255, 0, 500, SoundExpressionEffect.Vibrato, InterpolationCurve.Curve), music.PlaybackMode.InBackground)
    if (enemies == 0) {
        spawnSprites()
        level += 1
        laserSpeed += 10
        if (level == 2) {
            sprite3 = sprites.create(img`
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
                `, SpriteKind.static)
            sprite3.setPosition(153, 106)
            sprite3.sayText("B")
            sprite3.setScale(0.5, ScaleAnchor.Middle)
            isTimestopEnabled = true
        }
        
        //  sprite3.set_flag(SpriteFlag.INVISIBLE, False)
        //  plane.say_text(isTimestopEnabled)
        if (level >= 2) {
            //  sprite3.set_flag(SpriteFlag.INVISIBLE, True)
            isTimestopEnabled = true
            statusbar.value = 100
        }
        
    }
    
})
let randomNum = 0
let laser : Sprite = null
let enemies = 0
let plane : Sprite = null
let laserSpeed = 0
laserSpeed = 200
plane = sprites.create(img`
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
        `, SpriteKind.Player)
let level = 1
plane.x = 140
enemies = 1
info.setLife(3)
scene.setBackgroundColor(4)
controller.moveSprite(plane, 0, 100)
plane.setStayInScreen(true)
spawnSprites()
game.onUpdate(function on_on_update() {
    info.setScore(level)
})
