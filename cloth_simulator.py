import pygame
import sys
import math
import random

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

cols, rows = 30, 20
spacing = 20
gravity_val = 0.5
damping = 0.99
wind_strength = 2

class Point:
    def __init__(self, x, y, pinned=False):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.pinned = pinned

    def update(self, gravity_on):
        if self.pinned:
            return
        vx = (self.x - self.old_x) * damping
        vy = (self.y - self.old_y) * damping
        self.old_x = self.x
        self.old_y = self.y
        self.x += vx
        self.y += vy + (gravity_val if gravity_on else 0)

    def constrain(self):
        self.x = max(0, min(width, self.x))
        self.y = min(height, self.y)

class Constraint:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.length = math.dist((p1.x, p1.y), (p2.x, p2.y))
        self.broken = False

    def solve(self):
        if self.broken:
            return
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        difference = self.length - distance
        percent = difference / distance / 2
        offset_x = dx * percent
        offset_y = dy * percent

        if not self.p1.pinned:
            self.p1.x -= offset_x
            self.p1.y -= offset_y
        if not self.p2.pinned:
            self.p2.x += offset_x
            self.p2.y += offset_y

    def tear_if_stretched(self, max_stretch=40):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        distance = math.hypot(dx, dy)
        if distance > self.length + max_stretch:
            self.broken = True

def create_cloth():
    points = []
    constraints = []
    for y in range(rows):
        row = []
        for x in range(cols):
            p = Point(x * spacing + 100, y * spacing + 50, pinned=(y == 0 and x % 4 == 0))
            row.append(p)
            points.append(p)
            if x > 0:
                constraints.append(Constraint(row[x - 1], row[x]))
            if y > 0:
                constraints.append(Constraint(p, points[(y - 1) * cols + x]))
    return points, constraints

points, constraints = create_cloth()

dragging = None
paused = False
gravity_on = True
wind_on = False

while True:
    screen.fill((30, 30, 30))
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                points, constraints = create_cloth()
            elif event.key == pygame.K_w:
                wind_on = not wind_on
            elif event.key == pygame.K_g:
                gravity_on = not gravity_on
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for p in points:
                    if math.hypot(mx - p.x, my - p.y) < 10:
                        dragging = p
                        break
            elif event.button == 3:
                for p in points:
                    if math.hypot(mx - p.x, my - p.y) < 10:
                        p.pinned = not p.pinned
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

    if dragging:
        dragging.x, dragging.y = mx, my

    if not paused:
        for p in points:
            p.update(gravity_on)
        for _ in range(3):
            for c in constraints:
                if not c.broken:
                    c.solve()
                    c.tear_if_stretched()
        if wind_on:
            for p in points:
                if not p.pinned:
                    p.x += random.uniform(-wind_strength, wind_strength)
                    p.y += random.uniform(-wind_strength, wind_strength)
        for p in points:
            p.constrain()

    for c in constraints:
        if not c.broken:
            pygame.draw.line(screen, (200, 200, 200), (c.p1.x, c.p1.y), (c.p2.x, c.p2.y), 1)

    for p in points:
        color = (255, 50, 50) if p.pinned else (255, 255, 255)
        pygame.draw.circle(screen, color, (int(p.x), int(p.y)), 3)

    pygame.display.flip()
    clock.tick(60)
