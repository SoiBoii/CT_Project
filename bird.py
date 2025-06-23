import pygame
import random
import numpy as np
from pygame.locals import *

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -5
PIPE_WIDTH = 50
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
FONT = pygame.font.SysFont('Arial', 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)

class Bird:
    def __init__(self, x, y, brain=None):
        self.x = x
        self.y = y
        self.velocity = 0
        self.radius = 15
        self.alive = True
        self.fitness = 0
        self.score = 0
        self.pipes_passed = 0
        
        # Neural network (5 inputs, 8 hidden, 1 output)
        if brain is None:
            self.brain = NeuralNetwork(5, 8, 1)
        else:
            self.brain = brain.copy()
            self.brain.mutate(0.1)
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        if self.y >= SCREEN_HEIGHT - self.radius or self.y <= self.radius:
            self.alive = False
    
    def think(self, pipes):
        if not self.alive:
            return
            
        next_pipe = None
        for pipe in pipes:
            if pipe.x + PIPE_WIDTH > self.x - 20:
                next_pipe = pipe
                break
        
        if next_pipe:
            inputs = np.array([
                self.y / SCREEN_HEIGHT,
                (self.velocity + 10) / 20,
                next_pipe.top_height / SCREEN_HEIGHT,
                (next_pipe.x - self.x) / SCREEN_WIDTH,
                (self.y - (next_pipe.top_height + PIPE_GAP/2)) / SCREEN_HEIGHT
            ])
            
            output = self.brain.predict(inputs)
            
            if output[0] > 0.5:
                self.flap()
    
    def draw(self, screen, show_brain=False):
        if not self.alive:
            return
            
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 1)
        
        eye_x = self.x + 5 if self.velocity > 0 else self.x - 5
        pygame.draw.circle(screen, WHITE, (int(eye_x), int(self.y - 5)), 5)
        pygame.draw.circle(screen, BLACK, (int(eye_x), int(self.y - 5)), 2)
        
        beak_offset = 10 if self.velocity > 0 else -10
        pygame.draw.polygon(screen, (255, 165, 0), [
            (self.x + self.radius, self.y),
            (self.x + self.radius + beak_offset, self.y - 5),
            (self.x + self.radius + beak_offset, self.y + 5)
        ])
        
        if show_brain and self.alive:
            next_pipe = None
            for pipe in game.pipes:
                if pipe.x + PIPE_WIDTH > self.x - 20:
                    next_pipe = pipe
                    break
            
            if next_pipe:
                inputs = np.array([
                    self.y / SCREEN_HEIGHT,
                    (self.velocity + 10) / 20,
                    next_pipe.top_height / SCREEN_HEIGHT,
                    (next_pipe.x - self.x) / SCREEN_WIDTH,
                    (self.y - (next_pipe.top_height + PIPE_GAP/2)) / SCREEN_HEIGHT
                ])
                output = self.brain.predict(inputs)[0]
                
                decision_x = self.x + 30
                pygame.draw.rect(screen, BLACK, (decision_x - 15, self.y - 15, 30, 30), 1)
                if output > 0.5:
                    bar_height = (output - 0.5) * 30
                    pygame.draw.rect(screen, GREEN, (decision_x - 14, self.y + 14 - bar_height, 28, bar_height))

class Pipe:
    def __init__(self, x=None, top_height=None):
        self.x = SCREEN_WIDTH if x is None else x
        if top_height is None:
            self.top_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        else:
            self.top_height = top_height
        self.bottom_height = self.top_height + PIPE_GAP
        self.passed = False
        self.speed = 2
    
    def update(self, speed_factor=1):
        self.x -= self.speed * speed_factor
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 2)
        
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom_height, PIPE_WIDTH, SCREEN_HEIGHT - self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, self.bottom_height, PIPE_WIDTH, SCREEN_HEIGHT - self.bottom_height), 2)
        
        gap_center = self.top_height + PIPE_GAP/2
        pygame.draw.line(screen, YELLOW, (self.x, gap_center), (self.x + PIPE_WIDTH, gap_center), 2)
    
    def collides_with(self, bird):
        if not bird.alive:
            return False
            
        if (bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + PIPE_WIDTH):
            if (bird.y - bird.radius < self.top_height or bird.y + bird.radius > self.bottom_height):
                return True
        return False

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights1 = np.random.randn(input_size, hidden_size) * np.sqrt(2./input_size)
        self.weights2 = np.random.randn(hidden_size, output_size) * np.sqrt(2./hidden_size)
        self.bias1 = np.zeros((1, hidden_size))
        self.bias2 = np.zeros((1, output_size))
    
    def copy(self):
        new_nn = NeuralNetwork(1, 1, 1)
        new_nn.weights1 = self.weights1.copy()
        new_nn.weights2 = self.weights2.copy()
        new_nn.bias1 = self.bias1.copy()
        new_nn.bias2 = self.bias2.copy()
        return new_nn
    
    def predict(self, inputs):
        hidden = np.dot(inputs, self.weights1) + self.bias1
        hidden = np.maximum(0, hidden)
        output = np.dot(hidden, self.weights2) + self.bias2
        output = 1 / (1 + np.exp(-output))
        return output
    
    def mutate(self, rate):
        def mutate_array(arr):
            mask = np.random.random(arr.shape) < rate
            random_values = np.random.randn(*arr.shape) * 0.5
            arr[mask] += random_values[mask]
            arr = np.clip(arr, -5, 5)
            return arr
        
        self.weights1 = mutate_array(self.weights1)
        self.weights2 = mutate_array(self.weights2)
        self.bias1 = mutate_array(self.bias1)
        self.bias2 = mutate_array(self.bias2)

