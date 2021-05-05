import ItrDFS as DFS
def possibility_of_moving(current_state,From,To):
  try:
   peg_disk_from=current_state.d[From] # peg disk goes from
   peg_disk_to=current_state.d[To]   # peg disk goes to
   if peg_disk_from==[]: return False  # no disk to move.
   top_most_disk_from=peg_disk_from[-1]  # get topmost disk at From peg..
   if peg_disk_to==[]: return True # no disk to worry about at To peg.
   top_most_disk_to=peg_disk_to[-1]  # get topmost disk at To peg.
   if top_most_disk_from<top_most_disk_to: return True # Disk is smaller than one it goes on.
   return False # Disk too big for one it goes on.
  except (Exception) as e:
   print(e)

def moving_towards(state,From,To):
  new_state = state.__copy__() # start with a deep copy.
  state_diction = new_state.d # grab the new state's dictionary.
  peg_disk_from=state_diction[From] # peg disk goes from.
  disk_to_move=peg_disk_from[-1]  # the disk to move.
  state_diction[From]=peg_disk_from[:-1] # remove it from its old peg.
  state_diction[To]+=[disk_to_move] # Put disk onto destination peg.
  return new_state # return new state

def testing_goal(state):
  return state.d['peg1']==[] and state.d['peg2']==[] and state.d['peg3'] == []

def final_message(s):
  return "Hanoi Solved"

class using_operator:
  def __init__(self, name_beginning, pre_condition, post_state):
    self.name = name_beginning
    self.precond = pre_condition
    self.state_transf = post_state

  def is_applicable(self, state):
    return self.precond(state)

  def apply(self, state):
    return self.state_transf(state)

def h_hamming_dist(state):
  "Counts the number of disks not at the destination pole."
  last_pole = state.d['peg4']
  return _number_of_disks - len(last_pole)

def h_weighted_hamming(state):
  "Computes  theweighted sum of the number of disks not at the destination pole."
  last_pole = state.d['peg4']
  total_sum = 0
  for i in range(1,_number_of_disks+1):
    if not (i in last_pole): total_sum += i
  return total_sum


class Start():
  def __init__(self, d):
    self.d = d

  def __str__(self):
    d = self.d
    bracketholder = "|"
    for i, peg in enumerate(['peg1','peg2','peg3','peg4']):
      bracketholder += str(d[peg])
      if i<3: bracketholder += ","
    return bracketholder+"|"

  def __eq__(self, checker):
    if not (type(self)==type(checker)):
        return False
    P1 = self.d; P2 = checker.d
    return P1['peg1']==P2['peg1'] and P1['peg2']==P2['peg2'] and P1['peg3']==P2['peg3'] and P1['peg4']==P2['peg4']

  def __hash__(self):
    return (str(self)).__hash__()

  def __copy__(self):
    alert = Start({})
    for peg in ['peg1', 'peg2', 'peg3','peg4']:
      alert.d[peg]=self.d[peg][:]
    return alert


#_number_of_disks = int(input("enter number of disks"))
_number_of_disks = 5
initial_state = Start({'peg1': list(range(_number_of_disks,0,-1)), 'peg2':[], 'peg3':[],'peg4':[] })
initial_state_creation = lambda: initial_state
combination_of_pegs = [('peg'+str(first),'peg'+str(second)) for (first,second) in
                    [(1,2),(1,3),(1,4),(2,1),(2,3),(2,4),(3,1),(3,2),(3,4),(4,1),(4,2),(4,3)]]
available_operators = [using_operator("Move disk from "+comb1+" to "+comb2,
                      lambda state,first_comb=comb1,second_comb=comb2: possibility_of_moving(state,first_comb,second_comb),
                      lambda state,first_comb=comb1,second_comb=comb2: moving_towards(state,first_comb,second_comb) )
             for (comb1,comb2) in combination_of_pegs]
testing_final_goal = lambda state: testing_goal(state)
testing_final_goal_function = lambda state: final_message(state)

HEURISTICS = {'h_hamming_dist': h_hamming_dist, 'h_weighted_hamming':h_weighted_hamming}

