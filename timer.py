import pygame 

class Timer:
	def __init__(self,duration,func = None,activefunc = None):
		self.duration = duration
		self.func = func #will be done after timer is done
		self.activefunc = activefunc #will be done while timer is ticking
		self.start_time = 0
		self.active = False

	def activate(self):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self):
		self.active = False
		self.start_time = 0

	def update(self):
		current_time = pygame.time.get_ticks()
		if self.active and not (self.activefunc is None):			
			self.activefunc()
		if current_time - self.start_time >= self.duration:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()