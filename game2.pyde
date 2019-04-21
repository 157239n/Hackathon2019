import random
ball_y = 60
x = 150
vel = 5
tamgiac_x = 300
ball_x = 300
k = -5
i = 5
x_1 = 0
y_1 = 10
valid = True
class Ellipse:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
        ellipse(self.x, self.y, self.r, self.r)
    def change(self, x, y, r):
         self.x = x
         self.y = y
         self.r = r
         ellipse(self.x, self.y, self.r, self.r)

def setup():
    size(600,600)
    background(91, 51, 49)
    global circle1, circle2
    circle1 = Ellipse(0, 0, 0)
    circle2 = Ellipse(0,0,0)
    
def draw():
    valid == True
    if valid == True:
        global x, vel, tamgiac_x, ball_y, circle1, ball_x, k, i, x_1, valid
        fill(91, 51, 49, 20)
        rect(0, 0 , width, height)
        fill(255)
        trueX = mouseX
        trueY = mouseY
        if mouseX < 30:
            trueX = 30
        elif mouseX > 570:
            trueX = 570
        if mouseY < 285:
            trueY = 285
        elif mouseY >585:
            trueY = 585
        rect(trueX-30, trueY-15, 60, 30)
        
        #shooting ball
        x_1 = x + vel
        circle1.change(x_1, y_1, 20)
        x += vel 
        if x > random.randint(350,590):
            vel -= 3
        elif x < random.randint(10,250):
            vel = 3
        
        
        
    
        #random shooting
        triangle(280, 0, tamgiac_x, 50, 320, 0)
    
        if x in range(260,340):
            if ball_y < width:
                circle2.change(ball_x,ball_y,20)
                ball_x += 30 - k
                ball_y += 40 + 5
        elif ball_y >= 600 or ball_x >= 600 or ball_x <= 0:
            ball_y = 60
            ball_x = 300
            k = random.randint(0,80)
    
        circle2.change(ball_x, ball_y,20)
        println(vel)
        if ball_x - (trueX - 30) in range(-30,30) and ball_y - (trueY-15) in range(-30,30) and valid == True:
            valid = False
        
        

        

        
        

    
    
    
    
