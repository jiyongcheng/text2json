import json,os,sys,argparse

SEARCH_WORD = '[REPORT]'
def main():
    # initiate the parser
    parser = argparse.ArgumentParser()
    # add long and short argument
    parser.add_argument("--file", "-f", help="set file path which need to be parsed")
    parser.add_argument("--out", "-o", help="set output file for the json")
    # read arguments from the command line
    args = parser.parse_args()
    # check for file path
    if args.file:
        if not (os.path.exists(args.file)):
          print("file is not exists: %s" % args.file)
          sys.exit()
    else:
      print("you need to provide txt file path, check --help")
      sys.exit()
    fileinfo = os.path.split(args.file)
    dict = {
      "report name": fileinfo[1],
      "active": True,
      "sub_reports": [
        {
          "name": "a",
          "filename": "a.sql",
          "extension": "csv"
        }
      ]
    }
    f = open(args.file, "r")
    if f.mode == 'r':
      reports = []
      fl =f.readlines()
      for i in range(len(fl)-1):
        currentLine = fl[i+1]
        if (currentLine.strip() == SEARCH_WORD):
          infoBlock = {}
        # read next 2 lines and process the data
          infoBlock["type"] = currentLine[currentLine.find('[')+1 : currentLine.find(']')].lower()
          infoBlock = getInfoFromOneLineText(fl[i+2], infoBlock)
          infoBlock = getInfoFromOneLineText(fl[i+3], infoBlock)
          reports.append(infoBlock)
    dict['export'] = reports
    # convert into JSON:
    jsonString = json.dumps(dict);
    print(jsonString)
    saveToFile(jsonString, args.out)

def getInfoFromOneLineText(text, obj):
      text = text.strip()
      key = text[:text.find(':')].strip().lower()
      value = text[text.find(':') + 1:].strip().lower()
      obj[key] = value

      return obj

def saveToFile(string, file):
    if file==None:
        file = "output.json"
    f= open(file,"w+")
    f.write(string)
    f.close()
    print("json file is saved to: %s" % file)

if __name__== "__main__":
  main()