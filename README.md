# zipic
A PNG/JPEG image compression tool powered by tinypng.com

## First thing
Please visit https://tinypng.com/developers to get a API Key, and replace the key which in zipic.py, the first 500 compression each month are free.

## Usage:   

`./zipic.py --input=<filepath> --output=<filepath>`   
or   
`./zipic.py <filepath>`   

All arguments:

```
-h, --help: Show help tips
-i, --input=<path>: Set input file path, can't be a directory.
-o, --ouput=<path>: Set output file path, can't be a directory, if not set then overwrite the input file.
-r, --rename: If not set output path, then make output directory as same as input, but rename the output file for avoid overwrite.
-v, --verbose: Show detail result.
```
