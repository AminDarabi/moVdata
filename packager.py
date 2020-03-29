import sys      as sys
import os       as os



if len(sys.argv) < 2:
    print("FEW ARGUMANT")
    exit(1)
if len(sys.argv) < 4:
    print("NOTHING TO DONE")
    exit(0)

OUT = open(sys.argv[1], "w")

PP = "#!" + os.popen("command -v python3").read() + "\n"
OUT.write(PP)

for i in range(3, len(sys.argv)):
    
    FF = open(sys.argv[i], "r").read()

    LS = (21 - len(sys.argv[i])) / 2
    RS = (20 - len(sys.argv[i])) / 2

    OUT.write('\n' + '#' * 80 + '\n')
    OUT.write('#' * 30 + ' ' * LS + sys.argv[i] + ' ' * RS + '#' * 30 + '\n\n')

    OUT.write(FF)

    OUT.write('\n\n' + '#' * 30 + ' ' * LS + sys.argv[i] + ' ' * RS + '#' * 30 + '\n')
    OUT.write('#' * 80 + '\n\n\n')