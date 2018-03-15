import random
import os
import time

def nothing():
  while True:
    yield 0

def rand_gen():
  while True:
    yield random.choice([0, 1])  	

class History:
  def __init__(self):
    self.states = []

  def push(self, n):
    for i,state in enumerate(reversed(self.states)):
      if state == n:
        return i
    self.states.append(n)
    return -1

  def reset(self):
    self.states = []

class Life:
  def __init__(self, w=10, h=10, fill_by=nothing()):
    self.field = {}
    self.w, self.h = w, h
    self.fill_field(fill_by)
    
  def fill_field(self, fill_by=nothing()):
    for x in range(self.w):
      for y in range(self.h):
        self.field[(x,y)] = next(fill_by)
		
  def __getitem__(self, position):
    if position not in self.field:
      return 0
    return self.field[position]

  def __setitem__(self, position, value):
    self.field[position] = value

  def next_step(self):
    t = {}
    for x in range(self.w):
      for y in range(self.h):
        n = self.calculate_neighbours(x, y)
        if n > 3 or n < 2:
          t[(x,y)] = 0
        elif n == 3:
          t[(x,y)] = 1
        else:
          t[(x,y)] = self[x,y]
    self.field = t

  def calculate_neighbours(self, x, y):
    neighbours = 0
    for i in range(x-1,x+2):
      for j in range(y-1,y+2):
        if i == x and j == y:
          continue
        neighbours += self[i,j]
    return neighbours

class InfiniteLife(Life):
  def __getitem__(self, position):
    x,y = position
    nx = abs(x) % self.w
    ny = abs(y) % self.h
    if x < 0:
      nx = self.w - nx
    if y < 0:
      ny = self.h - ny
    return self.field[(nx, ny)]

class CycledLife(InfiniteLife):
  def __init__(self, *args, **kargs):
    self.history = History()
    InfiniteLife.__init__(self, *args, **kargs)
    self.cycled_life = InfiniteLife(self.w, self.h)
    self.history.push(self.field)
  def next_step(self):
    InfiniteLife.next_step(self)
    self.cycled_life.next_step()
    n = self.history.push(self.field)
    if n >= 0:
      self.cycled_life = InfiniteLife(self.w, self.h)
      self.cycled_life.field = self.field.copy()
      self.fill_field(rand_gen())

life = CycledLife(fill_by=rand_gen())

while True:
  os.system("cls")
  print("+" + life.w*2*"-" + "+" + life.w*2*"-" + "+")
  for y in range(life.h):
    print("|", end="")
    for x in range(life.w):
      print("[]" if life.cycled_life[x, y] == 1 else "  ", end="")
    print("|", end="")
    for x in range(life.w):
      print("[]" if life[x, y] == 1 else "  ", end="")
    print("|")
  print("+" + life.w*2*"-" + "+" + life.w*2*"-" + "+")
  
  time.sleep(0.1)
  life.next_step()
