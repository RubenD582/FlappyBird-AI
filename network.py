import random
import math


def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    else:
        return math.exp(x) / (1 + math.exp(x))


class NeuralNetwork:
    def __init__(self, input_layer, hidden_layer, output_layer):
        self.input = input_layer
        self.hidden = hidden_layer
        self.output = output_layer

        # Initialize the Neural Network with random float values
        self.input_hidden = [[random.uniform(-1, 1) for _ in range(self.hidden)] for _ in range(self.input)]
        self.hidden_output = [[random.uniform(-1, 1) for _ in range(self.output)] for _ in range(self.hidden)]

        self.hidden_bias = [random.uniform(-1, 1) for _ in range(self.hidden)]
        self.output_bias = [random.uniform(-1, 1) for _ in range(self.output)]

    def feedforward(self, inputs):
        # Calculate hidden layer
        self.hidden_values = []
        for i in range(self.hidden):
            sum = 0
            for j in range(len(inputs)):
                sum += inputs[j] * self.input_hidden[j][i]
            self.hidden_values.append(sigmoid(sum + self.hidden_bias[i]))

        # Calculate the output values
        self.output_values = []
        for i in range(self.output):
            sum = 0
            for j in range(self.hidden):
                sum += self.hidden_values[j] * self.hidden_output[j][i]
            self.output_values.append(sigmoid(sum + self.output_bias[i]))

        return self.output_values

    def mutation(self, mutation_rate=0.1, mutation_strength=0.1):
        # Mutate weights and biases with given mutation rate and strength
        for i in range(self.input):
            for j in range(self.hidden):
                if random.random() < mutation_rate:
                    self.input_hidden[i][j] += random.uniform(-mutation_strength, mutation_strength)
                    self.input_hidden[i][j] = max(min(self.input_hidden[i][j], 1), -1)

        for i in range(self.hidden):
            for j in range(self.output):
                if random.random() < mutation_rate:
                    self.hidden_output[i][j] += random.uniform(-mutation_strength, mutation_strength)
                    self.hidden_output[i][j] = max(min(self.hidden_output[i][j], 1), -1)

        for i in range(self.hidden):
            if random.random() < mutation_rate:
                self.hidden_bias[i] += random.uniform(-mutation_strength, mutation_strength)
                self.hidden_bias[i] = max(min(self.hidden_bias[i], 1), -1)

        for i in range(self.output):
            if random.random() < mutation_rate:
                self.output_bias[i] += random.uniform(-mutation_strength, mutation_strength)
                self.output_bias[i] = max(min(self.output_bias[i], 1), -1)

    def crossover(self, other):
        """Combine genes from this neural network and another."""
        child = NeuralNetwork(self.input, self.hidden, self.output)

        # Crossover input_hidden weights
        for i in range(self.input):
            for j in range(self.hidden):
                # Randomly choose gene from either parent
                child.input_hidden[i][j] = random.choice([self.input_hidden[i][j], other.input_hidden[i][j]])

        # Crossover hidden_output weights
        for i in range(self.hidden):
            for j in range(self.output):
                # Randomly choose gene from either parent
                child.hidden_output[i][j] = random.choice([self.hidden_output[i][j], other.hidden_output[i][j]])

        # Crossover hidden biases
        for i in range(self.hidden):
            child.hidden_bias[i] = random.choice([self.hidden_bias[i], other.hidden_bias[i]])

        # Crossover output biases
        for i in range(self.output):
            child.output_bias[i] = random.choice([self.output_bias[i], other.output_bias[i]])

        return child

    def get_hidden_values(self):
        return self.hidden_values if hasattr(self, 'hidden_values') else []

    def get_output_values(self):
        return self.output_values if hasattr(self, 'output_values') else []

    def get_input_hidden(self):
        return self.input_hidden

    def get_hidden_output(self):
        return self.hidden_output

    def get_hidden_bias(self):
        return self.hidden_bias

    def get_output_bias(self):
        return self.output_bias
