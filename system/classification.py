import sys
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import numpy as np


def scale_training_test_features(features_training, features_test):

    # Scale features (recommended in scikit learn)
    x_train = np.array(features_training)
    x_test = np.array(features_test)

    scaler = StandardScaler()

    scaler.fit(x_train)
    x_train_scaled = scaler.transform(x_train)

    x_test_scaled = scaler.transform(x_test)

    if len(x_train[0]) == 1:
        return x_train_scaled.reshape(-1, 1), x_test_scaled.reshape(-1, 1)
    else:
        return x_train_scaled, x_test_scaled



def train_classifier(X_train_scaled, Y_train, hidden_layer, activation):


    mlp = MLPClassifier(hidden_layer_sizes = hidden_layer, activation = activation)

    classifier = mlp.fit(X_train_scaled, Y_train)

    return classifier


def test_classifier(classifier, X_test_scaled):

    predictions = classifier.predict(X_test_scaled)

    return predictions
