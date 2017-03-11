source("rules.R")

### Play the Bayes Table Game 10,000 times ###

## Read user supplied score
readScore <- function() {
    n <- readline()

    if ( ! grepl("^[0-5]$", n) ) {
        cat("Score must be between 0-5, inclusive ")
        return(readScore())
    } else {
        return(as.integer(n))
    }
}

## Read user supplied integer
readInteger <- function() {
    n <- readline()

    if ( ! grepl("^[0-9]+$", n) ) {
        cat("You must enter an integer!  ")
        return(readInteger())
    } else {
        return(as.integer(n))
    }
}

message("
    We will simulate the Bayes Table Game n times (you specify n)
    You will enter a score for Alice that we will track
    And you will eneter a score for Bob that we will track
         
    We will then empirically estimate Bob's expectation of winning
    when that event occurs.
    ")

cat("Enter a score for Alice (e.g. 5): ")
A.score <- readScore()
cat("\n")

cat("Enter a score for Bob (e.g. 3): ")
B.score <- readScore()
cat("\n")

cat("Enter a number of times to simulate the game: ")
n <- readInteger()
cat("\n")

message(sprintf("About to simulate %i times tracking A=%i and B=%i", n, A.score, B.score))
x <- readline(sprintf("This will take ~%0.0f seconds on modern architecture. Do you want to continue? (y/n) ", 3.3/1000*n))
stopifnot(x == 'y')
cat("\n")

# Initialize counts
count = 0
A.win = 0
B.win = 0

# Play game n times
for (i in seq(1, n)) {

    # Initial conditions of game
    p = pick_p()
    A = 0
    B = 0
    roll = 0

    flag = FALSE

    # Roll until a player wins
    while ( TRUE ) {

        if ( roll == 0 ) {
            df = roll_ball(p)
        } else {
            df = roll_ball(p, df)
        }

        roll = roll + 1

        if ( tail(df$winner, n=1) == 'You' ) { 
            A = A + 1 
        } else { 
            B = B + 1
        }

        # Check for user-defined condition
        if ( (A == A.score) & (B == B.score) ) { flag=TRUE }

        if ( A == 6 ) {
            winner = 'Alice'
            break
        } else if ( B == 6 ) {
            winner = 'Bob'
            break
        }

    }

    # Count event occurances
    if ( flag ) {
        count = count + 1

        if (winner == 'Alice') { 
            A.win = A.win + 1 
        } else { 
            B.win = B.win + 1 
        }
    }
}

# Derive empirical expectations
B.exp = B.win / (A.win + B.win)
A.exp = 1 - B.exp

message(sprintf("The event {A=%i, B=%i} occured in %i out of %i simulations", A.score, B.score, count, n))
message(sprintf("Of those occurances, Alice won %i times and Bob won %i times", A.win, B.win)) 
message(sprintf("The empirical expectation that Bob wins when A=%i and B=%i is: %0.3f", A.score, B.score, B.exp))
