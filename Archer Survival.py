import pygame
import random
import math

WIDTH = 850
HEIGHT = 480
FPS = 30
SPRITESHEET = 'archer.png'
SKULLS = 'skulls.jpg'
TARGET = 'target.jpg'

# To access and animate images on a spritesheet
class Spritesheet(object):
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename)

    # Specify coorinates to isolate a particular image within spritesheet
    def getImage(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

# Using a given spritesheet, return arrays of the proper sprites to be used for animation
def loadAnimation(spritesheet, numImages, startingx, interval, y, width, height):
    animation = []
    for i in range(numImages):
        image = spritesheet.getImage(startingx + interval * i, y, width, height)
        animation.append(image)

    return animation

# Main archer playable character
class archer(object):
    vel = 8
    right = True
    left = False
    isJump = False
    jumpCount = 10
    walkCount = 0
    jumpingFrame = 0
    
    # Initialize spawn position and walking sprites
    def __init__(self, pos, walkingRight, walkingLeft, jumpingRight, jumpingLeft):
        self.x = pos[0]
        self.y = pos[1]
        self.walkingRight = walkingRight
        self.walkingLeft = walkingLeft               
        self.jumpingRight = jumpingRight
        self.jumpingLeft = jumpingLeft

        # Initialize player health and hitbox
        self.hitbox = (self.x + 20, self.y, 40, 70)
        self.health = 100
                  
    # Use W and D to control player   
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a] and self.x > -15:
            self.x = self.x - self.vel
            self.left = True
            self.right = False
        
        elif keys[pygame.K_d] and self.x < WIDTH - 60:
            self.x = self.x + self.vel
            self.left = False
            self.right = True
        else:
            self.walkCount = 0

        if not(self.isJump):
            if keys[pygame.K_w] and self.x < 700 - 40:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) // 2 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10
                self.jumpingFrame = 0

    # Animate player using spritesheet
    def draw(self, win):
        if not(self.isJump):
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if self.left:
                win.blit(self.walkingLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkingRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.jumpingFrame + 1 >=  9:
                self.jumpingFrame = 8
                
            if self.left:
                win.blit(self.jumpingLeft[self.jumpingFrame // 3], (self.x, self.y))
                self.jumpingFrame += 1
            else:
                win.blit(self.jumpingRight[self.jumpingFrame // 3], (self.x, self.y))
                self.jumpingFrame += 1

        # Update hitbox and health
        self.hitbox = (self.x + 20, self.y, 40, 70)
        pygame.draw.rect(win, (255, 0, 0), (742, 15, 100, 10))
        pygame.draw.rect(win, (0, 255, 0), (742, 15, 100 - ((100 - self.health - 2)), 10))

    # Subtract from health if player is hit
    def hit(self):
        if self.health > 0:
            self.health -= 1

# Arrow objects shot by player
class arrow(object):
    
    # Calculate arrow power and angle at click
    def __init__(self, x, y, pos, shootRight, shootLeft):
        self.x = x
        self.y = y
        self.startx = x
        self.starty = y
        self.shootRight = shootRight
        self.shootLeft = shootLeft
        # Contact point coords that eliminates enemy when in their hitbox
        self.impactx = x
        self.impacty = y
        self.time = 0
        self.power = math.sqrt((pos[1] - y)**2 + (pos[0] - x)**2)/2
        self.angle = findAngle(x, y, pos)
        vely = math.sin(self.angle) * self.power
        self.midpointTime = vely / 9.8
        self.maxheight = round(vely * self.midpointTime + ((-9.8 * (self.midpointTime)**2)/2))
                                          
    def draw(self, win, angle):
        # 0 degree shot
        if self.angle == -0.0:
            win.blit(self.shootRight[4], (self.x, self.y))
            self.impactx = self.x + 30
            self.impacty = self.y + 12

        # 0 to 30 degree shot    
        elif self.angle > 0 and self.angle < math.pi / 6:
            if self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[3], (self.x, self.y))
                    self.impactx = self.x + 30
                    self.impacty = self.y + 12

                elif self.time > self.midpointTime:
                    win.blit(self.shootRight[5], (self.x, self.y))
                    self.impactx = self.x + 29
                    self.impacty = self.y + 16
                
            else:
                win.blit(self.shootRight[4], (self.x, self.y))
                self.impactx = self.x + 30
                self.impacty = self.y + 12

        # 30 to 60 degree shot        
        elif self.angle >= math.pi / 6 and self.angle < math.pi / 3:
            intervals = 2
            if self.y > self.starty - self.maxheight / intervals:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[2], (self.x, self.y))
                    self.impactx = self.x + 30
                    self.impacty = self.y + 10
                    
                else:
                    win.blit(self.shootRight[6], (self.x, self.y))
                    self.impactx = self.x + 29
                    self.impacty = self.y + 20
            
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[3], (self.x, self.y))
                    self.impactx = self.x + 30
                    self.impacty = self.y + 12
                    
                else:
                    win.blit(self.shootRight[5], (self.x, self.y))
                    self.impactx = self.x + 29
                    self.impacty = self.y + 16
                    
            else:
                win.blit(self.shootRight[4], (self.x, self.y))
                self.impactx = self.x + 30
                self.impacty = self.y + 12

        # 60 to 90 degree shot
        elif self.angle >= math.pi / 3 and self.angle < math.pi / 2:
            intervals = 3
            if self.y > self.starty - self.maxheight / intervals:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[1], (self.x, self.y))
                    self.impactx = self.x + 25
                    self.impacty = self.y + 5

                else:
                    win.blit(self.shootRight[7], (self.x, self.y))
                    self.impactx = self.x + 25
                    self.impacty = self.y + 25
            
            elif self.y > self.starty - self.maxheight / intervals * 2:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[2], (self.x, self.y))
                    self.impactx = self.x + 30
                    self.impacty = self.y + 10
                    
                else:
                    win.blit(self.shootRight[6], (self.x, self.y))
                    self.impactx = self.x + 29
                    self.impacty = self.y + 20
                    
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[3], (self.x, self.y))
                    self.impactx = self.x + 30
                    self.impacty = self.y + 12
                    
                else:
                    win.blit(self.shootRight[5], (self.x, self.y))
                    self.impactx = self.x + 29
                    self.impacty = self.y + 16
                    
            else:
                win.blit(self.shootRight[4], (self.x, self.y))
                self.impactx = self.x + 30
                self.impacty = self.y + 12

        # 90 degree angle shot
        elif self.angle == math.pi / 2:
            intervals = 4
            if self.y > self.starty - (self.maxheight / intervals):
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[0], (self.x, self.y))
                    self.impactx = self.x + 14
                    self.impacty = self.y
                    
                else:
                    win.blit(self.shootRight[8], (self.x, self.y))
                    self.impactx = self.x + 12
                    self.impacty = self.y + 28
                    
            elif self.y > self.starty - (self.maxheight / intervals) * 2:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[1], (self.x, self.y))
                    self.impactx = self.x + 25
                    self.impacty = self.y + 5
                    
                else:
                    win.blit(self.shootRight[7], (self.x, self.y))
                    self.impactx = self.x + 25
                    self.impacty = self.y + 25
                    
            elif self.y > self.starty - (self.maxheight / intervals) * 3:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[2], (self.x, self.y))
                    self.impactx = self.x + 30
                    self.impacty = self.y + 10
                    
                else:
                    win.blit(self.shootRight[6], (self.x, self.y))
                    self.impactx = self.x + 29
                    self.impacty = self.y + 20
            
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[3], (self.x, self.y))
                    self.impactx = self.x + 30
                    self.impacty = self.y + 12
                    
                else:
                    win.blit(self.shootRight[5], (self.x, self.y))
                    self.impactx = self.x + 29
                    self.impacty = self.y + 16
                    
            else:
                win.blit(self.shootRight[4], (self.x, self.y))
                self.impactx = self.x + 30
                self.impacty = self.y + 12

        # 90 to 120 degree shot
        elif self.angle > math.pi / 2 and self.angle <= 2 * math.pi / 3:
            intervals = 3
            if self.y > self.starty - self.maxheight / intervals:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[1], (self.x, self.y))
                    self.impactx = self.x + 8
                    self.impacty = self.y + 5
                    
                else:
                    win.blit(self.shootLeft[7], (self.x, self.y))
                    self.impactx = self.x + 9
                    self.impacty = self.y + 22
                    
            elif self.y > self.starty - self.maxheight / intervals * 2:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[2], (self.x, self.y))
                    self.impactx = self.x + 4
                    self.impacty = self.y + 10
                    
                else:
                    win.blit(self.shootLeft[6], (self.x, self.y))
                    self.impactx = self.x + 5
                    self.impacty = self.y + 17
                    
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[3], (self.x, self.y))
                    self.impactx = self.x
                    self.impacty = self.y + 12
                    
                else:
                    win.blit(self.shootLeft[5], (self.x, self.y))
                    self.impactx = self.x + 2
                    self.impacty = self.y + 21
                        
            else:
                win.blit(self.shootLeft[4], (self.x, self.y))
                self.impactx = self.x
                self.impacty = self.y + 12

        # 120 to 150 degree shot
        elif self.angle > 2 * math.pi / 3 and self.angle <= 5 * math.pi / 6:
            intervals = 2
            if self.y > self.starty - self.maxheight / intervals:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[2], (self.x, self.y))
                    self.impactx = self.x + 4
                    self.impacty = self.y + 10
                    
                else:
                    win.blit(self.shootLeft[6], (self.x, self.y))
                    self.impactx = self.x + 5
                    self.impacty = self.y + 17
                    
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[3], (self.x, self.y))
                    self.impactx = self.x
                    self.impacty = self.y + 12
                    
                else:
                    win.blit(self.shootLeft[5], (self.x, self.y))
                    self.impactx = self.x + 2
                    self.impacty = self.y + 21
                    
            else:
                win.blit(self.shootLeft[4], (self.x, self.y))
                self.impactx = self.x
                self.impacty = self.y + 12

        # 150 to 180 degree shot
        elif self.angle > 5 * math.pi/6 and self.angle < math.pi:
            if self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[3], (self.x, self.y))
                    self.impactx = self.x
                    self.impacty = self.y + 12
                    
                elif self.time > self.midpointTime:
                    win.blit(self.shootLeft[5], (self.x, self.y))
                    self.impactx = self.x + 2
                    self.impacty = self.y + 21
                    
            else:
                win.blit(self.shootLeft[4], (self.x, self.y))
                self.impactx = self.x
                self.impacty = self.y + 12

        # 180 degree shot
        elif self.angle == math.pi:
            win.blit(self.shootLeft[4], (self.x, self.y))
            self.impactx = self.x
            self.impacty = self.y + 12

        # 180 to 210 degree shot       
        elif self.angle < 7 * math.pi / 6:
            win.blit(self.shootLeft[5], (self.x, self.y))
            self.impactx = self.x + 2
            self.impacty = self.y + 21

        # 210 to 240 degree shot            
        elif self.angle < 4 * math.pi / 3:
            win.blit(self.shootLeft[6], (self.x, self.y))
            self.impactx = self.x + 5
            self.impacty = self.y + 17

        # 240 to 270 degree shot            
        elif self.angle < 3 * math.pi / 2:
            win.blit(self.shootLeft[7], (self.x, self.y))
            self.impactx = self.x + 9
            self.impacty = self.y + 22

        # 270 to 300 degree shot           
        elif self.angle < 5 * math.pi / 3:
            win.blit(self.shootRight[7], (self.x, self.y))
            self.impactx = self.x + 25
            self.impacty = self.y + 25

        # 300 to 330 degree shot   
        elif self.angle < 11 * math.pi / 6:
            win.blit(self.shootRight[6], (self.x, self.y))
            self.impactx = self.x + 29
            self.impacty = self.y + 20

        # 330 to 360 degree shot    
        elif self.angle < 2 * math.pi:
            win.blit(self.shootRight[5], (self.x, self.y))
            self.impactx = self.x + 29
            self.impacty = self.y + 16
        

    # Calculates new arrow trajectory based on initial power and angle. Returns new postion after
    # increment
    @staticmethod
    def arrowPath(startx, starty, power, ang, time):
        velx = math.cos(ang) * power
        vely = math.sin(ang) * power
        distx = velx * time
        disty = vely * time + ((-9.8 * (time)**2)/2)
        newx = round(startx + distx)
        newy = round(starty - disty)
        return (newx, newy)

