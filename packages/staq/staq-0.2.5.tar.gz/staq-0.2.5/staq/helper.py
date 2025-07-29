

def splitWithEscapes(string, delimiter, escape_pairs = ['""',"{}","[]","<>","()"], strip = True):
    """
    Split a string by a delimiter, but ignore delimiters that are inside escape_pairs.
    """
    split = []
    counts = {}

    for pair in escape_pairs:
        counts[pair] = 0

    start = 0
    current = ""

    def processEscapes(char):
        for key in escape_pairs:
            if key[0] == key[1] and char == key[0]:
                #if the escape pair is the same character, then we toggle the escape at each instance
                counts[key] = counts[key] ^ 1
            else:
                if char == key[0]:
                    counts[key] += 1
                elif char == key[1]:
                    counts[key] -= 1
    
    def isEscaped():
        for key in escape_pairs:
            if counts[key] > 0:
                return True
        return False
        
    current = ''
    for i in range(len(string)):
        
        if string[i] == delimiter and not isEscaped() and current != '':

            if strip:
                current = current.strip()
            split.append(current)
            current = ''
        else:
            processEscapes(string[i])
            current += string[i]
    
    if current != '':
        if strip:
            current = current.strip()
        split.append(current)
    
    return split
