def partition(arr, low, high):
    pivot = arr[0]
    i = low
    j = high
    while True:
        while i <= j and arr[i] <= pivot:
            i += 1
        while i <= j and arr[j] > pivot:
            j -= 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else: 
            break
    arr[low], arr[j] = arr[j], arr[low]
    return j

def quicksort(arr, low, high):
    if low < high:
        pivot_i = partition(arr, low, high)
        quicksort(arr, low, pivot_i - 1)       
        quicksort(arr, pivot_i + 1, high)       

if __name__ == "__main__":
    arr = list(map(int,input("Enter array values: ").split()))
    print("Before Sorting: ", arr)
    quicksort(arr,0,len(arr)-1)
    print("After Sorting: ", arr)

code = '''
def partition(arr, low, high):
    pivot = arr[0]
    i = low
    j = high
    while True:
        while i <= j and arr[i] <= pivot:
            i += 1
        while i <= j and arr[j] > pivot:
            j -= 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else: 
            break
    arr[low], arr[j] = arr[j], arr[low]
    return j

def quicksort(arr, low, high):
    if low < high:
        pivot_i = partition(arr, low, high)
        quicksort(arr, low, pivot_i - 1)       
        quicksort(arr, pivot_i + 1, high)       

if __name__ == "__main__":
    arr = list(map(int,input("Enter array values: ").split()))
    print("Before Sorting: ", arr)
    quicksort(arr,0,len(arr)-1)
    print("After Sorting: ", arr)
'''

def getCode():
    global code
    print(code)
    