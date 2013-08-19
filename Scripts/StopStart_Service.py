# Demonstrates how to stop or start all services in a folder

# For Http calls
import httplib, urllib, json

# For system tools
import sys

# For reading passwords without echoing
import getpass

import arcpy


# Defines the entry point into the script
def main(argv=None):
    # Print some info
    print
    print "This tool is a sample script that stops or starts all services in a folder."
    print

    # Ask for admin/publisher user name and password
    username = str(arcpy.GetParameterAsText(0)) #raw_input("Enter user name: ")
    password = str(arcpy.GetParameterAsText(1)) #getpass.getpass("Enter password: ")

    # Ask for server name
    serverName = str(arcpy.GetParameterAsText(2)) #raw_input("Enter server name: ")
    serverPort = 6080

    folder = str(arcpy.GetParameterAsText(3)) #raw_input("Enter the folder name or ROOT for the root location: ")
    stopOrStart = str(arcpy.GetParameterAsText(4)) #raw_input("Enter whether you want to START or STOP all services: ")

    # Check to make sure stop/start parameter is a valid value
    if str.upper(stopOrStart) != "START" and str.upper(stopOrStart) != "STOP":
        print "Invalid STOP/START parameter entered"
        return

    # Get a token
    token = getToken(username, password, serverName, serverPort)
    if token == "":
        print "Could not generate a token with the username and password provided."
        return

    # Construct URL to read folder
    if str.upper(folder) == "ROOT":
        folder = ""
    else:
        folder += "/"

    folderURL = "/arcgis/admin/services/" + folder

    # This request only needs the token and the response formatting parameter
    params = urllib.urlencode({'token': token, 'f': 'json'})

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    # Connect to URL and post parameters
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", folderURL, params, headers)

    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Could not read folder information."
        return
    else:
        data = response.read()

        # Check that data returned is not an error object
        if not assertJsonSuccess(data):
            print "Error when reading folder information. " + str(data)
        else:
            print "Processed folder information successfully. Now processing services..."

        # Deserialize response into Python object
        dataObj = json.loads(data)
        httpConn.close()

        # Loop through each service in the folder and stop or start it
        for item in dataObj['services']:

            fullSvcName = item['serviceName'] + "." + item['type']

            # Construct URL to stop or start service, then make the request
            stopOrStartURL = "/arcgis/admin/services/" + folder + fullSvcName + "/" + stopOrStart
            httpConn.request("POST", stopOrStartURL, params, headers)

            # Read stop or start response
            stopStartResponse = httpConn.getresponse()
            if (stopStartResponse.status != 200):
                httpConn.close()
                arcpy.SetParameterAsText(0, False)
                print "Error while executing stop or start. Please check the URL and try again."
                return
            else:
                stopStartData = stopStartResponse.read()
                arcpy.SetParameterAsText(0, True)

                # Check that data returned is not an error object
                if not assertJsonSuccess(stopStartData):
                    if str.upper(stopOrStart) == "START":
                        print "Error returned when starting service " + fullSvcName + "."
                    else:
                        print "Error returned when stopping service " + fullSvcName + "."


                    print str(stopStartData)

                else:
                    print "Service " + fullSvcName + " processed successfully."


            httpConn.close()

        return


# A function to generate a token given username, password and the adminURL.
def getToken(username, password, serverName, serverPort):
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    tokenURL = "/arcgis/admin/generateToken"

    params = urllib.urlencode({'username': username, 'password': password, 'client': 'requestip', 'f': 'json'})

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    # Connect to URL and post parameters
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", tokenURL, params, headers)

    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while fetching tokens from admin URL. Please check the URL and try again."
        return
    else:
        data = response.read()
        httpConn.close()

        # Check that data returned is not an error object
        if not assertJsonSuccess(data):
            return

        # Extract the token from it
        token = json.loads(data)
        return token['token']


# A function that checks that the input JSON object
#  is not an error object.
def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print "Error: JSON object returns an error. " + str(obj)
        return False
    else:
        return True


# Script start
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))