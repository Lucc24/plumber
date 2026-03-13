import random
import pygame
import sys
import math

pygame.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


floor = pygame.Rect(0, 560, 800, 40)


coin = pygame.Rect(700, 450, 30, 30)
healthbar = pygame.Rect(120, 10, 200, 20)

health = 100
coins = 0
attack_positions = [450, 320, 190]



pos1 = random.choice(attack_positions)
pos2 = random.choice(attack_positions)
pos3 = random.choice(attack_positions)
pos4 = random.choice(attack_positions)
attacks = [
	pygame.Rect(-3000, pos1, 3000, 110),
	pygame.Rect(-3000, pos2, 3000, 110),
	pygame.Rect(-3000, pos3, 3000, 110),
	pygame.Rect(-3000, pos4, 3000, 110),
]
telegraphs = [
	pygame.Rect(-800, pos1, 800, 110),
	pygame.Rect(-800, pos2, 800, 110),
	pygame.Rect(-800, pos3, 800, 110),
	pygame.Rect(-800, pos4, 800, 110),
]


telegraph_surface = pygame.Surface((800, 110), pygame.SRCALPHA) #thanks to stackoverflow for this line

start_time = pygame.time.get_ticks()
attack_speed = 67
attack_started = [False, False, False, False]
attack_done = [False, False, False, False]
telegraph_started = [False, False, False, False]
telegraph_done = [False, False, False, False]
telegraph_show_times = [0, 0, 0, 0]
attack_timings = [2000, 5000, 8000, 11000]
telegraph_timings = [0, 3000, 6000, 9000]

player_rect = pygame.Rect(400, 300, 50, 50)
player_speed = 5

platform_rects = [
    pygame.Rect(150, 430, 120, 20),
    pygame.Rect(150, 300, 120, 20),
    pygame.Rect(150, 170, 120, 20),
    pygame.Rect(530, 430, 120, 20),
    pygame.Rect(530, 300, 120, 20),
    pygame.Rect(530, 170, 120, 20),
]

gravity = 0.5
velocity_y = 0
on_ground = False

title_font = pygame.font.SysFont('Comic Sans MS', 50)
small_font = pygame.font.SysFont('Comic Sans MS', 20)


on_start_screen = True

while on_start_screen:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			on_start_screen = False
	screen.fill((255, 255, 255))
	title_text = title_font.render("Instructions", False, (0, 0, 0))
	line1 = small_font.render("Goal: Collect 20 coins to win before the timer runs out", False, (100, 100, 100))
	line2 = small_font.render("Attacks: The flashing warnings mean an attack is coming", False, (100, 100, 100))
	line3 = small_font.render("Controls: You can jump one time in midair when falling off platforms", False, (100, 100, 100))
	start_text = my_font.render("Press ENTER to start", False, (0, 0, 0))
	screen.blit(title_text, (250, 150))
	screen.blit(line1, (170, 280))
	screen.blit(line2, (170, 320))
	screen.blit(line3, (170, 360))
	screen.blit(start_text, (250, 420))
	pygame.display.flip()
	clock.tick(60)

start_time = pygame.time.get_ticks()
timer_start = pygame.time.get_ticks()

on_death_screen = False

def on_death():

	while on_death_screen:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		screen.fill((255, 255, 255))
		title_text = title_font.render("You died :(", False, (0, 0, 0))
		screen.blit(title_text, (250, 150))
		pygame.display.flip()
