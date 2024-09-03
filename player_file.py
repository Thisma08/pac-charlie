import pygame as pg
from pygame.locals import *
from vector import Vector2
from constants_file import *
from characters_file import Character
from sprites_file import CharlieSprites


class Player(Character):
    def __init__(self, inter):
        pg.joystick.init()
        # self.joystick = pg.joystick.Joystick(0)
        Character.__init__(self, inter)
        self.name = PLAYER
        self.directions = {STOP: Vector2(), UP: Vector2(0, -1), DOWN: Vector2(0, 1), LEFT: Vector2(-1, 0),
                           RIGHT: Vector2(1, 0)}
        self.direction = LEFT
        self.speed = 120
        self.radius = 12
        self.color = YELLOW
        self.inter = inter
        self.setPosition()
        self.target = inter
        self.collideRadius = 3
        self.alive = True
        self.sprites = CharlieSprites(self)

    def getValidKey(self):
        key_pressed = pg.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT

        # if self.joystick.get_button(11):
        #     return UP
        # if self.joystick.get_button(12):
        #     return DOWN
        # if self.joystick.get_button(13):
        #     return LEFT
        # if self.joystick.get_button(14):
        #     return RIGHT
        return STOP

    def eatNonosses(self, nonosseList):
        for nonosse in nonosseList:
            if self.collideCheck(nonosse):
                return nonosse
        return None

    def collideEnemy(self, enemy):
        return self.collideCheck(enemy)

    def collideCheck(self, touchedSprite):
        d = self.pos - touchedSprite.pos
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + touchedSprite.collideRadius) ** 2
        if dSquared <= rSquared:
            return True
        return False

    def reset(self):
        Character.reset(self)
        self.direction = LEFT
        self.alive = True

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        self.sprites.update()
        self.pos += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.inter = self.target
            if self.inter.neighbors[PORTAL] is not None:
                self.inter = self.inter.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.inter:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.inter:
                self.direction = STOP
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def render(self, screen):
        ajustement = Vector2(TILE_W, TILE_H) / 2
        p = self.pos - ajustement
        screen.blit(self.image, p.asTuple())
