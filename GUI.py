# TODO
# + Show circuit
# - Show distribution
# - Allow measurement
# - Use actual circuit elements
# - Edit circuit

from QuantumCircuit import QuantumCircuit
from Executor import Executor

import pygame
from pygame.locals import *
pygame.font.init()

font_height = 72

font  = pygame.font.SysFont('Cascadia Mono Regular', font_height * 4 // 5)
sfont = pygame.font.Font('../Product Sans Regular.ttf', 12)

c = type('c', (), {'__matmul__': (lambda s, x: (*x.to_bytes(3, 'big'),)), '__sub__': (lambda s, x: (x&255,)*3)})()
bg = c-34
fg = c@0xff9088
transparent_fg = (*fg, 48)
green = c@0xa0ffe0

fps = 60

w, h = res = (1280, 720)

def updateStat(msg = None, update = True):
	rect = (0, h-20, w, 21)
	display.fill(c-0, rect)

	tsurf = sfont.render(msg or f'{curr_view_idx}', True, c--1)
	display.blit(tsurf, (5, h-20))

	if update: pygame.display.update(rect)

def resize(size):
	global w, h, res, display
	w, h = res = size
	display = pygame.display.set_mode(res, RESIZABLE)
	updateDisplay()

def updateDisplay():
	display.fill(bg)

	# Left Half - circuit
	surf = render_quantum_circuit(views[curr_view_idx].circuit)
	x, y = ((w//2-surf.get_width())//2, (h-surf.get_height())//2)
	display.blit(surf, (x, y))

	# Right Half - graphs
	graph_size = w//3
	graph = render_graph(views[curr_view_idx].executor.get_statevector(), graph_size)
	x, y = (w//2 + (w//2-graph.get_width())//2, (h-graph.get_height())//2)
	display.blit(graph, (x, y))

	updateStat(update = False)
	pygame.display.flip()

def toggleFullscreen():
	global pres, res, w, h, display
	res, pres =  pres, res
	w, h = res
	if display.get_flags()&FULLSCREEN: resize(res)
	else: display = pygame.display.set_mode(res, FULLSCREEN); updateDisplay()

def render_quantum_circuit(qc):
	lines = str(qc).splitlines()
	sizes = [font.size(line) for line in lines]
	c_w = max(size[0] for size in sizes)
	c_h = sizes[0][1]
	out = pygame.Surface((c_w, c_h*len(lines)), SRCALPHA)

	for i, line in enumerate(lines):
		tsurf = font.render(line, True, fg)
		out.blit(tsurf, (0, i*c_h))

	return out

def render_graph(values, size):
	out = pygame.Surface((size, size + 20), SRCALPHA)
	section_width = size // len(values)
	bar_width = section_width // 2
	qbits = len(values).bit_length() - 1
	for i, value in enumerate(values):
		out.fill(transparent_fg, (
			bar_width // 2 + section_width * i,
			0, bar_width, size))
		out.fill(fg, (
			bar_width // 2 + section_width * i,
			size * (1 - abs(value)), bar_width, size * abs(value)))
		tsurf = sfont.render(f'{i:0{qbits}b}', True, fg)
		offset = (section_width - tsurf.get_width()) // 2
		out.blit(tsurf, (offset + section_width * i, size))
	return out

class CircuitData:
	def __init__(self, circuit):
		self.circuit = circuit
		self.executor = Executor(circuit)
		self.measurements = None
		

pos = [0, 0]
dragging = False

circ1 = QuantumCircuit(2)
# circ1.h(0)
circ1.h(1)
circ1.y(0)

circ2 = QuantumCircuit(2)
circ2.h(0)
circ2.h(1)
circ2.y(0)

curr_view_idx = 0
views = [CircuitData(circ1), CircuitData(circ2)]

resize(res)
pres = pygame.display.list_modes()[0]
clock = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if   event.key == K_ESCAPE: running = False
			elif event.key == K_F11: toggleFullscreen()

		elif event.type == VIDEORESIZE:
			if not display.get_flags()&FULLSCREEN: resize(event.size)
		elif event.type == QUIT: running = False
		elif event.type == MOUSEBUTTONDOWN:
			if event.button in (4, 5):
				delta = event.button*2-9
				curr_view_idx += delta
				curr_view_idx = max(min(curr_view_idx, len(views)-1), 0)
			elif event.button == 1:
				dragging = True
		elif event.type == MOUSEBUTTONUP:
			if event.button == 1:
				dragging = False
		elif event.type == MOUSEMOTION:
			if dragging:
				pos[0] += event.rel[0]
				pos[1] += event.rel[1]

	updateDisplay()
	updateStat()
	clock.tick(fps)