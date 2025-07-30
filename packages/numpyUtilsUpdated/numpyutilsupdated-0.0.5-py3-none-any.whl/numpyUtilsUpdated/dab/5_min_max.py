code="""
def min_max(arr, low, high): 
    if low == high: 
        return arr[low], arr[low] 
    elif high == low + 1: 
        return (arr[low], arr[high]) if arr[low] < arr[high] else (arr[high], arr[low]) 
    else: 
        mid = (low + high) // 2 
        min1, max1 = min_max(arr, low, mid) 
        min2, max2 = min_max(arr, mid + 1, high) 
        return min(min1, min2), max(max1, max2) 

n = int(input("Enter size of array: ")) 
arr = list(map(int, input("Enter array: ").split())) 
minimum, maximum = min_max(arr, 0, n - 1) 
print(f"Maximum element: {maximum}") 
print(f"Minimum element: {minimum}")
"""
