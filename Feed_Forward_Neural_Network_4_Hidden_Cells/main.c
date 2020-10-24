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

double sigmoid(double x) {
    return 1/(1+exp(-x));
}

double dSigmoid(double x) {
    return x * (1 - x);
}

// Init all weights and biases between 0.0 and 1.0
double init_weight() {
    return ((double) rand())/((double)RAND_MAX); 
}

static const int numInputs = 4;
static const int numHiddenNodes = 5;
static const int numOutputs = 2;
static const int numTrainingSets = 4;



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


int main() {
    double hiddenLayer[numHiddenNodes];
    double outputLayer[numOutputs];

    double hiddenLayerBias[numHiddenNodes];
    double outputLayerBias[numOutputs];

    double hiddenWeights[numInputs][numHiddenNodes];
    double outputWeights[numHiddenNodes][numOutputs];
    double final_error_rate = 0.0;
    
    // Training set definition
    double training_inputs[4][4] = {
        {0.0f,0.0f,0.0f,0.0f},{1.0f,0.0f,0.0f,0.0f},{0.0f,1.0f,0.0f,0.0f},{1.0f,1.0f,0.0f,0.0f}
    };
    
    double training_outputs[4][2] = {
        {0.0f,0.0f},{1.0f,1.0f},{1.0f,1.0f},{0.0f,0.0f}
    };
        
    // Iterate through the entire training for a number of epochs
  
    int epochs = 10000;
    int trainingSetOrder[numTrainingSets];
    
    for (int i = 0; i < numTrainingSets; i++) {
        trainingSetOrder[i] = i;
    }
    
    for (int n = 0; n < epochs; n++) {
        // As per SGD, shuffle the order of the training set

        // Cycle through each of the training set elements
        for (int x = 0; x < numTrainingSets; x++) {
            int i = trainingSetOrder[x];
            // Compute hidden layer activation
            for (int j = 0; j < numHiddenNodes; j++) {
                double activation = hiddenLayerBias[j];
                for (int k = 0; k < numInputs; k++) {
                    activation += training_inputs[i][k]*hiddenWeights[k][j];
                    //printf("%f",hiddenWeights[k][j]);
                    //printf("\n");
                }
                hiddenLayer[j] = sigmoid(activation);
                //printf("Hidden Layer Num: %d",j);
                //printf(" - Equal: %f",hiddenLayer[j]);
                //printf("\n");
            }
            
            // Compute output layer activation
            for (int j = 0; j < numOutputs; j++) {
                double activation = outputLayerBias[j];
                for (int k = 0; k < numHiddenNodes; k++) {
                    activation += hiddenLayer[k]*outputWeights[k][j];
                    //printf("%f",outputWeights[k][j]);
                    //printf("\n");
                }
                outputLayer[j] = sigmoid(activation);
            }
            
            // Compute change in output weights
            double deltaOutput[numOutputs];
            for (int j = 0; j < numOutputs; j++) {
                double dError = (training_outputs[i][j]-outputLayer[j]);
                deltaOutput[j] = dError*dSigmoid(outputLayer[j]);
                //printf("Value of dSigmoid(outputLayer[j]): %f\n", outputLayer[j]);
                //printf("[ERROR RATE]: n°%d", n);
                //printf(" - %f\n", fabs(dError));
                final_error_rate = fabs(dError);
            }
            
            // Compute change in hidden weights
            double deltaHidden[numHiddenNodes];
            for (int j = 0; j < numHiddenNodes; j++) {
                double dError = 0.0f;
                for (int k = 0; k < numOutputs; k++) {
                    dError += deltaOutput[k]*outputWeights[j][k];
                    //printf("Value of deltaOutput[k]: %f\n", deltaOutput[j]);
                    //printf("Value dError: %f\n", dError);
                }
                deltaHidden[j] = dError*dSigmoid(hiddenLayer[j]);
                
            }
            
            // Apply change in output weights
            double lr = 0.1;
            for (int j = 0; j < numOutputs; j++) {
                outputLayerBias[j] += deltaOutput[j]*lr;
                //printf("Value of outputLayerBias[j]: %f\n", deltaOutput[j]);
                for (int k = 0; k < numHiddenNodes; k++) {
                    outputWeights[k][j] += hiddenLayer[k]*deltaOutput[j]*lr;
                    //printf("Value of outputWeights[k][j]: %f\n", outputWeights[k][j]);
                }
            }
            
            // Apply change in hidden weights
            for (int j = 0; j < numHiddenNodes; j++) {
                hiddenLayerBias[j] += deltaHidden[j]*lr;
                for(int k = 0; k < numInputs; k++) {
                    hiddenWeights[k][j] += training_inputs[i][k]*deltaHidden[j]*lr;
                }
            }
        } 
    }
    printf("[FINAL ERROR RATE]: %f\n", final_error_rate);
    return (EXIT_SUCCESS);
}

