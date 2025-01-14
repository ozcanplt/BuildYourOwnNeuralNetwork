import numpy
import matplotlib.pyplot as pyplot
import scipy.special

class neuralNetwork():
    
    def __init__(self, inodes, hnodes, onodes, rate):
        
        self.inodes = inodes
        self.hnodes = hnodes
        self.onodes = onodes
        self.lr = rate
        self.wih = numpy.random.normal(0.0, pow(self.hnodes, -0.5), 
                                   (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.onodes, -0.5), 
                                   (self.onodes, self.hnodes))
        
        self.activation_function = lambda x: scipy.special.expit(x)
        self.inverse_activation_function = lambda x: scipy.special.logit(x)
        pass
    
    def train(self, inputs_list, targets_list):
        
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors)
        
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                      numpy.transpose(hidden_outputs))
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
                                      numpy.transpose(inputs))
        pass
    
    def query(self, inputs_list):
        
        inputs = numpy.array(inputs_list, ndmin=2).T
        
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        return final_outputs
    
    def backquery(self, targets_list):
        # transpose the targets list to a vertical array
        final_outputs = numpy.array(targets_list, ndmin=2).T
        
        # calculate the signal into the final output layer
        final_inputs = self.inverse_activation_function(final_outputs)

        # calculate the signal out of the hidden layer
        hidden_outputs = numpy.dot(self.who.T, final_inputs)
        # scale them back to 0.01 to .99
        hidden_outputs -= numpy.min(hidden_outputs)
        hidden_outputs /= numpy.max(hidden_outputs)
        hidden_outputs *= 0.98
        hidden_outputs += 0.01
        
        # calculate the signal into the hidden layer
        hidden_inputs = self.inverse_activation_function(hidden_outputs)
        
        # calculate the signal out of the input layer
        inputs = numpy.dot(self.wih.T, hidden_inputs)
        # scale them back to 0.01 to .99
        inputs -= numpy.min(inputs)
        inputs /= numpy.max(inputs)
        inputs *= 0.98
        inputs += 0.01
        
        return inputs

  input_nodes = 784
hidden_nodes = 200
output_nodes = 10

learning_rate = 0.18

n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

training_data_file = open("training_data/mnist_train.csv","r")
training_data_list = training_data_file.readlines()
training_data_file.close()
epochs = 1
for e in range(epochs):
    for record in training_data_list:
        all_values = record.split(',')
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        targets = numpy.zeros(output_nodes) + 0.01
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)
        pass
    pass


test_data_file = open("training_data/mnist_test.csv", 'r') 
test_data_list = test_data_file.readlines() 
test_data_file.close()

all_values = test_data_list[0].split(',')
print(all_values[0])

for record in test_data_list: 
    all_values = record.split(',') 
    correct_label = int(all_values[0]) 
    print(correct_label, "correct label") 
    inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01 
    outputs = n.query(inputs) 
    label = numpy.argmax(outputs) 
    print(label, "network's answer") 
    if (label == correct_label): 
        scorecard.append(1) 
    else:
        scorecard.append(0) 
        pass

scorecard_array = numpy.asarray(scorecard)
print("Performance = ",scorecard_array.sum() / scorecard_array.size)


