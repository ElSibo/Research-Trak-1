from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

We start from the solution of the exercise 2
Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py exercise3.py

"""


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and -90< token.rot_y <90 :
            dist=token.dist
	    rot_y=token.rot_y
	    color_tok=token.info.marker_type
	    
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y, color_tok
   	
def find_silver():
	dist=2
	for sil in R.see():
 	
 		if sil.dist<1.3 and sil.info.marker_type and -90<sil.rot_y <90 :
 			dist=sil.dist
 			rot_y=sil.rot_y
 			color=sil.info.marker_type
 	if dist < 2:		
 		return dist,rot_y,color
 	else:
 		return find_token()
 		
def stability():
	a=0
	b=0
	for t in R.see():
		if t.dist < 1.5 and -90< t.rot_y <90 :
			if t.rot_y<0:
				a=a+1
			else:
				b=b+1
	print("Number of golden token in my Right: ",a," Number of golden token in my Left: ",b)
	if a<b:
		print("I am turning on my left") 
		return (10*(a-b)),0.5
	elif a>b:
		print("I am turning on my right")
		return (10*(a-b)),0.5
	else:
		return 0,0
def take_silver():

	while 1:
			
		a,b,c = find_silver()
			
		if a<d_th and c=='silver-token' :
			print("I found the silver oken.")
			gr_dr = R.grab()
			print("token was grabed ?   Answer: ",gr_dr)
			turn(-15,8.8)
			
			gr_dr=R.release()
			print("token was dropped ?   Answer: ",gr_dr)
			turn(-15,8.8)
			print("I am continue on my road")
			
			break
			
		elif -a_th <= b <= a_th and c=='silver-token' : # if the robot is well aligned with the token, we go forward
			print("Ah, here we are!.")
			drive(20, 1)
		elif b < -a_th and c == 'silver-token': # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...",find_silver())
			turn(-2, 0.5)
		elif b > a_th and c == 'silver-token' :
			print("Right a bit...",find_silver())
			turn(+2, 0.5)
   	
   
while 1:

	
	print("I see : ",find_silver())
	
	drive(150,0.5)
	
	
	
	a,b,c = find_silver()
	
	
	if c =='silver-token':
		take_silver()
	else:
		
		x,y=stability()
		turn(x,y)
	

