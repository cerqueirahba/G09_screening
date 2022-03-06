import os
import pprint
import shutil

######################## List of Outputs #############################
list_of_files = []
for filename in os.listdir():
    if filename.endswith('.log'):
         list_of_files.append(filename)

######################## Functions used #############################
#Defining a function to diferenciate lists
def diferenciate_lists(list1,list2):
    return list(set(list1) - set(list2))

#Defining a function to check double occurrency of the same file on normal_termination_list and delete them
def list_duplicates(seq):
  seen = set()
  seen_add = seen.add
  # adds all elements it doesn't know yet to seen and all other to seen_twice
  seen_twice = set( x for x in seq if x in seen or seen_add(x) )
   #turn the set into a list (as requested)
  return list(seen_twice)


######################## Geometry check #############################
###Verification of normal termination
has_the_pattern_list = []
pattern = "Normal termination of Gaussian 09"

#creating a list from the "list_of_files" that terminated normally
for each_file in list_of_files:
    with open(each_file) as current_file:
        for line in current_file:
            if pattern in line:
                has_the_pattern_list.append(current_file.name)

#Create a list of files that has pattern twice (this means that the calculation worked fine)
normal_termination_list= list_duplicates(has_the_pattern_list)

#Create a list of files that the pattern only appears once (this means that the frequency calculation failed)
freq_fail=diferenciate_lists(has_the_pattern_list,normal_termination_list)

#Create a list of files that fail the geometry calculation
geom_fail=diferenciate_lists(list_of_files,has_the_pattern_list)

######################## Frequency test #############################

#Searching for frequencies values in normal_termination_list and creating a dictionary with those values
frequencies=[]
structures=[]
for each_file in normal_termination_list:
    with open(each_file) as output:
        output_lines = output.readlines()
        for line in range(len(output_lines)):
            if 'Frequencies' in output_lines[line]:
                frequencies.append(float(output_lines[line].strip().split()[2]))
                structures.append(output.name)
                if True:
                    break

both_lists=zip(structures,frequencies)
all_frequencies=dict(both_lists)

#Separating between real and imaginary frequencies
real_frequencies=dict()
imaginary_frequencies=dict()

for (key,value) in all_frequencies.items():
    if value > 0:
        real_frequencies[key]=value
    else:
        imaginary_frequencies[key]=value

######################## Report creation #############################
#### NEEDS ENGLISH REVIEW
### TODO:  add datetime module!!

file= open("Report.txt","a")
file.write("The following outputs converged sucessfuly and has only real frequencies \n")
file.write(pprint.pformat(real_frequencies))
file.write("\n\nThis outputs has a imaginary frequency\n")
file.write(pprint.pformat(imaginary_frequencies))
file.write("\n\nThose outputs failed in the frequency calculation\n")
file.write(str(freq_fail))
file.write("\n\nThose outputs failed the geometry optimization\n")
file.write(str(geom_fail))
file.close()

######################## File manegement #############################
# Making the paths
path_ok=os.path.join(os.getcwd(),'Finished_outputs')
path_freq=os.path.join(os.getcwd(),'Imaginary_frequency')
path_geom_fail=os.path.join(os.getcwd(),'Geometry_fail')
path_freq_fail=os.path.join(os.getcwd(),'Frequency_fail')


#Check if list of files is empty or not. and then creating a directory
keys1=list(real_frequencies.keys())
if keys1:
    if not os.path.exists(path_ok):
        os.makedirs('Finished_outputs')
keys2=list(imaginary_frequencies.keys())
if keys2:
    if not os.path.exists(path_freq):
        os.makedirs('Imaginary_frequency')
if freq_fail:
    if not os.path.exists(path_freq_fail):
        os.makedirs('Frequency_fail')
if geom_fail:
    if not os.path.exists(path_geom_fail):
        os.makedirs('Geometry_fail')

#moving the files
for file in keys1:
    if os.path.exists(path_ok):
        old_path=os.path.join(os.getcwd(),file)
        new_path=os.path.join(path_ok,file)
        shutil.move(old_path,new_path)

for file in keys2:
    if os.path.exists(path_freq):
        old_path=os.path.join(os.getcwd(),file)
        new_path=os.path.join(path_freq,file)
        shutil.move(old_path,new_path)

for file in freq_fail:
    if os.path.exists(path_freq_fail):
        old_path=os.path.join(os.getcwd(),file)
        new_path=os.path.join(path_freq_fail,file)
        shutil.move(old_path,new_path)

for file in geom_fail:
    if os.path.exists(path_geom_fail):
        old_path=os.path.join(os.getcwd(),file)
        new_path=os.path.join(path_geom_fail,file)
        shutil.move(old_path,new_path)