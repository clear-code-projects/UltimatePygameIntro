import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0

		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		self.crouch = pygame.image.load('graphics/player/crouch_0.png').convert_alpha()
		crouch_1 = pygame.image.load('graphics/player/crouch_1.png').convert_alpha()
		crouch_2 = pygame.image.load('graphics/player/crouch_2.png').convert_alpha()
		crouch_3 = pygame.image.load('graphics/player/crouch_3.png').convert_alpha()
		self.player_crouch = [self.crouch,crouch_1,crouch_2,crouch_3]
		self.crouch_index = 0

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.05)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		keys = pygame.key.get_pressed()

		if self.rect.bottom < 300: 
			self.image = self.player_jump
			
		#TODO Optimization
		elif keys[pygame.K_DOWN] and self.rect.bottom == 300:
			self.crouch_index += 0.25
			if self.crouch_index >= len(self.player_crouch):
				self.crouch_index = 0
			self.image = self.player_crouch[int(self.crouch_index)]
			self.rect = self.image.get_rect(midbottom = (80,300))
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):
				self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]
			self.rect = self.image.get_rect(midbottom = (80,300))

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
			
		elif type == 'bee':
			bee_1 = pygame.image.load('graphics/bee/bee1.png').convert_alpha()
			bee_2 = pygame.image.load('graphics/bee/bee2.png').convert_alpha()
			self.frames = [bee_1,bee_2]
			y_pos = 240

		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# MUSIC
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.05)
bg_music.play(loops = -1)

# GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# BACKGROUND
### GROUND
# ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_surface_1 = pygame.image.load('graphics/infiniteSnowGround.png').convert()
ground_surface_2 = pygame.image.load('graphics/infiniteSnowGround.png').convert()
ground_surf_rect_1 = ground_surface_1.get_rect(topleft = (0,300))
ground_surf_rect_2 = ground_surface_2.get_rect(topleft = (786,300))
### SKY
# sky_surface = pygame.image.load('graphics/Sky.png').convert()
sky_surface_1 = pygame.image.load('graphics/infiniteNightSky.png').convert()
sky_surface_2 = pygame.image.load('graphics/infiniteNightSky.png').convert()
sky_surf_rect_1 = sky_surface_1.get_rect(left = 0)
sky_surf_rect_2 = sky_surface_2.get_rect(left = 800)
### SNOW (Optional)
snow_surface_1 = pygame.image.load('graphics/snow.png').convert_alpha()
snow_surface_2 = pygame.image.load('graphics/snow.png').convert_alpha()
snow_rect_1 = snow_surface_1.get_rect(top = 0)
snow_rect_2 = snow_surface_2.get_rect(top = -300)

# INTRO SCREEN
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# TIMER 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','bee','snail','snail'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		# SKY
		sky_surf_rect_1.left -= 1
		sky_surf_rect_2.left -= 1
		if sky_surf_rect_1.right == 0:
			sky_surf_rect_1.left = 800
		elif sky_surf_rect_2.right == 0:
			sky_surf_rect_2.left = 800
		screen.blit(sky_surface_1,sky_surf_rect_1)
		screen.blit(sky_surface_2,sky_surf_rect_2)
		# screen.blit(sky_surface,(0,0))

		# SNOW
		snow_rect_1.top += 1
		snow_rect_2.top += 1
		if snow_rect_1.top >= 300:
			snow_rect_1.bottom = 0
		if snow_rect_2.top >= 300:
			snow_rect_2.bottom = 0
		screen.blit(snow_surface_1,snow_rect_1)
		screen.blit(snow_surface_2,snow_rect_2)

		# GROUND
		ground_surf_rect_1.left -= 2
		ground_surf_rect_2.left -= 2
		if ground_surf_rect_1.right <= 0:
			ground_surf_rect_1.left = 786
		elif ground_surf_rect_2.right <= 0:
			ground_surf_rect_2.left = 786
		screen.blit(ground_surface_1,ground_surf_rect_1)
		screen.blit(ground_surface_2,ground_surf_rect_2)
		# screen.blit(ground_surface,(0,300))

		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)