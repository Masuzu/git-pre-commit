class LineTransformerPlugin:
  """
  Input
    line from one of the staged files
  Return a transformed line which will be used instead
  """
  def process_line(self, line):
    return line

class TrailingSpaceCleaner(LineTransformerPlugin):
  def process_line(self, line):
    return line.rstrip()
