# The Bayes Table Game

## Background

This mini project simulates the Bayes table game as outline in [this](http://www.nature.com/nbt/journal/v22/n9/full/nbt0904-1177.html) nature article.

In short: You and Bob are gambling in your local casino. Now this casino has a rather ideosyncratic gae of which you and Bob are big fans. The casion rolls a ball on a big table that neither of you can see. The casino then rolls another ball. If the ball ends up to the left of the original, you win the toss; if it ends up to the right of original Toss, Bob wins. The game continue as such until you or Bob wins a total of size toses. The only information you get is whether you or Bob won each toss.

Fancying yourself handy with numbers (and also disliking when Bob wins), you want to estimate where the original ball ended up and what Bob's expectation of winning is after any given toss.

## Statistics

Turns out, using thes standard MLE estimator of k/n where k is the number of time's you've won and n is the total number of tosses gives an innaccurate estimation of that expectation. However, a bayesian approach where the likelihood is p(Y=x, B=n-x | p) = Bin(n, x) where Y is the RV counting the number of tosses you've won and B is the corresponding variable counting the number of times Bob has won, and the prior is f(p) = Unif([0, 1]) gives an accurate estimate of the expectation. See the above paper for details.

## Usage

This mini projet provides two scripts

1. __play.R__
   Simulate playing the game once. Illustrates with plots how the posterior evolves with each new observation.

2. __play.n.times.R__
   Simulate playing the game n times. The user specifies a score for themselves (Alice), a score for Bob, and the number of times to simulate the game. The script them calculates an empirical estimate for the expectation that Bob wins given the observed scores. This estimated value can be checked against the analytical solution presented in the paper.

Both scripts should be run by sourcing them in RStudio
