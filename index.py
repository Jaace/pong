import pygame, sys, random

class Ball():
    def __init__(self, player, opponent):
    # def __init__(self, player):
        # super().__init__()
        self.speed_x = 7 * random.choice((1,-1))
        self.speed_y = 7 * random.choice((1,-1))
        self.rect = pygame.Rect(screen_width/2 -15, screen_height/2 - 15, 30, 30)
        self.player = player
        self.opponent = opponent

    def draw(self):
        pygame.draw.ellipse(screen, light_grey, self.rect)
    
    def animation_state(self):
        global player_score, opponent_score

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1

        if self.rect.left <= 0 or self.rect.right >= screen_width:
            if self.rect.left <= 0: player_score += 1
            else: opponent_score += 1
            self.restart()

        if self.rect.colliderect(self.player) or self.rect.colliderect(self.opponent):
            self.speed_x *= -1

        self.draw()
    
    def restart(self):
        global game_active
        game_active = False

        self.rect.center = (screen_width/2, screen_height/2)
        self.speed_x = 7 * random.choice((1,-1))
        self.speed_y = 7 * random.choice((1,-1))

    def opponent_ai(self):
        global opponent_speed

        if self.opponent.top < self.rect.y:
            self.opponent.top += opponent_speed
        if self.opponent.bottom > self.rect.y:
            self.opponent.bottom -= opponent_speed

        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= screen_height:
            self.opponent.bottom = screen_height

    def update(self):
        self.animation_state()
        self.opponent_ai()

# class Paddle():
#     def __init__(self, left, top, color):
#         self.color = color
#         self.left = left
#         self.top = top
#         # TODO: Do I need to set self.left and self.top?
#         self.rect = pygame.Rect(left, top, 10, 140)

#     def draw(self):
#         pygame.draw.rect(screen, light_grey, self.rect)

# class Opponent(Paddle):
#     def __init__(self, left, top, color):
#         super().__init__(left, top, color)
#         self.speed = 7

pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

screen_width = 1280
screen_height = 960
large = pygame.font.Font('fonts/Eight-Bit Madness.ttf', 150)
small = pygame.font.Font('fonts/Eight-Bit Madness.ttf', 50)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

game_active = False
player_score = 0
opponent_score = 0

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Game rectangles
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)
# opponent = Opponent(10, screen_height/2 - 70, light_grey)
# print(opponent)



game_name = large.render('Pong', False, light_grey)
game_name_rect = game_name.get_rect(center = (640,200))

game_start = small.render('Press Space to Start', False, light_grey)
game_start_rect = game_start.get_rect(center = (640,400))

ball = Ball(player, opponent)
player_speed = 0
opponent_speed = 7

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                if y >= screen_height - 140:
                    player.y = screen_height - 140
                else: player.y = y
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    if game_active:
        ball.update()
      
    else:
        screen.blit(game_name, game_name_rect)
        screen.blit(game_start, game_start_rect)

        ai_score = large.render(f'{opponent_score}', False, light_grey)
        ai_score_rect = ai_score.get_rect(center = (320,200))

        your_score = large.render(f'{player_score}', False, light_grey)
        your_score_rect = your_score.get_rect(center = (960,200))

        player_speed = 0
        ball.draw()
        # opponent.draw()

        screen.blit(ai_score, ai_score_rect)
        screen.blit(your_score, your_score_rect)


    pygame.display.flip()
    clock.tick(60)