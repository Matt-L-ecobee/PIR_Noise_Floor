from data import Compiler

x = Compiler()

x.add_sensor("rs2:100:1")
x.add_sensor("rs2:101:1")
x.add_sensor("rs2:102:1")


cmd = ['']

while cmd[0] != "0":
    cmd = str(input("Enter a command: ")).split(" ")
    if cmd[0] == "run":
        x.collect_data(50)
        x.export_data()
        
    elif cmd[0] == "plot":
        if len(cmd) > 1:
            x.plot_results(cmd[1])
        else:
            print("Plot command is missing 1 argument")
            
    elif cmd[0] == "hist":
        if len(cmd) > 1:
            x.plot_histogram(cmd[1])
        else:
            print("Hist command is missing 1 argument")
