class Car:
    def __init__(self, name):
        self.name = name
        self.remain_mile = 0

    def fill_fuel(self, miles):
        self.remain_mile = miles


class GasCar(Car):

    def fill_fuel(self, gas):
        self.remain_mile = gas * 6

gcar = GasCar("BWM")
gcar.fill_fuel(50)
print(gcar.remain_mile)

car = Car("car")
car.fill_fuel(50)
print(car.remain_mile)