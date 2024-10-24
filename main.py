import pygame
import time

from particles import *

from enemies import *
from player import Player

from settings import *
from ui import *

pygame.init()
clock = pygame.time.Clock()
fps = 60
screen, size, screen_rect = set_screen((SW, SH))

last_time = time.time()

running = True

particles_g = pygame.sprite.Group()
bullets_g = pygame.sprite.Group()
enemies_g = pygame.sprite.Group()
items_g = pygame.sprite.Group()
enemy_bullet_g = pygame.sprite.Group()

player_g = pygame.sprite.Group()
player = Player(bullets_g, particles_g, enemy_bullet_g, player_g)

enemy_spawn = EnemySpawn(enemies_g, particles_g, bullets_g, items_g,
                         enemy_bullet_g, player)

score_label = Text(screen, size, 40, pos=(SW // 2, 25))
health = ValueBar(screen, size, player.max_health, 'heart', (10, 10))
fps_label = Text(screen, size, 10, pos=(40, SH - 15))

hint_label = Text(screen, size, 12, pos=(SW // 2, SH - 15))

pause_label = Text(screen, size, 60, pos=(SW // 2, SH // 2))
dead_label = Text(screen, size, 60, pos=(SW // 2, SH // 2))

play_music(SONGS[1], 0.3)

show_hint = True
show_hitbox = False
show_rect = False

playing = True

while running:

    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_r:
                if player.health <= 0:
                    playing = True

                    particles_g = pygame.sprite.Group()
                    bullets_g = pygame.sprite.Group()
                    enemies_g = pygame.sprite.Group()
                    items_g = pygame.sprite.Group()
                    enemy_bullet_g = pygame.sprite.Group()

                    player_g = pygame.sprite.Group()
                    player = Player(bullets_g, particles_g, enemy_bullet_g,
                                    player_g)

                    enemy_spawn = EnemySpawn(enemies_g, particles_g, bullets_g,
                                             items_g, enemy_bullet_g, player)

            if event.key == pygame.K_ESCAPE:
                if player.health:
                    playing = not playing

            if event.key == pygame.K_F1:
                if fps == 120:
                    fps = 60
                elif fps == 60:
                    fps = 10
                elif fps == 10:
                    fps = 120

            if event.key == pygame.K_F2:
                show_hint = not show_hint

            if event.key == pygame.K_F3:
                show_hitbox = not show_hitbox

            if event.key == pygame.K_F4:
                show_rect = not show_rect

            if event.key == pygame.K_LSHIFT:
                player.sprint = True

            if event.key == pygame.K_w:
                player.dy = -1
            if event.key == pygame.K_s:
                player.dy = 1
            if event.key == pygame.K_a:
                player.dx = -1
            if event.key == pygame.K_d:
                player.dx = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.dy = 0
            if event.key == pygame.K_s:
                player.dy = 0
            if event.key == pygame.K_a:
                player.dx = 0
            if event.key == pygame.K_d:
                player.dx = 0

            if event.key == pygame.K_LSHIFT:
                player.sprint = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                player.hold = True

            elif event.button == 1:
                player.shoot(mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                player.hold = False

    if player.hold:
        player.shoot(mouse_pos)

    if player.health <= 0:
        playing = False

    screen.fill(pygame.Color('#0f380f'))

    if playing:
        particles_g.update(screen_rect, dt, fps)
        bullets_g.update(screen_rect, dt)
        enemies_g.update(screen, screen_rect, (player.rect.x, player.rect.y),
                         dt)
        enemy_spawn.update(dt)
        items_g.update(dt)
        enemy_bullet_g.update(screen_rect, dt)
        player_g.update(screen_rect, dt)

    bullets_g.draw(screen)
    enemy_bullet_g.draw(screen)
    particles_g.draw(screen)
    enemies_g.draw(screen)
    items_g.draw(screen)
    player_g.draw(screen)

    render_hitbox(screen, player, enemies_g,
                  bullets_g, enemy_bullet_g, items_g,
                  show_rect, show_hitbox)

    score_label.update(player.score)

    if player.health > 0:
        health_msg = player.health
    else:
        health_msg = 0
    health.update(health_msg)

    fps_label.update(f'FPS: {round(clock.get_fps())}')
    if show_hint:
        hint_label.update('[Q] - quit. [R] - restart (upon death). '
                          '[Esc] - pause/unpause. [F2] - toggle hint.')

    if not playing:
        if player.health > 0:
            pause_label.update('Paused')
        else:
            dead_label.update('Defeated')

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
