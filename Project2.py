import simpy
import random

#Daniel Walpole 
#Project 2
#System Simulation 
#Assignment is to make a simulation of a fast food resturant with 1 ordering window, 1 pickup window, and 1 payment window
#The Pickup line has 7 spots to include the pickup window and payment window
#The program will find the average time of orders that are complete

MeanCookTime = 5.0 
AR = 1 
Time = 60 
cars = 0 
carsServed = 0 
timesOfService = [] 

class FastFood(object):
    def __init__(self, env):
        self.env = env
        self.line1 = simpy.Resource(env, 1)
        self.pickupWindowLine = simpy.Resource(env, 4)
        self.payWindow = simpy.Resource(env, 1)
        self.payWindowLine = simpy.Resource(env, 2)
        self.pickupWindow = simpy.Resource(env, 1)
    def CookFood(self):
        return random.expovariate(1.0 / MeanCookTime)

def Customer(env, window, name):
    global carsServed
    global timesOfService
    if(len(window.line1.queue) < 5):
        startTime = env.now
        print('Customer %s arrived at {}'.format(startTime) % name)
        order = window.line1.request()
        yield order
        print('Customer %s has started ordering food at {}'.format(env.now) % name)
        yield env.timeout((random.lognormvariate(0.6722166, 0.38146434466)))
        #mean: 40.33333333, standard deviation: 22.88786068
        print('Customer %s has  finished ordering for food at {}'.format(env.now) % name)
        startOrder = env.now
        cookFood = window.CookFood()
        req = window.payWindowLine.request()
        yield req
        window.line1.release(order)
        rq = window.payWindow.request()
        yield rq
        window.payWindowLine.release(req)
        print('Customer %s started paying for food at {}'.format(env.now) % name)
        yield env.timeout((random.lognormvariate(0.498989899, 0.204121567833)))
        #mean: 29.93939394 in seconds, standard devation: 12.24729407 in seconds
        print('Customer %s has payed for food at {}'.format(env.now) % name)
        rqq = window.pickupWindowLine.request()
        yield rqq
        window.payWindow.release(rq)
        rqqq = window.pickupWindow.request()
        yield rqqq
        window.pickupWindowLine.release(rqq)
        atWindow = env.now
        #if atWindow < (cookFood + startOrder):
        #    yield env.timeout(abs(atWindow-cookFood+startOrder))
        #yield env.timeout(random.expovariate(1.0) * MeanPickupTime)
        print('Customer %s has started to pick up food at {}'.format(env.now) % name)
        yield env.timeout(random.lognormvariate(0.430006791166, 0.16948815833))
        #mean: 25.80040747 in seconds, standard devation: 10.1692895 in seconds
        print('Customer %s has picked up food at {}'.format(env.now) % name)
        window.pickupWindow.release(rqqq)
        endtime = env.now
        carsServed += 1
        print('Customer %s departed at {}'.format(endtime) % name)
        timesOfService.append(endtime-startTime)

def Start(env, AR):
    global cars
    global carsServed
    stuff = FastFood(env)
    while True:
        name = cars + 1
        cars += 1
        yield env.timeout(random.lognormvariate(0.8919192, 0.976957803))
        #mean: 53.51515152 in seconds, standard deviation: 58.61746818 in seconds
        env.process(Customer(env, stuff, name))

random.seed(123456)
env = simpy.Environment()
env.process(Start(env, AR))
env.run(until=Time)

print('%s cars seen' % cars)
print('%s cars got their food' % carsServed)
print(timesOfService)
sum = 0.0
for i in range(len(timesOfService)):
    sum += timesOfService[i]
print('The average time is %s' % (sum/len(timesOfService)))