class Game:
    def __init__(self, population_size=50):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird AI - Consistent Obstacles")
        self.clock = pygame.time.Clock()
        self.speed_factor = 1
        self.show_brain = False
        self.population_size = population_size
        self.pipe_sequence = []
        self.reset()
    
    def generate_pipe_sequence(self):
        self.pipe_sequence = []
        x = SCREEN_WIDTH
        for _ in range(50):
            top_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
            self.pipe_sequence.append((x, top_height))
            x += PIPE_FREQUENCY // 2
    
    def reset(self):
        if not self.pipe_sequence:
            self.generate_pipe_sequence()
        
        self.birds = [Bird(100, SCREEN_HEIGHT // 2) for _ in range(self.population_size)]
        self.pipes = []
        self.last_pipe_time = pygame.time.get_ticks()
        self.generation = 1
        self.best_score = 0
        self.best_pipes_passed = 0
        self.running = True
        self.next_pipe_index = 0
        self.add_pipe()
    
    def add_pipe(self):
        if self.next_pipe_index < len(self.pipe_sequence):
            x, top_height = self.pipe_sequence[self.next_pipe_index]
            self.pipes.append(Pipe(x, top_height))
            self.next_pipe_index += 1
            self.last_pipe_time = pygame.time.get_ticks()
    
    def natural_selection(self):
        for bird in self.birds:
            bird.fitness = bird.score + bird.pipes_passed * 500
        
        self.birds.sort(key=lambda x: x.fitness, reverse=True)
        
        top_birds = self.birds[:max(2, len(self.birds)//5)]
        
        new_birds = []
        
        for bird in top_birds[:2]:
            new_bird = Bird(100, SCREEN_HEIGHT // 2, bird.brain)
            new_birds.append(new_bird)
        
        for _ in range(self.population_size - 2):
            candidates = random.sample(top_birds, min(3, len(top_birds)))
            parent = max(candidates, key=lambda x: x.fitness)
            child_brain = parent.brain.copy()
            child_brain.mutate(0.15)
            new_birds.append(Bird(100, SCREEN_HEIGHT // 2, child_brain))
        
        self.birds = new_birds
        self.generation += 1
        self.pipes = []
        self.next_pipe_index = 0
        self.add_pipe()
        
        if self.generation % 20 == 0:
            for bird in self.birds:
                bird.brain.mutate(0.02)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_r:
                    self.generate_pipe_sequence()
                    self.reset()
                elif event.key == K_b:
                    self.show_brain = not self.show_brain
                elif event.key == K_0:
                    self.speed_factor = 10
                elif K_1 <= event.key <= K_9:
                    self.speed_factor = event.key - K_0
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_time > PIPE_FREQUENCY / self.speed_factor:
            self.add_pipe()
        
        for pipe in self.pipes[:]:
            pipe.update(self.speed_factor)
            if pipe.x < -PIPE_WIDTH:
                self.pipes.remove(pipe)
        
        alive_birds = [bird for bird in self.birds if bird.alive]
        
        if not alive_birds:
            self.natural_selection()
            return
        
        for _ in range(min(3, self.speed_factor)):
            for bird in alive_birds[:]:
                if not bird.alive:
                    alive_birds.remove(bird)
                    continue
                
                bird.think(self.pipes)
                bird.update()
                bird.score += 1
                
                for pipe in self.pipes:
                    if pipe.collides_with(bird):
                        bird.alive = False
                
                for pipe in self.pipes:
                    if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                        pipe.passed = True
                        bird.pipes_passed += 1
                        bird.score += 1000
        
        current_max_pipes = max(bird.pipes_passed for bird in self.birds)
        if current_max_pipes > self.best_pipes_passed:
            self.best_pipes_passed = current_max_pipes
        
        current_max_score = max(bird.score for bird in self.birds)
        if current_max_score > self.best_score:
            self.best_score = current_max_score
    
    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # Only draw alive birds
        for bird in self.birds:
            if bird.alive:
                bird.draw(self.screen, self.show_brain)
        
        alive_count = sum(1 for bird in self.birds if bird.alive)
        stats_text = [
            f"Generation: {self.generation}",
            f"Alive: {alive_count}/{len(self.birds)}",
            f"Best Pipes Passed: {self.best_pipes_passed}",
            f"Current Max Pipes: {max(bird.pipes_passed for bird in self.birds) if self.birds else 0}",
            f"Speed: {self.speed_factor}x (1-9,0)",
            f"Show Brain: {'ON' if self.show_brain else 'OFF'} (B)",
            f"Press R to generate new obstacles"
        ]
        
        for i, text in enumerate(stats_text):
            text_surface = FONT.render(text, True, BLACK)
            self.screen.blit(text_surface, (10, 10 + i * 25))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game(population_size=50)
    game.run()