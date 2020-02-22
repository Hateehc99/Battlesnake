import json
import os
import random
import bottle
import platform

from api import ping_response, start_response, move_response, end_response

lastMove = ''

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#50DEDA"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
    
    global lastMove
    
    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data, indent=2))

    directions = ['up', 'down', 'left', 'right']
    
    #Terminology
    # - data['board']['width']     how you tell max or least x
    # - data['board']['length']     how you tell max or least y
    
    
    #direction = random.choice(directions)
    #direction='right'
    
    
    
    #Ideas for moving toward food
    
    head_x = data['you']['body'][0]['x']
    head_y = data['you']['body'][0]['y']
    food_x = data['board']['food'][0]['x']
    food_y = data['board']['food'][0]['y']
    
    if health < 26:
        #this would have it doing any other code first untill it was low health
        
        if head_x > food_x:
            direction ='left'            
        elif head_x < food_x:
            direction ='right'
            #this makes the x cordinate align with the food
        
        elif head_y > food_y:
            direction ='up'
        elif head_y < food_y:
            direction ='down'
            #this makes the y cordinate align with the food
    
    
        #If head_x > food_x then *move left*            
        #If head_x < food_x then *move right*
            #If *Head x_location = food x_location = 0* then *don't change x_location*    - don't need
        
        #If head_y > food_y then *move up*
        #If head_y < food_y then *move down*
            #If *Head y_location = food y_location = 0* then *don't change y_location*    - don't need
    
   
    
    
    #Atempts to make the snake go around the outside of the board
    
    #Seems like it might work with proper terminology
    
    #if *snake's head location* ==   y_loction=*least*  then  *go*   'right'  unless    x_loction=*max*    *then go*   direction='down'
    #if *snake's head location* ==   x_loction=*max*  then  *go*   'down'  unless    x_loction=*max* y_loction=*max*   *then go*   direction='left'
    #if *snake's head location* ==   y_loction=*max*  then   *go*   'left'  unless    x_loction=*least*    *then go*   direction='up' 
    #if *snake's head location* ==   x_loction=*least*  then  *go*   'up'  unless    x_loction=*lest* y_loction=*least*   *then go*   direction='right'
    
    #This is just a direction I chose at random to start going
    
    #direction = 'right'
    
    
    
    
    
    
    #This makes the snake go in circles
    
    if lastMove=='':
        direction='right'
    if lastMove=='right':
        direction='down'
    if lastMove=='down':
        direction='left'
    if lastMove=='left':
        direction='up'
    if lastMove=='up':
        direction='right'
        
    lastMove=direction
    
    
    
    return move_response(direction)

    

@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data, indent=2))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    s = platform.system() # s now contains the name of your operating system
    if s == 'Windows' or s == 'Darwin': # if you’re running on Windows or Mac
        bottle.run(
            application,
            host=os.getenv('IP', '0.0.0.0'),
            port=os.getenv('PORT', '8080'),
            debug=os.getenv('DEBUG', True),
            #server='paste'
            server='tornado'
        )
    else: # otherwise serve on port 80
        bottle.run(
            application,
            host=os.getenv('IP', '0.0.0.0'),
            port=os.getenv('PORT', '80'),
            debug=os.getenv('DEBUG', True)
        )