# Find angle of aim line
def findAngle(arrowx, arrowy, pos):
    # If angle cannot be calculated, set it to 90 degrees
    try:
        angle = math.atan((arrowy - pos[1]) / (arrowx - pos[0]))
    except:
        angle = math.pi / 2

    # Adjust angle values based on quadrant
    if pos[1] < arrowy and pos[0] > arrowx:
        angle = abs(angle)
    elif pos[1] < arrowy and pos[0] < arrowx:
        angle = math.pi - angle
    elif pos[1] > arrowy and pos[0] < arrowx:
        angle = math.pi + abs(angle)
    elif pos[1] > arrowy and pos[0] > arrowx:
        angle = (math.pi * 2) - angle

    return angle

# Enemies
class skull(object):
    vel = 3
    counter = 0
    
    def __init__(self, playerx, playery, movingRight, movingLeft):
        # Enemies spawn in random locations
        self.x = random.randrange(WIDTH)
        self.y = random.randrange(HEIGHT - 200)
        self.impactx = self.x
        self.impacty = self.y
        self.movingRight = movingRight
        self.movingLeft = movingLeft

        # Set skull direction
        if self.x > playerx:
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = True
        
        # Initialize hitbox
        self.hitbox = (self.x - 5, self.y - 5, 32, 40)

    # Skulls move towards player location
    def move(self, playerx, playery):
        if self.impactx > playerx + 40:
            self.x -= self.vel
        elif self.impactx < playerx + 40: 
            self.x += self.vel

        if self.impacty > playery + 30:
            self.y -= self.vel
        elif self.impacty < playery + 30:
            self.y += self.vel

        if self.impactx > playerx + 10:
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = True

    # Draw skulls using loaded sprites       
    def draw(self, win):
        if self.counter + 1 >= 12:
            self.counter = 0

        if self.left:
            win.blit(self.movingLeft[self.counter // 3], (self.x, self.y))
            self.counter += 1

        if self.right:
            win.blit(self.movingRight[self.counter // 3], (self.x, self.y))
            self.counter += 1
        
        self.hitbox = (self.x - 5, self.y - 5, 32, 40)
        self.impactx = self.x + 10
        self.impacty = self.y + 10
        
# Redraw window for each game frame
def redrawWindow(win):
    global player1, bg, line, arrows, skulls, font, score
    
    # Redraw background, player, score and aim line
    win.blit(bg, (0, 0))
    player1.draw(win)
    pygame.draw.line(win, (0, 0, 0), line[0], line[1])
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (390, 10))
    text = font.render("Health: ", 1, (0, 0, 0))
    win.blit(text, (650, 10))
    
    # Redraw arrow shots
    arrownum = 0
    for shot in arrows:
        if shot.x < WIDTH and shot.x > 0:
            if shot.y < HEIGHT:
                
                # Increment time and get new position to draw arrow to
                shot.time += 0.2
                newpos = shot.arrowPath(shot.startx, shot.starty, shot.power, shot.angle, shot.time)
                shot.x = newpos[0]
                shot.y = newpos[1]
                shot.draw(win, shot.angle)

                # Check for arrow and skull collision. If collision exists, pop arrow and skull from
                # respective lists
                skullnum = 0
                for enemy in skulls:
                    if shot.impactx >= enemy.hitbox[0] and shot.impactx <= enemy.hitbox[0] +  enemy.hitbox[2]:
                        if shot.impacty >= enemy.hitbox[1] and shot.impacty <= enemy.hitbox[1] + enemy.hitbox[3]:
                            skulls.pop(skullnum)
                            arrows.pop(arrownum)
                            arrownum -= 1
                            skullnum -= 1
                            score += 1
                    skullnum += 1

        # If arrow offscreen, pop from arrow list
        else:
            arrows.pop(arrownum)
            arrownum -= 1
        arrownum += 1

    # Redraw skulls
    for enemy in skulls:
        enemy.draw(win)
        
    pygame.display.update()

# Main game loop. Walk and aim to shoot as many targets as possible in the time limit   
def main():
    # Initialize pygame and create window
    global player1, bg, win, line, arrows, skulls, font, score
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.image.load('bg.jpg')
    pygame.display.set_caption("Archer Survival")
    font = pygame.font.SysFont('comicsans', 30, True)
    score = 0

    # Spritesheets for player, arrows, and skull enemies
    spritesheet = Spritesheet(SPRITESHEET)
    skullsheet = Spritesheet(SKULLS)

    # Load player animations
    walkingRight = loadAnimation(spritesheet, 9, 220, 81, 8, 80, 70)
    walkingLeft = []
    for i in range(len(walkingRight)):
        walkingLeft.append(pygame.transform.flip(walkingRight[i], True, False))
                       
    jumpingRight = loadAnimation(spritesheet, 3, 60, 75, 290, 70, 65)
    jumpingLeft = []
    for i in range(len(jumpingRight)):
        jumpingLeft.append(pygame.transform.flip(jumpingRight[i], True, False))

    # Load arrow animations
    shootRight = loadAnimation(spritesheet, 4, 980, 35, 280, 34, 40)
    temp = loadAnimation(spritesheet, 5, 995, 37, 330, 35, 40)
    for i in range(len(temp)):
        shootRight.append(temp[i])
    shootLeft = []
    for i in range(len(shootRight)):
        shootLeft.append(pygame.transform.flip(shootRight[i], True, False))

    # Load skull animations
    movingRight = loadAnimation(skullsheet, 4, 0, 210, 0, 170, 280)
    movingLeft = []
    for i in range(len(movingRight)):
        image = pygame.transform.scale(movingRight[i], (23, 35))
        image.set_colorkey((152, 108, 183))
        movingRight[i] = image
        image = pygame.transform.flip(image, True, False)
        image.set_colorkey((152, 108, 183))
        movingLeft.append(image)

    # Spawn player
    player1 = archer((350, 400), walkingRight, walkingLeft, jumpingRight, jumpingLeft)

    # Arrow variables
    x = 0
    y = 0
    time = 0
    power = 0
    angle = 0
    
    # Main game loop. Set clock
    run = True
    arrows = []
    skulls = []
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    counter = 0
    while run:
        
        # Get mouse position and set up aim line
        pos = pygame.mouse.get_pos()
        if player1.right:
            line = [(player1.x + 50, player1.y), pos]
        else:
            line = [(player1.x + 20, player1.y), pos]
            
        # Check for closing window and mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Mouse click shoots an arrow object. Add shot to list of arrows
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = line[0][0]
                y = line[0][1]
                shot = arrow(x, y, pos, shootRight, shootLeft)
                arrows.append(shot)

        if counter % 15 == 0:
            enemy = skull(player1.x, player1.y, movingRight, movingLeft)
            skulls.append(enemy)

        if len(skulls) >= 1:
           for enemy in skulls:
               if enemy.impactx >= player1.hitbox[0] and enemy.impactx <= player1.hitbox[0] +  player1.hitbox[2]:
                        if enemy.impacty >= player1.hitbox[1] and enemy.impacty <= player1.hitbox[1] + player1.hitbox[3]:
                            player1.hit()

                            if player1.health == 0:
                                print("You lost with a score of " + str(score) +  "! Play again!")
                                run = False
        
        # Keep loop running at same speed
        clock.tick(FPS)
        player1.move()
        for enemy in skulls:
            enemy.move(player1.x, player1.y)
            
        # Frame counter, used for enemy spawn rate
        counter += 1
        redrawWindow(win)

main()
pygame.quit()
