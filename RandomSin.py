# %%
import math
import time
import statistics
import plotly.express as px
import plotly.subplots as sp
from plotly.offline import plot
import random
import pandas as pd 

#
# Get x value from an index
def get_x(idx):
  idx = abs(idx)
  if idx == 0:
    idx = idx + 1
  
  # the range where sin(1 / x) presents a chaotic behavior is with a very small x
  return idx / 10000000
  
#
# Random generation based on sine
def get_rnd(seed, idx):
  x = get_x(idx)
  res = math.sin(seed / x)
  if res < 0:
    res = 1 + res # the 'abs' would be even worse
  return res

#
# Class to handle the random generation
class MyRnd:
  def __init__(self, seed) -> None:
    MAX_NUMS = 100000 # maximum number of random values
    
    self.seed = seed
    if self.seed == 0: # seed 0 is not accepted
      self.seed == 1

    # random values
    self.rnd_nums = []
    for idx in range(MAX_NUMS):
      self.rnd_nums.append(get_rnd(seed, idx))
    
    self.rnd_idx = 0 # index of the generated random values
  
  #
  # random double between 0 and 1
  def random(self):
    if self.rnd_idx >= len(self.rnd_nums):
      raise Exception("Sorry, no more number available") 
    res = self.rnd_nums[self.rnd_idx]
    self.rnd_idx = self.rnd_idx + 1
    return res
  
  #
  # random integer between min and max
  def randint(self, min, max):
    OldValue = self.random()
    OldMax = 1
    OldMin = 0
    OldRange = (OldMax - OldMin)  
    NewRange = (max + 1 - min)  
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + min
    return math.floor(NewValue)

#
# Wald–Wolfowitz runs test - https://en.wikipedia.org/wiki/Wald%E2%80%93Wolfowitz_runs_test
def wwRunsTest(vals):
  median = statistics.median(vals)
  runs = 0
  nPos = 0
  nNeg = 0

  for i in range(len(vals)):
    # the randomness of a distribution, by taking the data in the given order and marking 
    # with + the data greater than the median, and with – the data less than the median 
    # (numbers equalling the median are omitted.)
    if abs(vals[i] - median) < 0.001:
      continue
    
    if (vals[i] >= median and vals[i-1] < median) or (vals[i] < median and vals[i-1] >= median):
      runs = runs + 1
    
    if vals[i] >= median:
      nPos = nPos + 1
    else:
      nNeg = nNeg + 1

  runs_exp = ((2 * nPos * nNeg) / (nPos + nNeg)) + 1
  stan_dev = math.sqrt((2 * nPos * nNeg * (2 * nPos * nNeg - (nPos + nNeg))) / (((nPos + nNeg) ** 2) * ((nPos + nNeg) - 1)))

  # https://en.wikipedia.org/wiki/Standard_score#Standardizing_in_mathematical_statistics
  z = (runs - runs_exp) / stan_dev
  return abs(z)

#
# Chi-squared test - https://en.wikipedia.org/wiki/Chi-squared_test - https://www.youtube.com/watch?v=PiS0Fm-_xrw
def chiSquaredTest(vals):
  k = 10 - 1 # 9 degrees of freedom
  exp = len(vals) / 10
  df = pd.DataFrame({'val' : vals})
  chisquared = 0
  for obs in df['val'].value_counts(bins = 10, sort = False):
    chisquared = chisquared + ((obs - exp)**2 / exp)
  
  return chisquared
  
#
# Main
#

# %% 
# 1. Show the sine function with seed 1
items = list(range(0, 10000, 1))
dfX = [get_x(idx) for idx in items]
dfY = [get_rnd(1, idx) for idx in items]
df = pd.DataFrame(
    {
        "x": dfX,
        "y": dfY
    })
px.line(df, "x", "y", title="y = sin(1 / x)")

# %%
# 2. Prepare random data with seed set on the time
seed = time.time()
myrnd = MyRnd(seed)
s = ''
myvals = []
stdvals = []
for i in range(100000):
  val = myrnd.random()
  myvals.append(val)
  stdvals.append(random.random())
  s = s + str(val) + ', '
#print(s)

#fig1 = px.histogram(myvals, nbins=10, title='10 bin histogram of my random value')
#fig2 = px.histogram(stdvals, nbins=10, title='10 bin histogram of standard random value')
#figures = [fig1, fig2]
#
#fig = sp.make_subplots(rows=1, cols=len(figures))
#for i, figure in enumerate(figures):
#    for trace in range(len(figure["data"])):
#        fig.append_trace(figure["data"][trace], row=1, col=i+1)
#        
#plot(fig)

# %%
# 3. Histogram of standard random function
px.histogram(stdvals, nbins=10, title='10 bin histogram of standard random value')

# %%
# 4. Histogram of sine random function
px.histogram(myvals, nbins=10, title='10 bin histogram of sine random value')

# %%
# Run tests
print("| Z | = " + str(wwRunsTest(myvals)))
print("Z (ref) = 1.96")

# %%
# Chi-squared tests
print("Chi-squared (std) = " + str(chiSquaredTest(stdvals)))
print("Chi-squared (sine) = " + str(chiSquaredTest(myvals)))
print("Chi-squared (ref) = 16.919")



# %%
# Test on integer values
myrnd = MyRnd(seed)
s = ''
ls = []
for i in range(10):
  val = myrnd.randint(0, 10)
  ls.append(val)
  s = s + str(val) + ', '
#print(s)

