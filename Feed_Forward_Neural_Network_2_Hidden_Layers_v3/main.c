/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.c
 * Author: Issam
 *
 * Created on 13 février 2020, 19:53
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
/*
 * 
 */

float sigmoid(float x) {
    return 1/(1+exp(-x));
}

float dSigmoid(float x) {
    return x * (1 - x);
}

// Init all weights and biases between 0.0 and 1.0


static const int numInputs = 4;
static const int numHiddenNodes = 6;
static const int numOutputs = 1;
static const int numTrainingSets = 7;

void shuffle (int *array, size_t n) {
    if (n > 1) {
        size_t i;
        for (i = 0; i < n-1; i++) {
            size_t j = i + rand() / (RAND_MAX / (n-i) + 1);
            int t = array[j];
            array[j] = array[i];
            array[i] = t;
        }
    }
}

float randomWeights(float lower, float upper) {
    float randomNum = lower + rand() / (RAND_MAX / (upper - lower+1)+1.0);
    float weights = randomNum*sqrt(2.0/upper);
    return weights;
}

void randomWeightsInitialisation(float arr[numInputs][numHiddenNodes]) {
    for (int i = 0; i < numInputs; i++) {
        for (int j = 0; j < numHiddenNodes; j++) {
            float randomNum = randomWeights(2.0, 4.0);
            arr[i][j] = randomNum;
        }
    }
}

int main() {
    float outputLayer[numOutputs];
    float hiddenLayer_2[numHiddenNodes];
    float hiddenLayer[numHiddenNodes];
    
    float outputLayerBias[numOutputs];
    float hiddenLayerBias_2[numHiddenNodes];
    float hiddenLayerBias[numHiddenNodes];
    
    float outputWeights[numHiddenNodes][numOutputs];
    float hiddenWeights_2[numInputs][numHiddenNodes];
    float hiddenWeights[numInputs][numHiddenNodes];
    
    randomWeightsInitialisation(hiddenWeights_2);
    randomWeightsInitialisation(hiddenWeights);
    
    // Training set definition
    /*
    float training_inputs[4][2] = {
        {0.0f,0.0f},
        {1.0f,0.0f},
        {0.0f,1.0f},
        {1.0f,1.0f}
    };
    
    float training_outputs[4][1] = {
        {0.0f},
        {1.0f},
        {1.0f},
        {0.0f}
    };
     */
    
    float training_inputs[7][4] = {
        {0.0f,0.0f,0.0f,1.0f},
        {1.0f,1.0f,1.0f,1.0f},
        {1.0f,0.0f,1.0f,0.0f},
        {0.0f,1.0f,1.0f,0.0f},
        {0.0f,0.0f,1.0f,1.0f},
        {0.0f,1.0f,0.0f,1.0f},
        {1.0f,0.0f,0.0f,1.0f}
    };
    
    float training_outputs[7][1] = {
        {0.0f},
        {1.0f},
        {0.0f},
        {1.0f},
        {0.0f},
        {1.0f},
        {0.0f}
    };
 
    // Iterate through the entire training for a number of epochs
    int epochs = 10000;
    for (int n = 0; n < epochs; n++) {
        // As per SGD, shuffle the order of the training set
        int trainingSetOrder[] = {0,1,2,3,4,5,6};
        shuffle(trainingSetOrder,numTrainingSets);
        
        // Cycle through each of the training set elements
        for (int x = 0; x < numTrainingSets; x++) {
            int i = trainingSetOrder[x];
            //float randomNum = randomWeights(2.0, 4.0);
            //printf(" - [ERROR RATE]: %f\n", randomNum);
                
            // Compute hidden layer activation LAYER 1
            for (int j = 0; j < numHiddenNodes; j++) {
                float activation = hiddenLayerBias[j];
                for (int k = 0; k < numInputs; k++) {
                    activation += training_inputs[i][k]*hiddenWeights[k][j];
                }
                hiddenLayer[j] = sigmoid(activation);
            }
            
            // Compute hidden layer activation LAYER 2
            for (int j = 0; j < numHiddenNodes; j++) {
                float activation2 = hiddenLayerBias_2[j];
                for (int k = 0; k < numInputs; k++) {
                    activation2 += training_inputs[i][k]*hiddenLayer[j]*hiddenWeights_2[k][j];
                }
                hiddenLayer_2[j] = sigmoid(activation2);
            }
            
            // Compute output layer activation
            for (int j = 0; j < numOutputs; j++) {
                float activation = outputLayerBias[j];
                for (int k = 0; k < numHiddenNodes; k++) {
                    activation += outputWeights[k][j]*hiddenLayer_2[k];
                }
                outputLayer[j] = sigmoid(activation);
            }
            
            // Compute change in output weights
            float deltaOutput[numOutputs];
            for (int j = 0; j < numOutputs; j++) {
                float dError = (training_outputs[i][j]-outputLayer[j]);
                deltaOutput[j] = dError*dSigmoid(outputLayer[j]);
                printf("Num output: %d", j);
                printf(" - [ERROR RATE]: %f\n", fabs(dError));
                
            }
            
            // Compute change in hidden weights LAYER 2
            float deltaHidden_2[numHiddenNodes];
            for (int j = 0; j < numHiddenNodes; j++) {
                float dError = 0.0f;
                for (int k = 0; k < numOutputs; k++) {
                    dError += deltaOutput[k]*outputWeights[j][k];
                    
                }
                deltaHidden_2[j] = dError*dSigmoid(hiddenLayer_2[j]);
            }
            
            // Compute change in hidden weights LAYER 1
            float deltaHidden[numHiddenNodes];
            for (int j = 0; j < numHiddenNodes; j++) {
                float dError = 0.0f;
                for (int k = 0; k < numOutputs; k++) {
                    dError += deltaOutput[k]*outputWeights[j][k]*deltaHidden_2[j];
                }
                deltaHidden[j] = dError*dSigmoid(hiddenLayer[j]);
            }
            
            // Apply change in output weights
            float lr = 0.1;
            for (int j = 0; j < numOutputs; j++) {
                outputLayerBias[j] += deltaOutput[j]*lr;
                for (int k = 0; k < numHiddenNodes; k++) {
                    outputWeights[k][j] += hiddenLayer[k]*hiddenLayer_2[k]*deltaOutput[j]*lr;
                }
            }
            
            // Apply change in hidden weights LAYER 2
            for (int j = 0; j < numHiddenNodes; j++) {
                hiddenLayerBias_2[j] += deltaHidden[j]*lr;
                for(int k = 0; k < numInputs; k++) {
                    hiddenWeights_2[k][j] += training_inputs[i][k]*deltaHidden_2[j]*lr;
                }
            }
            
            // Apply change in hidden weights LAYER 1
            for (int j = 0; j < numHiddenNodes; j++) {
                hiddenLayerBias[j] += deltaHidden[j]*lr;
                for(int k = 0; k < numInputs; k++) {
                    hiddenWeights[k][j] += training_inputs[i][k]*deltaHidden[j]*lr;
                }
            }
        }   
    }
    return (EXIT_SUCCESS);
}
