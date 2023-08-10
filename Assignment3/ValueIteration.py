import copy
import operator
grid = [
    [0, 1, -1],
    [0, 0, 0],
    [0, -2, 0],
    [0, 0, 0]
]

discount_factor = 0.95
step_cost = -0.04
prob_act = 0.7
prob_perp = 0.15

grid = [
    [0, 'absorb', 'sink'],
    [0, 0, 0],
    [0, 'wall', 0],
    [0, 0, 0]
]

utility = [
    [0, 1, -1],
    [0, 0, 0],
    [0, 'wall', 0],
    [0, 0, 0]
]

policy=[
    ["","-","-"],
    ["","",""],
    ["","wall",""],
    ["","",""]
]

def util_iteration(i, j):
    if(grid[i][j]=='absorb'):
        return 1
    elif(grid[i][j]=='sink'):
        return -1
    elif(grid[i][j]=='wall'):
        return 0
    
    utility_up= utility[i][j] if grid[max(0,i-1)][j]=='wall' else utility[max(0,i-1)][j]
    utility_down=utility[i][j] if grid[min(3,i+1)][j]=='wall' else utility[min(3,i+1)][j]
    utility_left=utility[i][j] if grid[i][max(0,j-1)]=='wall' else utility[i][max(0,j-1)]
    utility_right=utility[i][j] if grid[i][min(2,j+1)]=='wall' else utility[i][min(2,j+1)]

    curr_util_arr=[]
    expect_util_up= prob_act*utility_up + prob_perp*utility_left+prob_perp*utility_right
    curr_util_arr.append({
        'dir':'up',
        'val':expect_util_up
    })
    expect_util_down= prob_act*utility_down + prob_perp*utility_left+prob_perp*utility_right
    curr_util_arr.append({
        'dir':'down',
        'val':expect_util_down
    })
    expect_util_right= prob_act*utility_right + prob_perp*utility_up+prob_perp*utility_down
    curr_util_arr.append({
        'dir':'right',
        'val':expect_util_right
    })
    expect_util_left= prob_act*utility_left + prob_perp*utility_up+prob_perp*utility_down
    curr_util_arr.append({
        'dir':'left',
        'val':expect_util_left
    })
    curr_util_arr.sort(key=operator.itemgetter('val'),reverse=True)
    policy[i][j]=curr_util_arr[0]['dir']
    return step_cost + curr_util_arr[0]['val']*discount_factor
    # return step_cost + max(expect_util_down,expect_util_left,expect_util_right,expect_util_up)*discount_factor


error_val = float('inf')
max_error = 0.0001
iteration = 0
while (error_val > max_error):
    error_val=float('-inf')
    iteration += 1
    temp_utility = copy.deepcopy(utility)
    for i in range(4):
        for j in range(3):
            if(grid[3-i][j]=='wall'):
                continue
            temp_utility[3-i][j] = util_iteration(3-i, j)
            
            error_val= max(error_val,abs(temp_utility[3-i][j]-utility[3-i][j]))
    utility=copy.deepcopy(temp_utility)
    print("Iteration Number : ", iteration)
    for i in range(4):
        for j in range(3):
            print(utility[i][j]," ",end="")
        print()
    print()

print("Policy : ")
for i in range(4):
    for j in range(3):
        print(policy[i][j]," ",end="\t")
    print()