import sys

TOKENS_MAP = {"program": 1, "begin": 2, "end": 3, "int": 4, "if": 5,
              "then": 6, "else": 7, "while": 8, "loop": 9, "read": 10, "write": 11, ";": 12, ",": 13, "=": 14, "!": 15, "[": 16, "]": 17, "&&": 18, "||": 19, "(": 20, ")": 21, "+": 22, "-": 23, "*": 24, "!=": 25, "==": 26, "<": 27, ">": 28, "<=": 29, ">=": 30, "unsigned_int": 31, "identifier": 32, "EOF": 33, "\t": 34, "\r": 35, "\n": 36}
RESERVED_WORDS = {"program", "begin", "end", "int", "if",
                  "then", "else", "while", "loop", "read", "write"}
RESERVED_WORDS_FIRST_LETTER = {'p', 'b', 'e', 'i', 't', 'w', 'l', 'r'}
WHITESPACE_TOKENS = {"\n", "\r", "\t", " "}
# list of symbols that can only have one character (ie cannot be !=)
SINGLE_SPECIAL_SYMBOLS = {";", ",", "[", "]", "(", ")", "+", "-", "*"}
# list of symbols that require more analyzing because they could have another character going with it
VERY_SPECIAL_SYMBOLS = {"=", "!", "&", "|", "<", ">"}
#LOWERCASE_CHARS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
UPPERCASE_CHARS = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                   'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
INTEGERS = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}


class Tokenizer:
    def __init__(self, input_file):
        self.currentToken = ""  # a buffer for the current token
        self.file = open(input_file, "r")
        self.line = self.file.readline()
        self.pointer = 0  # initialize a pointer to point to the first element in the line
        self.outputBuffer = []  # each time we get a full token, we append it to this buffer. In the end, getToken will be called on this buffer repeatedly to convert the built tokens into integers
        self.bufferPointer = 0  # points to index for current element in output buffer
        self.tokenizeLine()

    # returns integer from mapping corresponding to key (current token)
    def getToken(self):
        return TOKENS_MAP.get(self.outputBuffer[self.bufferPointer])

    # skips current token so that the next token becomes the current
    def skipToken(self):
        # increment bufferPointer
        self.bufferPointer += 1
        if self.bufferPointer == len(self.outputBuffer):
            # indicates that we are at the end of the line
            # clear output buffer and start new line
            self.outputBuffer.clear()  # clear output buffer
            self.line = self.file.readline()  # get next line
            if self.line == "":
                # indicates we are at the end of the file
                # append EOF to output buffer and return
                self.outputBuffer.append("EOF")
                self.bufferPointer = 0
                return
            self.line += "\n"  # forcing "\n" at the end of the line in order to know that the line is done without going out of index bounds and crashing
            self.bufferPointer = 0  # reset
            self.currentToken = ""  # reset
            self.pointer = 0
            self.tokenizeLine()  # tokenize new line
            # if the outputBuffer is still empty, then that means the line had nothing in it
            # so we basically need to try again
            # account for this in newer versions

    # returns the value of the current (integer) token; error if not integer
    def intVal(self):
        if int(self.currentToken).isnumeric():
            return int(self.currentToken)
        else:
            print("Error: not an integer")
            return

    # returns the name (string) of the current (id) token; error if not id
    def idName(self):
        if self.currentToken.isIdentifier:
            return self.currentToken
        else:
            print("Error: not an identifier")
            return

    def tokenizeReservedWord(self):
        self.currentToken = ""
        # build entire token
        while self.line[self.pointer] not in WHITESPACE_TOKENS and self.line[self.pointer].islower():
            self.currentToken += self.line[self.pointer]
            self.pointer += 1
        # add the tokenized word to the output buffer
        self.outputBuffer.append(self.currentToken)

    def tokenizeInteger(self):
        self.currentToken = ""
        while self.line[self.pointer].isnumeric():
            self.currentToken += self.line[self.pointer]
            self.pointer += 1  # move pointer forward
        # add tokenized integer (simply "unsigned_int") to output buffer
        self.outputBuffer.append("unsigned_int")

    def tokenizeIdentifier(self):
        self.currentToken = ""
        while self.line[self.pointer].isnumeric() or self.line[self.pointer] in UPPERCASE_CHARS:
            self.currentToken += self.line[self.pointer]
            self.pointer += 1  # move pointer forward
        self.outputBuffer.append("identifier")

    def tokenizeSpecialSymbols(self):
        self.currentToken = ""
        # check for symbols that only have one character , ; * - + ( ) [ ]
        if self.line[self.pointer] in SINGLE_SPECIAL_SYMBOLS:
            # add to current token
            self.currentToken += self.line[self.pointer]

        elif self.line[self.pointer] in VERY_SPECIAL_SYMBOLS:
            # these symbols could have more than one character
            # add to current token
            self.currentToken += self.line[self.pointer]
            if self.currentToken == "<" or self.currentToken == ">" or self.currentToken == "=" or self.currentToken == "!":
                # could have "=" after. if so, append
                if self.line[self.pointer+1] == "=":
                    self.currentToken += self.line[self.pointer+1]
                    # increment pointer by 1 (we will increment this again at the end of the conditional)
                    self.pointer += 1
            elif self.currentToken == "&":
                # make sure there's another &, else throw an error
                if self.line[self.pointer+1] == "&":
                    self.currentToken += self.line[self.pointer+1]
                else:
                    # throw error
                    print("Error: invalid token. Exiting program")
                    quit()
            elif self.currentToken == "|":
                # make sure there's another |, else throw an error
                if self.line[self.pointer+1] == "|":
                    self.currentToken += self.line[self.pointer+1]
                else:
                    # throw error
                    print("Error: invalid token. Exiting program")
                    quit()
        # add currentToken to buffer
        self.outputBuffer.append(self.currentToken)
        # increment pointer
        self.pointer += 1

    def tokenizeLine(self):
        # reset current token to be empty
        self.currentToken = ""
        while self.pointer < len(self.line):
            self.currentToken = self.line[self.pointer]
            if self.currentToken in RESERVED_WORDS_FIRST_LETTER:
                # call tokenize_reservedword
                self.tokenizeReservedWord()  # this updates currentToken
            elif self.currentToken.isnumeric():
                self.tokenizeInteger()
            elif self.currentToken in UPPERCASE_CHARS:
                self.tokenizeIdentifier()
            elif self.currentToken in SINGLE_SPECIAL_SYMBOLS or self.currentToken in VERY_SPECIAL_SYMBOLS:
                self.tokenizeSpecialSymbols()
            # FIX BELOW
            elif self.currentToken in WHITESPACE_TOKENS:
                if self.currentToken == "\n":
                    # hard code pointer such that the while loop exits
                    self.pointer = len(self.line)
                else:
                    self.pointer += 1


def main():
    tokenizer = Tokenizer(sys.argv[1])
    # for debugging:
    #tokenizer = Tokenizer("data/prog1_correct.txt")
    # call Tokenizer class constructor and pass input_file
    token = tokenizer.getToken()

    # repeatedly call getToken(), print token, call skipToken() until getting EOF token -> terminate loop
    while token != 33:
        token = tokenizer.getToken()
        print(token)
        tokenizer.skipToken()
    tokenizer.file.close()


if __name__ == "__main__":
    main()
