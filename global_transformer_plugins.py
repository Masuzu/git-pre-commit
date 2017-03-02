import java_imports
import tabulation_fixer

from collections import defaultdict
from java_imports import BLANK_LINE
from sets import Set


class GlobalTransformerPlugin:
  def process_lines(self, lines, file):
    """
    Inputs
      file name of a staged file
      line list of lines from this staged file
    Return a transformed list of lines which will be used instead
    """
    return lines

  def process(self, file):
    lines = []
    with open(file, "r") as input_file:
      lines = input_file.readlines()
    return self.process_lines(lines, file)

class ImportOrganizerPlugin(GlobalTransformerPlugin):
  
  JAVA_RULES = [
    "java*",
    BLANK_LINE,
    "*",
    BLANK_LINE,
    "com.mycompany*",
    BLANK_LINE,
    "import static*"
  ]
  
  SCALA_RULES = [
    "java*",
    BLANK_LINE,
    "scala*",
    BLANK_LINE,
    "*",
    BLANK_LINE,
    "com.mycompany*",
    BLANK_LINE,
    "import static*"
  ]

  def process_java_source_file(self, lines, rules):
    imports = []
    for line in lines:
      if line.strip().startswith("package"):
        package_declaration = line.strip()
      elif line.strip().startswith("import"):
        imports.append(line.strip())
    reorganized_imports = java_imports.reorganize_imports(imports, rules)
    
    fixed_lines = []
    for line in lines:
      if line.strip().startswith("package"):
        fixed_lines.append(package_declaration)
        fixed_lines.append("")
        for imp in reorganized_imports:
          fixed_lines.append(imp)
      elif line.strip().startswith("import"):
        continue
      else:
        fixed_lines.append(line)
    return fixed_lines

  def process_lines(self, lines, file):
    if file.endswith(".java"):
      print "Processing java file " + file
      return self.process_java_source_file(lines, self.JAVA_RULES)
    if file.endswith(".scala"):
      print "Processing scala file " + file
      return self.process_java_source_file(lines, self.SCALA_RULES)
    return lines

class TabulationFixer(GlobalTransformerPlugin):
  def process_lines(self, lines, file):
    tabulation_fixer.infer_number_of_spaces_per_tabulation(lines)
    return lines