import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import interact_manual, fixed

def simulate_CLT(dist, outer_n=100, inner_n=20, density=False):
    f = plt.figure(figsize=(20, 10))
    ax1 = f.add_subplot(121)
    ax2 = f.add_subplot(122)
    
    try:
        x1 = np.linspace(dist.ppf(0.001), dist.ppf(0.999), 100)
        ax1.plot(x1, dist.pdf(x1))
    except:
        x1 = np.arange(np.floor(dist.ppf(0.001)), np.ceil(dist.ppf(0.999)), 1)
        ax1.vlines(x1, 0, dist.pmf(x1))

    n_bins = int(np.log10(outer_n)*10)
    x_bar = np.array([np.mean(dist.rvs(size=inner_n)) for i in range(outer_n)])
    normed = np.sqrt(inner_n) * (x_bar - dist.stats('mean')) / np.sqrt(dist.stats('variance'))

    if not density:
        ax2.hist(normed, bins=n_bins, normed=True, label='sample means')
    else:
        sns.kdeplot(normed, ax=ax2, shade=True, label='sample means')
    # plt.hist(x_bar, bins=30, normed=True)
    
    x = np.linspace(stats.norm.ppf(0.001), stats.norm.ppf(0.999), 100)
    ax2.plot(x, stats.norm.pdf(x), color='black', label='standard normal')

    ax2.legend()
    sns.despine(fig=f, trim=True)
    plt.show()

def binomial_CLT(n, p, outer_n=100, inner_n=5, density=False):
    binom = stats.binom(n, p)
    simulate_CLT(binom, outer_n, inner_n, density=density)

def binomial_CLT2(n, p, outer_n=100, density=False):
    """ Traditional binomial central limit theorem where we evaluate the normality of p
    """
    bern = stats.binom(1, p)
    dist = stats.binom(n, p)
    mu = p
    var = p * (1-p) / n
    sig = np.sqrt(var)
    x_bar = np.array([np.mean(bern.rvs(size=n)) for i in range(outer_n)])
    normed = (x_bar - mu) / sig

    f = plt.figure(figsize=(20, 10))
    ax1 = f.add_subplot(121)
    ax2 = f.add_subplot(122)
    
    try:
        x1 = np.linspace(dist.ppf(0.001), dist.ppf(0.999), 100)
        ax1.plot(x1, dist.pdf(x1))
    except:
        x1 = np.arange(np.floor(dist.ppf(0.001)), np.ceil(dist.ppf(0.999)), 1)
        ax1.vlines(x1, 0, dist.pmf(x1))

    n_bins = int(np.log10(outer_n)*10)

    if not density:
        ax2.hist(normed, bins=n_bins, normed=True, label='sample means')
    else:
        sns.kdeplot(normed, ax=ax2, shade=True, label='sample means')
    # plt.hist(x_bar, bins=30, normed=True)
    
    x = np.linspace(stats.norm.ppf(0.001), stats.norm.ppf(0.999), 100)
    ax2.plot(x, stats.norm.pdf(x), color='black', label='standard normal')

    ax2.legend()
    sns.despine(fig=f, trim=True)
    plt.show()

def binomial_interactive():
    return interact_manual(binomial_CLT2, n=(5, 100, 5), p=(0.0, 1.0, 0.1), outer_n=fixed(1000), density=False)
    # return interact_manual(binomial_CLT, n=(10, 100, 5), p=(0.0, 1.0, 0.1), outer_n=fixed(1000), inner_n=fixed(5), density=False)

def general_CLT(dist_str, outer_n=1000, inner_n=20, density=False):
    if dist_str == 'normal':
        dist = stats.norm()
    elif dist_str == 'gamma':
        dist = stats.gamma(2)
    elif dist_str == 'beta':
        dist = stats.beta(a=2, b=6)
    elif dist_str == 'poisson':
        dist = stats.poisson(10)
    elif dist_str == 'hypergeometric':
        dist = stats.hypergeom(20, 7, 12)
    elif dist_str == 'binomial':
        dist = stats.binom(100, 0.25)
        
    simulate_CLT(dist, outer_n, inner_n, density=density)

def CLT_interactive():
    return interact_manual(general_CLT, dist_str = ['normal', 'gamma', 'beta','binomial', 'poisson', 'hypergeometric'], outer_n=[10, 100, 1000, 10000], inner_n=(5, 100, 5), density=False)

def cauchy_CLT(outer_n=100, inner_n=20, density=False, showMe=False):
    dist = stats.cauchy()
    f = plt.figure(figsize=(20, 10))
    ax1 = f.add_subplot(121)
    ax2 = f.add_subplot(122)
    
    x1 = np.linspace(dist.ppf(0.01), dist.ppf(0.99), 100)
    ax1.plot(x1, dist.pdf(x1))

    n_bins = int(np.log10(outer_n)*50)
    x_bar = np.array([np.mean(dist.rvs(size=inner_n)) for i in range(outer_n)])
    if not density:
        ax2.hist(x_bar, bins=n_bins, normed=True, label='sample means')
    else:
        sns.kdeplot(x_bar, ax=ax2, shade=True, label='sample means')
    
    if not showMe:
        x = np.linspace(stats.norm.ppf(0.001), stats.norm.ppf(0.999), 100)
        ax2.plot(x, stats.norm.pdf(x), color='black', label='standard normal')
    else:
        ax2.plot(x1, dist.pdf(x1), label='Cauchy')

    ax2.legend()
    sns.despine(fig=f, trim=True)
    plt.show()

def cauchy_CLT_interactive():
    return interact_manual(cauchy_CLT, outer_n=[10, 100, 1000, 10000, 100000], inner_n=(5, 100, 5), density=False, showMe=False)

