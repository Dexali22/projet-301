import pygame

from entity import Entity
from keylistener import KeyListener
from screen import Screen
from switch import Switch


class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__(keylistener, screen, x, y)

        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.change_map: Switch | None = None
        self.can_move = True

    def update(self) -> None:
        self.check_input()
        self.check_move()
        super().update()

    def check_input(self):
        if self.keylistener.key_pressed(pygame.K_a):
            self.switch_run()
        if self.keylistener.key_pressed(pygame.K_e):
            self.check_interaction()

    def check_interaction(self):
        for sprite in self.screen.map.npcs:
            if self.hitbox.colliderect(sprite.hitbox.inflate(10, 10)):
                sprite.talk()

    def check_move(self) -> None:
        if self.animation_walk is False:
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_q):
                temp_hitbox.x -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_left()
                else:
                    self.direction = "left"
            elif self.keylistener.key_pressed(pygame.K_d):
                temp_hitbox.x += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_right()
                else:
                    self.direction = "right"
            elif self.keylistener.key_pressed(pygame.K_z):
                temp_hitbox.y -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_up()
                else:
                    self.direction = "up"
            elif self.keylistener.key_pressed(pygame.K_s):
                temp_hitbox.y += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_down()
                else:
                    self.direction = "down"

    def add_switchs(self, switchs: list[Switch]):
        self.switchs = switchs

    def check_collisions_switchs(self, temp_hitbox):
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch
        return None

    def add_collisions(self, collisions):
        self.collisions = collisions

    def check_collisions(self, temp_hitbox: pygame.Rect):
        for collision in self.collisions:
            if temp_hitbox.colliderect(collision):
                return True
        return False

    def check_input(self):
        if self.keylistener.key_pressed(pygame.K_a):
            self.switch_run()

    def switch_run(self, deactive=False):
        if self.speed == 2 and not deactive:
            self.speed = 3
        else:
            self.speed = 2

