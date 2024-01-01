import simplegui
import random
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_line_width = 1
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [-1, -1]  # pixels per tick
time = 0
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel, paddle2_vel = 0, 0
score1, score2 = 0, 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel[1] = - random.randrange(1, 3)
    if direction == RIGHT:
        ball_vel[0] = (random.randrange(2, 4)) 
        #pass
    if direction == LEFT:
        ball_vel[0] = - (random.randrange(2, 4))
        #pass
             
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1, score2 = 0, 0
    spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel  
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
     
    # hit the top or bottom
    if (ball_pos[1] + BALL_RADIUS + ball_line_width >= HEIGHT) or \
    (ball_pos[1] - BALL_RADIUS - ball_line_width <= 0):
        ball_vel[1] = - ball_vel[1]
    
    
    # update ball
    ball_pos[0] +=  ball_vel[0]
    ball_pos[1] +=  ball_vel[1]   
    
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, ball_line_width, 'White', 'White')
    # update paddle's vertical position, keep paddle on the screen
    
    # draw paddles
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT and \
    paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT and \
    paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
        #print paddle2_pos - HALF_PAD_HEIGHT
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], \
                         [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], \
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], \
                         [0, paddle1_pos + HALF_PAD_HEIGHT]], 1, 'White', 'White')
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], \
                         [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], \
                         [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], \
                         [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]], 1, 'White', 'White')
    # determine whether paddle and ball collide    
    # hit the gutters
    if (ball_pos[0] + BALL_RADIUS + ball_line_width >= WIDTH - PAD_WIDTH):
        # hit the paddle2
        if ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT and \
        ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = - 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score1 += 1
            spawn_ball(LEFT)
    if (ball_pos[0] - BALL_RADIUS - ball_line_width <= PAD_WIDTH):
        # hit the paddle1
        if ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT and \
        ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = - 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 += 1
            spawn_ball(RIGHT)
    #print ball_vel[0]
    # draw scores
    canvas.draw_text(str(score1), (WIDTH/4, HEIGHT/4), 50, 'White')
    canvas.draw_text(str(score2), (WIDTH*3/4, HEIGHT/4), 50, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 4
    # palyer 1
    if key == simplegui.KEY_MAP["w"]:            
        paddle1_vel -= vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += vel
    if key == simplegui.KEY_MAP["w"] and key == simplegui.KEY_MAP["s"]:
        pass
    
    # player 2
    if key == simplegui.KEY_MAP["up"]:            
        paddle2_vel -= vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += vel
    if key == simplegui.KEY_MAP["down"] and key == simplegui.KEY_MAP["up"]:
        pass
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    # palyer 1
    if key == simplegui.KEY_MAP["w"]:            
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["w"] and key == simplegui.KEY_MAP["s"]:
        pass
    
    # player 2
    if key == simplegui.KEY_MAP["up"]:            
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"] and key == simplegui.KEY_MAP["up"]:
        pass
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
new_game = frame.add_button('Restart', new_game, 100)
# start frame
#new_game()
frame.start()
