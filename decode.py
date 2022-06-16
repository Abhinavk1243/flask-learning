class rectangle():
    def __init__(self,side1,side2):
        self.__side1=side1
        self.__side2=side2
        

    @property
    def length(self):
        print("Getting length...")
        return self.__side1
    
    @property   
    def breadth(self):
        print("Getting breadth...")
        return self.__side2
    
    @length.setter
    def length(self,side1):
        print("setting value...")
        self.__side1=side1
    
    @breadth.setter
    def breadth(self,side2):
        print("setting value...")
        self.__side1=side2
    
    def perimeter(self):
        return 2 * (self.__side1 + self.__side2)
    
    def area(self):
        return self.__side1 * self.__side2
    
    
    
shape=rectangle(2,3)
# shape.length=12
# print(shape.length)

print(shape.area())

    
