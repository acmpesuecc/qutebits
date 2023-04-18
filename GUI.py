# TODO
# + Show circuit
# + Show distribution
# + Allow measurement
# + Use actual circuit elements
# - Edit circuit

from QuantumCircuit import QuantumCircuit, QGate
from Executor import Executor, np

import pygame
from pygame.locals import *
pygame.font.init()

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

gate_size = 80

gate_sprites = {
	QGate.HADAMARD:   pygame.image.load('./sprites/hadamard.png'),
	QGate.PAULI_X:    pygame.image.load('./sprites/x.png'),
	QGate.PAULI_Y:    pygame.image.load('./sprites/y.png'),
	QGate.PAULI_Z:    pygame.image.load('./sprites/z.png'),
	QGate.CNOT_START: pygame.image.load('./sprites/cnot start.png'),
	QGate.CNOT_END:   pygame.image.load('./sprites/cnot end.png'),
	QGate.IDENTITY:   pygame.image.load('./sprites/identity.png'),
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
	updateDisplay()

def updateDisplay():
	display.fill(bg)

	graph_animation = None
	for animation in animations:
		if isinstance(animation, GraphAnimation):
			graph_animation = animation

	# Left Half - circuit
	surf = render_quantum_circuit(curr_view.circuit)
	x, y = ((w//2-surf.get_width())//2, (h-surf.get_height())//2)
	display.blit(surf, (x, y))

	# Right Half - graphs
	graph_size = w//3
	if showing_distribution:
		graph = render_measurement(curr_view.measurements, graph_size)
	else:
		if graph_animation is None:
			display_state = curr_view.executor.get_statevector()
		else:
			display_state = graph_animation.state
		graph = render_graph(display_state, graph_size)
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
	c_w = max(len(line) for line in qc.circ)
	c_h = qc.no_qubits

	out = pygame.Surface((gate_size + c_w*gate_size, c_h*gate_size), SRCALPHA)

	for row, qubit_line in enumerate(qc.circ):
		for col, gate in enumerate(qubit_line):
			out.blit(gate_sprites[gate[0]], (gate_size*(1+col), gate_size*row))

	return out

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

def render_measurement(values: list, size):
	out = pygame.Surface((size, 25 + size + 25), SRCALPHA)
	section_width = size // len(values)
	bar_width = section_width // 2
	qbits = len(values).bit_length() - 1
	shots = sum(values)
	norms = [value / shots for value in values]
	for i, (norm, value) in enumerate(zip(norms, values)):
		out.fill(transparent_fg, (
			bar_width // 2 + section_width * i,
			25, bar_width, size))
		out.fill(fg, (
			bar_width // 2 + section_width * i,
			25 + size * (1 - abs(norm)), bar_width, size * abs(norm)))

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
		self.measurements = None


class Animation:
	def __init__(self, start, target):
		self.state = start
		self.target = target

class GraphAnimation(Animation):
	def tick(self):
		self.state = (5 * self.state + self.target) / 6

	def is_complete(self):
		return np.all(abs(self.state - self.target) < 0.00001)

pos = [0, 0]
dragging = False
showing_distribution = False

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
clock = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if   event.key == K_ESCAPE: running = False
			elif event.key == K_F11: toggleFullscreen()

			elif event.key == K_r:  # reset experiment
				curr_view.measurements = None

			elif event.key == K_d:  # show distribution
				showing_distribution = True
				if curr_view.measurements is None:
					curr_view.measurements = curr_view.executor.measure_all()

		elif event.type == KEYUP:
			if event.key == K_d:
				showing_distribution = False

		elif event.type == VIDEORESIZE:
			if not display.get_flags()&FULLSCREEN: resize(event.size)
		elif event.type == QUIT: running = False
		elif event.type == MOUSEBUTTONDOWN:
			if event.button in (4, 5):
				delta = event.button*2-9
				old_view = curr_view
				curr_view_idx += delta
				curr_view_idx = max(min(curr_view_idx, len(views)-1), 0)
				curr_view = views[curr_view_idx]

				old_state = old_view.executor.get_statevector().copy()
				new_state = curr_view.executor.get_statevector().copy()

				animations.append(GraphAnimation(old_state, new_state))
			elif event.button == 1:
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