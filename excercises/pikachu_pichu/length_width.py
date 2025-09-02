import numpy as np
import matplotlib.pyplot as plt
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(BASE_DIR, "pika_data")

# function to read in the .txt files
def read_txt_to_array(path):
    data = []
    with open(path, "r") as f:
        lines = f.readlines()
    for line in lines[1:]: 
        line = line.strip()
        if not line:
            continue
        parts = line.replace("(", "").replace(")", "").split(",")
        try:
            x = float(parts[0])
            y = float(parts[1])
            data.append([x, y])
        except ValueError:
            continue
    return np.array(data, dtype=float)

# saving the txt to arrays
pichu_array = read_txt_to_array(os.path. join(data_dir,"pichu.txt"))
pikachu_array = read_txt_to_array(os.path.join(data_dir, "pikachu.txt"))

print("Pichu shape:", pichu_array.shape)
print("Pikachu shape:", pikachu_array.shape)


# scatter plot over height and width
# [:,0] and [:,1] splits 2D the array into two 1D arrays
# by taking the first column(width) and placing it into x 
# and the second (length) into y
plt.scatter(pichu_array[:,0], pichu_array[:,1], label="Pichu", color="yellow", marker="o")
plt.scatter(pikachu_array[:,0], pikachu_array[:,1], label="Pikachu", color="orange", marker="^")
plt.xlabel("Width (cm)")
plt.ylabel("Height (cm)")
plt.legend();

# read in the test data
with open(os.path. join(data_dir,"test_points.txt")) as f:
    line = f.readline()

replace = line.replace("(","").replace(")", "").split(",")

test_array = np.array(replace, dtype = float).reshape(-1, 2)
print(test_array)

# stacking the data points together into one training set
# creates a label array where 0 = pichu and 1 = pikachu
X_train = np.vstack([pichu_array, pikachu_array])
y_train = np.array([0]*len(pichu_array) + [1]*len(pikachu_array))

# calculate the difference between each training point and test point
# by using broadcasting I get a difference matrix of shape(N, M, 2)
# calculate the distance with np.linalg.norm(Euclidean distance) for each difference
# by axis = 2 to calculate the distance over width and height, not the whole matrix
diffs = X_train[:, None,:] - test_array[None,: ,:]
dists = np.linalg.norm(diffs, axis=2)

print(f"{dists}")

# sort the columns with np.argsort, the distance to a certain test point
# it returns an array with the same shape with index in ascending order
k = 3
nearest_idx = np.argsort(dists, axis = 0)[:k, :]

print(nearest_idx)



# save the predictions in an array
# bincount calclulates how many times teach label appears among the neighbors

labels = np.array(["Pichu", "Pikachu"])
for point, j in zip(test_array, range(test_array.shape[0])):
    neighb = y_train[nearest_idx[:, j]]
    pred = np.argmax(np.bincount(neighb, minlength=2))
    width, height = point
    print(f"Sample with (width, height) : ({width:.1f}, {height:.1f}) classified as {labels[pred]}")


# part 2
while True:
    try:

        user_input = input("Please enter a test point, width and height: ")

        # empty input
        if not user_input.strip():
            print("Please enter a valid number")
            continue

        # split the comma
        parts = user_input.split(",")
        if len(parts) != 2:
            print("Please enter two numbers separated by a comma")
            continue

        # convert to float
        width = float(parts[0])
        height = float(parts[1])

        # check for negative numbers
        if width < 0 or height < 0:
            print("Width and height must be non-negative")
            continue
        
        # put the data in an array
        x_new = np.array([width, height])
        diffs = X_train - x_new
        dists = np.linalg.norm(diffs, axis=1)

        k = 3
        nearest_idx = np.argsort(dists)[:k]

        neighb = y_train[nearest_idx]
        pred = np.argmax(np.bincount(neighb, minlength=2))

        labels = np.array(["Pichu", "Pikachu"])
        print(f"The input gave: {labels[pred]}")
        break

    except ValueError:
        print("Please enter valid numbers, e.g. 20,30")
