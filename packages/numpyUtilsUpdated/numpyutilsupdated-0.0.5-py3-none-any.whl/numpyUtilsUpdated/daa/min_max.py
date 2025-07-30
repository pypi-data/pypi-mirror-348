def max_min(arr, low, high):
    if low == high:
        return arr[low], arr[high]
    elif low == high - 1:
        if arr[low] > arr[high]:
            return arr[low], arr[high]
        else:
            return arr[high], arr[low]
    else:
        mid = (low + high) // 2
        max1, min1 = max_min(arr, low, mid)
        max2, min2 = max_min(arr, mid + 1, high)
        return max(max1, max2), min(min1, min2) 

arr = list(map(int,input("Enter List elements: ").split()))
max_v, min_v = max_min(arr, 0, len(arr) -1)
print(f"Maximum: {max_v}  Minimum: {min_v}")

code = '''
def max_min(arr, low, high):
    if low == high:
        return arr[low], arr[high]
    elif low == high - 1:
        if arr[low] > arr[high]:
            return arr[low], arr[high]
        else:
            return arr[high], arr[low]
    else:
        mid = (low + high) // 2
        max1, min1 = max_min(arr, low, mid)
        max2, min2 = max_min(arr, mid + 1, high)
        return max(max1, max2), min(min1, min2) 

arr = list(map(int,input("Enter List elements: ").split()))
max_v, min_v = max_min(arr, 0, len(arr) -1)
print(f"Maximum: {max_v}  Minimum: {min_v}")
'''

def getCode():
    global code
    print(code)
