from os import listdir
from os.path import isfile, join

mypath = "../convote/data_stage_three"
directories = [f for f in listdir(mypath)]
print(len(directories))

for dir in directories:
    files = [f for f in listdir(mypath +"/" + dir)]
    data_file = open("{}_strip.csv".format(dir), "a")
    for f in files:
        party = f.split('_')[3][0]
        f_name = mypath + "/" + dir + "/" + f
        text = open(f_name).read().strip().replace(',', '')
        data_file.write("{},{}\n".format(text, party))
    data_file.close()
