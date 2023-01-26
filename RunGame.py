import pygame
import TraceGame
import MemoryGame

def main_menu():
    # Set the size of the window
    width = 500
    height = 560
    size = (width, height)
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode(size)

    # Set the title of the window
    pygame.display.set_caption("Game Menu")

    # Create the font
    font = pygame.font.Font(None, 30)

    # Create the run_trace button
    run_trace_button = pygame.Rect(width//2 - 100, height//2 - 75, 200, 50)
    run_trace_text = font.render("Trace", True, (255, 255, 255))

    # Create the memory button
    memory_button = pygame.Rect(width//2 - 100, height//2, 200, 50)
    memory_text = font.render("Memory", True, (255, 255, 255))

    # Create a loop to run the menu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if run_trace_button.collidepoint(pos):
                    # Start the run_trace game
                    TraceGame.TraceGame()
                elif memory_button.collidepoint(pos):
                    # Start the memory game
                    MemoryGame.MemoryGame()

            screen = pygame.display.set_mode(size)


        # Draw the buttons on the screen
        screen.fill((0, 0, 0))
        screen.blit(run_trace_text, (width//2 - run_trace_text.get_width()//2, height//2 - 60))
        pygame.draw.rect(screen, (255, 255, 255), run_trace_button, 2)
        screen.blit(memory_text, (width//2 - memory_text.get_width()//2, height//2 + 15))
        pygame.draw.rect(screen, (255, 255, 255), memory_button, 2)
        pygame.display.update()

    # Quit pygame
    pygame.quit()

main_menu()