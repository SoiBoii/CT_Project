import pygame
import subprocess
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
WHITE, BLACK, BLUE, GREEN = (255, 255, 255), (0, 0, 0), (70, 130, 180), (50, 205, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Selector")
font = pygame.font.SysFont(None, 48)

def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect)
    txt = font.render(text, True, BLACK)
    screen.blit(txt, txt.get_rect(center=rect.center))

def main():
    running = True
    button1 = pygame.Rect(150, 100, 300, 80)
    button2 = pygame.Rect(150, 220, 300, 80)

    while running:
        screen.fill(WHITE)

        draw_button(button1, "Game of Life", BLUE)
        draw_button(button2, "Cloth Simulator", GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(event.pos):
                    subprocess.run([sys.executable, "game_of_life.py"])
                    pygame.quit()
                elif button2.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run([sys.executable, "cloth_simulator.py"])

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
