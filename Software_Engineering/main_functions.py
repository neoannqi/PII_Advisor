from flask import Flask, request, jsonify, abort, make_response
import pymysql, sys
import db_connection
import importlib.util

# helper function to import functions to read PDF and flag/mask resume contents
def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# convert pdf to string
convert_to_text = module_from_file("unit_tests", "data_science/unit_tests/convert_to_text.py")
# flagging and masking 
process_string = module_from_file("unit_tests", "data_science/unit_tests/process_string.py")

db_connection.upsert({"individual_id": "5", "parsed_content_v2": "Updated_Text for user id 5"})

# TEST COMMANDS
# curl POST -d "filepath='data_science/unit_tests/sample_resumes/kh_resume.pdf'&raw_contents=Ang Kian Hwee is the greatest!" 192.168.99.100:5000/upload/

## Note list
# users may re-upload their resumes. This generates a new job ID everytime they upload a new resume. 
# How do we link the job ID and the new resume with the same user? 
# Have a column 'user id' that contains each unique user id?

app = Flask(__name__)

# This function sends the uploaded resume to our scanning and masking functions 
# which will flag out PIIs and mask them inside the resume
# they will return both the flagged PIIs or masked contents back 
# after which, it will generate a job id and store the contents inside the database
# input: operation to be applied on Resume
# output: flagged PIIs, filtered contents, operation type, job id in JSON format
@app.route('/upload/', methods=['POST'])
def read_resume(filepath):
    # Insert convert_to_text op here

    # Insert flagging of PIIs op here

    # Insert masking of PIIs op here

    task = {"raw text": "placeholder"}
    return jsonify(task), 201

# function to flag out PIIs and mask contents
# input: raw text from document
# output: JSON object with PIIs and Parsed contents
def process_text(contents):
    result = {
        'PIIs': "flagged PIIs",
        'Parsed contents': "parsed text"
    }
    return result

# Return error 404 in JSON format
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)