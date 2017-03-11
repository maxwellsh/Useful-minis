## A script to play the Bayes Table Game a single time
## Run in RStudio
##      > source("play.R")

source("rules.R")

### Play the game ###

readline("Welcome to the Bayes Table Game. Press enter to play: ")
cat("\n")

# Initial conditions for game
p = pick_p()
A = 0
B = 0
roll = 0

# Prior distribution
message("The casino has roled the initial ball.")
x <- readline("Do you want to see the prior density of p? (y/n) ")

if ( x == 'y') { 
    prior <- estimate_p_density(A, B)
    j <- plot_density(prior, roll, A, B)

    print(j)
}

message("\nLet's play!") 

# Roll ball until one player reaches 6 successes
while ( TRUE ) {
    readline("Press enter to roll a ball...")
    cat("\n")

    # Call to actual roll function
    if ( roll == 0 ) {
        df = roll_ball(p)
    } else {
        df = roll_ball(p, df)
    }

    roll = roll + 1

    # Keep track of who won
    if ( tail(df$winner, n=1) == 'You' ) { 
        message("You won that toss. Good job!\n")
        A = A + 1 
    } else { 
        message("Bob won that toss. Boo Bob!")
        B = B + 1
    }

    # Exit loop if a player won
    if ( A == 6 ) {
        winner = 'You'
        break
    } else if ( B == 6 ) {
        winner = 'Bob'
        break
    }

    # Print standings
    message(sprintf("The current standing is\nYou: %i\tBob: %i\n", A, B))

    # Generate posterior
    message(sprintf("Generating prior after roll %i", roll))
    posterior <- estimate_p_density(A, B)
    j <- plot_density(posterior, roll, A, B)
    print(j)
}

# Winner message
message("\n======================================\n")
if ( winner == 'You') { 
    message("Congratulations, you won!\n") 
} else { 
    message("Bob won =(. Better luck next time\n") 
}
message("======================================\n")

# Final outcome
message(sprintf("The final standings are\nYou: %i\tBob: %i\n", A, B))

# Final posterior
posterior <- estimate_p_density(A, B)
x <- readline("Do you want to see the final posterior on p? (y/n) ")
if ( x == 'y') { 
    j <- plot_density(posterior, roll, A, B)
    print(j)
    cat("\n")
}

# Expected value of p vs actual value of p
p.exp <- calc_p_expected(posterior)
message(sprintf("The expected value of p under the posterior is: %0.3f", p.exp))
message(sprintf("The actual value of p was: %0.3f\n", p))

# Render table
x <- readline("Do you want to see the table? (y/n) ")
if ( x == 'y') { 
    j <- render_table(df, p)
    print(j)
}

readline("Press enter to exit game.")
cat("\n")
