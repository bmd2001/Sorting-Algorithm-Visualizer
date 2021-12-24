import pygame
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 840 , 480
FPS = 60

pygame.display.set_caption("Sorting Algorithm Visualizer by Davide Bressani")

class DrawingInfo:

	WHITE = 255, 255, 255
	BLACK = 0, 0, 0
	RED = 255, 0, 0
	BLUE = 0, 0, 255
	BACKGROUND_COLOR = WHITE

	GREYS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	SIDE_PAD = 100
	TOP_PAD = 75

	SMALL_FONT = pygame.font.SysFont('comicsans', 10)
	FONT = pygame.font.SysFont('comicsans', 30)
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Sorting Algorithm Visualizer by Davide Bressani")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.lst_max = max(lst)
		self.lst_min = min(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.lst_max - self.lst_min))
		self.start_x = self.SIDE_PAD//2


def generate_start_lst(n, min_val, max_val):
	lst = random.sample(range(min_val, max_val+1), n)
	return lst
	
def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	sorting = draw_info.LARGE_FONT.render(str(algo_name)+ "-" + f"{'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 5))

	draw_list(draw_info)
	pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg=False):

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(draw_info.lst):

		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.lst_min) * draw_info.block_height
		color = draw_info.GREYS[i % 3]

		if i in color_positions:
			color = color_positions[i]
		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
	
	if clear_bg:
		pygame.display.update()

def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.BLUE, j + 1: draw_info.RED}, True)
				time.sleep(0.05)
				yield True

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.BLUE, i: draw_info.RED}, True)
			time.sleep(0.10)
			yield True

	return lst    

def main():
	
	clock = pygame.time.Clock()

	n, min_val, max_val = 50, 1, 100
	draw_info = DrawingInfo(WIDTH, HEIGHT, generate_start_lst(n, min_val, max_val))

	sorting = False
	ascending = True

	count = 0
	sorting_algos = [bubble_sort, insertion_sort]
	sorting_algo_names = ["Bubble Sort", "Insertion Sort"]
	sorting_algorithm_generator = None

	run = True
	while run:

		clock.tick(FPS)

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_names[count//2], ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN and not sorting:
				count += 1
				count = count % (len(sorting_algos)*2)
				if count % 2 == 0:
					ascending = True
				else:
					ascending = False
			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_start_lst(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			if event.key == pygame.K_SPACE and not sorting:
				sorting = True
				sorting_algorithm_generator = sorting_algos[count//2](draw_info, ascending)

	pygame.quit()        

if __name__ == '__main__':
	main()