class TestClass:
    var = 10
    def __init__(self):
        self.num = 30
        self.name= "Adams"
    def FunName(self):
        return self.name
    def funNum(self):
        return self.num


tt = TestClass()
tt.name = "Joe"

tx = TestClass()
tx.num = 90
print(tt.FunName())
print(tx.funNum())
        