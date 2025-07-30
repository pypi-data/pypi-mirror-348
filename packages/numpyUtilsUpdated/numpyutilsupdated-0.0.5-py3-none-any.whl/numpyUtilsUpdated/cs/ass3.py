code = """
import scipy.stats as stat 
 
alpha = float(input("Enter the level of Significance: ")) 
n = int(input("Enter no. of samples: ")) 
sizes = list(map(int, input("Enter each Sample length: ").split())) 
data = [list(map(int, input(f"Enter values of List{i + 1} ").split())) for i in range(n)] 
 
N = (sum(sizes)) 
ti = [sum(lst) for lst in data] 
G = sum(ti) 
cor_fact = G**2 / N 
 
Tot_sum = sum(x**2 for group in data for x in group) 
ti_ri_sum = sum(t**2/r for t, r in zip(ti, sizes)) 
 
TreatSS = ti_ri_sum - cor_fact 
TotalSS = Tot_sum - cor_fact 
ErrorSS = TotalSS - TreatSS 
 
df_treat = n - 1 
df_err = N - n 
 
MS_treat = TreatSS / df_treat 
MS_err = ErrorSS / df_err 
 
F_Ra = round(MS_treat/ MS_err, 4) 
F_ta = round(stat.f.ppf(1-alpha, df_treat, df_err), 4) 
 
print(F_Ra) 
print(F_ta) 
 
if F_Ra <= F_ta: 
    print("Accept Null Hypothesis") 
else: 
    print("Reject Null Hypothesis") 

---------------------------------------------------------------------------
Question_2 

import scipy.stats as stat 
 
alpha = float(input("Enter level of Significance: ")) 
t = int(input("Enter no.of rows: ")) 
b = int(input("Enter no.of columns: ")) 
 
rows = [list(map(int, input(f"Enter elements of Row{i + 1}").split())) for i in range (t)] 
 
N = t * b 
G = sum(sum(row) for row in rows) 
Tot_sum = sum(i ** 2 for row in rows for i in row) 
ti_ri_sum = sum(sum(row)**2 for row in rows) 
bi_ri_sum = 0 
for i in range(b): 
    col_sum = sum(rows[j][i] for j in range(t)) 
    bi_ri_sum += col_sum ** 2 
 
cor_fact = G**2 / N 
 
TreatSS = ti_ri_sum / b - cor_fact 
BlockSS = bi_ri_sum / t - cor_fact 
TotalSS = Tot_sum - cor_fact 
ErrorSS = TotalSS - TreatSS - BlockSS 
 
df_block = b - 1 
df_treat = t - 1 
df_error = N - b - t + 1 
 
MSS_block = BlockSS/ df_block 
MSS_treat = TreatSS / df_treat 
MSS_error = ErrorSS / df_error 
 
fBlock = round(MSS_block / MSS_error, 4) 
fTreat = round(MSS_treat / MSS_error, 4) 
fcritic_block = round(stat.f.ppf(1-alpha, df_block, df_error),4) 
fcritic_treat = round(stat.f.ppf(1-alpha, df_treat, df_error),4) 
 
print(fBlock) 
print(fTreat) 
print(fcritic_block) 
print(fcritic_treat)         

"""


def getCode():
    global code
    print(code)