on_win_screen = False
def on_win():
	while on_win_screen:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		screen.fill((255, 255, 255))
		title_text = title_font.render("You win :)", False, (0, 0, 0))
		screen.blit(title_text, (250, 150))
		pygame.display.flip()

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		player_rect.x -= player_speed
	if keys[pygame.K_RIGHT]:
		player_rect.x += player_speed
	if keys[pygame.K_UP] and on_ground:
		velocity_y = -12
		on_ground = False
	if keys[pygame.K_DOWN]:
		player_rect.y += player_speed
	for i in range(4):
		if not attack_started[i] and not attack_done[i] and pygame.time.get_ticks() - start_time >= attack_timings[i]:
			attack_started[i] = True
		if not telegraph_started[i] and not telegraph_done[i] and pygame.time.get_ticks() - start_time >= telegraph_timings[i]:
			telegraph_started[i] = True
			telegraphs[i].x = 0
			telegraph_show_times[i] = pygame.time.get_ticks()
	clock.tick(60)

	for i in range(4):
		if attack_started[i] and not telegraph_done[i]:
			telegraph_done[i] = True
			telegraphs[i].x = -800
		if attack_started[i] and not attack_done[i]:
			attacks[i].x += attack_speed
		if attacks[i].x > 800:
			attack_started[i] = False
			attack_done[i] = True
			attacks[i].x = -3000

	if attack_done[0] and attack_done[1] and attack_done[2] and attack_done[3]:
		pos1 = random.choice(attack_positions)
		pos2 = random.choice(attack_positions)
		pos3 = random.choice(attack_positions)
		pos4 = random.choice(attack_positions)
		attacks[0].y = pos1
		attacks[1].y = pos2
		attacks[2].y = pos3
		attacks[3].y = pos4
		telegraphs[0].y = pos1
		telegraphs[1].y = pos2
		telegraphs[2].y = pos3
		telegraphs[3].y = pos4
		for i in range(4):
			attack_done[i] = False
			attacks[i].x = -3000
			telegraph_started[i] = False
			telegraph_done[i] = False
			telegraphs[i].x = -800
			telegraph_show_times[i] = 0
		start_time = pygame.time.get_ticks()

	if coins >= 10:
		telegraph_timings = [0, 2000, 4000, 6000]
		attack_timings = [1000, 3000, 5000, 7000]


	prev_bottom = player_rect.bottom
	velocity_y += gravity
	player_rect.y += velocity_y
	if player_rect.colliderect(floor):
		player_rect.y = floor.y - player_rect.height
		velocity_y = 0
		on_ground = True
	if player_rect.x < 0:
		player_rect.x = 0
	if player_rect.right > 800:
		player_rect.right = 800
	if player_rect.y < 0:
		player_rect.y = 0
	if player_rect.colliderect(coin):
		coins += 1
		coin.x = random.randint(50, 750)
		coin.y = random.randint(50, 500)
	if coin.colliderect(platform_rects[0]) or coin.colliderect(platform_rects[1]) or coin.colliderect(platform_rects[2]) or coin.colliderect(platform_rects[3]) or coin.colliderect(platform_rects[4]) or coin.colliderect(platform_rects[5]):
			coin.x = random.randint(50, 750)
			coin.y = random.randint(50, 500)
	healthbar.width = health * 2
	remaining = 45 - (pygame.time.get_ticks() - timer_start) / 1000.0
	if coins >= 20:
		on_win_screen = True
		on_win()
	if health <= 0 or remaining <= 0:
		on_death_screen = True
		on_death()
	screen.fill((255, 255, 255))
	pygame.draw.rect(screen, (255, 0, 0), player_rect)
	pygame.draw.rect(screen, (0, 0, 0), floor)
	pygame.draw.rect(screen, (255, 205, 0), coin)
	pygame.draw.rect(screen, (0, 255, 0), healthbar)
	for i in range(4):
		telegraph = telegraphs[i]
		if telegraph.x >= 0:
			time_passed = (pygame.time.get_ticks() - telegraph_show_times[i]) / 1000.0 
			alpha = int(64 + 64 * math.sin(time_passed * 12)) #yet again stackoverflow is the goat
			alpha = max(0, min(128, alpha))
			telegraph_surface.fill((255, 0, 255, alpha))
			screen.blit(telegraph_surface, (telegraph.x, telegraph.y))
	for attack in attacks:
		pygame.draw.rect(screen, (255, 0, 255), attack)
		if player_rect.colliderect(attack):
			health -= 1
	for platform in platform_rects:
		pygame.draw.rect(screen, (0, 0, 0), platform)
		if player_rect.colliderect(platform) and velocity_y > 0 and prev_bottom <= platform.top + 10:
			player_rect.y = platform.y - player_rect.height
			velocity_y = 0
			on_ground = True

	text_surface = my_font.render( 'Health:' + str(health), False, (0, 0, 0))
	timer_text = my_font.render('Timer: '+ str(int(remaining)), False, (0, 0, 0))
	coins_text = my_font.render('Coins: ' + str(coins) + "/20", False, (0, 0, 0))
	screen.blit(text_surface, (10, 10))
	screen.blit(timer_text, (400, 10))
	screen.blit(coins_text, (620, 10))

	pygame.display.flip()

