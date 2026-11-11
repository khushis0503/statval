# Statistical validation report: `data/mtcars.csv`

**Rows:** 32 | **Columns:** 12

## Numeric columns

| column | n | missing | mean | median | std | min | max | iqr | skewness | kurtosis | outliers | normality |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mpg | 32 | 0 | 20.09 | 19.2 | 6.027 | 10.4 | 33.9 | 7.375 | 0.6724 | -0.02201 | 1 | normal |
| cyl | 32 | 0 | 6.188 | 6 | 1.786 | 4 | 8 | 4 | -0.1923 | -1.763 | 0 | non-normal |
| disp | 32 | 0 | 230.7 | 196.3 | 123.9 | 71.1 | 472 | 205.2 | 0.4202 | -1.068 | 0 | non-normal |
| hp | 32 | 0 | 146.7 | 123 | 68.56 | 52 | 335 | 83.5 | 0.7994 | 0.2752 | 1 | non-normal |
| drat | 32 | 0 | 3.597 | 3.695 | 0.5347 | 2.76 | 4.93 | 0.84 | 0.2928 | -0.4504 | 0 | normal |
| wt | 32 | 0 | 3.217 | 3.325 | 0.9785 | 1.513 | 5.424 | 1.029 | 0.4659 | 0.4166 | 3 | normal |
| qsec | 32 | 0 | 17.85 | 17.71 | 1.787 | 14.5 | 22.9 | 2.008 | 0.4063 | 0.8649 | 1 | normal |
| vs | 32 | 0 | 0.4375 | 0 | 0.504 | 0 | 1 | 1 | 0.2645 | -2.063 | 0 | non-normal |
| am | 32 | 0 | 0.4062 | 0 | 0.499 | 0 | 1 | 1 | 0.4008 | -1.967 | 0 | non-normal |
| gear | 32 | 0 | 3.688 | 4 | 0.7378 | 3 | 5 | 1 | 0.5823 | -0.8953 | 0 | non-normal |
| carb | 32 | 0 | 2.812 | 2 | 1.615 | 1 | 8 | 2 | 1.157 | 2.02 | 1 | non-normal |

## Categorical columns

| column | n | missing | unique | top | top_freq |
|---|---|---|---|---|---|
| model | 32 | 0 | 32 | Mazda RX4 | 1 |

## Validation flags

- mpg: 1 IQR outlier(s)
- cyl: not normal (Shapiro p = 0.0000)
- disp: not normal (Shapiro p = 0.0208)
- hp: 1 IQR outlier(s)
- hp: not normal (Shapiro p = 0.0488)
- wt: 3 IQR outlier(s)
- qsec: 1 IQR outlier(s)
- vs: not normal (Shapiro p = 0.0000)
- am: not normal (Shapiro p = 0.0000)
- gear: not normal (Shapiro p = 0.0000)
- carb: 1 IQR outlier(s)
- carb: not normal (Shapiro p = 0.0004)
- carb: highly skewed (1.16)
- cyl ~ disp: strong correlation (r = 0.90)
- disp ~ wt: strong correlation (r = 0.89)
- mpg ~ wt: strong correlation (r = -0.87)
- mpg ~ cyl: strong correlation (r = -0.85)
- mpg ~ disp: strong correlation (r = -0.85)
- cyl ~ hp: strong correlation (r = 0.83)
- cyl ~ vs: strong correlation (r = -0.81)
