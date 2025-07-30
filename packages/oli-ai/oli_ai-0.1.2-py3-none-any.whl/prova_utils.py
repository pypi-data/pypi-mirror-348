from oli_ai import oli_ai
from oli_ai.utils import *
from oli_ai.maze import *


queue = Queue()

queue.push("Mario")
queue.push("Luigi")
queue.push("Anna")

print(queue.pop())
print(queue.pop())


print(random_maze(10, 5))