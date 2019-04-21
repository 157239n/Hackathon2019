class Ball(object):
    def __init__(self, platforms):
        self.accY = -0.1
        self.velX = 7
        self.velY = 0
        self.x = 0
        self.y = 10
        self.jumping = False
        self.platforms = platforms
        self.tolerance = 7
        self.gameover=True
    def update(self):
        self.x += self.velX
        self.y += 2 * self.velY
        self.velY += 2 * self.accY
        
        if (self.x > width):
            self.velX = -abs(self.velX)
        elif (self.x < 0):
            self.velX = abs(self.velX)
        
        groundTouched = False
        for i in range(len(self.platforms)):
            if self.onPlatform(self.platforms[i]):
                self.jumping = False
                self.velY = 0
                self.y = self.platforms[i].y
                groundTouched = True
                break

        if (self.y > height):
            self.velY = -abs(self.velY)
        return groundTouched

    def onPlatform(self, platform):
        return (platform.x <= self.x < platform.x + platform.w) and (platform.y - self.tolerance < self.y < platform.y + self.tolerance)
    
    def display(self):
        ellipse(self.x, height - self.y, 20, 20)
        
    def kickUpward(self):
        if not self.jumping:
            self.y += self.tolerance/2
            # self.velY = 7.66
            self.velY = 5
            self.jumping = True
            
    def close(self, ball, tolerance):
        return ball.x - tolerance < self.x < ball.x + tolerance and ball.y - tolerance < self.y < ball.y + tolerance

class Player(Ball):
    def __init__(self, platforms, blades, bladeHolding):
        Ball.__init__(self, platforms)
        self.angle = 0.0
        self.velAngle = 0.05
        self.blades = blades
        self.gameover = False
        self.isHoldingBlade = True
        self.bladeIndexHolding = bladeHolding

    def updateAngle(self):
        self.angle += self.velAngle
        if (self.angle > PI):
            self.velAngle = -abs(self.velAngle)
        elif (self.angle < 0):
            self.velAngle = abs(self.velAngle)

    def update(self):
        if not self.gameover:
            super(Player, self).update()
            if self.isHoldingBlade:
                self.blades[self.bladeIndexHolding].setCoor(self.x, self.y)
            for i in range(len(self.blades)):
                self.updateAngle()
                if self.close(self.blades[i], 15) and not (self.blades[i].static):
                    self.gameover = True
                elif self.close(self.blades[i], 5) and self.blades[i].static and self.blades[i].free and (not self.isHoldingBlade):
                    self.blades[i].reclaim()
                    self.bladeIndexHolding = i
                    self.isHoldingBlade = True

    def display(self):
        if not (self.gameover):
            # fill(255, 0, 0)
            super(Player, self).display()
            line(self.x, height - self.y, self.x + 30 * cos(self.angle), height - (self.y + 30 * sin(self.angle)))

    def release(self):
        if self.isHoldingBlade:
            self.isHoldingBlade = False
            self.blades[self.bladeIndexHolding].release(self.angle)
            self.bladeIndexHolding = -1

class Blade(Ball):
    def __init__(self, platforms):
        Ball.__init__(self, platforms)
        self.free = False
        self.static = True
        self.bladeAngle = 0
        self.bladeAngleSpeed = 0.05

    def release(self, theta):
        if not self.free:
            self.free = True
            magnitude = 10
            self.y += 20
            self.velX = magnitude * cos(theta)
            self.velY = magnitude * sin(theta)
            self.static = False

    def update(self):
        self.bladeAngle += self.bladeAngleSpeed
        if self.static:
            self.bladeAngleSpeed = 0
        else:
            self.bladeAngleSpeed = 0.05

        if (self.free):
            self.static = super(Blade, self).update()
            if self.static:
                self.velX = 0
                self.velY = 0
                
        
    def reclaim(self):
        self.free = False
        self.static = True
        
    def display(self):
        global img
        fill(0, 255, 0)
        # super(Blade, self).display()
        pushMatrix()
        translate(self.x, height - self.y)
        rotate(self.bladeAngle)
        if self.free:
            image(img, -25, -25, 50, 50)
        popMatrix()
        
    def setCoor(self, x, y):
        if not self.free:
            self.x = x
            self.y = y

ground = 10

class Platform:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w
                
    def display(self):
        rect(self.x, height - (self.y), self.w, 10)
                      
def setup():
    size(600, 500)
    stroke(255)
    strokeWeight(3)
    frameRate(30)
    global platforms, ball1, ball2, blade1, blade2, img, bg
    img = loadImage("blade.png")
    bg = loadImage("bg3.PNG")    
    platforms = [
            Platform(0, 58, 48),
            Platform(54, 130, 150),
            Platform(282, 130, 150),
            Platform(510, 160, 72),
            Platform(0, 264, 430),
            Platform(360, 335, 240),
            Platform(0, 10, width)
            ]
    blade1 = Blade(platforms)
    blade2 = Blade(platforms)
    ball1 = Player(platforms, [blade1, blade2], 0)
    ball2 = Player(platforms, [blade1, blade2], 1)
    ball2.x = width

    background(0)
    
count = 1
def draw():
    global count
    count += 1
    global bg
    if ball1.gameover or ball2.gameover:
        noLoop()
        fill(200, 200, 200, 200)
        rect(0, 0, width, height)
        fill(0)
        textAlign(CENTER, CENTER)
        textSize(30)
        if ball1.gameover:
            text("Red loses", width/2, height/2)
        else:
            text("Blue loses", width/2, height/2)
    else:
        background(0)
        image(bg, 0, 0, width, height)
        # drawPlatforms()
        ball1.update()
        blade1.update()
        ball2.update()
        blade2.update()
        
        fill(255, 0, 0)
        ball1.display()
        fill(0, 0, 255)
        ball2.display()
        blade1.display()
        blade2.display()
def keyTyped():
    global ball1, ball2
    if (key == 'a'):
        ball1.kickUpward()
    if (key == 'd'):
        ball1.release()
    if (key == 'j'):
        ball2.kickUpward()
    if (key == 'l'):
        ball2.release()
        
def drawPlatforms():
    global platforms
    for platform in platforms:
        platform.display()
