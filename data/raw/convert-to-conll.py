# convert-to-conll.py


import json

# Loads the JSON file exported from LightTag
def loadLightTag(filename):
    print("Loading " + filename)

    # Opening JSON file
    f = open(filename)    
    data = json.load(f)

    return data


# Converts one LightTag Sentence Example into a simpler, light-weight dictionary. 
def processSentence(example):
    id = example['example_id']
    text = example['content']

    spans = []
    
    for oneTag in example['annotations']:
        span = {
            'start': oneTag['start'],
            'end': oneTag['end'],
            'tag': oneTag['tag'],
            'value': oneTag['value'],
        }

        isCorrect = oneTag['correct']
        isReviewed = oneTag['reviewed']

        if (isCorrect == True) and (isReviewed == True):
            spans.append( span ) 


    # return
    packed = {
        'id': id,
        'text': text,
        'spans': spans
    }

    return packed


# Input: A list of sentence structures
# Output: A list of sentence structures, where any missing a SatelliteName span have been filtered out
def filterNoSatellite(dataIn):
    out = []

    for record in dataIn:
        hasSatellite = False
        for span in record['spans']:
            if (span['tag'] == "Satellite"):
                hasSatellite = True

        if (hasSatellite == True):
            out.append(record)
        else:
            print("FILTERING: ")
            print(record)
            print("***********")
            print("")

    print("Filter: Started with " + str(len(dataIn)) + " sentences, ended with " + str(len(out)) + ".")

    return out

# This one filters out sentences if there is not a satellite or launch vehicle -- should only be used for Failures. 
def filterNoSatelliteOrLaunchVehicle(dataIn):
    out = []

    for record in dataIn:
        hasSatellite = False
        for span in record['spans']:
            if (span['tag'] == "Satellite"):
                hasSatellite = True
            if (span['tag'] == 'LaunchVehicle'):
                hasSatellite = True

        if (hasSatellite == True):
            out.append(record)
        else:
            print("FILTERING: ")
            print(record)
            print("***********")
            print("")

    print("Filter: Started with " + str(len(dataIn)) + " sentences, ended with " + str(len(out)) + ".")

    return out



# Convert one record to CoNLL BIO format
def convertToCONLLBIO(example):
    text = example['text']
    spans = example['spans']

    words = text.split(" ")
    charIdx = 0

    out = []
    lastTag = "O"
    for word in words:
        #print("")
        tag = "O"

        # Calculate end spans for this word
        endCharIdx = charIdx + len(word) + 1

        # Tag
        for span in spans:
            #print(span)
            # Case 1: Single word
            if (charIdx <= span['start']) and (endCharIdx >= span['end']-1):
                tag = span['tag']
            elif (charIdx >= span['start']) and (endCharIdx-1 <= span['end']):
                tag = span['tag']


        # Remove any errant trigger tags
        if (tag == "Trigger"):
            tag = "O"
        # Normalize name of one tag
        if (tag == "Vehicle"):
            tag = "LaunchVehicle"


        # BIO tagging
        if (tag != "O"):
            if (lastTag == tag):
                # Same tag, now inside
                bioTag = "I-" + tag
            else:
                # Different tag, means beginning
                bioTag = "B-" + tag
        else:
            bioTag = "O"

        # Display
        #print("word: " + str(word) + "\t" + str(charIdx) + "\t" + str(endCharIdx) + "\t" + text[charIdx:endCharIdx] + "\t" + tag)        
        #print(str(word) + " " + bioTag)        

        out.append( {'word': word, 'tag': bioTag} )

        # New start span
        charIdx = endCharIdx
        lastTag = tag
        
    return out


def exportAsCONLLBIO(dataIn, filenameOut):
    conllData = []
    # Convert to CoNLL
    for record in dataIn:
        conllData.append( convertToCONLLBIO(record) )


    # Export
    numLines = 0
    numNonemptyTags = 0
    file = open(filenameOut, 'w')
    for record in conllData:
        for elem in record:            
            file.write(elem['word'] + " " + elem['tag'] + "\n")
            if (elem['tag'] != "O"):
                numNonemptyTags += 1
            numLines += 1
        file.write("\n")

    print("Exported " + str(numLines) + " to " + str(filenameOut) + " (" + str(numNonemptyTags) + " non-empty tags)")


#
#   Train/dev/test
#

def loadSetTSV(filenameIn):
    out = {}

    file = open(filenameIn, 'r')
    for line in file.readlines():
        #print(line)
        fields = line.split("\t")
        setName = fields[0]
        text = fields[1].strip()

        out[text] = setName

        #print("Text: " + text)
        #print("Set: " + setName)

    
    return out


def splitIntoSets(sentsIn, setDict):
    train = []
    dev = []
    test = []

    for sent in sents:
        text = sent['text'].strip()

        setName = setDict[text]

        if (setName == "train"):
            train.append(sent)
        elif (setName == "dev"):
            dev.append(sent)
        elif (setName == "test"):
            test.append(sent)
        else:
            print("ERROR: Could not find set for sentence (" + text + ")")


    # Rebalance dev and test folds
    sizeDev = len(dev)
    sizeTest = len(test)
    combinedSize = sizeDev + sizeTest
    toSlice = int(sizeDev - (combinedSize/2))

    balancedDev = dev[0:sizeDev-toSlice]
    balancedTest = dev[sizeDev-toSlice:] + test
    
    return train, balancedDev, balancedTest


#
#   Main
#

#filenameIn = "ssa-decommisionings_annotations.json"
#filenameIn = "ssa-launches_annotations.json"
filenameIn = "ssa-failures_annotations.json"

# Load lighttag data
decom = loadLightTag(filenameIn)
examples = decom['examples']

# Load TSV file determining train/dev/test sets
setDict = loadSetTSV("unannotated/" + filenameIn + ".sets.tsv")


# Process
sents = []
for idx, example in enumerate(examples): 
    processed = processSentence(example)
    print(processed)
    print("")

    sents.append(processed)

# Filter based on not having a satellitename
#sents = filterNoSatellite(sents)                       # USE FOR LAUNCHES, DECOMMISIONINGS
sents = filterNoSatelliteOrLaunchVehicle(sents)         # USE FOR FAILURES

# Split into sets
setDict = loadSetTSV("unannotated/" + filenameIn + ".sets.tsv")
train, dev, test = splitIntoSets(sents, setDict)
print("Train size: " + str(len(train)))
print("Dev size: " + str(len(dev)))
print("Test size: " + str(len(test)))

# Export in CoNLL format
filenameOut = filenameIn + ".conll-bio.txt"
exportAsCONLLBIO(sents, filenameOut)

# Train
exportAsCONLLBIO(train, filenameIn + ".train.conll-bio.txt")
exportAsCONLLBIO(dev, filenameIn + ".dev.conll-bio.txt")
exportAsCONLLBIO(test, filenameIn + ".test.conll-bio.txt")