import matplotlib.pyplot as plt

def plot(title, labelx, labely, data):
    
    plt.figure(figsize=(8,5))
    plt.title(title)
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.plot(data)
    plt.show()

