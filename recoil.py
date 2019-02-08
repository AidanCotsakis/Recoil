import pygame
import os
import math
import numpy
import random
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

os.system('cls')

clock = pygame.time.Clock()

win_w = 1920
win_h = 1080

win = pygame.display.set_mode((win_w, win_h), pygame.FULLSCREEN)

pygame.display.set_caption("Recoil")

MU_01 = pygame.image.load('MU_sndO.png')
MU_02 = pygame.image.load('MU_sndF.png')
MU_selPL = pygame.image.load('MU_PLAY.png')
MU_selSU = pygame.image.load('MU_SOUND.png')
MU_selEX = pygame.image.load('MU_EXIT.png')

_songs = ['music_cake.mp4', 'music_ruby.mp4', 'music_good.mp3', 'music_bubble.mp3', 'music_biscut.mp3']
random.shuffle(_songs)

SONG_END = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(SONG_END)

def play_next_song():
	if sound:
		global _songs
		_songs = _songs[1:] + [_songs[0]] # move current song to the back of the list 
		pygame.mixer.music.load(_songs[0])
		pygame.mixer.music.play()

sound = False

mouseX = 0
mouseY = 0
click = False

while True:
	loop = True
	while loop:
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True

			if event.type == SONG_END:
				play_next_song()

		if sound:
			win.blit(MU_01, (0, 0))

		else:
			win.blit(MU_02, (0, 0))

		mouseX, mouseY = pygame.mouse.get_pos()

		if mouseX > 675 and mouseX < 1245 and mouseY > 300 and mouseY < 413:
			win.blit(MU_selPL, (0, 0))
			if click:
				loop = False

		if mouseX > 675 and mouseX < 1245 and mouseY > 450 and mouseY < 563:
			win.blit(MU_selSU, (0, 0))

			if click:
				if sound == True:
					sound = False
					pygame.mixer.music.stop()
				else:
					sound = True
					play_next_song()

		if mouseX > 675 and mouseX < 1245 and mouseY > 600 and mouseY < 713:
			win.blit(MU_selEX, (0, 0))
			if click:
				pygame.quit()
		click = False

		pygame.display.update()

	rot_sprite = pygame.image.load('AR_01.png')
	BG = pygame.image.load('BG.png')


	class player(object):
		def __init__(self, x, y):
			self.x = x
			self.y = y
			self.w = 75
			self.h = 75
			self.image = pygame.image.load('AR_01.png')
			self.angle = 0
			self.dirX = 0
			self.dirY = 0
			self.diffX = 0
			self.diffY = 0
			self.set_vel = 45
			self.vel = 0
			self.friction = 0
			self.set_friction = 1.5
			self.click = False
			self.bumpX = 1
			self.bumpY = 1
			self.shotdelay = 0
			self.setshotdelay = 10
			self.delX = 0
			self.delY = 0
			self.delXY = 3
			self.lives = 3
			self.kills = 0
			self.power = 0
			self.trishottime = 100

		def move(self):
			if self.click:
				mouseX, mouseY = pygame.mouse.get_pos()
				self.diffX = mouseX - self.x
				self.diffY = mouseY - self.y

				self.dirX = abs(self.diffX) / (abs(self.diffX) + abs(self.diffY))
				self.dirY = abs(self.diffY) / (abs(self.diffX) + abs(self.diffY))

				self.vel = self.set_vel

				if self.delX < 0:
					self.bumpX = 1
				if self.delY < 0:
					self.bumpY = 1

				self.shotdelay = self.setshotdelay

				self.click = False

			if self.vel > 0:
				if self.diffX < 0:
					self.x -= self.vel * self.dirX * -1 * self.bumpX
				else:
					self.x -= self.vel * self.dirX * self.bumpX

				if self.diffY < 0:
					self.y -= self.vel * self.dirY * -1 * self.bumpY
				else:
					self.y -= self.vel * self.dirY * self.bumpY
				
				self.vel -= self.friction

			if self.x - (self.w / 2) < 0 or self.x + (self.w / 2) > win_w and self.delX <= 0:
				self.bumpX *= -1
				self.delX = self.delXY
				self.vel += self.friction * 2

			if self.y - (self.h / 2) < 0 or self.y + (self.h / 2) > win_h and self.delY <= 0:
				self.bumpY *= -1
				self.delY = self.delXY
				self.vel += self.friction * 2

			self.delX -= 1
			self.delY -= 1 

			if self.shotdelay > 0:
				self.shotdelay -= 1


		def draw_self(self):
			self.rot_sprite = pygame.transform.rotate(self.image, self.angle)

			# What!?
			angle = (self.angle + 45)*numpy.pi/180
			trig = max([abs(numpy.sin(angle)), abs(numpy.cos(angle))])
			if self.w != self.h:
				raise Exception()
			win.blit(self.rot_sprite, (self.x - self.w/numpy.sqrt(2)*trig, self.y - self.h/numpy.sqrt(2)*trig))
			# end what

		def get_angle(self):
			mouseX, mouseY = pygame.mouse.get_pos()
			self.angle = math.degrees(math.atan2(self.y-mouseY, self.x-mouseX))+180

			self.angle = 360 - self.angle

	arrow = player(640, 360)


	class projectile(object):
		def __init__(self, x, y, dirX, dirY, diffX, diffY):
			self.x = x
			self.y = y
			self.dirX = dirX
			self.dirY = dirY
			self.diffX = diffX
			self.diffY = diffY
			self.vel = 45
			self.radius = 21

		def move(self):
			if self.diffX < 0:
				self.x -= self.vel * self.dirX * 1
			else:
				self.x -= self.vel * self.dirX * -1

			if self.diffY < 0:
				self.y -= self.vel * self.dirY * 1
			else:
				self.y -= self.vel * self.dirY * -1

		def draw(self, win):
			self.x = math.floor(self.x)
			self.y = math.floor(self.y)
			pygame.draw.circle(win, (255, 255, 255), (self.x,self.y), self.radius)


	class enemy(object):
		def __init__(self, x, y, power, vel, avoidX, avoidY):
			self.x = x
			self.y = y
			self.w = 37
			self.h = 37
			self.power = power
			self.vel = vel
			self.dirX = 0
			self.dirY = 0
			self.diffX = 0
			self.diffY = 0
			self.image = pygame.image.load('EN_01.png')
			self.angle = 0
			self.spin_speed = 1
			self.avoidX = avoidX
			self.avoidY = avoidY
			self.avoidrange = 10
			self.speed = 1

		def move(self):
			mob_col = random.choice(mobs)
			if self.x != mob_col.x and self.y != mob_col.y and self.avoidX != mob_col.avoidX and self.avoidY != mob_col.avoidY and self.x > mob_col.x - mob_col.avoidrange and self.x < mob_col.x + mob_col.avoidrange and self.y > mob_col.y - mob_col.avoidrange and self.y < mob_col.y + mob_col.avoidrange:
				mobs.pop(mobs.index(self))
					
			self.diffX = self.x - arrow.x
			self.diffY = self.y - arrow.y
			
			if (abs(self.diffX) + abs(self.diffY)) != 0:
				self.dirX = abs(self.diffX) / (abs(self.diffX) + abs(self.diffY))
				self.dirY = abs(self.diffY) / (abs(self.diffX) + abs(self.diffY))

			if self.diffX < 0:
				self.x -= self.vel * self.dirX * -1
			else:
				self.x -= self.vel * self.dirX

			if self.diffY < 0:
				self.y -= self.vel * self.dirY * -1
			else:
				self.y -= self.vel * self.dirY

		def draw(self, win):
			self.angle += (self.vel * 2)
			self.rot_sprite = pygame.transform.rotate(self.image, self.angle)

			# What!?
			angle = (self.angle + 45)*numpy.pi/180
			trig = max([abs(numpy.sin(angle)), abs(numpy.cos(angle))])
			if self.w != self.h:
				raise Exception()
			win.blit(self.rot_sprite, (self.x - self.w/numpy.sqrt(2)*trig, self.y - self.h/numpy.sqrt(2)*trig))
			# end what

	font_name = pygame.font.match_font('impact')

	def topleft_text(surf, text, size, x, y, colour):
		font = pygame.font.Font(font_name, size)
		text_surface = font.render(text, True, (colour))
		text_rect = text_surface.get_rect()
		text_rect.topleft = (x, y)
		surf.blit(text_surface, text_rect)

	def topright_text(surf, text, size, x, y, colour):
		font = pygame.font.Font(font_name, size)
		text_surface = font.render(text, True, (colour))
		text_rect = text_surface.get_rect()
		text_rect.topright = (x, y)
		surf.blit(text_surface, text_rect)

	def draw():
		win.blit(BG, (0, 0))

		arrow.draw_self()

		for bullet in bullets:
			bullet.draw(win)

		for mob in mobs:
			mob.draw(win)

		topright_text(win, ("Kills: " + str(arrow.kills)), 60, win_w - 20, 10, (255, 255, 255))
		topleft_text(win, ("Lives: " + str(arrow.lives)), 60, 20, 10, (255, 255, 255))

		if hittime > 0:
			pygame.draw.rect(win, (255, 255, 255), (((win_w * -1) + (hittime * (win_w * 2 / set_hit_time))), (arrow.y - 4), win_w, 9))

		pygame.display.update()


	mobs = []
	bullets = []
	arrowmoved = False
	spawn_mob = 0 
	set_spawn_mob = 210
	mob_count = 0
	hittime = 0
	set_hit_time = 15

	loop = True
	while loop:
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN and arrow.shotdelay <= 0:
				arrow.click = True

				arrow.friction = arrow.set_friction / 2
			
				arrow.move()
				arrowmoved = True

				bullets.append(projectile(arrow.x, arrow.y, arrow.dirX, arrow.dirY, arrow.diffX, arrow.diffY))

				if arrow.power == 1:
					arrow.trishottime = 0

			if event.type == pygame.MOUSEBUTTONUP:
				arrow.friction = arrow.set_friction

			if event.type == SONG_END:
				play_next_song()

		if arrow.power == 1:
			arrow.trishottime += 1

		if arrow.trishottime == 4 or arrow.trishottime == 7:
			bullets.append(projectile(arrow.x, arrow.y, arrow.dirX, arrow.dirY, arrow.diffX, arrow.diffY))

		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			loop = False

		for bullet in bullets:
			if bullet.x > 0 and bullet.x < win_w and bullet.y > 0 and bullet.y < win_h:
				bullet.move()

			else:
				bullets.pop(bullets.index(bullet))

		if arrowmoved == False:
			arrow.move()
		arrowmoved = False

		arrow.get_angle()

		if spawn_mob < 0:
			mobS_side = random.randint(1,4)
			if mobS_side == 1:
				mobS_X = -50
				mobS_Y = random.randint(0, win_h)

			if mobS_side == 2:
				mobS_X = win_w + 50
				mobS_Y = random.randint(0, win_h)

			if mobS_side == 3:
				mobS_X = random.randint(0, win_w)
				mobS_Y = -50

			if mobS_side == 4:
				mobS_X = random.randint(0, win_w)
				mobS_Y = win_h + 50

			mob_count += 1
			mobs.append(enemy(mobS_X, mobS_Y, 0, random.randint(4, (4 + int(mob_count * 0.15))), random.randint(0, win_w), random.randint(0, win_h)))
			if spawn_mob < -2:
				spawn_mob = set_spawn_mob - (mob_count)
		spawn_mob -= 1

		for mob in mobs:
			for bullet in bullets:
				if mob.x > bullet.x - (bullet.radius) and mob.x < bullet.x + (bullet.radius) and mob.y > bullet.y - (bullet.radius) and mob.y < bullet.y + (bullet.radius):
					mobs.pop(mobs.index(mob))
					arrow.kills += 1

			if arrow.x > mob.x - (arrow.w / 2) and arrow.x < mob.x + (arrow.w / 2) and arrow.y > mob.y - (arrow.h / 2) and arrow.y < mob.y + (arrow.h / 2):
				hittime = set_hit_time
				mobs = []
				arrow.lives -= 1

		hittime -= 1

		for mob in mobs:
			mob.move()

		draw()
		if arrow.lives <= 0:
			loop = False

	DIS = pygame.image.load('MU_DES.png')

	def midtop_text(surf, text, size, x, y, colour):
		font = pygame.font.Font(font_name, size)
		text_surface = font.render(text, True, (colour))
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		surf.blit(text_surface, text_rect)

	loop = True
	while loop:
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				loop = False

			if event.type == SONG_END:
				play_next_song()

		win.blit(DIS, (0,0))
		if arrow.kills == 1:
			midtop_text(win, ("You killed " + str(arrow.kills) + " enemy"), 80, win_w / 2, 377, (255, 255, 255))
		else:
			midtop_text(win, ("You killed " + str(arrow.kills) + " enemys"), 80, win_w / 2, 377, (255, 255, 255))

		pygame.display.update()