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

# Main archer playable character
class archer(object):
    vel = 8
    right = True
    left = False
    isJump = False
    jumpCount = 10
    walkCount = 0
    shootCount = 0
    walkingLeft = []
    walkingRight = []
    shootRight = []
    shootLeft = []
    jumpingLeft = []
    jumpingRight = []
    jumpingFrame = 0
    spritesheet = Spritesheet(SPRITESHEET)

    # Initialize spawn position and walking sprites
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        for i in range(9):
            image = self.spritesheet.getImage(220 + 81 * i, 8, 80, 70)
            self.walkingRight.append(image)
            image = pygame.transform.flip(image, True, False)
            self.walkingLeft.append(image)
            if i < 8:
                image = self.spritesheet.getImage(220 + 81 * i, 188, 80, 70)
                self.shootRight.append(image)
                image = pygame.transform.flip(image, True, False)
                self.shootLeft.append(image)
            if i < 3:
                image = self.spritesheet.getImage(75  + 75 * i, 290, 80, 65)
                self.jumpingRight.append(image)
                image = pygame.transform.flip(image, True, False)
                self.jumpingLeft.append(image)
                
             
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
        

    def shootAnim(self, win):
        if self.shootCount + 1 >= 24:
            self.shootCount = 0
        if self.left:
            win.blit(self.shootLeft[self.shootCount // 3], (self.x, self.y))
            self.shootCount += 1
        elif self.right:
            win.blit(self.shootRight[self.shootCount // 3], (self.x, self.y))
            self.shootCount += 1

# Arrow objects shot by player
class arrow(object):
    spritesheet = Spritesheet(SPRITESHEET)
    shootRight = []
    shootLeft = []
    
    # Calculate arrow power and angle at click
    def __init__(self, x, y, pos):
        self.x = x
        self.y = y
        self.startx = x
        self.starty = y
        self.time = 0
        self.power = math.sqrt((pos[1] - y)**2 + (pos[0] - x)**2)/2
        self.angle = findAngle(x, y, pos)
        vely = math.sin(self.angle) * self.power
        self.midpointTime = vely / 9.8
        self.maxheight = round(vely * self.midpointTime + ((-9.8 * (self.midpointTime)**2)/2))
       
        for i in range(4):
            image = self.spritesheet.getImage(980 + 35 * i, 280, 34, 40)
            self.shootRight.append(image)
            image = pygame.transform.flip(image, True, False)
            self.shootLeft.append(image)
        for i in range(5):
            image = self.spritesheet.getImage(995 + 37 * i, 330, 35, 40)
            self.shootRight.append(image)
            image = pygame.transform.flip(image, True, False)
            self.shootLeft.append(image)

    def draw(self, win, angle):

        if self.angle == -0.0:
            win.blit(self.shootRight[4], (self.x, self.y))
        elif self.angle > 0 and self.angle < math.pi / 6:
            if self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[3], (self.x, self.y))
                elif self.time > self.midpointTime:
                    win.blit(self.shootRight[5], (self.x, self.y))
            else:
                win.blit(self.shootRight[4], (self.x, self.y))
                
        elif self.angle >= math.pi / 6 and self.angle < math.pi / 3:
            intervals = 2
            if self.y > self.starty - self.maxheight / intervals:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[2], (self.x, self.y))
                else:
                    win.blit(self.shootRight[6], (self.x, self.y))
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[3], (self.x, self.y))
                else:
                    win.blit(self.shootRight[5], (self.x, self.y))
            else:
                win.blit(self.shootRight[4], (self.x, self.y))

        elif self.angle >= math.pi / 3 and self.angle < math.pi / 2:
            intervals = 3
            if self.y > self.starty - self.maxheight / intervals:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[1], (self.x, self.y))
                else:
                    win.blit(self.shootRight[7], (self.x, self.y))
            elif self.y > self.starty - self.maxheight / intervals * 2:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[2], (self.x, self.y))
                else:
                    win.blit(self.shootRight[6], (self.x, self.y))
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[3], (self.x, self.y))
                else:
                    win.blit(self.shootRight[5], (self.x, self.y))
            else:
                win.blit(self.shootRight[4], (self.x, self.y))
    
        elif self.angle == math.pi / 2:
            intervals = 4
            if self.y > self.starty - (self.maxheight / intervals):
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[0], (self.x, self.y))
                else:
                    win.blit(self.shootRight[8], (self.x, self.y))
            elif self.y > self.starty - (self.maxheight / intervals) * 2:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[1], (self.x, self.y))
                else:
                    win.blit(self.shootRight[7], (self.x, self.y))
            elif self.y > self.starty - (self.maxheight / intervals) * 3:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[2], (self.x, self.y))
                else:
                    win.blit(self.shootRight[6], (self.x, self.y))
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootRight[3], (self.x, self.y))
                else:
                    win.blit(self.shootRight[5], (self.x, self.y))
            else:
                win.blit(self.shootRight[4], (self.x, self.y))

        elif self.angle > math.pi / 2 and self.angle <= 2 * math.pi / 3:
            intervals = 3
            if self.y > self.starty - self.maxheight / intervals:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[1], (self.x, self.y))
                else:
                    win.blit(self.shootLeft[7], (self.x, self.y))
            elif self.y > self.starty - self.maxheight / intervals * 2:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[2], (self.x, self.y))
                else:
                    win.blit(self.shootLeft[6], (self.x, self.y))
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[3], (self.x, self.y))
                else:
                    win.blit(self.shootLeft[5], (self.x, self.y))
            else:
                win.blit(self.shootLeft[4], (self.x, self.y))

        elif self.angle > 2 * math.pi / 3 and self.angle <= 5 * math.pi / 6:
            intervals = 2
            if self.y > self.starty - self.maxheight / intervals:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[2], (self.x, self.y))
                else:
                    win.blit(self.shootLeft[6], (self.x, self.y))
            elif self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[3], (self.x, self.y))
                else:
                    win.blit(self.shootLeft[5], (self.x, self.y))
            else:
                win.blit(self.shootLeft[4], (self.x, self.y))

        elif self.angle > 5 * math.pi/6 and self.angle < math.pi:
            if self.y > self.starty - self.maxheight:
                if self.time < self.midpointTime:
                    win.blit(self.shootLeft[3], (self.x, self.y))
                elif self.time > self.midpointTime:
                    win.blit(self.shootLeft[5], (self.x, self.y))
            else:
                win.blit(self.shootLeft[4], (self.x, self.y))

        elif self.angle == math.pi:
            win.blit(self.shootLeft[4], (self.x, self.y))
        elif self.angle < 7 * math.pi / 6:
            win.blit(self.shootLeft[5], (self.x, self.y))
        elif self.angle < 4 * math.pi / 3:
            win.blit(self.shootLeft[6], (self.x, self.y))
        elif self.angle < 3 * math.pi / 2:
            win.blit(self.shootLeft[7], (self.x, self.y))
        elif self.angle < 5 * math.pi / 3:
            win.blit(self.shootRight[7], (self.x, self.y))
        elif self.angle < 11 * math.pi / 6:
            win.blit(self.shootRight[6], (self.x, self.y))
        elif self.angle < 2 * math.pi:
            win.blit(self.shootRight[5], (self.x, self.y))
        

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

