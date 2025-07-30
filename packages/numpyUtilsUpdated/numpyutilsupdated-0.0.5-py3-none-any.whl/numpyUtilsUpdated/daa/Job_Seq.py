class Job:
    def __init__(self, id, deadline, profit):
        self.id = id
        self.deadline = deadline
        self.profit = profit
        
def Job_schedulling(arr):
    arr.sort(key = lambda x: x.profit, reverse = True)
    sum = 0
    
    max_deadline = max(jb.deadline for jb in arr)
    
    result = [None] * max_deadline
    slot = [False] * max_deadline
    for job in arr:
        for j in range(min(max_deadline, job.deadline) -1, -1, -1):
            if not slot[j]:
                result[j] = job.id
                slot[j] = True
                sum += job.profit
                break
    
    print(f"Job Sequence: {result}")
    print(slot)
    print(f"Total profit: {sum}")
    
if __name__ == "__main__":
    
    # arr = [ Job('a', 3, 100), Job('b', 4, 80), Job('c', 2, 60), Job('d', 1, 40), Job('e', 2, 20)]
    arr = [ Job('a', 3, 100), Job('b', 4, 80), Job('e', 2, 20)]
    Job_schedulling(arr)


code = '''
class Job:
    def __init__(self, id, deadline, profit):
        self.id = id
        self.deadline = deadline
        self.profit = profit
        
def Job_schedulling(arr):
    arr.sort(key = lambda x: x.profit, reverse = True)
    sum = 0
    
    max_deadline = max(jb.deadline for jb in arr)
    
    result = [None] * max_deadline
    slot = [False] * max_deadline
    for job in arr:
        for j in range(min(max_deadline, job.deadline) -1, -1, -1):
            if not slot[j]:
                result[j] = job.id
                slot[j] = True
                sum += job.profit
                break
    
    print(f"Job Sequence: {result}")
    print(slot)
    print(f"Total profit: {sum}")
    
if __name__ == "__main__":
    
    # arr = [ Job('a', 3, 100), Job('b', 4, 80), Job('c', 2, 60), Job('d', 1, 40), Job('e', 2, 20)]
    arr = [ Job('a', 3, 100), Job('b', 4, 80), Job('e', 2, 20)]
    Job_schedulling(arr)
'''

def getCode():
    global code
    print(code)
    