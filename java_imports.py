import itertools
import re

from collections import defaultdict
from collections import deque

try:
    set
except NameError:
    from sets import Set as set 
  
BLANK_LINE = "<blank_line>"
# Assumes that each import falls in at least one of the defined RULES
RULES = [
  "java*",
  BLANK_LINE,
  "com*",
  "*",
  BLANK_LINE,
  "com.mycompany*",
  BLANK_LINE,
  "import static*"
]

def build_rule_precendence_graph(rules):
  """
  Return a graph defining in which order the RULES should be parsed when multiple of them apply to the input.
  For instance, both the RULES "*" and "com.*" apply to "com.foo" but "com.*" will
  have precedence since it is more qualified.
  """
  sanitized_rules = set([rule.strip() for rule in rules if rule != BLANK_LINE])
  if "*" not in sanitized_rules:
    sanitized_rules.add("*")

  rule_precedence = { rule: set() for rule in sanitized_rules }

  # If rule B is in rule_precedence[A] then B has precedence over A
  for rule_1, rule_2 in itertools.permutations(sanitized_rules, 2):
    if re.search(rule_1.replace(".", "\.").replace("*", ".*"), rule_2) is not None:
      rule_precedence[rule_1].add(rule_2)
  return rule_precedence

def reorganize_imports(imports, rules = RULES):
  """
  Return list of reorganized imports
  """
  rule_precedence = build_rule_precendence_graph(rules)
  reorganized_imports = { rule: [] for rule in rule_precedence.keys() }
  # Find for each import the rule to apply
  for imp in imports:
    rules_to_check = deque()
    for rule in rule_precedence.keys():
      if re.search(rule.replace(".", "\.").replace("*", ".*"), imp) is not None:
        rule_to_apply = rule
        for sub_rule in rule_precedence[rule]:
          rules_to_check.append(sub_rule)
        break
    while rules_to_check:
      rule = rules_to_check.popleft()
      if re.search(rule.replace(".", "\.").replace("*", ".*"), imp) is not None:
        rule_to_apply = rule
        for sub_rule in rule_precedence[rule]:
          rules_to_check.append(sub_rule)
    reorganized_imports[rule_to_apply].append(imp)

  for rule in reorganized_imports:
    reorganized_imports[rule] = sorted(reorganized_imports[rule])
  
  new_imports = []
  for rule in rules:
    if rule == BLANK_LINE:
      new_imports.append("")
    else:
      for imp in reorganized_imports[rule]:
        new_imports.append(imp)
  return new_imports