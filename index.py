import pygame, sys, random

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        if ball.left <= 0: player_score += 1
        else: opponent_score += 1
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_y, ball_speed_x, game_active
    game_active = False
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_y *= random.choice((1,-1))
    ball_speed_x *= random.choice((1,-1))

pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 960
large = pygame.font.Font('fonts/Eight-Bit Madness.ttf', 150)
small = pygame.font.Font('fonts/Eight-Bit Madness.ttf', 50)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

game_active = False
player_score = 0
opponent_score = 0

# Game rectangles
ball = pygame.Rect(screen_width/2 -15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

game_name = large.render('Pong', False, light_grey)
game_name_rect = game_name.get_rect(center = (640,200))

game_start = small.render('Press Space to Start', False, light_grey)
game_start_rect = game_start.get_rect(center = (640,400))

ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    if game_active:
        ball_animation()
        player_animation()
        opponent_ai()

    else:
        screen.blit(game_name, game_name_rect)
        screen.blit(game_start, game_start_rect)

        ai_score = large.render(f'{opponent_score}', False, light_grey)
        ai_score_rect = ai_score.get_rect(center = (320,200))

        your_score = large.render(f'{player_score}', False, light_grey)
        your_score_rect = your_score.get_rect(center = (960,200))

        player_speed = 0

        screen.blit(ai_score, ai_score_rect)
        screen.blit(your_score, your_score_rect)


    pygame.display.flip()
    clock.tick(60)