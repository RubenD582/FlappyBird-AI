import random
import pygame
import sys
from ground import Ground
from pipe import Pipe
from menu import MenuSprite
from player import Player

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 288, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption("Flappy Bird")

sprites = pygame.sprite.Group()
ground1 = Ground(0, HEIGHT)
ground2 = Ground(ground1.get_position_x() + ground1.get_width(), HEIGHT)

menu = MenuSprite(WIDTH, HEIGHT)

generation = 0
performance = []
population_size = 10
players = [Player(HEIGHT) for _ in range(population_size)]

pipe1 = Pipe(210, random.randint(50, 250), True)
pipe2 = Pipe(210, pipe1.get_position_y() + pipe1.get_height()*2 + pipe1.GAP)

# Add ground sprites to the sprite group
sprites.add(pipe1, pipe2, ground1, ground2, players)

# Set the background image
background = pygame.image.load(f'images/background-{random.randint(1, 2)}.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

points = 0
point = False
game_over = False

count = 0
show_best = False


def draw_neural_network(screen, network, x, y, width, height):
    input_layer = network.input
    hidden_layer = network.hidden
    output_layer = network.output

    node_radius = 5
    input_spacing = height // (input_layer + 1)
    hidden_spacing = height // (hidden_layer + 1)
    output_spacing = height // (output_layer + 1)

    input_positions = [(x, y + i * input_spacing) for i in range(1, input_layer + 1)]
    hidden_positions = [(x + width // 2, y + i * hidden_spacing) for i in range(1, hidden_layer + 1)]
    output_positions = [(x + width, y + i * output_spacing) for i in range(1, output_layer + 1)]

    hidden_values = network.get_hidden_values()
    output_values = network.get_output_values()

    for i, input_pos in enumerate(input_positions):
        for j, hidden_pos in enumerate(hidden_positions):
            weight = network.input_hidden[i][j]
            color = (0, 255, 0) if weight > 0 else (255, 0, 0)
            pygame.draw.line(screen, color, input_pos, hidden_pos, 1)

    for i, hidden_pos in enumerate(hidden_positions):
        for j, output_pos in enumerate(output_positions):
            weight = network.hidden_output[i][j]
            color = (0, 255, 0) if weight > 0 else (255, 0, 0)
            pygame.draw.line(screen, color, hidden_pos, output_pos, 1)

    for i, pos in enumerate(input_positions):
        color_intensity = 128
        pygame.draw.circle(screen, (255, 255, 0), pos, node_radius)

    for i, pos in enumerate(hidden_positions):
        value = hidden_values[i] if i < len(hidden_values) else 0 
        color_intensity = int(value * 255)
        pygame.draw.circle(screen, (color_intensity, color_intensity, 0), pos, node_radius)

    for i, pos in enumerate(output_positions):
        value = output_values[i] if i < len(output_values) else 0
        color_intensity = int(value * 255)
        pygame.draw.circle(screen, (color_intensity, color_intensity, 0), pos, node_radius)


def selection(performance):
    selected_players = []
    while len(selected_players) < len(performance):
        candidates = random.sample(performance, 2)
        winner = max(candidates, key=lambda player: player.fitness)
        selected_players.append(winner)
    return selected_players


running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update pipes and players
    pipe1.update(pipe1.get_position_x() - pipe1.SPEED)
    pipe2.update(pipe2.get_position_x() - pipe2.SPEED)

    # Reset pipes when off-screen
    if pipe1.get_position_x() + pipe1.get_width() <= 0:
        for sprite in sprites:
            sprites.remove(sprite)

        pipe1 = Pipe(WIDTH, random.randint(50, 250), True)
        pipe2 = Pipe(WIDTH, pipe1.get_position_y() + pipe1.get_height()*2 + pipe1.GAP)

        # Add ground sprites to the sprite group
        sprites.add(pipe1, pipe2, ground1, ground2, players)

    for player in players[:]:
        output = player.neural_network.feedforward([
            (player.y + (player.height / 2)) - (pipe1.y + pipe1.get_height()),
            (player.y + (player.height / 2)) - (pipe2.y),
            pipe1.x,
            player.vy,
            player.get_position_y() / HEIGHT,
            (pipe1.x - player.get_position_x()) / WIDTH,
        ])
        
        if output[0] >= 0.5:
            player.jump()

        # Check for collisions with ground or pipes
        if (player.get_position_y() + player.get_height() >= ground1.get_position_y()) or player.get_position_y() <= 0:
            player.alive = False
            performance.append(player)
            sprites.remove(player)
            players.remove(player)

        elif (player.get_position_x() + player.get_width() >= pipe1.get_position_x() and
              player.get_position_x() <= pipe1.get_position_x() + pipe1.get_width()):
            if (player.get_position_y() <= pipe1.get_position_y() + pipe1.get_height()) or \
               (player.get_position_y() + player.get_height() >= pipe2.get_position_y()):
                player.alive = False
                performance.append(player)
                sprites.remove(player)
                players.remove(player)

        elif (player.get_position_x() + player.get_width() >= pipe1.get_position_x() - pipe1.get_width() / 2):
            if (player.get_position_y() >= pipe1.get_position_y() + pipe1.get_height()) and \
               (player.get_position_y() + player.get_height() <= pipe2.get_position_y()):
                player.score += 10

        player.update()

    if not players:
        max_score = max(player.score for player in performance) if performance else 1

        for player in performance:
            player.fitness = player.score / max_score

        performance = selection(performance)
        retained_players = sorted(performance, key=lambda p: p.fitness, reverse=True)[:6]
        
        players = []
        while len(players) < population_size:
            parent1, parent2 = random.sample(retained_players, 2)
            
            child_network = parent1.neural_network.crossover(parent2.neural_network)

            child_network.mutation(mutation_rate=0.2, mutation_strength=0.5)

            offspring = Player(HEIGHT, child_network)
            players.append(offspring)

        pipe1.SPEED = 1
        pipe2.SPEED = 1
        points = 0

        # Clear the previous population
        performance = []
        for sprite in sprites:
            sprites.remove(sprite)

        pipe1 = Pipe(210, random.randint(50, 250), True)
        pipe2 = Pipe(210, pipe1.get_position_y() + pipe1.get_height()*2 + pipe1.GAP)

        # Add ground sprites to the sprite group
        sprites.add(pipe1, pipe2, ground1, ground2, players)

        generation += 1
        pygame.display.set_caption(f"Generation: {generation}")


    # if point:
    #     pipe1.SPEED += 1
    #     pipe2.SPEED += 1
    #     points += 1

    #     print(points)

    #     point = False

    # ----------------------------------------------------
    # UPDATE AND DRAW THE GROUND

    ground1_x = ground1.get_position_x()
    if ground1_x + ground1.get_width() <= 0:
        ground1_x = WIDTH
    ground1.update(ground1_x - ground1.SPEED, game_over)

    ground2_x = ground2.get_position_x()
    if ground2_x + ground2.get_width() <= 0:
        ground2_x = WIDTH
    ground2.update(ground2_x - ground2.SPEED, game_over)

    # Fill the background with white
    screen.blit(background, (0, 0))
    
    # Draw here
    sprites.draw(screen)

    if len(players) > 0:
        best_player = max(players, key=lambda player: player.fitness)
        draw_neural_network(screen, best_player.neural_network, WIDTH - 130, 0, 120, 200)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

    count += 1
    
# Quit Pygame
pygame.quit()
sys.exit()