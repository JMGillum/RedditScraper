class Text:
    content = ""
    displayContent = []
    justify = 0 # 0 - Left, 1 - Center, 2 - Right
    width = 80

    def __init__(self,contents,preformatted=False,width=80):
        self.updateContents(contents,preformatted,width)

    def updateContents(self,contents,preformatted=False,width = 80):
        self.content = contents
        self.width = width
        self.updateDisplay(preformatted)
    
    def updateDisplay(self,preformatted = False):
        if(self.content == ""):
            return
        self.displayContent = []
        index = 0
        while(index < len(self.content)):
            endIndex = index + (self.width)
            if(endIndex >= len(self.content)):
                endIndex = len(self.content)
            else:
                if(preformatted == False):
                    while(not self.content[endIndex] == " "):
                        endIndex = endIndex - 1
                        if(endIndex == index):
                            endIndex = index + (self.width)
                            break
            string = self.content[index:endIndex]
            # if(not string.find("\n") == -1):
            #     endIndex = string.find("\n")
            #     string = self.content[index:endIndex]
            #     index = endIndex + 1
            # else:
            #     index = endIndex

            self.displayContent.append(Line(string,self.width))
            
            if(preformatted == False):
                while(index < len(self.content) and self.content[index] == " "):
                    index = index +1
            

        # while(line*self.width <= len(self.content)):
        #     string = ""
        #     string = self.content[line*self.width:(line+1)*self.width]
        #     self.displayContent.append(Line(string,self.width))
        #     line = line + 1
    
    def returnLines(self):
        return self.displayContent



class Line:
    content = ""
    displayContent = ""
    justify = 0 # 0 - Left, 1 - Center, 2 - Right
    width = 80
    def __init__(self,content,width = 80):
        self.updateContent(content,width)

    def updateContent(self,content,width = 80):
        if(len(content) <= width):
            self.content = content
            self.width = width
            self.content = self.content.replace("\n","")
            self.content = self.content.replace("\t","")
            self.content = self.content.replace(chr(8226),"*")
            self.displayContent = self.content
            if(self.justify == 1):
                self.justifyCenter()
            elif(self.justify == 2):
                self.justifyRight()
            else:
                self.justifyLeft()
            return True
        else:
            return False
    
    def returnLine(self):
        return self.displayContent

    def justifyLeft(self):
        self.justify = 0
        self.displayContent = self._placeString(self.content,self.width)
    
    def justifyCenter(self):
        self.justify = 1
        frontMargin = int((self.width - len(self.content))/2) # Number of leading spaces before content
        self.displayContent = self._placeString(self.content,self.width,frontMargin)

    def justifyRight(self):
        self.justify = 2
        frontMargin = self.width - len(self.content) # Number of leading spaces before content
        self.displayContent = self._placeString(self.content,self.width,frontMargin)

    def _placeString(self,string,length,start=0):
        if(len(string)>=length):
            return string
        s = ""
        s = s.zfill(length)
        s = s.replace("0"," ")
        s = s[:start] + string + s[start+len(string):]
        return s