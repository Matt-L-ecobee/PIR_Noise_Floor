from data import Compiler

test_number = str(input("Enter the test number: "))

x = Compiler(test_number)

x.add_sensor("TD2Q")


x.new_export()
while True:
    x.collect_data(0)
