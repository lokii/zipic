#!/usr/bin/env python3

import os
import sys
import getopt
import json
from os.path import dirname
from urllib.request import Request, urlopen
from base64 import b64encode

# You must replace the key to yours! 
# Get the API key from: https://tinypng.com/developers
# The first 500 images compression each month are free. 
key = "A5Qa0H-oFnK3i5ocCuzwEebgS7y9BxQ7"

def compress(input, output, verbose):
    request = Request("https://api.tinypng.com/shrink", open(input, "rb").read())

    cafile = None
    # Uncomment below if you have trouble validating our SSL certificate.
    # Download cacert.pem from: http://curl.haxx.se/ca/cacert.pem
    # cafile = dirname(__file__) + "/cacert.pem"

    auth = b64encode(bytes("api:" + key, "ascii")).decode("ascii")
    request.add_header("Authorization", "Basic %s" % auth)

    response = urlopen(request, cafile = cafile)
    if response.status == 201:
        info = json.loads(response.read().decode('ascii'))
        inputSize = info['input']['size'];
        outputSize = info['output']['size'];
        reduceSize = inputSize - outputSize
        ratio = info['output']['ratio'] * 100

        if verbose:
            print('Input file type:\t{}'.format(info['input']['type']))
            print('Input file size:\t{} bytes'.format(inputSize))
            print('Output file size:\t{0} bytes, reduced {1} bytes({2}%)'
                    .format(outputSize, reduceSize, 100 - ratio))
            print('output path:\t{0} {1}'.format('overwrite' if input == output else '', output))
        else:
            print("Reduced {0} bytes({1}%)".format(reduceSize, ratio))

        # Compression was successful, retrieve output from Location header.
        if reduceSize > 0:
            result = urlopen(response.getheader("Location"), cafile = cafile).read()
            open(output, "wb").write(result)
        return reduceSize
    else:
        # Something went wrong! You can parse the JSON body for details.
        print("Compression failed")
        return -1


def usage():
    print(
            ''' Please keep network available when use this tool. Usage:
            ./zipic [args] --input=<filepath> --output=<filepath>
            or
            ./zipic [args must before file path] <filepath>
            All args:
            -h, --help: Show help tips
            -i, --input=<path>: Set input file path, can't be a directory.
            -o, --ouput=<path>: Set output file path, can't be a directory, if not set then overwrite the input file.
            -r, --rename: If not set output path, then make output directory as same as input, but rename the output file for avoid overwrite.
            -v, --verbose: Show detail result.
            ''')

def getNewPath(originPath):
    dirName, fileName = os.path.split(originPath)
    return dirName + '/__' + fileName

if __name__ == '__main__':
    try:                                
        opts, args = getopt.getopt(sys.argv[1:], "hvri:o:", ["help", "verbose", "rename", "input=", "output="])
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)

    verbose = False
    rename = False
    inputFiles = ''
    outputFile = ''

    #print(opts, args)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-r', '--rename'):
            rename = True
        elif opt in ('-i', '--input'):
            inputFiles = (arg, )
        elif opt in ('-o', '--output'):
            outputFile = arg

    if len(inputFiles) == 0 and len(args) > 0:
        if len(outputFile) > 0:
            inputFiles = (args[0], )
        else:
            inputFiles = args

    if len(inputFiles) == 0:
        print('Must set input file path!')
    else:
        for input in inputFiles:
            if os.path.isfile(input):
                if len(outputFile) == 0 or len(inputFiles) > 1:
                    outputFile = input if not rename else getNewPath(input)
                print('Try to compress file: {}'.format(input))
                compress(input, outputFile, verbose)
            else:
                print('Input file is not exists!')

