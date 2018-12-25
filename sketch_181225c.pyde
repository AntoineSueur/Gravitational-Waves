import math

funberOfPArticles = 150
particles = [[0.0]*funberOfPArticles for _ in range(funberOfPArticles)]


zoom = 800.0/funberOfPArticles

planet_size = 30.0
a = 75.0
m1 = 1e9
m2 = 1e9
v = 20
theta1 = 0
theta2 = PI
x1, y1, x2, y2 = 100,300, 500, 300
max_wave_value = 80.
img = loadImage("star.jpg")
G = 6.67e-11

eyeX, eyeY, eyeZ = 0,0,0

def setup():    
    size(800, 800,P3D)
    #fullScreen(P3D)
    smooth(8)

def keyPressed():
    global eyeX, eyeY, eyeZ
    if (keyCode == UP):    
        eyeZ += 50
    elif (keyCode == DOWN):
        eyeZ -= 50
    elif (keyCode == LEFT):
        eyeY += 50
    elif (keyCode == RIGHT):
        eyeY -= 50

def reset():
    global x1, y1, x2, y2, theta1, theta2, a, history
    a = 50.0
    m1 = 1e9
    m2 = 1e9
    v = 20
    theta1 = 0
    theta2 = math.pi
    x1, y1, x2, y2 = 100,300, 500, 300
    particles = [[0.0]*funberOfPArticles for _ in range(funberOfPArticles)]


def calculate_gravity():
    global particles
    for i in range(funberOfPArticles):     
        for j in range(funberOfPArticles):
            particle_x, particle_y = zoom*i - width/2, zoom*j - height/2
            dist1 = dist(x1,y1, particle_x, particle_y)
            dist2 = dist(x2,y2, particle_x, particle_y)
            if( dist1 < planet_size/10 or dist2 < planet_size/10):
                continue
            local_gravity = G*m1/(dist1**2) + G*m2/(dist2**2)
            particles[i][j] = min(local_gravity/(1e-7),20)

    
def drawMesh():
    
    strokeWeight(1)
    stroke(50,50,50)    
    for x in range(funberOfPArticles):
        beginShape()
        for y in range(funberOfPArticles):     
            blue_color = 255*(4*particles[x][y]/max_wave_value)
            if(particles[x][y] > 1.0):
                fill(0,0,150)
                stroke(28,44,blue_color)            
            else:
                stroke(50,50,50)  
            vertex( x*zoom, y*zoom, particles[x][y] )
        endShape()
    for y in range(funberOfPArticles):
        beginShape()
        for x in range(funberOfPArticles):
            blue_color = 255*(4*particles[x][y]/max_wave_value)
            if(particles[x][y] > 1.0):
                fill(0,0,150)
                stroke(28,44,blue_color)            
            else:
                stroke(50,50,50)    
            vertex( x*zoom, y*zoom, particles[x][y] )
        endShape()
  
def calculate_waves():
            
    global particles
    spiral_radius = 16*a
    scale_factor = 500.0
    rotation_factor = a/1e3
    n_points = 7000
    angle_offset = 0.6*PI
    
    particles = [[0.0]*funberOfPArticles for _ in range(funberOfPArticles)]
    
    for i in range(n_points):
        # double spiral
        i /= scale_factor        
        u,v = spiral_radius*i*cos(theta1 + angle_offset  - i/rotation_factor), spiral_radius*i*sin(theta1 + angle_offset - i/rotation_factor)
        if(abs(u) < width/2 and abs(v) < height/2):
            x, y = int((u+ width/2)/zoom), int((v+ height/2)/zoom)
            if(x*y!=0.0 and x!=funberOfPArticles -1 and y!=funberOfPArticles -1):
                particles[x][y] = max_wave_value
                if(dist(u,v,0,0) < a):
                    particles[x][y] = 0.0
        u,v = spiral_radius*i*cos(theta1 + angle_offset +  PI - i/rotation_factor), spiral_radius*i*sin(theta1 + angle_offset + PI - i/rotation_factor)
        if(abs(u) < width/2 and abs(v) < height/2):
            x, y = int((u+ width/2)/zoom), int((v+ height/2)/zoom)
            if(x*y!=0 and x!=funberOfPArticles -1 and y!=funberOfPArticles -1):
                particles[x][y] = max_wave_value 
                if(dist(u,v,0,0) < a):
                    particles[x][y] = 0.0
        

    new_particles = [[0.0]*funberOfPArticles for _ in range(funberOfPArticles)]
    for i in range(3):
        for x in range(1, funberOfPArticles - 1):  
            for y in range(1, funberOfPArticles - 1):  
                force = 0.0
                
                force += particles[x-1][y-1] - particles[x][y];
                force += particles[x-1][y] - particles[x][y];
                force += particles[x-1][y+1] - particles[x][y];  
                
                force += particles[x+1][y-1] - particles[x][y];
                force += particles[x+1][y] - particles[x][y];
                force += particles[x+1][y+1] - particles[x][y];
                
                force += particles[x][y-1] - particles[x][y];
                force += particles[x][y+1] - particles[x][y];
                force -= particles[x][y+1] / 8;
                
                new_particles[x][y] = min(particles[x][y] + force/10.0, 100)
        particles = new_particles
    
            
def draw():
    global x1, y1, x2, y2, theta1, theta2, a
    background(0)
    fill(0)
    #camera()
    #camera(width, height, width/2, 0,0,0,0,0,-1)
    camera(eyeX, eyeY, width + eyeZ, width/2, height/2,0,0,0,-1)
    
    drawMesh()
    
    translate(width/2, height/2);
    
    w = v/a
    theta1 += w
    theta2 += w
    a -= 0.5
    x1, y1 = a*cos(theta1), a*sin(theta1)
    x2, y2 = a*cos(theta2), a*sin(theta2)

    if(dist(x1, y1, x2, y2) < planet_size/2.0):
        reset()
    
    calculate_waves()
    #calculate_gravity()
    
    fill(0)
    stroke(169)
    lights()
    translate(x1, y1, 0)
    sphere(planet_size/2)
    
    translate(-x1, -y1, 0)
    translate(x2, y2, 0)

    sphere(planet_size/2)
    
    
    #saveFrame('./frames/####.png')

        
    
  