class skull(object):
    skullsheet = Spritesheet(SKULLS)
    vel = 3
    movingLeft = []
    movingRight = []
    counter = 0
    
    def __init__(self, playerx, playery):
        self.x = random.randrange(WIDTH)
        self.y = random.randrange(HEIGHT)
        if self.x > playerx:
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = True

        for i in range(4):
            image = self.skullsheet.getImage(0 + 210 * i, 0, 170, 280)
            image = pygame.transform.scale(image, (23, 35))
            image.set_colorkey((152, 108, 183))
            self.movingRight.append(image)
            image = pygame.transform.flip(image, True, False)
            image.set_colorkey((152, 108, 183))
            self.movingLeft.append(image)
        
    def move(self, playerx, playery):
        if self.x > playerx:
            self.x -= self.vel
        elif self.x < playerx:
            self.x += self.vel

        if self.y > playery:
            self.y -= self.vel
        elif self.y < playery:
            self.y += self.vel

        if self.x > playerx:
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = True
            
    def draw(self, win):
        if self.counter + 1 >= 12:
            self.counter = 0

        if self.left:
            win.blit(self.movingLeft[self.counter // 3], (self.x, self.y))
            self.counter += 1

        if self.right:
            win.blit(self.movingRight[self.counter // 3], (self.x, self.y))
            self.counter += 1
        
# Redraw window for each game frame
def redrawWindow(win):
    global player1, bg, line, arrows, skulls
    # Redraw background, player and aim line
    win.blit(bg, (0, 0))
    player1.draw(win)
    pygame.draw.line(win, (0, 0, 0), line[0], line[1])
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
                skullnum = 0
                for enemy in skulls:
                    if shot.x == enemy.x and shot.y == enemy.y:
                        skulls.pop(skullnum)
                        arrows.pop(arrownum)
                    skullnum += 1
        # If arrow offscreen, pop from arrow list
        else:
            arrows.pop(arrownum)
        arrownum += 1

    for enemy in skulls:
        enemy.draw(win)
    pygame.display.update()

# Main game loop. Walk and aim to shoot as many targets as possible in the time limit   
def main():
    # Initialize pygame and create window
    global player1, bg, win, line, arrows, skulls
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.image.load('bg.jpg')
    pygame.display.set_caption("Shoota")

    # Set clock and spawn player
    player1 = archer((350, 400))

    # Arrow variables
    x = 0
    y = 0
    time = 0
    power = 0
    angle = 0
    
    # Main game loop
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
                shot = arrow(x, y, pos)
                arrows.append(shot)
                #for i in range(24):
                    #player1.shootAnim(win)

        if counter % 50 == 0:
            enemy = skull(player1.x, player1.y)
            skulls.append(enemy)
        
        # Keep loop running at same speed
        clock.tick(FPS)
        player1.move()
        for enemy in skulls:
            enemy.move(player1.x, player1.y)

        

            
        redrawWindow(win)
        counter += 1

main()
pygame.quit()
