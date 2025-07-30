code = '''
mport pandas as pd 
from statsmodels.multivariate.manova import MANOVA 
 
alpha = float(input("Enter level of Significance: ")) 
data = { 
    'Treatment': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'], 
    'BloodPressure':[120, 123, 131, 124, 126, 127, 129, 125, 123], 
    'Heartrate':[81, 78, 92, 83, 79, 80, 86, 88, 87] 
} 
df = pd.DataFrame(data) 
 
manova = MANOVA.from_formula('BloodPressure + Heartrate ~ Treatment', data=df) 
res = manova.mv_test() 
 
pval = res.results['Treatment']['stat']['Pr > F']['Wilks\' lambda'] 
print(f"P Value: {pval:.4f}",) 
if pval < alpha: 
    print("Reject Null Hypothesis") 
else: 
    print("Accept Null Hypothesis") 


-------------------------------------------------


import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

X = np.array([
    [1, 2], 
    [2, 3],
    [3, 4],
    [4, 5], 
    [5, 6],
    [6, 7]
])
y = np.array([0, 0, 0, 1, 1, 1])

lda = LinearDiscriminantAnalysis(n_components=1)
lda.fit(X, y)

new_sample = np.array([[5, 7]])
predicted_class = lda.predict(new_sample)

print("===== LDA Classification Result (Deterministic) =====")
print(f"New Observation: {new_sample.flatten()}")
print(f"Predicted Class: {predicted_class}")

'''

def getCode():
    global code
    print(code)
    