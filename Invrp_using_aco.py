import fileinput
import math
import sys

sys.stdin=open('input.txt',"r")
sys.stdout=open('output.txt',"w")


customer_number = int(input())

customer = []*customer_number
each_customer = []*6
for i in range(customer_number):
    s=input()
    each_customer.append(s.split())
    # each_customer[0] = int(input())
    # each_customer[1] = int(input())
    # each_customer[2] = int(input())
    # each_customer[3] = int(input())
    # each_customer[4] = int(input())
    d_t = []
    for j in range(customer_number):
        x=input()
        d_t=x.split()
    each_customer.append(d_t)
    customer.append(each_customer)

print(customer)


def distance_between_two_Node(x1: int, y1: int, x2: int, y2: int) -> int:
    return math.sqrt(math.pow((x2-x1), 2)+pow(y2-y1), 2)


"""Calculate the distance between each node"""

distance_Array = []
for i in range(customer_number+1):
    temp = []
    for j in range(customer_number+1):
        temp.append(distance_between_two_Node())