def paired_sample_test(mu1, sigma1, mu2, sigma2, n):
    global slider
    
    try:
        sliders.close()
    except NameError:
        pass
    
    f = plt.figure()
    ax = f.add_subplot(111)
    # ax2 = f.add_subplot(122)
    
    norm1 = stats.norm(mu1, sigma1)
    norm2 = stats.norm(mu2, sigma2)
    
    lower, upper = np.min([norm1.ppf(0.001), norm2.ppf(0.001)]), np.max([norm1.ppf(0.999), norm2.ppf(0.999)])
    x = np.linspace(lower, upper, 100)
    # x = np.linspace(norm1.ppf(0.001), norm2.ppf(0.999), 100)
    cp = sns.color_palette()
    ax.plot(x, norm1.pdf(x))
    ax.fill_between(x, norm1.pdf(x), color=cp[0], alpha=0.25)
    ax.plot(x, norm2.pdf(x))
    ax.fill_between(x, norm2.pdf(x), color=cp[1], alpha=0.25)
    
    paired_sample_run(norm1, norm2, n, ax)
    sns.despine(fig=f, trim=True)
    plt.show()

def paired_sample_run(dist1, dist2, n, ax):
    samp1 = dist1.rvs(n)
    samp2 = dist2.rvs(n)
    
    z = (dist1.mean() - dist2.mean()) / np.sqrt(dist1.var()/n + dist2.var()/n)
    p_true = np.min([stats.norm.cdf(z), 1-stats.norm.cdf(z)])
    
    t = stats.ttest_rel(samp1, samp2)[1]
    sr = stats.wilcoxon(samp1, samp2)[1]
    
    ax.text(1.05, 0.9, "True p-value: {:0.5f}".format(p_true), transform=ax.transAxes)
    ax.text(1.05, 0.7, "Paired T-test p-value: {:0.5f}".format(t), transform=ax.transAxes)
    ax.text(1.05, 0.5, "Wilcoxon sign-rank p-value: {:0.5f}".format(sr), transform=ax.transAxes)

    
    cp = sns.color_palette()
    ax.plot(samp1, dist1.pdf(samp1), 'o', color=cp[0])
    ax.plot(samp2, dist2.pdf(samp2), 'o', color=cp[1])

def paired_sample_interactive():
    return interact_manual(paired_sample_test, mu1=(1, 20, 1), sigma1=(1, 10, 1), mu2=(1, 20, 1), sigma2=(1, 10, 1), n=(2, 100, 1))

def outlier_simulation(n1, n2, n3, mu, sigma):
    norm1 = stats.norm(50, 5)
    norm2 = stats.norm(mu, sigma)
    
    samp1 = norm1.rvs(n1)
    samp2 = norm1.rvs(n2)
    samp_outlier = norm2.rvs(n3)
    
    samp_comp = np.append(samp2, samp_outlier)
    t = stats.ttest_ind(samp_comp, samp1, equal_var=False)[1]
    manu = stats.mannwhitneyu(samp_comp, samp1)[1]
    
    f = plt.figure(figsize=(28, 10))
    ax1 = plt.subplot(131)
    ax2 = plt.subplot(132)
    ax3 = plt.subplot(133)
    
    x1 = np.linspace(norm1.ppf(0.001), norm1.ppf(0.999), 100)
    x2 = np.linspace(norm2.ppf(0.001), norm2.ppf(0.999), 100)
    ax1.plot(x1, norm1.pdf(x1), label='True Distribution')
    ax1.plot(x2, 0.2*norm2.pdf(x2), label='Outlier Distribution')
    
    ax1.plot(samp1, norm1.pdf(samp1), 'o', label='True Sample 1')
    ax1.plot(samp2, norm1.pdf(samp2), 'o', label='True Sample 2')
    ax1.plot(samp_outlier, 0.2*norm2.pdf(samp_outlier), 'o', label='Outlier Sample 2')
    ax1.legend()
    # ax1.legend(loc=(0.2, 0.7))
    
    mu1 = np.mean(samp1)
    sig1 = np.std(samp1, ddof=1)
    t_dist1 = stats.t(df=len(samp1)-1, loc=mu1, scale=sig1)
    
    mu2 = np.mean(samp_comp)
    sig2 = np.std(samp_comp, ddof=1)
    t_dist2 = stats.t(df=len(samp_comp)-1, loc=mu2, scale=sig2)
   
    cp = sns.color_palette()
    
    sns.distplot(samp1, ax=ax2, label='True Sample 1', rug=True, hist=False, kde_kws={'shade':True})
    sns.distplot(samp_comp, ax=ax2, label='All Sample 2', rug=True, hist=False, kde_kws={'shade':True}, color=cp[1])
    
    x3 = np.linspace(t_dist1.ppf(0.001), t_dist1.ppf(0.999), 100)
    ax3.plot(x3, t_dist1.pdf(x3), '--', color=cp[1], label='t-dist Sample 1')
    
    x4 = np.linspace(t_dist2.ppf(0.001), t_dist2.ppf(0.999), 100)
    ax3.plot(x4, t_dist2.pdf(x4), '--', color=cp[0], label='t-dist Sample 2')
    ax3.legend()
    
    ax2.text(0.1, -0.15, "t-test p-value: {:0.4f}".format(t), transform=ax2.transAxes, fontsize=24)
    ax2.text(0.1, -0.20, "Wilcoxon rank-sum p-value: {:0.4f}".format(manu), transform=ax2.transAxes, fontsize=24)
    
    sns.despine(fig=f, trim=True)
    plt.show()

def outlier_interactive():
    return interact_manual(outlier_simulation, n1=(0, 50, 5), n2=(0, 50, 5), n3=(0, 50, 1), mu=(0, 50, 1), sigma=(1, 10, 1))
