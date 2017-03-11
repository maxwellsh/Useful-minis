library("ggplot2")

pick_p <- function() {

    p <- runif(1, min=0, max=1)
    return(p)

}

roll_ball <- function(p, df=NULL) {
    x <- runif(1, min=0, max=1)
    y <- runif(1, min=0, max=1)

    if ( x <= p) { 
        winner = 'You'
    } else { 
        winner = 'Bob' 
    }

    if ( is.null(df) ) {
        df = data.frame(x=x, y=y, winner=winner, stringsAsFactors=F)
    } else {
        r = data.frame(x=x, y=y, winner=winner)
        df = rbind(df, r)
    }

    return(df)
}

estimate_p_density <- function(n.A, n.B) {

    # n.rolls <- nrow(df)
    # n.A <- length(df$winner[df$winner == 'A'])
    # n.B <- n.rolls - n.A
    p.range <- seq(0, 1, length.out=1001)

    density <- gamma(n.A + n.B + 2) * p.range^n.A * (1-p.range)^n.B / (gamma(n.A+1) * gamma(n.B+1))

    return(data.frame('p'=p.range, 'density'=density))

}

plot_density <- function(df.density, roll, A, B) {
    j <- ggplot(df.density, aes(x=p, y=density)) + 
         geom_density(stat='identity', color='red', fill='red', alpha=0.5) + 
         labs(title=sprintf("Density after %i rolls   {A=%i, B=%i}", roll, A, B)) +
         theme_bw()

    return(j)
}

calc_p_expected <- function(df.density) {
    dp = df.density$p[2] - df.density$p[1]
    p.exp <- sum(df.density$p * df.density$density * dp)

    return(p.exp)
}

render_table <- function(df, p) {
    df.rect <- data.frame(x=0, y=0)

    j <- ggplot() +
         geom_rect(data=df.rect, aes(xmin=0, xmax=p, ymin=0, ymax=1), fill='green', alpha=0.1) +
         geom_rect(data=df.rect, aes(xmin=p, xmax=1, ymin=0, ymax=1), fill='red', alpha=0.1) +
         geom_point(data=df, aes(x=x, y=y, shape=winner, color=winner)) +
         geom_vline(xintercept=p, linetype='dashed')

    return(j)

}
