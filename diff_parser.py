import os
import subprocess

from collections import defaultdict
from collections import namedtuple
from enum import Enum

class ErrorType(Enum):
  TRAILING_WHITE_SPACE = 1
  UNKNOWN = 2

Difference = namedtuple("Difference", ["file", "line", "error"])

def parse_error(error):
  if error.startswith("trailing whitespace"):
    return ErrorType.TRAILING_WHITE_SPACE
  return ErrorType.UNKNOWN

def identify_git_diff_check_issue(line):
  (file, line, error) = tuple(map(str.strip, line.split(":")))
  return Difference(file, int(line), parse_error(error))

def find_differences_to_fix():
  """
  Return a dictionary of namedtuple("Difference", ["file", "line", "error"]) indexed by file name
  """
  p = subprocess.Popen("git diff --check --cached", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

  # Differences returned by git diff can only include added lines  
  differences_per_files = defaultdict(list)
  for line in p.stdout.readlines():
    if line.startswith("+"):
      continue
    diff = identify_git_diff_check_issue(line)
    differences_per_files[diff.file].append(diff)
  return differences_per_files

def find_files_with_differences():
  """
  Return a list of staged files
  """
  p = subprocess.Popen("git diff --cached", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  files_with_differences = []
  for line in p.stdout.readlines():
    if line.startswith("+++ b/"):
      files_with_differences.append(os.path.join(".", line[len("+++ b/"):].strip()))
  return files_with_differences
