import sys
import random
import string

def get_random_string(length):
    
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    return ('"'+result_str+'"')

def Read_argument():

    print('Start reading arguments')
    if len(sys.argv)!=11:
        print('ERROR: Something from arguments is missing!')
        return -1
    
    list_arg=sys.argv

    key_file_name=''
    number_of_lines=-1
    max_level_of_nesting=-1
    max_number_of_keys=-1
    max_length_of_string=-1
    for index,value in enumerate(list_arg):
        #print(index,value)
        if value=='-k':
            key_file_name=list_arg[index+1]
        elif value=='-n':
            number_of_lines=list_arg[index+1]
        elif value=='-d':
            max_level_of_nesting=list_arg[index+1]
        elif value=='-m':
            max_number_of_keys=list_arg[index+1]
        elif value=='-l':
            max_length_of_string=list_arg[index+1]
    
    print('End reading arguments')
    return key_file_name, int(number_of_lines), int(max_level_of_nesting), int(max_number_of_keys), int(max_length_of_string)

def get_list_of_keys(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    file1.close()
    list_of_keys=[]
    for line in Lines:
        list_of_keys.append((line.split()))
    
    return list_of_keys

def get_random_one_list_of_keys(list):
    print ('LIST ',list)
    temp=random.randint(0,len(list)-1)
    return '"'+list[temp][0]+'"',list[temp][1],temp

def find_type(name,list):
    for i,j in list:
        if i==name.replace('"',''):
            return j
            

if __name__ == "__main__": # python3 genData.py -k keyFile.txt -n 10 -d 3 -l 4 -m 2

    key_file_name, number_of_lines, max_level_of_nesting, max_number_of_keys, max_length_of_string=Read_argument()

    list_of_keys=get_list_of_keys(key_file_name)
    #print(list_of_keys)

    string_line=''
    parent=''
    f= open('dataToIndex.txt',"w+")
    for i in range(1,number_of_lines+1):
        #print('line = ',i)

        random_max_level = random.randint(1,max_level_of_nesting)
        #print('max level',random_max_level)

        list_of_levels=[]
        string_line= 'key1 -> []'
        list_of_levels.append((None,'key1'))
        temp_list=list_of_levels.copy()
        for level in range(1,random_max_level+1):

            temp_list=list_of_levels.copy()
            #print('\nlevel : ',level,temp_list)
            for val in temp_list:
                old_parent=val[0]
                new_parent=val[1]
                #print('    old parent : ',old_parent,' new parent : ',new_parent,temp_list,'\n')
                temp2_list=''
                if int(len(new_parent))==int(level)+3:
                    temp2_list=temp2_list+'[ '
                    random_max_key = random.randint(0,max_number_of_keys)
                    for keys in range(1,random_max_key+1):
                        #print(new_parent,new_parent+str(keys))

                        temp2_list=temp2_list+ new_parent+str(keys)+' -> []'
                        if keys!=random_max_key: temp2_list=temp2_list+" | "
                        list_of_levels.append((str(new_parent),str(new_parent+str(keys))))
                    
                    temp2_list=temp2_list+' ]'
                    if temp2_list=='[  ]':
                        temp2_list='[]'

                    string_line = string_line.replace(new_parent+' -> []',new_parent+" -> "+temp2_list)


        list_string=string_line.split()
        result_string = ' '.join(list_string)
        f.write(result_string)
        f.write('\n')
