import random # generating random probabilities or integers in a range

#
# in builts used to test efficency of some methods such as strip(), remove() etc. 
# this is mainly un-used in my final product as it often resulted in no visable difference, but its included because it was done as an attempt to optimize some processes
#

class ording:
    def __init__(self, value): # returning the unicode value of an integer
        self.__value = value # making private variables
        
    def findord(self):
        return ord(self.__value) # returning a ord(inputted value) which is a unicode integer

#
#
#
#

class append:
    def __init__(self, array, value):
        self.__array = array # private access modifiers
        self.__value = value

    def concat(self): # adding a value at the end of an array
        self.__array = self.__array + [self.__value]
        return self.__array

    def insert(self, pos): # adding a value at any point in the array depending on input of self.__postition
        self.__postition = pos
        self.__array = self.__array[:pos] + [self.__value] + self.__array[pos:]
        return self.__array

#
#
#
#

class randomint:
    def __init__(self, min, max): # making all attributes private
        self.__min = min
        self.__max = max
        self.__allvalues = []

    def prob(self, place): # returning a probability at the decimal place level of input eg. inputting 4 would output 0.4253
        self.__place = place
        self.__int = "0." + "0"*self.__place
        self.__int = str(self.__int)
        for t in range(2, self.__place+2): # iteration through and adding a random digit in the middle of the string
            self.__temp = random.randint(0, 9)
            self.__temp = str(self.__temp)
            self.__int = self.__int[:t] + self.__temp + self.__int[t+1:]
        return float(self.__int) # outputting it in a float

    def calculate(self):
        for x in range(self.__min, self.__max):
            self.__allvalues = append(self.__allvalues, x).concat() # creating an array that contains all of the possible values
        return self.__allvalues[random.randint(self.__min, self.__max)] # randomly pick from the array

#
#print(randomint(100, 1000).prob(3))
#
#

class sort:
    def __init__(self, array): # base class that contains all of the public variables to be inherited
        self.count = 0
        self.array = array
        self.sort1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.sort2 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.static = []
        self.allstatic = []
        self.final = []
        #self.split = int(len(self.__array) / 2)
        self.test = False
        self.rep = []
        self.extra = [""]*len(self.array)

class bubble(sort): # inheriting the base sort class
    def __init__(self, array):
        sort.__init__(self, array) # using the inherited variables
        self.__temp = 0

    def ints(self): # works with chars and integers
        for i in range(0, len(self.array)):
            for y in range(0, len(self.array)-1): # standard bubble sort procedure of iterating through each two array values and comparing magnitude
                if self.array[y] > self.array[y+1]:
                    self.__temp = self.array[y]
                    self.array[y] = self.array[y+1] # swapping places by using self.__temp for storage of the variables to not be lost
                    self.array[y+1] = self.__temp
        return self.array

class merge(sort):
    def __init__(self, array):
        sort.__init__(self, array) # inheriting base class variables

    def ints(self):
        self.__left = self.array[:self.split]
        self.__right = self.array[self.split:] # splitting into left and right arrays
        self.__left = bubble(self.__left).ints()
        self.__right = bubble(self.__right).ints()
        # not completed as the inbuilt sort() method is quicker than even these steps above so it was not nessasary to continue without purpose

class alpha(sort):
    def __init__(self, array): 
        sort.__init__(self, array) # inheriting base class variables
    
    def main(self):
        for i in range(len(self.array)-1): # similar to the bubble sort mechanism, but I tried to make a few ajustments for optimization purposes, this was the final outcome
            for j in range(i+1,len(self.array)):
                if self.array[i]>self.array[j]:
                    temp = self.array[i]
                    self.array[i] = self.array[j] 
                    self.array[j] = temp
        return self.array
                    
#
# 
# 
#            
    
class up_down:
    def __init__(self, char): # making variables private
        self.__char = str(char)
        self.__alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    def down(self):
        for v in range(0, len(self.__alpha)):
            if self.__alpha[v] == self.__char: # find the character in the array
                if v > 25:
                    self.__z = False # if it is a capital it moves 26 backwards for the lower case version
                    return self.__alpha[v-26]
                else:
                    return self.__alpha[v] # if input is already a lower case character

    def up(self):
        for v in range(0, len(self.__alpha)): # find the character in the array
            if self.__alpha[v] == self.__char: 
                if v < 25:
                    self.__z = False
                    return self.__alpha[v+26] # if it is a lower case it moves 26 forwards for the upper case version
                else:
                    return self.__alpha[v] # if input is already a upper case character

#
#
#
#

class delete:
    def __init__(self, array, pos):
        self.__pos = pos
        self.__array = array # making variables private
        
    def _del(self):
        self.__array = self.__array[:self.__pos] + self.__array[self.__pos+1:] # collecting all of the data before and after the postition into a new array without the postition inputted
        return self.__array

