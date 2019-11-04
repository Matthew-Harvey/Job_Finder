import random

class complex: # replacing all possible in-built functions with calculations

    class ording:
        def __init__(self, value):
            self.__value = value
        
        def findord(self):
            return ord(self.__value)

    class append:
        def __init__(self, array, value):
            self.__array = array # private access modifiers
            self.__value = value

        def concat(self):
            self.__array = self.__array + [self.__value]
            return self.__array

        def insert(self, pos):
            self.__postition = pos
            self.__array = self.__array[:pos] + [self.__value] + self.__array[pos:]
            return self.__array

    class randomint:
        def __init__(self, min, max):
            self.__min = min
            self.__max = max
            self.__allvalues = []

        def prob(self, place):
            self.__place = place
            self.__int = "0." + "0"*place
            self.__int = str(self.__int)
            for t in range(2, self.__place+2):
                self.__temp = random.randint(0, 9)
                self.__temp = str(self.__temp)
                self.__int = self.__int[:t] + self.__temp + self.__int[t+1:]
            return float(self.__int)

        def calculate(self):
            for x in range(self.__min, self.__max):
                self.__allvalues = complex.append(self.__allvalues, x).concat()
            return self.__allvalues[random.randint(self.__min, self.__max)]

    class sort:
        def __init__(self, array):
            self.__count = 0
            self.__array = array
            self.__sort1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            self.__sort2 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
            self.__static = []
            self.__allstatic = []
            self.__final = []
            self.__test = False
            self.__rep = []

        #class bubble(self):
            #def ints(self):

        def nums(self):
            while self.__test == False:
                self.__repeat = 0
                for y in range(0, len(self.__array)):
                    for x in range(0, len(self.__array)):
                        try:
                            self.__num = self.__array[x]
                            self.__num = int(self.__num)
                            self.__num2 = self.__array[x+1]
                            self.__num2 = int(self.__num2)
                            if self.__num >= self.__num2:
                                self.__array[x] = self.__num2
                                self.__array[x+1] = self.__num
                                self.__test = False
                            else:
                                self.__repeat = self.__repeat+1
                        except:
                            self.__test = False
                self.__len = len(self.__array)/2
                self.__len = int(self.__len)+1
                if self.__repeat >= self.__len:
                    self.__test = True
            return self.__array

        def alpha(self):
            for word in self.__array:
                self.__static = []
                for letter in word:
                    for y in range(0, len(self.__sort2)):
                        if self.__sort2[y] == letter:
                            self.__static.append(int(y))
                self.__allstatic.append(self.__static)
            self.__one = []
            for c in range(0, len(self.__allstatic)):
                self.__one.append(self.__allstatic[c][0])
            self.__one = complex.sort(self.__one).nums()
            for u in range(0, len(self.__one)):
                for h in range(0, len(self.__allstatic)):
                    if self.__allstatic[h][0] == self.__one[u]:
                        if self.__array[h] not in self.__final:
                            self.__final.append(self.__array[h])
            self.__firsts = []
            for item in self.__final:
                if item not in self.__firsts:
                    self.__firsts.append(item[0])
                
            return self.__final
                
    class up_down:
        def __init__(self, char):
            self.__char = char
            self.__alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
            self.__z = True

        def down(self):
            for v in range(0, len(self.__alpha)):
                if self.__alpha[v] == self.__char:
                    if v > 26:
                        self.__z = False
                        return self.__alpha[v-26]
            if self.__z == True:
                return self.__char

        def up(self):
            for v in range(0, len(self.__alpha)):
                if self.__alpha[v] == self.__char:
                    if v < 27:
                        self.__z = False
                        return self.__alpha[v+26]
            if self.__z == True:
                return self.__char

    class delete:
        def __init__(self, array, pos):
            self.__pos = pos
            self.__array = array
        
        def _del(self):
            self.__array = self.__array[:self.__pos] + self.__array[self.__pos+1:]
            return self.__array

    class reverse:
        def __init__(self, array):
            self.__array = array
            self.__newarray = []
            self.__len = len(array)
            self.__iter = 1

        def swap(self):
            for item in self.__array:
                self.__newarray = complex.append(self.__newarray, self.__array[self.__len - self.__iter]).concat()
                self.__iter = self.__iter + 1
            return self.__newarray

    class pop:
        def __init__(self, array):
            self.__pos = len(array)-1
            self.__array = array
            self.__temp = array
        
        def last(self):
            self.__array = complex.delete(self.__array, self.__pos)._del()
            return self.__array, self.__temp[self.__pos]

    class strip:
        def __init__(self, string):
            self.__string = str(string)
            self.__set = True

        def trailorfront(self):
            return self.__string

    class lencalc:
        def __init__(self, string):
            self.__string = string
            self.__iter = 0

        def calc(self):
            try:
                for char in self.__string:
                    self.__iter = self.__iter + 1
            except:
                self.__string = str(self.__string)
                self.__iter = complex.lencalc(self.__string).calc()
            return self.__iter

    class replace:
        def __init__(self, char, string):
            self.__string = string
            self.__char = char
            self.__newstring = ""
        
        def chars(self):
            skip = False
            for letter in self.__string:
                if letter == self.__char:
                    skip = True
                if skip == False:
                    self.__newstring = self.__newstring + letter
                skip = False
            return self.__newstring

#for y in range(0, 100):
    #print(complex.randomint(0, 1).prob(6))
#print(complex.lencalc(3536).calc())
#print(complex.strip("teseet").trailorfront())
print(complex.sort(["abcs", "poP", "q", "Queen", "strong", "tuple", "poop", "aBcd", "wow"]).alpha())
