import sys
import builder

####
#   Makes file with spread's quotes. To make the spread, only simultaneous prices are used.
#   Spread = Price1 * Coefficient1 - Price2 * Coefficient2
#
#   Command line arguments: 1. path_to_file1 path_to_file2 name_of_result_file
#                           2. path_to_file1 path_to_file2 coefficient1 coefficient2 name_of_result_file
#   Input file's format:
#         DATE   ;  TIME  ; OPEN ; HIGH ; LOW ; CLOSE ; VOLUME
#       ddmmyyyy   hhmmss    0.0   0.0    0.0    0.0      0
####


file_name1 = ""
file_name2 = ""
spread_name = ""
factor1 = 1
factor2 = 1

#  check command line arguments:
if len(sys.argv) == 4 or len(sys.argv) == 6:
    file_name1 = sys.argv[1]
    file_name2 = sys.argv[2]
    if len(sys.argv) == 6:
        factor1 = float(sys.argv[3])
        factor2 = float(sys.argv[4])
        spread_name = sys.argv[5]
    else:
        spread_name = sys.argv[3]
else:
    print("Invalid command line arguments! \n")
    sys.exit()

#  read all data from both files:
with open(file_name1, 'r') as file1:
    list1 = file1.readlines()
with open(file_name2, 'r') as file2:
    list2 = file2.readlines()

#  calc spread
spread_data = builder.build_spread(list1, list2, factor1, factor2)

#  save spread to file
with open(spread_name + ".txt", 'w') as res_file:
    for candle in spread_data:
        res_file.write(candle.to_string() + '\n')
