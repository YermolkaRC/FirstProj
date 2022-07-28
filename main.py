import pygame
from sprites import *
from config import *
from player import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('arial.ttf', 32)
        self.running = True

        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.go_background = pygame.image.load('img/gameover.png')

    def createTilemap(self):
        for row, i in enumerate(tilemap):
            for column, j in enumerate(i):
                Ground(self, column, row)
                if j == 'B':
                    Block(self, column, row)
                if j == 'P':
                    self.player = Player(self, column, row)
                if j == 'E':
                    Enemy(self,column, row)
        InventoryItem(self, 50, 50)
                

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.inventory_toggle = False
        self.inventory = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)


    def update(self):
        self.all_sprites.update()
        self.inventory.update()
        #print(self.clock.get_fps())
        #print(self.inventory_toggle)
        if self.player.rect.right > self.screen.get_width():
            for sprite in self.all_sprites:
                sprite.rect.x -= self.screen.get_width()
        if self.player.rect.right < 0:
            for sprite in self.all_sprites:
                sprite.rect.x += self.screen.get_width()
        if self.player.rect.bottom > self.screen.get_height():
            for sprite in self.all_sprites:
                sprite.rect.y -= self.screen.get_height()
        if self.player.rect.bottom < 0:
            for sprite in self.all_sprites:
                sprite.rect.y += self.screen.get_height()


    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        if self.inventory_toggle:
            self.inventory.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


    def intro_screen(self):
        intro = True

        title = self.font.render('RPG Epic Game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()