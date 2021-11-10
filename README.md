Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

## Exercise
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

I am proposing you three exercises, with an increasing level of difficulty.
The instruction for the three exercises can be found inside the .py files (exercise1.py, exercise2.py, exercise3.py).

When done, you can run the program with:

```bash
$ python run.py exercise1.py
```

You have also the solutions of the exercises (folder solutions)

```bash
$ python run.py solutions/exercise1_solution.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/





ABSTRACT AND INTRUDUCTION:
================================

The target of this assignment is to write a python script capable of running the robot on a circuit in anticlockwise, trying to avoid golden toke, who represent the border of the circuit, and when encountered silver token it must be turn them behind him and continue in his way. 
For do this we must be lean to use R.see(), R.grab() ,R.release() and we have used the function who  was defined prof. like  turn(), drive(), find_token() with some modifications in additional we are added a new function.
This is the first assignment of Research Track I and for beginning the prof. Carmine Tommaso Recchiuto gave us the scripts from which can starts.

MATERIALS AND METODS:
================================

In the top of the script have  the minimum distant (d_th=0.4) and the minimum angle (a_th=2) who can permitted to take the silver token.
The first think we did is to modify the find_token() function so that it can also return the type of token and to see only the token who have at +- 90°. 
After that we did move the robot with the drive() function ( we are set the function on 150 of velocity and 0.5 second)  in a while loop.
In side the loop we did use the find_silver() function and  checked  if the robot see a golden or silver token, if it see a silver one them it must to use toke_silver() function otherwise, that means that have see the golden one, so it use  a stability() function to return the velocity and the time to enter in the turn() function and restart in the while loop.
Now explain the function who we have added, we are defined find_silver() it’s similar al the find_token() function but in this one the robot don’t see the closest token if there is a silver token at a distance less than 1.3 this function use the take_token(), then there is a take_silver() function which has a while loop who make robot walk up and align to the silver token; when the robot arrive at the toke it grab it and make it behind him ta the and hi continue in his way.
The last function is stability() it a function with has a radios of 2 (+-90°)  and cont the gold token who have at the left and right then if has more token at the right so the robot must be turn to the left and the same thing at reverse, this function return different velocity depends how many token see, the time it always the same.


PSEUDOCODE:
================================


We are fixed the minimum distance(d_th) and rotation( a_th) to take the token

# Function looking for tokens:				   find_token()

	we fix the distant at 100 dist =100
	we make a circle for to see al token with R.see()
	if we fond token how has a distant less than dist and the rotation si less than +-90°
	 	we change the dist to the new distance and memories the  distance the rotation 				and the tape of marker 
	at the end of the cycle  for we have the distance, rotation and type of token of the more 			closest token

	If dist it equal at 100 return -1,-1,-1 it mens there is not token closes than 100
	Else return the data of the closest token
# Function looking for silver token: 			find_silver()

	we fix dist at 2  
	we make a cycle for to see al token in R.see()
	if  distance of token is closest than 1.3 and the token is silver and the rotation is less than 		+-90°
		save the data of distance, rotation and type of marker
	if dist is less than 2 
		return data saved 
	else 
		return data of find_token()


# Function of the stability of the robot :   		stability()

we fix a equal 0 and b equal 0
we make a cycle for to see the all token in R.see()

		if the token who see have a distance less than 1.5 and the rotation is between 	+-90°
      
      if the rotation is less than 0 ( right side of the robot)
			  increases a by 1
			else 				( left side of the robot)
			  increases b by 1

At the end we have the number of the token in the left and in the right side of the robot starting to +-90°
Print the Message

  If a it less than b
  
	  print the message and
    return for the velocity 10 multiply the difference between a and b (the different is negative so the turn will be turned in the left side) and for the time 0.5
  
  If a greater than b
  
	  print the message and 
    return for the velocity 10 multiply the difference between a and b ( the different is positive so the turn will be turned in the right side) and for the time 0.5
    
  else
  
    return 0,0 ( the robot same token in left and right it means it parallel and cantered ) 

# Function how the silver token: 			take_silver():
  We make a while loop who finish when the robot will be continue in his road 
  
  we asked the data of the silver token at the find_silver() and memorized at a b c
  
    if the distance (a) is less than a_th and the toke is silver (we are add this think because in same cases we are still in the loop and the token is near a gold token)
    
     print the message grab() the token print other message turn release print the message turn print message and
     break the loop ( the robot has make the token behind him and hi is ready to continue)
    
    else if the rotation is between +- a_th but the distance is greater than d_th
     print the message and we went to the silver token
    
    else if rotation is less than-a_th 
     print the message and turn left  to alined to the token
    
    else if rotation is greater than  +a_th
     print the message and turn right to alined to the token
# in the main():

We are make the while loop that’s never ends
we print what token see 
the robot go on with 150 to velocity at 0.5 second
the robot take data to the near token from find_silver()

  if is an silver token:
  
    we use the take_silver() function to take it behind him
    
  else: 
  
    we take the velocity (x) and the time (y) from stability() function and
    put them in the turn() function to turn the robot for  alined 
 
 When we need to stop the robot we stoped from the terminal. 

