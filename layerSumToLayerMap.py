################################################################################
# Name: layerSumToLayerMap.py                                                  #
# Purpose:  create a layermap from L-edit's layer summery file                 #
#                                                                              #
# Please use this script at your own discretion and responsbility. Eventhough  #
# This script was tested and passed the QA criteria to meet the intended       #
# specifications and behaviors upon request, the user remains the primary      #
# responsible for the sanity of the results produced by the script.            #
# The user is always advised to check the imported design and make sure the    #
# correct data is present.                                                     #
#                                                                              #
# For further support or questions, please e-mail support@eda-solutions.com    #
#                                                                              #
# Test platform version: L-Edit 2022.2u1 Release build                         #
# Author: Henry Frankland                                                      #
################################################################################
#LIMITATION OF LIABILITY:  Because this Software is provided “AS IS”, NEITHER MENTOR GRAPHICS NOR ITS LICENSORS SHALL BE LIABLE FOR ANY DAMAGES WHATSOEVER IN CONNECTION WITH THE SOFTWARE OR ITS USE.  Without limiting the foregoing, in no event will Mentor Graphics or its licensors be liable for indirect, special, incidental, or consequential damages (including lost profits or savings) whether based on contract, tort (including negligence), strict liability, or any other legal theory, even if Mentor Graphics or its licensors have been advised of the possibility of such damages.  THE FOREGOING LIMITATIONS SHALL APPLY TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW.
#unless otherwise agreed in writing, Mentor Graphics or Tanner EDA or its partners has no obligation to support or otherwise maintain Software.”

################################################################################
#########################################################################
#                                                                       #
#   History:                                                            #
#   Version 0.0 | 12/02/2022 - started work on script                   #
#   Version 0.1 | 23/03/2022 - finished first draft, pending testing    #
#   Version 1.0 | 27/10/2022 - initial release                          #
#########################################################################
# Prerequisite
# 1. python 3
# 2. windows (Linux should work but not tested)
# script usage:
# 1. open a command prompt and execute the "layerSumToLayerMap.py"
#
#           
#         ------------------------------------- library_name
#         |             ----------------------- input file arg option
#         |             |    ------------------ Input summery file from L-edit
#         |             |    |      ----------- output file arg option 
#         |             |    |      |    ------ New output file name
#         |             |    |      |    |
#layerSumToLayerMap.py -s file.txt -O file.txt
#########################################################################33

import logging
import sys
import argparse
import os
import csv
import shutil
from tempfile import NamedTemporaryFile
import copy

logging.basicConfig(filename=f'{sys.argv[0]}.log', encoding='utf-8',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__)

debug = 0

#Log levels
# 0 --> no-log
# 1 --> function message
# 2 --> data information

#write out file using the csv dict writer
def updateCSV(data, csv_loc, headers):
    #if debug_dmy: csv_loc = os.path.join(os.path.dirname(csv_loc), os.path.basename(csv_loc) + ".debug")
    logging.info(f"Updating CSV: {csv_loc}")
    csvTempfile = NamedTemporaryFile(mode='w', delete=False)
    
    if debug == 2: logging.info(f"header: {headers}")

    csvfile = csv.DictWriter(csvTempfile,delimiter='\t', lineterminator='\n',fieldnames=headers)
    csvfile.writeheader()
    print(data)
    for i in data:
        csvfile.writerow(i)
    #for i in data:
    #    print("test",i)
    #    csvfile.writerow(i)
    csvTempfile.close()
    
    if debug: logging.info(f"tempfile name: {csvTempfile.name} -- csv_loc: {csv_loc}")
    shutil.move(csvTempfile.name,csv_loc)

#check if the path given to script exist and contains valid data
def checkInExist(value, path):
    if debug >= 1: logger.info("checkInExist")

    if not value : logger.error("Incorect args! -- missing arg"); return 0
    if path == 1:
        #input is a string so lets feed it directly to the exists command
        if type(value) == str:
            if os.path.exists(value):
                if debug == 2: logger.info("path exists: {}".format(value))
                return 1                                                               #returning at this point means that the string is a valid path
            return 0                                                                   #returning at this point means that the single string is not a valid file
        
        #the input is a list of paths, lets loop through and return 0 if 1 does not exist
        elif type(value) == list:
            if debug == 2: logger.info("path list: {}".format(value))
            for pathEl in value:
                if os.path.exists(pathEl):
                    if debug == 2: logger.info("path exists: {}".format(pathEl))
                else:
                    logger.error("path does not exists: {}".format(pathEl))
                    return 0                                                            #returning at this point means 1 of the paths was not valid
            return 1                                                                    #returning at this point means all listed paths are valid
    if value != '': return 0                                                            #returning at this point will indicate if simple var does not exist
    if debug == 2: logger.info("value: {}".format(value))
    return 1                                                                            #default return

#gets user inputs and return a dictionary of all the keys
def grabinput(args):
    if debug >= 1: logger.info("grabinput")

    for i,key in enumerate(args):
        if i == 0:
            #gaurd clause to exit program if input dict is incomplete
            if key != "DESCRIPTION": logger.error("Incorect args! -- incorrect script config, missing arg header description"); return 0
            my_parser = argparse.ArgumentParser(description=args[key])
        elif i > 0:
            #gaurd clause to exit program if script configured with incomplete infomation
            if len(args[key]) != 5: logger.error("Incorect args! -- incorrect script config, wrong arg count"); return 0
            my_parser.add_argument(key, args[key][0],required=args[key][1],nargs=args[key][2],help=args[key][3])
    
    return my_parser.parse_args()

