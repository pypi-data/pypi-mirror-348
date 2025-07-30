from oli_ai import oli_ai
from oli_ai.utils import *
from oli_ai.maze import *


queue = Queue()

queue.put("Anna")
queue.put("Luigi")
queue.put("Mario")

print(queue.pop())
print(queue.pop())


queue = Stack()

queue.put("Anna")
queue.put("Luigi")
queue.put("Mario")

print(queue.pop())
print(queue.pop())



print(random_maze(10, 5))



M = random_maze(20, 20)
plot_maze(M)

a = search_animated(M, Queue())

a

print(a)
print("----")
