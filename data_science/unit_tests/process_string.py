import unittest

#import re

#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage
#from io import StringIO

def process_string(raw_text):
    """
	Takes in a string and outputs a parsed string. Calls flagging() and parsing() functions to identify PIIs and mask the data respectively. 
    
    The raw string, Output from flagging(), Output from parsing() will be upsert into 3 different columns (Raw Contents, PIIs, Parsed Contents)
    for the record with the same uuid in database.

	Input:
	  text: String output from convert_to_text()

	Main Output:
      Returns HTTP status code 201 and indication msg to signify processing was done successfully. Upserts the values into database.

      Secondary (Indirect) Output:
      The raw resume string, Output from flagging(), Output from parsing() will be upsert into 3 different columns for the record with the same uuid in database. 
	"""
    PIIs = flagging(raw_text)
    parse_text = parsing(raw_text, PIIs)
    return [PIIs, parse_text] # for testing purposes only...remove this after confirming process_string works
    # return ("Successfully processed and uploaded resume into database!")

def flagging(raw_text):
    """
      Sub-function within process_string

      Input: Output from convert_to_text()

      Output: returns an array of unique PIIs / returns a dictionary PIIs 
	"""
    nric = re.findall('(?i)[SFTG]\d{7}[A-Z]', raw_text)
    email_address = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", raw_text)
    return {'nric':nric, 'email':email_address} #e.g. {'email': ['angkianhwee@u.nus.edu'], 'nric': ['S1234567A']}



def parsing(raw_text, dic):
    """
      Sub-function within process_string. Mask each pii with a <pii: category>, where category is the group which the pii belongs to. 

      Input:
          raw_text: Output from convert_to_text(), String
          dic: Output from flagging(), list/dict

      Output: 
      Entire string from convert_to_text() <pii: nric> labels over sensitive information.
    """
    processed_text = raw_text
    # Removing hard PIIs by default: NRIC, email address, phone, physical address
    processed_text = re.sub("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", '<pii_email>', processed_text)
    processed_text = re.sub('(?i)[SFTG]\d{7}[A-Z]', '<pii_nric>', processed_text)
    # if PIIs then remove 
    return processed_text

###################################################################

class Test(unittest.TestCase):
    
    def test_process_string(self):
        raw_text = "Ang Kian Hwee Blk123 Choa Chu Kang Loop #02-34 S680341 \
        Email: angkianhwee@u.nus.edu EDUCATION \
        National University of Singapore (NUS)"
        actual = process_string(raw_text)

        # expected is an array of 2 items - dictionary of PIIs, parsed text
        expected = [{'name': 'Ang Kian Hwee', 'address': 'Blk123 Choa Chu Kang Loop #02-34 S680341', 
                    'email': 'angkianhwee@u.nus.edu'} , 
                    "<pii_name> <pii_address> <pii_nric> Email: <pii_email> EDUCATION National University of Singapore (NUS)"]
        self.assertEqual(actual, expected)

# Still up for discussion
#    def test_parsing(self):
#        actual = parsing("Name: Ang Kian Hwee \nAge: 25 \nNRIC: S1234567A \nSkills: Blah blah \nWorking Experience: Blah Blah", 
#                        flagging("Name: Ang Kian Hwee \nAge: 25 \nNRIC: S1234567A \nSkills: Blah blah \nWorking Experience: Blah Blah"))
#
#        expected = "Name: <pii_Name> \nAge: <pii_Age> \nNRIC: <pii_NRIC> \nSkills: Blah blah \nWorking Experience: Blah Blah"
#        self.assertEqual(actual, expected)
#        
#    def test_flagging(self):
#        actual = flagging("Name: Ang Kian Hwee \nAge: 25 \nNRIC: S1234567A \nSkills: Blah blah \nWorking Experience: Blah Blah")
#        expected = ["Ang Kian Hwee", "25", "S1234567A"]
#        expected = {"name": "Ang Kian Hwee", "age": "25", "nric": "S1234567A"}
#        self.assertEqual(actual, expected)
        
        
unittest.main(verbosity=2)
