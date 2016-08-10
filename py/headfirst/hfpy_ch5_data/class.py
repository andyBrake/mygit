class Athlete:
    def __init__(self, name, dob=None, times=None):
        self.name = name
        self.dob = dob
        self.times = times

sarah = Athlete("sarah")
print(sarah.name)
print(sarah.dob)
print(sarah.times)

sarah.times = [1,3]
print(sarah.times)


class Namelist(list):
    def __init__(self, name=None):
        list.__init__([])
        self.name = name
        
