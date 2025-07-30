experiment = {
    3: """
    experiment : 3
    -------------------------------------------------------------
    from sklearn import preprocessing
    from sklearn.naive_bayes import GaussianNB

    weather = ['Sunny','Sunny','Overcast','Rainy','Rainy','Rainy','Overcast',
               'Sunny','Sunny','Rainy','Sunny','Overcast','Overcast','Rainy']
    temp = ['Hot','Hot','Hot','Mild','Cool','Cool','Cool',
            'Mild','Cool','Mild','Mild','Mild','Hot','Mild']
    play = ['No','No','Yes','Yes','Yes','No','Yes',
            'No','Yes','Yes','Yes','Yes','Yes','No']

    le = preprocessing.LabelEncoder()
    weather_encoded = le.fit_transform(weather)
    temp_encoded = le.fit_transform(temp)
    label = le.fit_transform(play)

    features = list(zip(weather_encoded, temp_encoded))
    model = GaussianNB()
    model.fit(features, label)
    predicted = model.predict([[2, 2]])
    print("Predicted Value:", predicted)
    """,

    4: """
    experiment : 4
    -------------------------------------------------------------
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression

    data = {
        'StudyHours': [1,2,3,4,5,6,7,8,9,10],
        'ExamScore': [35,45,50,55,60,70,75,80,85,90]
    }

    data_set = pd.DataFrame(data)
    x = data_set.iloc[:, :-1].values
    y = data_set.iloc[:, 1].values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=0)
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
    print("Accuracy:", accuracy_score(y_test, y_pred))
    """,

    7: """
    experiment : 7
    -------------------------------------------------------------
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
    print("Accuracy:", accuracy_score(y_test, y_pred))
    """,

    8: """
    experiment : 8
    -------------------------------------------------------------
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier, plot_tree
    from sklearn.metrics import accuracy_score

    data = {
        'ID': [1,2,3,4,5,6,7,8,9,10],
        'Experience': ['Low','Low','Medium','Medium','Medium','High','High','High','High','High'],
        'Tech_Skills': ['Poor','Poor','Average','Average','Average','Good','Good','Good','Good','Good'],
        'Job_Offer': ['No','No','No','No','Yes','Yes','Yes','Yes','Yes','Yes']
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
    """,

    9: """
    experiment : 9
    -------------------------------------------------------------
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans

    data = np.array([[2, 4], [4, 6], [4, 4], [6, 2], [8, 4]])
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(data)

    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200)
    plt.title('K-Means Clustering')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()
    """,

    10: """
    experiment : 10
    -------------------------------------------------------------
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

            Q_table[state, action] += alpha * (
                reward + gamma * np.max(Q_table[next_state]) - Q_table[state, action]
            )

            state = next_state

    print("Final Q-Table:")
    print(Q_table)
    """
} 
