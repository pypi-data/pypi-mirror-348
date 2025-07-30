def Binary_search(arr,l,r,n):
    if r >= l:
        mid = (l+r)//2
        if arr[mid] == n:
            print("step")
            return mid
        elif n > arr[mid]:
            print("step")
            return Binary_search(arr,mid+1,r,n)
        else:
            print("step")
            return Binary_search(arr,l,mid-1,n)
    else:
        return -1
    
arr = list(map(float,input("Enter values:  ").split()))
target = float(input("Enter value to search: "))

b = Binary_search(arr,0,len(arr)-1,target)

if b != -1:
    print(f"{target} found at {b+1} position in array {arr}")
else:
    print(f"{target} not found in the data")