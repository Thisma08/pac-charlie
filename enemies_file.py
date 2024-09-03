import pygame as pg
from pygame.locals import *
from vector import Vector2
from constants_file import *
from characters_file import Character
from modes_file import ModeController
from sprites_file import EnemySprites

class Enemy(Character):
    def __init__(self, inter, player=None, teammate=None):
        Character.__init__(self, inter)
        self.sprites = None
        self.name = ENEMY
        self.points = 200
        self.radius = 12
        self.defaultSpeed = 60
        self.setSpeed(self.defaultSpeed)
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.player = player
        self.mode = ModeController(self)
        self.teammate = teammate
        self.homeInter = inter
        self.freightFlashTime = 0.05
        self.timer = 0

    def update(self, dt):
        self.sprites.update()
        self.timer += dt
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        elif self.mode.current is FREIGHT:
            if self.timer >= self.freightFlashTime:
                self.visible = not self.visible
                self.timer = 0
        Character.update(self, dt)

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.color = BLUE
            self.setSpeed(40)
            self.directionMethod = self.randomDirection

    def normalMode(self):
        if self.name == ENEMY1:
            self.color = RED
            self.visible = True
            self.setSpeed(self.defaultSpeed)
        elif self.name == ENEMY2:
            self.color = PINK
            self.visible = True
            self.setSpeed(self.defaultSpeed)
        elif self.name == ENEMY3:
            self.color = CYAN
            self.visible = True
            self.setSpeed(self.defaultSpeed)
        elif self.name == ENEMY4:
            self.color = ORANGE
            self.visible = True
            self.setSpeed(self.defaultSpeed)
        self.directionMethod = self.goalDirection
        self.homeInter.denyAccess(DOWN, self)

    def spawn(self):
        self.goal = self.spawnInter.pos

    def setSpawnInter(self, inter):
        self.spawnInter = inter

    def startSpawn(self):
        self.mode.setSpawnMode()
        pg.time.wait(1)
        if self.mode.current == SPAWN:
            self.setSpeed(180)
            self.color = WHITE
            self.directionMethod = self.goalDirection
            self.spawn()

    def reset(self):
        Character.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection
        self.setSpeed(self.defaultSpeed)


class Enemy1(Enemy):
    def __init__(self, inter, player=None, teammate=None):
        Enemy.__init__(self, inter, player, teammate)
        self.name = ENEMY1
        self.color = RED
        self.sprites = EnemySprites(self)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.player.pos


class Enemy2(Enemy):
    def __init__(self, inter, player=None, teammate=None):
        Enemy.__init__(self, inter, player, teammate)
        self.name = ENEMY2
        self.color = PINK
        self.sprites = EnemySprites(self)

    def scatter(self):
        self.goal = Vector2(TILE_W*COLS, 0)

    def chase(self):
        self.goal = self.player.pos + self.player.directions[self.player.direction] * TILE_W * 4


class Enemy3(Enemy):
    def __init__(self, inter, player=None, teammate=None):
        Enemy.__init__(self, inter, player, teammate)
        self.name = ENEMY3
        self.color = CYAN
        self.sprites = EnemySprites(self)

    def scatter(self):
        self.goal = Vector2(TILE_W * COLS, TILE_H * ROWS)

    def chase(self):
        self.goal = self.player.pos + self.player.directions[self.player.direction] * TILE_W * 4


class Enemy4(Enemy):
    def __init__(self, inter, player=None, teammate=None):
        Enemy.__init__(self, inter, player, teammate)
        self.name = ENEMY4
        self.color = ORANGE
        self.sprites = EnemySprites(self)

    def scatter(self):
        self.goal = Vector2(0, TILE_H * ROWS)

    def chase(self):
        d = self.player.pos - self.pos
        ds = d.magnitudeSquared()
        if ds <= (TILE_W * 8) ** 2:
            self.scatter()
        else:
            self.goal = self.player.pos + self.player.directions[self.player.direction] * TILE_W * 4


class EnemyGroup(object):
    def __init__(self, inter, player):
        self.enemy1 = Enemy1(inter, player)
        self.enemy2 = Enemy2(inter, player)
        self.enemy3 = Enemy3(inter, player)
        self.enemy4 = Enemy4(inter, player)
        self.enemies = [self.enemy1, self.enemy2, self.enemy3, self.enemy4]

    def __iter__(self):
        return iter(self.enemies)

    def update(self, dt):
        for enemy in self:
            enemy.update(dt)

    def startFreight(self):
        for enemy in self:
            enemy.startFreight()
        self.resetPoints()

    def setSpawnInter(self, inter):
        for enemy in self:
            enemy.setSpawnInter(inter)

    def updatePoints(self):
        for enemy in self:
            enemy.points *= 2

    def resetPoints(self):
        for enemy in self:
            enemy.points = 200

    def reset(self):
        for enemy in self:
            enemy.reset()

    def hide(self):
        for enemy in self:
            enemy.visible = False

    def show(self):
        for enemy in self:
            enemy.visible = True

    def render(self, screen):
        for enemy in self:
            enemy.render(screen)

    def increaseSpeed(self):
        for enemy in self:
            enemy.defaultSpeed += 60
            enemy.setSpeed(enemy.defaultSpeed)

    def resetSpeed(self):
        for enemy in self:
            enemy.defaultSpeed = 60
            enemy.setSpeed(enemy.defaultSpeed)
