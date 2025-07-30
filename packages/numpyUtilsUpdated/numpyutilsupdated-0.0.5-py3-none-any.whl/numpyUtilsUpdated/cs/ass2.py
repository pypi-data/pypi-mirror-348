code = '''
x = list(map(int, input("Enter x coordinates : ").split()))
y = list(map(int, input("Enter y coordinates : ").split()))


xy_list = [x * y for x, y in zip(x, y)]
x2_list = [x ** 2 for x in x]
y2_list = [y ** 2 for y in y]


x_mean = sum(x) / len(x)
y_mean = sum(y) / len(y)


cov_x_y = (sum(xy_list) / len(x)) - (x_mean * y_mean)


sigma_x = ((1 / len(x)) * sum(x2_list) - (x_mean ** 2)) ** 0.5  
sigma_y = ((1 / len(y)) * sum(y2_list) - (y_mean ** 2)) ** 0.5


karl_coeff = cov_x_y / (sigma_x * sigma_y)
print(f"Karl pearson correlation of coefficient is : {karl_coeff:.4f}")

Output : 
Z:\Y23CM012\work_cs> python .\karl_pearson_correlation_coefficient.py
Enter x coordinates : 65 66 67 67 68 69 70 72 
Enter y coordinates : 67 68 65 68 72 72 69 71
Karl pearson correlation of coefficient is : 0.6030

-----------------------------------------------------------------------
Question_2

def ranking(val_lst):
    lst = sorted(val_lst)
    rank = []
    for x in val_lst:
        val = lst.index(x) + 1
        rank.append(val)
    return rank


x_list = list(map(int, input("Enter the Values of x : ").split()))
y_list = list(map(int, input("Enter the Values of y : ").split()))


rank_x = ranking(x_list)
rank_y = ranking(y_list)


di = [i - j for i, j in zip(rank_x, rank_y)]
di_2 = [i ** 2 for i in di]


n = len(x_list)
Cor_coeff = 1 - ((6 * sum(di_2)) / (n ** 3 - n))


print(f"The Spearsman Correlation Coeff. is {Cor_coeff:.4f}")

Output : 
Z:\Y23CM012\work_cs> python .\spearman_correaltion_coefficient.py
Enter the Values of x : 72 35 63 76 57 42 59 66 74 68
Enter the Values of y : 68 44 74 71 62 51 65 78 59 37
The Spearsman Correlation Coeff. is 0.3455

'''

def getCode():
    global code
    print(code)
