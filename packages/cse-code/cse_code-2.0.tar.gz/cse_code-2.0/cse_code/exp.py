experiment = {
    3: """
    experiment : 3
    -------------------------------------------------------------
    EX 3

    weather=['Sunny','Sunny','Overcast','Rainy','Rainy','Rainy','Overcast','Sunny','Sunny',
    'Rainy','Sunny','Overcast','Overcast','Rainy']
    temp=['Hot','Hot','Hot','Mild','Cool','Cool','Cool','Mild','Cool','Mild','Mild','Mild','Hot','Mild']
    play=['No','No','Yes','Yes','Yes','No','Yes','No','Yes','Yes','Yes','Yes','Yes','No']

    from sklearn import preprocessing

    le = preprocessing.LabelEncoder()

    weather_encoded=le.fit_transform(weather)
    print (weather_encoded)

    temp_encoded=le.fit_transform(temp)
    label=le.fit_transform(play)
    print ("Temp:",temp_encoded)
    print ("Play:",label)

    features=zip(weather_encoded,temp_encoded)
    features=list(features)
    print (features)


    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()

    model.fit(features,label)

    predicted= model.predict([[2,2]])
    print ("Predicted Value:", predicted)
    """,

    4: """
    experiment : 4
    -------------------------------------------------------------
    EX4

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = {
    'StudyHours': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'ExamScore': [35, 45, 50, 55, 60, 70, 75, 80, 85, 90]
}
data_set = pd.DataFrame(data)

x = data_set.iloc[:, :-1].values
y = data_set.iloc[:, 1].values

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=0)

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x_train, y_train)

y_pred = regressor.predict(x_test)
x_pred = regressor.predict(x_train)

plt.scatter(x_train, y_train, color="green")
plt.plot(x_train, x_pred, color="red")
plt.title("Exam Score vs Study Hours (Training Dataset)")
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.show()

plt.scatter(x_test, y_test, color="blue")
plt.plot(x_train, x_pred, color="red")
plt.title("Exam Score vs Study Hours (Test Dataset)")
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.show()
    """,

    5: """
    experiment : 5
    -------------------------------------------------------------
    import numpy as np

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(x):
        return x * (1 - x)

    inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    expected_output = np.array([[0], [1], [1], [0]])

    epochs = 10000
    lr = 0.1
    inputLayerNeurons, hiddenLayerNeurons, outputLayerNeurons = 2, 2, 1

    hidden_weights = np.random.uniform(size=(inputLayerNeurons, hiddenLayerNeurons))
    hidden_bias = np.random.uniform(size=(1, hiddenLayerNeurons))
    output_weights = np.random.uniform(size=(hiddenLayerNeurons, outputLayerNeurons))
    output_bias = np.random.uniform(size=(1, outputLayerNeurons))

    for _ in range(epochs):
        hidden_layer_activation = np.dot(inputs, hidden_weights) + hidden_bias
        hidden_layer_output = sigmoid(hidden_layer_activation)

        output_layer_activation = np.dot(hidden_layer_output, output_weights) + output_bias
        predicted_output = sigmoid(output_layer_activation)

        error = expected_output - predicted_output
        d_predicted_output = error * sigmoid_derivative(predicted_output)

        error_hidden_layer = d_predicted_output.dot(output_weights.T)
        d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output)

        output_weights += hidden_layer_output.T.dot(d_predicted_output) * lr
        output_bias += np.sum(d_predicted_output, axis=0, keepdims=True) * lr
        hidden_weights += inputs.T.dot(d_hidden_layer) * lr
        hidden_bias += np.sum(d_hidden_layer, axis=0, keepdims=True) * lr

    print("Output from neural network after 10,000 epochs:")
    print(predicted_output)
    """,

    6: """
    experiment : 6
    -------------------------------------------------------------
    EX6

    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score

    data = {'X1': [2, 4, 4, 6, 8], 'X2': [4, 6, 4, 2, 4], 'Class': ['A', 'A', 'B', 'B', 'B']}
    df = pd.DataFrame(data)

    X = df[['X1', 'X2']]
    y = df['Class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    print("\nTest sample:")
    print(X_test.values)

    distances, indices = knn.kneighbors(X_test)

    print("\nTop 3 Nearest Neighbors (with distances and classes):")
    for i, (dists, idxs) in enumerate(zip(distances, indices)):
        print(f"\nTest sample {i+1}: {X_test.iloc[i].values}")
        for rank, (dist, idx) in enumerate(zip(dists, idxs), start=1):
            neighbor_point = X_train.iloc[idx].values
            neighbor_class = y_train.iloc[idx]
            print(f" Rank {rank}: Point={neighbor_point}, Class={neighbor_class}, Distance={dist:.2f}")

        print(f"→ Predicted Class: {y_pred[i]}")
    """,

    7: """
    experiment : 7
    -------------------------------------------------------------
    EX7

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score

    data = {'X1': [2, 4, 4, 6, 8, 7], 'X2': [4, 6, 4, 2, 4, 1], 'Class': ['A', 'A', 'B', 'B', 'B', 'A']}
    df = pd.DataFrame(data)

    X = df[['X1', 'X2']]
    y = df['Class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    svm_model = SVC(kernel='linear')
    svm_model.fit(X_train, y_train)


    y_pred = svm_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    plt.figure(figsize=(6, 4))

    plt.scatter(df[df['Class'] == 'A']['X1'], df[df['Class'] == 'A']['X2'], color='blue', label='Class A', s=100)
    plt.scatter(df[df['Class'] == 'B']['X1'], df[df['Class'] == 'B']['X2'], color='red', label='Class B', s=100)

    xx, yy = np.meshgrid(np.linspace(X['X1'].min()-1, X['X1'].max()+1, 100),
                        np.linspace(X['X2'].min()-1, X['X2'].max()+1, 100))
    Z = svm_model.predict(np.c_[xx.ravel(), yy.ravel()])

    Z_numeric = np.where(Z == 'A', 0, 1)
    Z_numeric = Z_numeric.reshape(xx.shape)

    plt.contourf(xx, yy, Z_numeric, alpha=0.2, cmap="coolwarm")

    plt.title("SVM Decision Boundary")
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.legend()
    plt.show()
    """,

    8: """
    experiment : 8
    -------------------------------------------------------------
    EX8

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

data = {
    'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Experience': ['Low', 'Low', 'Medium', 'Medium', 'Medium', 'High', 'High', 'High', 'High', 'High'],
    'Tech_Skills': ['Poor', 'Poor', 'Average', 'Average', 'Average', 'Good', 'Good', 'Good', 'Good', 'Good'],
    'Job_Offer': ['No', 'No', 'No', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes']
}

df = pd.DataFrame(data)

df = pd.get_dummies(df, columns=['Experience', 'Tech_Skills'], drop_first=True)

X = df.drop(columns=['Job_Offer', 'ID'])
y = df['Job_Offer']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dt_model = DecisionTreeClassifier(criterion='entropy', random_state=42)
dt_model.fit(X_train, y_train)

y_pred = dt_model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))

plt.figure(figsize=(12, 8))
plot_tree(dt_model, filled=True, feature_names=X.columns, class_names=['No', 'Yes'], fontsize=10)
plt.title('Decision Tree for Job Offer Prediction')
plt.show()
    """,

    9: """
    experiment : 9
    -------------------------------------------------------------
    EX9

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Sample dataset
data = np.array([[2, 4], [4, 6], [4, 4], [6, 2], [8, 4]])

kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(data)
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

# Visualizing clusters
plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis', marker='o', edgecolors='k',
label='Data Points')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200, label='Centroids')
plt.xlabel('X1')
plt.ylabel('X2')
plt.title('K-Means Clustering')
plt.legend()
plt.show()
    """,

    10: """
    experiment : 10 - A
    -------------------------------------------------------------
    EX10 A

#Q-Learning
import numpy as np
import random

env_states = 5
env_actions = 2

Q_table = np.zeros((env_states, env_actions))
alpha = 0.1
gamma = 0.9
epsilon = 0.2

def get_reward(state, action):
    return random.choice([-1, 0, 1])

def get_next_state(state, action):
    return (state + action) % env_states

for episode in range(100):
    state = random.randint(0, env_states - 1)
    for step in range(10):
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, env_actions - 1)
        else:
            action = np.argmax(Q_table[state])

        reward = get_reward(state, action)
        next_state = get_next_state(state, action)

        Q_table[state, action] = Q_table[state, action] + alpha * (
            reward + gamma * np.max(Q_table[next_state]) - Q_table[state, action]
        )

        state = next_state

print("Final Q-Table:")
print(Q_table)

-------------------------------------------------------------------------------------------------------------------

    EXPERIMENT : 10 - B
    ----------------------------------------------------------------------------------------------------------------

    EX10 B

#Genetic Algorithm
import random
import numpy as np

def fitness_function(x):
    return x**2

def selection(population):
    return sorted(population, key=fitness_function, reverse=True)[:2]

def crossover(parent1, parent2):
    return (parent1 + parent2) / 2

def mutation(child):
    return child + random.uniform(-1, 1)

population = [random.uniform(-10, 10) for _ in range(6)]

for _ in range(5):
    parents = selection(population)
    child = crossover(parents[0], parents[1])
    child = mutation(child)
    population.append(child)
    population = selection(population)

print("Final population:", population)
    """
} 
