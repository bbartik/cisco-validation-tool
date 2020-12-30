from ciscoconfparse import CiscoConfParse
import glob
import pdb
import sys
import re

sections = {}

# open golden config and create list of lines
with open("golden.ini", "r") as f:
    for line in f:
        if line == "\n":
            continue
        if 'end' in line:
            continue
        if '[' in line:
            key = line.replace("\n","").replace("[","").replace("]","")
            sections.update({
                key: []
            })
        else:
            sections[key].append(line.replace("\n",""))
        continue

# use netmiko or nornir in future

configs = glob.glob('configs/*.conf')

# headings for csv output
f = open("validation.csv", "w")
print("device,","parent,","child1,","found")
f.write("device,parent,child1,found\n")

for config in configs:

    d = config.replace("configs/","").replace(".conf","")

    # Parse the device config into objects
    device_config = CiscoConfParse(f'{config}', syntax='ios')
    #pdb.set_trace()

    # global loop
    for golden_line in sections["global"]:
        found = 0
        # find line from golden config
    
        for line in device_config.find_objects(golden_line):
            found = 1
            # single line command found
    
            if (line == line.parent and len(line.children) == 0 and 
                    "interface" not in line.parent.text):
                to_write = f"{d},{line.parent.text},,found\n"
                f.write(to_write)    
            
            # single parent child command found (skip parent altogether)
            if line != line.parent and line.parent.text in sections["global"]:
                to_write = (f"{d},{line.parent.text},{golden_line},found\n")  
                f.write(to_write)  

            '''
            # parent interface, we are in childe
            if line != line.parent and "interface" in line.parent.text:
                for intf_line in golden_intf:
                    to_write = (f"{d},{line.parent.text},{intf_line},found\n")
                    f.write(to_write)
            '''

        # check if golden line is a top level command
        toplevel = re.match('^\w', golden_line) 
        # we didn't find the top level golden line
        if toplevel is not None and found == 0:
            to_write = (f"{d},{golden_line},,not found\n")
            f.write(to_write)
            # store parent so we can write it later
            prev_line = golden_line

        # we found a child, write parent and child to file
        if toplevel is None and found == 0:
            to_write = (f"{d},{prev_line},{golden_line},not found\n")
            f.write(to_write)
            #prev_line = ""

    # build interface list for device
    interfaces = device_config.find_objects('^interface.*Eth')
    #REDUCE LIST FOR TEST ONLY
    interface_list = [i.text for i in interfaces]
    #interface_list = [i.text for i in interfaces][12:14]

    # interface loop
    for i in interface_list:
        # create a mini device config for just interface data
        data = device_config.find_objects(f"^{i}")[0].children
        with open("temp.txt","w") as temp:
            for da in data:
                temp.write(f"{da.text}\n")
        interface_config = CiscoConfParse("temp.txt", syntax='ios')

        for golden_line in sections["interface"]:
            found = 0
        
            for line in interface_config.find_objects(golden_line):
                found = 1

                if line == line.parent and len(line.children) == 0:
                    to_write = (f"{d},{i},{line.parent.text},found\n") 
                    f.write(to_write)
                    # we found a child
            if found == 0:
                to_write = (f"{d},{i},{golden_line},not found\n") 
                f.write(to_write)

f.close()    
            