#retrievs data from file, and creates a dictionary 
def getData(csv_pth):
    if debug >= 1: logger.info("getData")
    if debug == 2: logger.info("getData inputs: {}".format(csv_pth))
    data = []
    with open(csv_pth,encoding='utf-8-sig', newline='') as File:
        reader = csv.DictReader(File,delimiter='\t')
        for i, row in enumerate(reader):
            if i != 1: data.append(row)
    return data

#take the input file and copy it into a temporary file
def initialread(file, sline=0):
    if debug >= 1: logger.info("initialread")
    
    destf = NamedTemporaryFile(mode='w', delete=False)
    if debug >= 2: logger.info("input file: {}".format(file))
    if debug >= 2: logger.info("output file: {}".format(destf.name))

    with open(file,'r') as origf:
        for i in range(sline):
            if debug >= 2: logger.info("ignored line: {}".format(i))
            next(origf)
        for line in origf:
            if debug >= 2: logger.info("write line: {}".format(line))
            destf.write(line)
    destf.close()

    return destf.name

#function takes 2	0	Deep_N_Well:drawing ----- to -> 2	0	Deep_N_Well drawing
def spliton_char(data, splitchar, target, newKey):
    if debug >= 1: logger.info("spliton_char")

    #loop through all dictionaries
    for entry in data:
        if debug >= 2: logger.info("Data entry: {}".format(entry))
        complexEntry = entry[target].split(splitchar)
        #gaurd clauses
        
        if type(complexEntry) == list and len(complexEntry) < 2: logger.error("invalid split output list detected. target key: {} --> newkey {} --- split char {} --- result: {}".format(target,newKey,splitchar, complexEntry)); return 0
        if type(complexEntry) == str: logger.error("unexpected single output detected. target key: {} --> newkey {} --- split char {} --- result: {}".format(target,newKey,splitchar, complexEntry)); return 0
        
        if debug >= 2: logger.info("split input: {} --> split output: {}".format(entry[target],complexEntry))

        entry[newKey] = copy.deepcopy(complexEntry[1])
        entry[target] = copy.deepcopy(complexEntry[0])
    return data

#reorder the dictionary, might be redundant function as the dict writer might be able to reorder depending on header
def reOrder(data, map):
    if debug >= 1: logger.info("reOrder")

    newEntry={}
    list = []
    if debug >= 1: logger.info("Main_func")
    for entry in data:
        if debug >= 2: logger.info("Data entry: {}".format(entry))
        for key in entry:
            if debug >= 2: logger.info("Data entry selected key: {} data: {}, to be changed to: {}".format(key, entry[key], map[key]))
            if map[key] == '': logger.error("Incorect map! -- could not find key: {}, in map".format(key)); return 0
            newEntry[map[key]] = entry[key]
        if debug >= 2: logger.info("new entry: {}".format(key))
        list.append(copy.deepcopy(newEntry))
    return list

#main function
def main():
    #func start
    if debug >= 1: logger.info("Main_func")

    #arguments we want, this will be put into a json as config for script, reason for this implementation is that it makes the construction easier, during building i can predefine what i want the inputs to be but limit the number of inputs i have to test without adjusting the code. can switch to the complete code later (makes it easier to define the programs parameters)
    #syntax '-option':[op_longhand[--xxx], required[True|False], howmany args['+'|n], description, is path[1|0]]
    #args = {\
    #    'DESCRIPTION':'adjusting CSV files acording to a maping file',
    #    '-s':['--sumf', True,'+', "summery file input",1],
    #    '-o':['--ouput', True, 1, "output layermap file",1]
    #}
    args = {\
        'DESCRIPTION':'adjusting CSV files acording to a maping file',
        '-s':['--sumf', True,1, "summery file input",1]
    }

    new_header = ['#Layer Name','Layer Purpose','GDS Layer','GDS Datatype']

    #get the users inputs
    userInp = grabinput(args)
    
    #sanity check inputs
    for i, key in enumerate(args):
        if i > 0: 
            if not checkInExist(getattr(userInp, args[key][0].strip('-')), args[key][4]): logger.error("exiting program error while prossesing: {} in input configuration".format(key))
            elif debug == 2: logger.info("user input config: {} -- conf: {}".format(key,args[key]))

    #initialise readin
    tempf = initialread(getattr(userInp, args['-s'][0].strip('-'))[0], 1)

    #read in file
    data = getData(tempf)

    dataNew = spliton_char(data, ':','Layer Name','Layer Purpose_n')
    if not dataNew: return 1

    map = {'Layer Name':'#Layer Name','Layer Purpose_n':'Layer Purpose','GDS#':'GDS Layer','GDS DataType':'GDS Datatype'}

    finalData = reOrder(data, map)

    #manipulate file contents
    #file headers as they stand: <GDS#>	<GDS DataType>	<Layer Name>
    #required order: <#Layer Name> <Layer Purpose>  <GDS Layer>   <GDS Datatype>

    updateCSV(finalData, 'layer.map', new_header)

if __name__ == "__main__":
    logger.info("layerSumToLayerMap.py RUN")
    main()
    logger.info("layerSumToLayerMap.py FINISH")