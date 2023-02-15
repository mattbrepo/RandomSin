# RandomSin
Analysis on a random generation function based on sine.

**Language: Python**

**Start: 2023**

## Why
In mathematics, a [chaotic map](https://en.wikipedia.org/wiki/List_of_chaotic_maps) is a function that exhibits some sort of chaotic behavior. For example, where a small change in the input can result in a large difference in the output. On [this site](https://humphryscomputing.com/Notes/Neural/chaos.html) is mentioned that a simple function like:

$$ y = \sin \frac{1}{x} $$

can show a chaotic behavior when x is very small:

![sin(1 / x)](/images/function.jpg)

![sin(1 / x)](/images/function2.jpg)

Intrigued by this use of the sine, I defined a random generation function based on it:

$$ f(i) = \sin \frac{s}{(i / 10000000)} $$

where _s_ is the seed and _i_ is the 1-based index of the randomized array.

### Histograms
Therefore, I performed a bit of analysis to determine how good this function is. First, I compared the histograms of the "standard" Python random function and of the "sine" random function:

![histograms](/images/histos.jpg)


The "sine" function histogram shows a distribution which favors values on the extreme sides (0 and 1). The "standard" function histogram also shows, surprisingly enough, an uneven distribution where the extreme values are disadvantaged.

### Wald–Wolfowitz runs test
On the many test mentioned in [this Wikipedia page](https://en.wikipedia.org/wiki/Randomness_test), there is the [Wald–Wolfowitz runs test](https://en.wikipedia.org/wiki/Wald%E2%80%93Wolfowitz_runs_test) which is a non-parametric statistical test that checks the randomness hypothesis. It does it by applying the [Z-test](https://en.wikipedia.org/wiki/Z-test) with a confidence level of 95% (i.e., &alpha; of 5% and Z = 1.96):

![z-test](/images/z_test.jpg)

which was confirmed with a absolute value of Z:

```python
| Z | = 0.98
```

which is less than 1.96.

### Chi-squared test
The [Chi-squared test](https://en.wikipedia.org/wiki/Chi-squared_test) assuming a degree of freedom equal to 9 (k = 10 - 1 where 10 is the number of bins) requires a value of _X^2_ less than [16.919](https://people.richland.edu/james/lecture/m170/tbl-chi.html) to prove the null hypotesis (the randomness hypotesis in this case). The result here are fine for the standard Python function and quite terrible for the sine function:

```python
Chi-squared (standard) = 4.7686
Chi-squared (sine) = 14668.3238
```

### Kolmogorov–Smirnov test
[Kolmogorov–Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test): TBD

### Diehard tests
It is worth mentioning a battery of statistical tests for measuring the quality of a random number generator known as the [Diehard tests](https://en.wikipedia.org/wiki/Diehard_tests) that I didn't try.