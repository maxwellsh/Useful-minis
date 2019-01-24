# Algorithms for Inference in Hidden Markov Models

## Background

Hidden Markov models are powerful tools for performing statistical inference on latent variables of sequence data (that is data, which can be ordered and indexed). The Markov property that the probability of being in a state at time t depend only on the state at time t-1 makes for elegent mathematics for performing calculations of inference, for example calculating the likelihood of the observations given a sequence of hidden states or the maxmimum likelihood path given the observations.

However, the practical implementation of these mathematical constructrs requires some thought to 1) make them efficient (quadratic in the number of observations) and 2) to prevent underflow errors in the calculations.

Here I provide example implementations of the major HMM algorithms and demonstrate their use on some toy data.

## Setup

Running these demos requires python and a jupyter notebook. The easiest way to do this is to install the latest version of `anaconda`.

1. Go [here](https://www.anaconda.com/download) to download the latest version of anaconda for you OS. BE SURE TO DOWNLOAD PYTHON 3.X
2. Follow the instructions to install anaconda.
3. Clone this repository to your computer.

## Running

1. Open a terminal.
2. Navigate to the clone of this repository. Be sure to be in `/path/to/Useful-minis/Central_Limit_Theorem`
3. Run `$ jupyter notebook`. This will automatically open a jupyter notebook server in your web browser
4. In the jupyter brower page, open `HMM_algorithm_tests.ipynb`
5. Read the instructions and enjoy.

## Questions?
Email me.
