
#imports
import time
start_time = time.time()
import TowerOfHanoi as Hanoi
heuristics = lambda s: Hanoi.HEURISTICS['h_weighted_hamming'](s)
heuristics.__name__ = 'h_weighted_hamming'
heuristics2 = lambda s: Hanoi.HEURISTICS['h_hamming_dist'](s)
heuristics2.__name__ = 'h_hamming_dist'
Backtrack = {}
Priority = []   

#Initializing the A star algorithm
def startAlgorithmAStar():
    #Getting the default formation of the disks from the Hanoi four poles with N disks at pole 1
    original_hanoi_state = Hanoi.initial_state_creation()
    global Path_States, Backtrack
    Path_States = 0
    Backtrack = {}
    print("Original postions of disks in the first pole for four poles tower of hanoi:\n",original_hanoi_state)
    full_path, name_of_heu = AStarSearch(original_hanoi_state)
    print(str(Path_States)+" states tracked using",heuristics2.__name__ )
    return full_path, name_of_heu

# A star search algorithm
def AStarSearch(original_hanoi_state):
    global Path_States, Backtrack
    # Puting the original_hanoi_state in Priorityority queue  and setting the order of disks based on size
    Start_Search = []
    Stop_Search = []
    Backtrack[original_hanoi_state] = -1
    Start_Search.append(original_hanoi_state)
    Priority.append(0)
    Steps = {}
    Cost = {}
    Steps[original_hanoi_state] = 0

    while len(Start_Search) > 0:
        current_position = MinPath()
        Starting_search = Start_Search[current_position]
        del Start_Search[current_position]
        del Priority[current_position]
        while Starting_search in Stop_Search:
            current_position = MinPath()
            Starting_search = Start_Search[current_position]
            del Start_Search[current_position]
            del Priority[current_position]
        Stop_Search.append(Starting_search)
        
        # Checking Goals
        if Hanoi.testing_final_goal(Starting_search):
            print(Hanoi.testing_final_goal_function(Starting_search))
            path = backtrace(Starting_search)
            return path, Hanoi
        
        Path_States += 1
        for operator in Hanoi.available_operators:
            if operator.precond(Starting_search):
                new_state = operator.state_transf(Starting_search)
                if not (new_state in Start_Search) and not (new_state in Stop_Search):
                    Steps[new_state] = Steps[Starting_search] + 1
                    Cost[new_state] = Steps[new_state] + heuristics2(new_state)
                    Backtrack[new_state] = Starting_search
                    Start_Search.append(new_state)
                    Priority.append(Cost[new_state])
                elif Backtrack[new_state] != -1:
                    other_possible_parent = Backtrack[new_state]
                    temporary = Cost[new_state]-Steps[other_possible_parent]+Steps[Starting_search]
                    if temporary < Cost[new_state]:
                        Steps[new_state] = Steps[new_state]-Cost[new_state]+temporary
                        Cost[new_state] = temporary
                        Backtrack[new_state] = Starting_search
                        if new_state in Stop_Search:
                            Start_Search.append(new_state)
                            Priority.append(Cost[new_state])
                            Stop_Search.remove(new_state)

def MinPath():
    min = Priority[0]
    current_position = 0
    for i in range(len(Priority)):
        if Priority[i] < min:
            min = Priority[i]
            current_position = i
    return current_position


def backtrace(trace):
    global Backtrack
    path = []
    while not trace == -1:
        path.append(trace)
        trace = Backtrack[trace]
    path.reverse()
    print("Graph Path: ")
    for graphs in path:
        print(graphs)
    print("\nPath length = "+str(len(path)-1))
    return path    

if __name__=='__main__':
    path, name = startAlgorithmAStar()
    print(Hanoi._number_of_disks,"            ",time.time() - start_time)
