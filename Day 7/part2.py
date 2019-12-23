class intcode:
  def __init__(self, intfile, inputs):
    self.index = 0
    self.inputs = inputs
    self.output = 0

    with open(intfile) as f:
      line = f.readline()
      self.ops = list(map(int, line.split(',')))

    full_command = self.ops[self.index]
    self.command = full_command % 100
    self.parameters = list(map(int, str(full_command // 100)))

  def has_inputs(self):
    return len(self.inputs) > 0

  def get_inputs(self):
    return self.inputs

  def add_input(self, new_input):
    self.inputs.append(new_input)

  def has_finished(self):
    return self.command == 99

  def get_output(self):
    return self.output

  def get_input(self):
    return self.inputs.pop(0)

  def get_parameter(self):
    if len(self.parameters) == 0:
      return 0
    else:
      return self.parameters.pop()

  def execute_next(self):
    if not self.has_finished():
      #print(self.command, self.parameters)
      if self.command == 1:
          # addition
          operand1 = self.ops[self.index+1]
          operand2 = self.ops[self.index+2]
          dest = self.ops[self.index+3]

          mode1 = self.get_parameter()
          mode2 = self.get_parameter()

          value1 = self.ops[operand1] if mode1 == 0 else operand1
          value2 = self.ops[operand2] if mode2 == 0 else operand2

          result = value1 + value2
          self.ops[dest] = result

          self.index += 4

      elif self.command == 2:
          # multiplication
          operand1 = self.ops[self.index+1]
          operand2 = self.ops[self.index+2]
          dest = self.ops[self.index+3]

          mode1 = self.get_parameter()
          mode2 = self.get_parameter()

          value1 = self.ops[operand1] if mode1 == 0 else operand1
          value2 = self.ops[operand2] if mode2 == 0 else operand2

          result = value1 * value2
          self.ops[dest] = result

          self.index += 4

      elif self.command == 3:
        # input
        operand = self.ops[self.index+1]

        result = self.inputs.pop(0)
        self.ops[operand] = result
        self.index += 2

      elif self.command == 4:
        # output
        operand = self.ops[self.index+1]

        self.output = self.ops[operand]
        self.index += 2

      elif self.command == 5:
        # jump if true (non-zero)
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        if value1 != 0:
          self.index = value2
        else:
          self.index += 3

      elif self.command == 6:
        # jump if false (zero)
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        if value1 == 0:
          self.index = value2
        else:
          self.index += 3

      elif self.command == 7:
        # less than
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]
        operand3 = self.ops[self.index+3]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        if value1 < value2:
          self.ops[operand3] = 1
        else:
          self.ops[operand3] = 0

        self.index += 4

      elif self.command == 8:
        # equal to
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]
        operand3 = self.ops[self.index+3]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        if value1 == value2:
          self.ops[operand3] = 1
        else:
          self.ops[operand3] = 0

        self.index += 4

      else:
          print("Unexpected operation:", self.ops[self.index])
          self.index += 1

      full_command = self.ops[self.index]
      self.command = full_command % 100
      self.parameters = list(map(int, str(full_command // 100)))

    else:
      print("Running a halted machine")

  def run_to_completion(self):
    while not self.has_finished():
      self.execute_next()
      return self.get_output()

def part2():
  intfile = "test2.txt"
  amp_a = intcode(intfile, [9, 0])
  amp_b = intcode(intfile, [7])
  amp_c = intcode(intfile, [8])
  amp_d = intcode(intfile, [5])
  amp_e = intcode(intfile, [6])

  while not amp_e.has_finished():
    while amp_a.has_inputs() and not amp_a.has_finished():
      print(amp_a.get_inputs(), amp_a.get_output())
      amp_a.execute_next()

    print("Amp A stalled with output:", amp_a.get_output())
    amp_b.add_input(amp_a.get_output())
    while amp_b.has_inputs() and not amp_b.has_finished():
      print(amp_b.get_inputs(), amp_b.get_output())
      amp_b.execute_next()

    print("Amp B stalled with output:", amp_b.get_output())
    amp_c.add_input(amp_b.get_output())
    while amp_c.has_inputs() and not amp_c.has_finished():
      print(amp_c.get_inputs(), amp_c.get_output())
      amp_c.execute_next()

    print("Amp C stalled with output:", amp_c.get_output())
    amp_d.add_input(amp_c.get_output())
    while amp_d.has_inputs() and not amp_d.has_finished():
      print(amp_d.get_inputs(), amp_d.get_output())
      amp_d.execute_next()

    print("Amp D stalled with output:", amp_d.get_output())
    amp_e.add_input(amp_d.get_output())
    while amp_e.has_inputs() and not amp_e.has_finished():
      print(amp_e.get_inputs(), amp_e.get_output())
      amp_e.execute_next()

    if not amp_e.has_finished():
      print("Amp E stalled with output:", amp_e.get_output())
      amp_a.add_input(amp_e.get_output())

  print(amp_e.get_output())

amp = intcode("test1-1.txt", [4,0])
output = amp.run_to_completion()
print(output)
amp.add_input(3)
amp.add_input(output)
output = amp.run_to_completion()
print(output)
amp.add_input(2)
amp.add_input(output)
output = amp.run_to_completion()
print(output)
amp.add_input(1)
amp.add_input(output)
output = amp.run_to_completion()
print(output)
amp.add_input(0)
amp.add_input(output)
output = amp.run_to_completion()
print(output)