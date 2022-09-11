import matplotlib.pyplot as plt
import numpy as np
from aco_imp import track_min_distance,gen_number

generation_array =[]
for i in range(1,gen_number+1):
    generation_array.append(i)

# plt.rcParams["figure.figsize"] = [7.50, 3.50]
# plt.rcParams["figure.autolayout"] = True

# print(track_min_distance)
# print(generation_array)

x=np.array(track_min_distance)
y=np.array(generation_array)

plt.title("Change of Minimum distance - Iteration")
plt.xlabel("Number of Iteration")
plt.ylabel("Minimum Distance")
plt.plot(y,x,color="blue")
plt.savefig("output.png")