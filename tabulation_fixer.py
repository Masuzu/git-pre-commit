from collections import defaultdict

def infer_number_of_spaces_per_tabulation(lines):
  starting_spaces = defaultdict(int)
  for line in lines:
    num_starting_spaces = 0
    for i, c in enumerate(line):
      num_starting_spaces = i
      if c != " ":
        break
    starting_spaces[num_starting_spaces] += 1
  print(starting_spaces)