import requests
from requests_oauthlib import OAuth1
import xml.etree.ElementTree as ET
from operator import itemgetter
from tabulate import tabulate

#print ("Welcome to API sanity script!!")


auth = OAuth1('54d71db9-8297-4154-b990-5ff90c85aaa9', 'KGSPDo7AwmX5zM0Llci2RGlfgDvTqLIt')

#This url query cdets for all outstanding defcts with query string :: Project:CSC.datacenter and Product:cloupia-cuic and Status:N,A,O,W,H,I,P,M and Severity:1,2,3,4,5

outstanding_bugs_url = "https://cdetsng.cisco.com/wsapi/LTS-4.0/api/search?criteria=%28%5BProduct%5D%20%3D%20%27cloupia-cuic%27%29%20AND%20%28%5BProject%5D%20%3D%20%27CSC.datacenter%27%29%20AND%20%28%5BSeverity%5D%20%3D%20%271%27%20OR%20%5BSeverity%5D%20%3D%20%272%27%20OR%20%5BSeverity%5D%20%3D%20%273%27%20OR%20%5BSeverity%5D%20%3D%20%274%27%20OR%20%5BSeverity%5D%20%3D%20%275%27%29%20AND%20%28%5BStatus%5D%20%3D%20%27A%27%20OR%20%5BStatus%5D%20%3D%20%27N%27%20OR%20%5BStatus%5D%20%3D%20%27O%27%20OR%20%5BStatus%5D%20%3D%20%27P%27%20OR%20%5BStatus%5D%20%3D%20%27W%27%20OR%20%5BStatus%5D%20%3D%20%27H%27%20OR%20%5BStatus%5D%20%3D%20%27I%27%20OR%20%5BStatus%5D%20%3D%20%27M%27%29&maxResults=0"

r = requests.get(outstanding_bugs_url, auth=auth)

print(r.status_code)

#print(r.text)

#printing api response
#print(r.text)
#Parsing xml string into xml elements, then you can access all the tags ,tag attributes and value, tag text value

#To convert xml string into python xml element use formstring function - it returns the root element
root = ET.fromstring(r.text)

#look at your xml string the root tag is CDETS, and below line will print the same
print (root.tag)

#To read attributes of an element use attrib ; it will give dictionary of attribute and attribute values, here root CDETS doesn't have any attribute so it wil print {}

print (root.attrib)


# you can use findall function to search all subelemenst by tag name
# this function return list of subelements -- -here it will give list of defect 
# each member in the returned list is xml representaion of 'defect' here again you can iterate over that to access defect child elements

outstanding_defect_list= root.findall('{cdetsng}Defect')

#print number of defects 

print ('Total number of outstanding defects =====>', len(outstanding_defect_list))

#acess first defect details

#print ('first defect id ===>', outstanding_defect_list[0].attrib['id'])
#print ('first defect submitter ===>', list(outstanding_defect_list[0])[-1].text)

#declare dictionary to hold status wise defect count
od_status_wise_dict = {"A": 0, "N": 0,  "O": 0,  "P": 0,  "W": 0,  "I": 0,  "H": 0 , "M":0}

#declare dictionary to hold severity wise defect count
od_severity_wise_dict = {"S1": 0, "S2": 0,  "S3": 0,  "S4": 0,  "S5": 0}

#declare dictionary to hold DE-Manager wise defect count
od_DE_manager_wise_dict = {"kdattatr":0, "viananth":0,  "smohanty":0,  "reranave":0,  "reswaran":0, "sthiruka":0,  "vachyuta":0,  "rtharmar":0,  "vikothan":0,  "rkumble":0 } 

#declare dictionary to hold module wise defect summary
#TBD

for defect in outstanding_defect_list:
	defect_sub_elements = list(defect)
	for defect_sub_element in defect_sub_elements:
		if 'Status' in defect_sub_element.attrib.values():
			status = defect_sub_element.text
		if 'Severity' in defect_sub_element.attrib.values():
			severity = defect_sub_element.text
		if 'DE-manager' in defect_sub_element.attrib.values():
			de_manager = defect_sub_element.text
	if status == 'A':
		od_status_wise_dict['A']+=1
	elif status == 'N':
		od_status_wise_dict['N']+=1
	elif status == 'O':
		od_status_wise_dict['O']+=1
	elif status == 'P':
		od_status_wise_dict['P']+=1
	elif status == 'W':
		od_status_wise_dict['W']+=1
	elif status == 'I':
		od_status_wise_dict['I']+=1
	elif status == 'H':
		od_status_wise_dict['H']+=1
	elif status == 'M':
		od_status_wise_dict['M']+=1
	
	
		
	if severity == '1':
		od_severity_wise_dict['S1']+=1
	elif severity == '2':
		od_severity_wise_dict['S2']+=1
	elif severity == '3':
		od_severity_wise_dict['S3']+=1
	elif severity == '4':
		od_severity_wise_dict['S4']+=1
	elif severity == '5':
		od_severity_wise_dict['S5']+=1
		
		
	if de_manager == 'kdattatr':
		od_DE_manager_wise_dict['kdattatr']+=1
	elif de_manager == 'viananth':
		od_DE_manager_wise_dict['viananth']+=1
	elif de_manager == 'smohanty':
		od_DE_manager_wise_dict['smohanty']+=1
	elif de_manager == 'reranave':
		od_DE_manager_wise_dict['reranave']+=1
	elif de_manager == 'reswaran':
		od_DE_manager_wise_dict['reswaran']+=1
	elif de_manager == 'sthiruka':
		od_DE_manager_wise_dict['sthiruka']+=1
	elif de_manager == 'vachyuta':
		od_DE_manager_wise_dict['vachyuta']+=1
	elif de_manager == 'rtharmar':
		od_DE_manager_wise_dict['rtharmar']+=1
	elif de_manager == 'vikothan':
		od_DE_manager_wise_dict['vikothan']+=1
	elif de_manager == 'rkumble':
		od_DE_manager_wise_dict['rkumble']+=1

def Quickstatus():
    print("Outstanding Bug`status wise===>"+ ":", end = ' ')
    for k,v in sorted(od_status_wise_dict.items(),key=itemgetter(1),reverse=True):
        if v>0:
            print(k,":",v, end= ' ' )
    return ''


def Severity():
    print("Outstanding Bug`s Severity wise===>"+ ":", end = ' ')
    for k,v in sorted(od_severity_wise_dict.items(),key=itemgetter(1),reverse=True):
        if v>0:
            print(k,":",v, end = ' ' )     
    return ''
        

    
def DEManager():
    print("DE-Manager wise Outstand Bug`s count===>"+ ":", end = ' ')
    for k,v in sorted(od_DE_manager_wise_dict.items(),key=itemgetter(1),reverse=True):
        if v>0:
            print(k,":",v, end = ' ')     
    return ''



#for i in od_status_wise_dict:
    #if od_status_wise_dict[i]>0:
        #print(i + ":" + str(od_status_wise_dict[i]),end=' ')
print(Quickstatus())
print(Severity())
print(DEManager())


		
#print (od_status_wise_dict)
#print (od_severity_wise_dict)
#print (od_DE_manager_wise_dict)
