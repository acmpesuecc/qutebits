# TODO
# + Show circuit
# + Show distribution
# + Allow measurement
# + Use actual circuit elements
# - Edit circuit

from QuantumCircuit import QuantumCircuit, QGate
from Executor import Executor, np, DEFAULT_SHOTS

import pygame
from pygame.locals import *
pygame.font.init()

from tkinter.filedialog import asksaveasfilename as tksave
from tkinter.filedialog import askopenfilename as tkopen
from tkinter import Tk

root = Tk()
root.withdraw()

font_height = 72

font  = pygame.font.SysFont('Consolas', font_height * 4 // 5)
tfont = pygame.font.SysFont('Helvetica', 24)
sfont = pygame.font.SysFont('', 24)

c = type('c', (), {'__matmul__': (lambda s, x: (*x.to_bytes(3, 'big'),)), '__sub__': (lambda s, x: (x&255,)*3)})()
bg = c-34
fg = c@0xff9088
transparent_fg = (*fg, 48)
green = c@0xa0ffe0

fps = 60

w, h = res = (1280, 720)

gate_size = 256

gate_sprites = {
	QGate.HADAMARD:   pygame.image.load('./sprites/hadamard.png'),
	QGate.PAULI_X:    pygame.image.load('./sprites/x.png'),
	QGate.PAULI_Y:    pygame.image.load('./sprites/y.png'),
	QGate.PAULI_Z:    pygame.image.load('./sprites/z.png'),
	QGate.CNOT_START: pygame.image.load('./sprites/cnot start.png'),
	QGate.CNOT_END:   pygame.image.load('./sprites/cnot end.png'),
	QGate.IDENTITY:   pygame.image.load('./sprites/identity.png'),
	'start':          pygame.image.load('./sprites/start.png')
}

def updateStat(msg = None, update = True):
	rect = (0, h-20, w, 21)
	display.fill(c-0, rect)

	tsurf = sfont.render(msg or
		f'Current view: {curr_view_idx}; '
		f'{len(animations)} animations in progress',
	True, c--1)
	display.blit(tsurf, (5, h-20))

	if update: pygame.display.update(rect)

def resize(size):
	global w, h, res, display
	w, h = res = size
	display = pygame.display.set_mode(res, RESIZABLE)
	update_sizes()
	updateDisplay()

def updateDisplay():
	display.fill(bg)

	graph_animation = None
	dist_animation = None
	for animation in animations:
		if isinstance(animation, GraphAnimation):
			graph_animation = animation
		if isinstance(animation, DistAnimation):
			dist_animation = animation

	# Left Half - circuit
	surf = render_quantum_circuit(curr_view.circuit)
	display.blit(surf, get_qc_display_pos(surf.get_size()))

	# Right Half - graphs
	graph_size = h//3

	if dist_animation is None or curr_view.measurements is None:
		dist_state = curr_view.measurements
	else:
		dist_state = dist_animation.state
	dist = render_measurement(dist_state, graph_size,
		DEFAULT_SHOTS, curr_view.showing_distribution)
	if curr_view.showing_distribution:
		tsurf = font.render('Measurements', True, fg)
	else:
		tsurf = font.render('Probabilities', True, fg)


	if graph_animation is None:
		graph_state = curr_view.executor.get_statevector()
	else:
		graph_state = graph_animation.state
	graph = render_graph(graph_state, graph_size)

	x, y = (w//2 + (w//2-graph_size)//2, (h-2*graph_size)//3)
	display.blit(dist, (x, y))

	x, y = (w//2 + (w//2-graph_size)//2, (2*h-graph_size)//3)
	display.blit(graph, (x, y))

	hover = pygame.mouse.get_pos() in measure_button
	measure_surf = measure_button.render(hover=hover)
	display.blit(measure_surf, measure_button.get_pos())

	hover = pygame.mouse.get_pos() in reset_button
	reset_surf = reset_button.render(hover=hover)
	display.blit(reset_surf, reset_button.get_pos())

	updateStat(update = False)
	pygame.display.flip()

def toggleFullscreen():
	global pres, res, w, h, display
	res, pres =  pres, res
	w, h = res
	if display.get_flags()&FULLSCREEN: resize(res)
	else:
		display = pygame.display.set_mode(res, FULLSCREEN)
		update_sizes()
		updateDisplay()

def update_sizes():
	measure_button.update_pos(((w//2-2*measure_button.rect.w)//3, 6*h//7))
	reset_button.update_pos(((w-reset_button.rect.w)//3, 6*h//7))

def render_quantum_circuit(qc):
	c_w = max(len(line) for line in qc.circ)
	c_h = qc.no_qubits

	out = pygame.Surface((gate_size + c_w*gate_size, c_h*gate_size), SRCALPHA)

	for row, qubit_line in enumerate(qc.circ):
		out.blit(gate_sprites['start'], (0, gate_size*row))
		for col, gate in enumerate(qubit_line):
			out.blit(gate_sprites[gate[0]], (gate_size*(1+col), gate_size*row))

	return out

def get_qc_display_pos(surf_size):
	return ((w//2-surf_size[0])//2, (h-surf_size[1])//2)

def render_graph(values: np.ndarray, size):
	out = pygame.Surface((size, 25 + size + 25), SRCALPHA)
	section_width = size // len(values)
	bar_width = section_width // 2
	qbits = len(values).bit_length() - 1
	for i, value in enumerate(values):
		out.fill(transparent_fg, (
			bar_width // 2 + section_width * i,
			25, bar_width, size))
		out.fill(fg, (
			bar_width // 2 + section_width * i,
			25 + size * (1 - abs(value)), bar_width, size * abs(value)))
		tsurf = tfont.render(f'{i:0{qbits}b}', True, fg)
		offset = (section_width - tsurf.get_width()) // 2
		out.blit(tsurf, (offset + section_width * i, 25 + size))
	return out

def render_measurement(values: list, size, shots, showing_distribution = False):
	out = pygame.Surface((size, 25 + size + 25), SRCALPHA)
	if not values: return out

	section_width = size // len(values)
	bar_width = section_width // 2
	qbits = len(values).bit_length() - 1
	norms = [value / shots for value in values]
	for i, (norm, value) in enumerate(zip(norms, values)):
		out.fill(transparent_fg, (
			bar_width // 2 + section_width * i,
			25, bar_width, size))
		out.fill(fg, (
			bar_width // 2 + section_width * i,
			25 + size * (1 - norm), bar_width, size * norm))

		if showing_distribution:
			tsurf = tfont.render(f'{value}', True, fg)
			offset = (section_width - tsurf.get_width()) // 2
			out.blit(tsurf, (offset + section_width * i, 0))

		tsurf = tfont.render(f'{i:0{qbits}b}', True, fg)
		offset = (section_width - tsurf.get_width()) // 2
		out.blit(tsurf, (offset + section_width * i, 25 + size))
	return out

class CircuitView:
	def __init__(self, circuit):
		self.circuit = circuit
		self.executor = Executor(circuit)
		self.showing_distribution = False
		self.generate_probabilities()

	def generate_probabilities(self, shots=DEFAULT_SHOTS):
		self.measurements = [int(i*shots) for i in self.executor.get_probs()]

# Number of qubits must be constant between views
class Animation:
	def __init__(self, start, target):
		self.state = start
		self.target = target

class GraphAnimation(Animation):
	def tick(self):
		self.state = (5 * self.state + self.target) / 6

	def is_complete(self):
		return np.all(abs(self.state - self.target) < 0.00001)

class DistAnimation(Animation):
	def tick(self):
		self.state = [(5 * state + target) // 6
			for state, target in zip(self.state, self.target)]

	def is_complete(self):
		return all(abs(state - target) <= 6
			for state, target in zip(self.state, self.target))

def update_animations(old_view, new_view, animations):
	old_state = old_view.executor.get_statevector().copy()
	new_state = curr_view.executor.get_statevector().copy()

	animations.append(GraphAnimation(old_state, new_state))

	old_state = old_view.measurements
	new_state = curr_view.measurements
	if new_state is not None and old_state is not None:
		animations.append(DistAnimation(old_state, new_state))

class Button:
	def __init__(self, label, fg, bg, hover_col, *rect_args):
		self.label = label
		self.fg = fg
		self.bg = bg
		self.hover_col = hover_col
		self.rect = pygame.Rect(*rect_args)

	def update_pos(self, pos):
		self.rect.topleft = pos  # rect has getters and setters

	def __call__(self, handler):  # for use as a decorator
		# a side effect is that I can use the
		# decorator syntax to reassign a handler
		self.handler = handler
		return self

	def __contains__(self, pos):
		return pygame.Rect(pos, (0, 0)) in self.rect

	def get_pos(self):
		return self.rect[:2]

	def render(self, hover = False):
		out = pygame.Surface(self.rect.size, SRCALPHA)
		out.fill(self.hover_col if hover else self.bg)

		tsurf = font.render(self.label, True, self.fg)
		x, y = (
			(self.rect.w - tsurf.get_width()) // 2,
			(self.rect.h - tsurf.get_height()) // 2
		)
		out.blit(tsurf, (x, y))

		return out

@Button('Measure', c-0, transparent_fg, fg, (w//4, 6*h//7, w//5, 75))
def measure_button(view):
	old_dist = view.measurements
	view.measurements = view.executor.measure_all()
	view.showing_distribution = True
	animations.append(
		DistAnimation(old_dist, view.measurements)
	)

@Button('Reset', c-0, transparent_fg, fg, (w//4, 6*h//7, w//5, 75))
def reset_button(view):
	print('Reset button is clicked')
	old_dist = view.measurements
	view.generate_probabilities()
	view.showing_distribution = False
	animations.append(
		DistAnimation(old_dist, view.measurements)
	)

@Button('Add View', c-0, transparent_fg, fg, (w//4, 6*h//7, w//5, 75))
def add_column_button(view):
	file = tkopen()
	
	update_animations(view)

@Button('Delete View', c-0, transparent_fg, fg, (w//4, 6*h//7, w//5, 75))
def delete_column_button(curr_view_idx):
	if len(views) <= 1: return
	old_dist = views[curr_view_idx].measurements
	old_graph = views[curr_view_idx].circuit.get_statevector().copy()
	view.generate_probabilities()
	view.showing_distribution = False
	update_animations(view)

'''  I could do this
@measure
def hi:
	print('measure')
'''

pos = [0, 0]
dragging = False

circ1 = QuantumCircuit(2)
circ1.h(1)
circ1.y(0)

circ2 = QuantumCircuit(2)
circ2.h(0)
circ2.h(1)
circ2.y(0)

curr_view_idx = 0
views = [CircuitView(circ1), CircuitView(circ2)]
curr_view = views[curr_view_idx]

animations = []

resize(res)
pres = pygame.display.list_modes()[0]
toggleFullscreen()
clock = pygame.time.Clock()
pygame.key.set_repeat(500, 50)
running = True
while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if   event.key == K_ESCAPE: running = False
			elif event.key == K_F11: toggleFullscreen()

			elif event.key == K_r:  # reset measurement
				reset_button.handler(curr_view)

			elif event.key == K_m:  # perform measurement
				measure_button.handler(curr_view)
				
			elif event.key in (K_UP, K_DOWN):
				if event.key == K_DOWN: curr_view_idx += 1
				elif event.key == K_UP: curr_view_idx -= 1

				old_view = curr_view
				curr_view_idx = max(min(curr_view_idx, len(views)-1), 0)
				curr_view = views[curr_view_idx]
				update_animations(old_view, curr_view, animations)

		elif event.type == VIDEORESIZE:
			if not display.get_flags()&FULLSCREEN: resize(event.size)
		elif event.type == QUIT: running = False
		elif event.type == MOUSEBUTTONDOWN:
			if event.button in (4, 5):
				curr_view_idx += event.button*2-9

				old_view = curr_view
				curr_view_idx = max(min(curr_view_idx, len(views)-1), 0)
				curr_view = views[curr_view_idx]
				update_animations(old_view, curr_view, animations)

			elif event.button == 1:
				if   event.pos in measure_button:
					measure_button.handler(curr_view)
				elif event.pos in reset_button:
					reset_button.handler(curr_view)
				dragging = True
		elif event.type == MOUSEBUTTONUP:
			if event.button == 1:
				dragging = False
		elif event.type == MOUSEMOTION:
			if dragging:
				pos[0] += event.rel[0]
				pos[1] += event.rel[1]

	deletees = []
	for i, animation in enumerate(animations):
		animation.tick()
		if animation.is_complete():
			deletees.append(i)

	for deletee in reversed(deletees):
		animations.pop(deletee)

	updateDisplay()
	updateStat()
	clock.tick(fps)
