import random
import sys
import string

max_length_of_string=-1

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", result_str)

    return ('"'+result_str+'"')

def generate_nested_string(depth,listofkeys):
  
  # get random keys for this level
  random_list = random.sample(list_of_keys, random.randint(0, len(list_of_keys)))
  print('level: ',depth,' -> ',random_list)

  if depth == 1:

    string=[]
    string.append(('['))
    for lzero in random_list:
      
      if lzero[1]=='int':
        string.append((' "{}" -> {} '.format(lzero[0], random.randint(1, 100))))
      elif lzero[1]=='float' :
        string.append((' "{}" -> {} '.format(lzero[0], round(random.uniform(0.1, 99.9),2)) ))
      elif lzero[1]=='string' :
        string.append((' "{}" -> {} '.format(lzero[0], get_random_string(random.randint(1,int(max_length_of_string))))))
    
      string.append(('|'))
    string.append((']'))

    string_n=''
    for s in string:
      string_n=string_n+s

    string_n=string_n.replace("|]","]")
    return string_n
  else:
    string=[]
    string.append(('['))
    for l in random_list:
      string.append((' "{}" -> {} '.format(l[0], generate_nested_string(depth - 1,listofkeys))))
      string.append(('|'))
    string.append((']'))

    string_n=''
    for s in string:
      string_n=string_n+s
    string_n=string_n.replace("|]","]")
    return string_n

def get_list_of_keys(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    file1.close()
    list_of_keys=[]
    for line in Lines:
        list_of_keys.append((line.split()))
    
    return list_of_keys

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

if __name__ == "__main__": # python3 test.py -k keyFile.txt -n 1000 -d 3 -l 4 -m 5

    key_file_name, number_of_lines, max_level_of_nesting, max_number_of_keys, max_length_of_string=Read_argument()

    list_of_keys=get_list_of_keys(key_file_name)
    #print(list_of_keys)

    # get random max level
    random_max_level = random.randint(1,max_level_of_nesting)

    #if max number of keys is higher from list get exactly the the len of list of keys
    if max_number_of_keys>len(list_of_keys):
      max_number_of_keys=len(max_number_of_keys)


    f= open('dataToIndex.txt',"w+")

    for i in range(1,number_of_lines+1):
      print('random_max_level = ',random_max_level)

      
      nested_string = generate_nested_string(random_max_level,list_of_keys)

      # print the nested string
      nested_string='"key'+str(i)+'" -> '+nested_string
      print('\n',nested_string)
      

        
        
      f.write(nested_string)
      f.write('\n')
