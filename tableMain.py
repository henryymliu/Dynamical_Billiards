import sys, pygame
import numbers, math

pygame.init();

size = width, height = 1020,600
speed = [1, 1]
white = (255, 255, 255)
black = (0,0,0)
screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif").convert()
# pygame.draw.circle(ball, (255,0,0), (100,100),50, 10)



ballrect = ball.get_rect()


while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(white)
    pygame.draw.arc(screen, black, [0, 0, 300, 600], math.pi / 2, 3 * math.pi / 2, 1)
    pygame.draw.line(screen, black, [0,300], [0,650],1)

    screen.blit(ball, ballrect)
    pygame.display.flip()
