#
#Name: Tristan McGinnis
#Assignment: Programming Assignment 1
#Title: Dynamic Movement
#Class: 330-01
#
import numpy as np
import math as math

#Steering function simply used to store both a vector and a scalar in one object
class Steering:
   def __init__(self, linear, angular):
      self.linear = linear
      self.angular = angular

#Gets vector magnitude
#Source: https://www.geeksforgeeks.org/how-to-get-the-magnitude-of-a-vector-in-numpy/
def magnitude(vector): 
    return math.sqrt(sum(pow(element, 2) for element in vector))

#Character class, stores all information for each character
class Character:
   #self, id, behavior, posX, posZ, velX, velZ, orientation, maxVel, maxAccel, target, arrivalRadius, slowRadius, time2target
   def __init__(self, id, behavior, posX, posZ, velX, velZ, orientation, maxVel, maxLin, target, arriveRadius, slowRadius, time2target):
      self.id = id #int number
      self.behavior = behavior #1=Continue, 6=Seek, 7=Flee, 8=Arrive
      #behavior is analogous to "steer" in the R code

      position_input = [posX, posZ]
      self.pos = np.array(position_input)

      velocity_input = [velX, velZ]
      self.vel = np.array(velocity_input)
      self.maxVel = maxVel

      linear_input = [0, 0]
      self.accel = np.array(linear_input)
      self.maxLin = maxLin

      self.angular = 0
      self.maxAngular = 0

      self.orientation = orientation #radians
      self.rotation = 0
      self.maxRotation = 0

      self.target = target
      #print(f'Target is: {target}')

      self.collided = False #Currently remains false

      self.arriveTime = time2target
      self.slowTime = .05 #Hardcoded to 0.5 because I think that's what the lectures recommended
      self.arriveRadius = arriveRadius
      self.slowRadius = slowRadius
      self.time2target = time2target

   #Function of class character so you can just pass self to access attributes
   #Computes all value changes upon updates
   def getSteering(self):
      result = Steering([0,0], 0)

      if self.behavior == 1: #Continue
         result = Steering(self.accel, self.angular)

         return result
      if self.behavior == 6: #Seek

         result.linear = self.target.pos - self.pos
         result.angular = 0

         linearArray = result.linear
         linearArray = np.array(linearArray)
      
         #print(f'char to targe pos: {self.pos} to {self.target.pos} is {result.linear}')
         result.linear = result.linear/np.linalg.norm(linearArray)
         result.linear = result.linear * self.maxLin
         
         return result
      if self.behavior == 7: #Flee

         result.linear = self.pos - self.target.pos
         result.angular = 0

         linearArray = result.linear
         linearArray = np.array(linearArray)
      
         #print(f'char to targe pos: {self.pos} to {self.target.pos} is {result.linear}')
         result.linear = result.linear/np.linalg.norm(linearArray)
         result.linear = result.linear * self.maxLin
         
         return result
      if self.behavior == 8: #Arrive
         direction = self.target.pos - self.pos
         distance = magnitude(np.array(direction))

         if distance < self.arriveRadius:
            arriveSpeed = 0
         elif distance > self.slowRadius:
            arriveSpeed = self.maxVel
         else:
            arriveSpeed = self.maxVel * distance / self.slowTime


         arriveSpeed = ((np.array(direction))/np.linalg.norm(direction)) * arriveSpeed
         result.linear = arriveSpeed - self.vel
         result.linear = result.linear / self.arriveTime

         if magnitude(result.linear) > self.maxLin:
            result.linear = result.linear/np.linalg.norm(result.linear)
            result.linear = result.linear * self.maxLin

         return result
      else:
         pass

   #Updates values for characters based on those received from it's steering behavior
   #This is also a function of the Character class in order to access all attributes simply by passing self
   def update(self, delta_time): #delta_time should be 0.5 for half second time steps
      self.pos = self.pos + (self.vel * delta_time) #Might just seperate into X and Z calls
      self.orientation = self.orientation + (self.rotation * delta_time)

      self.orientation = self.orientation % (2*np.pi)

      steering = self.getSteering()

      self.vel = self.vel + (steering.linear * delta_time)
      self.rotation = self.rotation + (steering.angular * delta_time)

      self.accel = steering.linear
      self.angular = steering.angular  


      #Checks for breaching maximums
      if abs(magnitude(self.vel)) > self.maxVel:
         print(f'{self.id} surpassed max Velocity at {magnitude(self.vel)}, max: {self.maxVel}')
         self.vel = self.maxVel * self.vel/np.linalg.norm(self.vel)

      if abs(magnitude(self.accel)) > self.maxLin:
         print(f'{self.id} surpassed max Linear Accel at {magnitude(self.accel)}, max: {self.maxLin}')
         self.accel = self.maxLin * self.accel/np.linalg.norm(self.accel)
      
      if abs(self.rotation) > self.maxRotation:
         print(f'{self.id} surpassed max Rotation at {magnitude(self.rotation)}, max: {self.maxRotation}')
         self.rotation = self.maxRotation * self.rotation/np.linalg.norm(self.rotation)

      if abs(self.angular) > self.maxAngular:
         print(f'{self.id} surpassed max Angular Vel at {magnitude(self.angular)}, max: {self.maxAngular}')
         self.angular = self.maxAngular * self.angular/np.linalg.norm(self.angular)

#Parameters for the run
delta_time = 0.5
Time = -delta_time
stop_time = 50

#self, id, behavior, posX, posZ, velX, velZ, orientation, maxVel, maxAccel, target, arriveRadius, slowRadius, time2target
character1 = Character(2601, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
character2 = Character(2602, 7, -30, -50, 2, 7, (np.pi)/4.0, 8, 1.5, character1, 0,0, 0)

#I'm unsure why, at this time, character3's trajectory around target wraps so much tighter than the desired
character3 = Character(2603, 6, -50, 40, 0, 8, (3*np.pi)/2.0, 8, 2, character1, 0, 0, 0)
character4 = Character(2604, 8, 50, 75, -9, 4, np.pi, 10, 2, character1, 4, 32, 1)
characters = [character1, character2, character3, character4]

with open("outputFile.txt", "w") as outFile:
   while (Time < stop_time):
      Time += delta_time
      for c in characters:
         outFile.write(f'{Time}, {c.id}, {c.pos[0]}, {c.pos[1]}, {c.vel[0]}, {c.vel[1]}, {c.accel[0]}, {c.accel[1]}, {c.orientation}, {c.behavior}, {c.collided} \n')
         print(f'{Time}, {c.id}, {c.pos[0]}, {c.pos[1]}, {c.vel[0]}, {c.vel[1]}, {c.accel[0]}, {c.accel[1]}, {c.orientation}, {c.behavior}, {c.collided}')
         c.update(delta_time)   
