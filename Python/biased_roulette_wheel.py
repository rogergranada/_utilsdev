import numpy as np
import random, operator

def roulette_wheel(values):
    #create an index to each value according to its position
    sorted_values = sorted(enumerate(values), key=operator.itemgetter(1));
    indices, values = zip(*sorted_values);

    # calculate the probability of each value and make the division between them
    sum_values = sum(values)
    probabilities = [float(v)/sum_values for v in values]
    #print probabilities

    accumulate_probs = np.cumsum(probabilities)
    #print accumulate_probs

    # runs the roullete and select a random a number in the range [0,1]
    selected_num = random.random()

    # check where is the selected value in the roulette
    for index, accumulated_prob in zip(indices, accumulate_probs):
        if selected_num < accumulated_prob:
            return index


if __name__ == "__main__":
    values = [1,2,3,4,5,10]
    index = roulette_wheel(values)
    print index

