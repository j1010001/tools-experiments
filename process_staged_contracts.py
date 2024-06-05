import json, getopt, sys

argumentList = sys.argv[1:]

# Options
options = "hi:"
 
# Long options
long_options = ["Help", "Input="]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h", "--Help"):
            print ("Displaying Help")
            print ("bla")
             
        elif currentArgument in ("-i", "--Input"):
            input_file = currentValue;
            print (("JSON input file: % s") % currentValue)
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

with open(input_file, 'r') as f:
    data = json.load(f)

FiatTokenCounter = 0
def analyze_error(err):
    global FiatTokenCounter
    if err.find("FiatToken") != -1:
        FiatTokenCounter = FiatTokenCounter + 1
        return "FiatToken found in error"
    else:
        return 0

success = []
error = []
print("contracts:", len(data))
i = 0
for contract in data:
    account = contract["account_address"]
    name = contract["contract_name"]
    if contract.get("kind"):
        kind = contract.get("kind")
        if kind == "contract-update-success":
            print("{:03d}".format(i), account, name, "success")
            success.append(contract)
        elif kind == "contract-update-failure":
            print("{:03d}".format(i), account, name, "error")
            error.append(contract)
        else:
            print("parsing error")
            exit()
    i = i + 1

print("errors:", len(error))
i = 0
for contract in error:
    account = contract["account_address"]
    name = contract["contract_name"]
    error_analysis = analyze_error(contract.get("error"))
    if error_analysis != 0:
        print("{:03d}".format(i), account, name, " : ", error_analysis)
    else:
        print("{:03d}".format(i), account, name)
    i = i + 1
print("errors with FiatToken found:", FiatTokenCounter)
print("success:", len(success))
i = 0
for contract in success:
    account = contract["account_address"]
    name = contract["contract_name"]
    print("{:03d}".format(i), account, name)
    i = i + 1