#
#
#
#

class reverse:
    def __init__(self, array):
        self.__array = array
        self.__newarray = [] # creating / assigning private varibles
        self.__len = len(array)
        self.__iter = 1

    def swap(self):
        for item in self.__array:
            self.__newarray = append(self.__newarray, self.__array[self.__len - self.__iter]).concat() # appending to a new array starting from the end of the populated array
            self.__iter = self.__iter + 1
        return self.__newarray

#
#
#
#

class pop:
    def __init__(self, array):
        self.__pos = len(array)-1
        self.__array = array # making variables private
        self.__temp = array
        
    def last(self):
        self.__array = delete(self.__array, self.__pos)._del() # deleting the last value in the array as self.__pos is set as length minus 1
        return self.__array, self.__temp[self.__pos] # returning new array and what was popped off

#
#
#
#

class strip:
    def __init__(self, string):
        self.__string = str(string)
        self.__set = True

    def trailorfront(self):
        return self.__string # not relevant as tested the .strip() method and it runs completely in under 100 miliseconds for me and hence doesnt require any attempt at improvment

#
#
#
#

class lencalc:
    def __init__(self, string):
        self.__string = string # making class variables private
        self.__iter = 0

    def calc(self):
        try:
            for char in self.__string:
                self.__iter = self.__iter + 1 # counting iterations
        except:
            self.__string = str(self.__string)
            try:
                self.__iter = lencalc(self.__string).calc() # cast to a string and recursively call the function to retry
            except:
                self.__iter = "Invalid" # if it still cannot be interpreted give error
        return self.__iter

#
#
#
#

class replace:
    def __init__(self, char, string):
        self.__string = string
        self.__char = char # making class attributes private
        self.__newstring = ""
        
    def chars(self):
        skip = False
        for letter in self.__string:
            if letter == self.__char: # if the string contains the character skip adding it back into the string when its re-made
                skip = True
            if skip == False:
                self.__newstring = self.__newstring + letter
            skip = False
        return self.__newstring

#
#
#
#
class search:
    def __init__(self, arr, value):
        self.array = arr
        self.val = value
        self.found = False
        self.other = True # making base class attributes (all public as need to be inherited)
        self.pointer = 0
        self.point = 0
        self.N = self.array[0]
        self.test = False
        self.l = 0
        self.u = len(self.array)
        self.m = (self.u+self.l) // 2
        self.i = 0

class linear(search):
    def ___init__(self, arr, value):
        search.__init__(self, arr, value) # inherited base class attributes

    def main(self):
        while self.found == False and i < len(self.array): # iterating through the array to see if the value is present
            if self.array[i] == self.val:
                self.found = True
            self.i=self.i+1
        return self.found, self.i-1 # returning whether the value was found, and either the last position or where it was found in the array

class binary(search):
    def ___init__(self, arr, value):
        search.__init__(self, arr, value) # inherit the base class attributes

    def main(self):
        self.array.sort() # to perfrom binary search the array must be sorted
        while self.found == False and self.test == False:
            self.m = (self.u+self.l) // 2
            if self.val > self.array[self.m]: # finding the central value and then comparing with the value
                self.l = self.m # making the new array to the left of the central value
                if self.array[self.l] == self.val:
                    self.found = True
            else:
                self.u = self.m
                if self.array[self.u] == self.val: # making the new array to the right of the central value
                    self.found = True
            self.testing = self.l - self.u
            self.testing = str(self.testing)
            if self.testing == "-1":
                self.test = True
            elif self.testing == "1": # conditions for ending the while loop
                self.test = True
        return self.found, self.val

class binarytree(search):
    def __init__(self, arr, value, L, R):
        search.__init__(self, arr, value) # inherit the base class attributes
        self.L = 0
        self.R = 0

    def main(self):
        while self.found == False and self.other == True:
            if self.N == self.val:
                self.found = True
            else:
                if self.array[pointer] > self.val:
                    self.point = self.R[self.pointer] # if its greater than the pointer look to the right else look left and iterate
                    self.pointer = self.point
                    if self.point != 0:
                        self.N = self.array[self.point]
                    else:
                        self.other = False
                else:
                    self.point = self.L[self.pointer]
                    self.pointer = self.point
                    if self.point != 0:
                        self.N = self.array[point]
                    else:
                        self.other = False 
        return self.found, self.val #returning the value and if it was in the binary tree

#print(complex.sort(["abcs", "poP", "q", "Queen", "strong", "tuple", "poop", "aBcd", "wow"]).alpha()) # examples of calling some methods
#print(complex.sort([1, 5, 2, 5, 3, 7, 2, 8, 4]).merge.ints())