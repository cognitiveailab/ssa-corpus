from bert import Ner

#
#   File I/O
#

def loadBIOFile(filename):
    file1 = open(filename, 'r')
    lines = file1.readlines()

    sents = []
    sent = []
    for line in lines:
        if (len(line) < 2):
            sents.append(sent)
            sent = []
        else:
            fields = str(line).strip().split(" ")            
            if (len(fields) > 1):
                word = fields[0]
                tag = fields[1]
                packed = {'word': word, 'goldTag': tag}
                sent.append(packed)
    
    if (len(sent) > 0):
        sents.append(sent)
        
    print("Loaded " + str(len(sents)) + " sentences from BIO file: " + str(filename))
    
    return sents


def mkSentText(sent):
    text = ""
    for elem in sent:
        text += elem['word'] + " "
        
    text = text.strip()
    return text


#
#   Inference
#

def doInference(sent, model):
        
    text = mkSentText(sent)
    output = model.predict(text)
    
    
    #print(output)    
    #print(len(sent))
    #print(len(output))
    
    if (len(sent) != len(output)):
        print("ERROR: Length error")
        return []
    
    else:
        out = []
        for idx in range(0, len(sent)):
            score = 0
            if (sent[idx]['goldTag'] == output[idx]['tag']):
                score = 1
                
            packed = {'word': sent[idx]['word'], 'goldTag': sent[idx]['goldTag'], 'tag': output[idx]['tag'], 'score': score}
            
            out.append(packed)
    
    return out
    

def doInferenceBatch(sents, model, filenameOut):

    f = open(filenameOut, "w")
    
    
    for idx, sent in enumerate(sents):
        print(str(idx) + " / " + str(len(sents)))
        text = mkSentText(sent)
        
        try:                        
            print( mkSentText(sent) )
            out = doInference(sent, model)
        
            for elem in out:
                f.write(elem['word'] + "\t" + elem['goldTag'] + "\t" + elem['tag'] + "\t" + str(elem['score']) + "\n")
    
            f.write("\n")
            
        except:
            print("Unable to process")
            
    f.close()

#
#   Main
#

# LAUNCH
#dataIn = "/home/peter/github/ssa-ie2/data/launch/test.txt"
#filenameOut = "60_epoch_launch_inference.test.txt"
#model = Ner("out_launch/60_epoch/")

# FAILURE
#dataIn = "/home/peter/github/ssa-ie2/data/failure/test.txt"
#filenameOut = "60_epoch_failure_inference.test.txt"
#model = Ner("out_failure/60_epoch/")

# DECOMMISION
dataIn = "/home/peter/github/ssa-ie2/data/decom/test.txt"
filenameOut = "60_epoch_decom_inference.test.txt"
model = Ner("out_decom/60_epoch/")



sents = loadBIOFile(dataIn)


doInferenceBatch(sents, model, filenameOut)

