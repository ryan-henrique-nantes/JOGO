import pygame #Imports the package and modules 

pygame.init() #Initializes the modules
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breaking Bricks")

#bat
bat = pygame.image.load("./images/paddle.png")
bat = bat.convert_alpha()
bat_rect = bat.get_rect()
bat_rect[1] = screen.get_height() - 100

#ball
ball = pygame.image.load('./images/football.png')
ball = ball.convert_alpha()
ball_rect = ball.get_rect()
ball_start = (200, 200)
ball_speed = (3.0, 3.0)
ball_served = False
sx, sy = ball_speed
ball_rect.topleft = ball_start

#brick
brick = pygame.image.load('./images/brick.png')
brick = brick.convert_alpha()
brick_rect = brick.get_rect()
bricks = [] #Holding position of bricks
brick_rows = 5
brick_gap = 10
brick_cols = screen.get_width() // (brick_rect[2] + brick_gap)
side_gap = (screen.get_width() - (brick_rect[2] + brick_gap) * brick_cols + brick_gap) // 2

#Creating a for loop to get the amount of bricks and position them on the screen
for y in range(brick_rows):
    brickY = y * (brick_rect[3] + brick_gap) #Setting the location of the bricks in the Y axis
    for x in range(brick_cols):
        brickX = x * (brick_rect[2] + brick_gap) + side_gap #setting the location of the bricks in the X axis
        bricks.append((brickX,brickY))#Adding the positions of all the bricks to the screen

game_over = False 
#Our conditional for our while loop, It will keep looping until this becomes True
clock = pygame.tyme.Clock()
while not game_over: #Loop Runs until game_over is True
        dt = clock.tick(50)#Setting up the frames per second
        screen.fill((0, 0, 0)) #This makes the screen black each loop

        for b in bricks: #Looping through the positions of bricks
          screen.blit(brick, b) #Drawing them on the screen
         
          screen.blit(bat, bat_rect)#Sets the bat in the position of bat_rect
          screen.blit(ball, ball_rect)#Sets the ball in the position of ball_rect

        for event in pygame.event.get(): #Loops over all events in pygame
            if event.type == pygame.QUIT: #Checks for the event type "QUIT" which is exiting your screen
                game_over = True 

        pressed = pygame.key.get_pressed()#gets all pressable keys
        if pressed[pygame.K_LEFT]: #If left arrow is pressed it will move 0.5 * 50 to the left
          x -= 0.5 * dt
        if pressed[pygame.K_RIGHT]:#If right arrow is pressed it will move 0.5 * 50 to the right
          x += 0.5 * dt
        if pressed[pygame.K_SPACE]:
          ball_served = True

        if bat_rect[0] + bat_rect.width >= ball_rect[0] >= bat_rect[0] and \
        ball_rect[1] + ball_rect.height >= bat_rect[1] and \
         sy > 0:
#if the bat x position + bat width is >= ball x position >= bat x position and 
#ball x position + ball height >= bat x position and 
#if the ball is heading in a downwards direction:
          sy *= -1
          sx *= 1.01  #increase difficulty
          sy *= 1.01
          continue

        delete_brick = None
        for b in bricks:
            bx, by = b
            if bx <= ball_rect[0] <= bx + brick_rect.width and \
               by <= ball_rect[1] <= by + brick_rect.height:
                delete_brick = b
    
                if ball_rect[0] <= bx + 2: #Changing the direction of the ball when it hits the left
                    sx *= -1
                elif ball_rect[0] >= bx + brick_rect.width - 2:#Changing the direction of the ball when it hits the right side
                    sx *= -1
                if ball_rect[1] <= by + 2:
                    sy *= -1
                elif ball_rect[1] >= by + brick_rect.height - 2:
                    sy *= -1
                break

        if delete_brick is not None:
            bricks.remove(delete_brick)
        
        #top 
        if ball_rect[1] <= 0: #if the ball hits the top it changes the y speed to go down
            ball_rect[1] = 0
            sy *= -1

        #bottom
        if ball_rect[1] >= screen.get_height() - ball_rect.height: #if the ball hits the bottom it will change the value of ball_served and reset the position of the ball
            ball_served = False
            ball_rect.topleft = ball_start

        #left
        if ball_rect[0] <= 0: #if the ball hits the right it will change the direction of the ball direction to 
            ball_rect[0] = 0
            sx *= -1

        #right
        if ball_rect[0] >= screen.get_width() - ball_rect.width:
            ball_rect[0] = screen.get_width() - ball_rect.width
            sx *= -1
      
        bat_rect[0] = x
        if ball_served:
            ball_rect[0] += sx
            ball_rect[1] += sy
#If the user triggers the event it will change game_over = True, and exit out of the loop

        pygame.display.update() #Updates screen after each loop
#Once the loop ends it will run pygame.quit()
pygame.quit()