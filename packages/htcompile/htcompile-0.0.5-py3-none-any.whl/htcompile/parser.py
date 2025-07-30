import re
import os
import shutil

class Parser:
    
    def __init__(self, src: str, dst: str, infiles: list[str]):
        self.src: str = os.path.normpath(src)
        self.dst: str = os.path.normpath(dst)
        self.infiles: list[str] = []
        self.stack: list[str] = []
        self.outfiles: list[str] = []
        
        for p in infiles:
            self.infiles.append(os.path.normpath(p))
        print(self.infiles)
    
    def findImportMatch(self, data: str) -> str:
        pattern = r"<htcompile\s+.*?>"
        match = re.search(pattern, data)
        if match:
            return match.group()
        return ""
    
    def findImportPath(self, fileP: str, imp: str) -> str:
        pattern = r'<htcompile\s+src="(.*?)"\s*\\?>'
        match = re.search(pattern, imp)
        if match:
            if match.group(1).startswith("/"):
                return self.processPath(match.group(1)[1:])
            return os.path.join(os.path.dirname(fileP), match.group(1))
        return ""
    
    def readPath(self, path: str) -> str:
        return os.path.join(self.src, path)
    
    def writePath(self, path: str) -> str:
        return os.path.join(self.dst, path)

    def processPath(self, path: str) -> str:
        return os.path.normpath(path)
    
    def parse(self):
        
        l: int = len(self.infiles)
        
        while l > 0:
            fileP = self.infiles[0]
            self.processFile(fileP)
            l = len(self.infiles)
            
    
    def processFile(self, fileP: str) -> str:
        print(fileP)
        if fileP not in self.infiles:
            raise Exception("ERR: File not in list of files!!! " + fileP)

        self.infiles.remove(fileP)
        self.stack.append(fileP)
        
        data: str = ""

        try:
            with open(self.readPath(fileP), 'r') as file:
                data = file.read()
        except UnicodeDecodeError:
            os.makedirs(os.path.dirname(self.writePath(fileP)), exist_ok=True)
            shutil.copy(self.readPath(fileP), self.writePath(fileP))
            return ""
        
        imp: str = self.findImportMatch(data)
        while imp:
            impPath: str = self.processPath(self.findImportPath(fileP, imp))
            if impPath in self.stack:
                raise Exception("ERR: Circular import!!! " + imp)
            if impPath not in self.infiles and impPath not in self.outfiles:
                print(self.findImportPath(fileP, imp))
                raise Exception("ERR: File not found!!! " + impPath + " in " + fileP)

            if impPath in self.outfiles:
                impData: str
                with open(self.writePath(impPath), 'r') as file1:
                    impData = file1.read()
                data = data.replace(imp, impData)
            
            elif impPath in self.infiles:
                impData: str = self.processFile(impPath)
                data = data.replace(imp, impData)
            imp = self.findImportMatch(data)
        
        outPath: str = self.writePath(fileP)
        print(outPath)
        os.makedirs(os.path.dirname(outPath), exist_ok=True)
        with open(outPath, 'w+') as file:
            file.write(data)

        self.outfiles.append(self.stack.pop())
        
        return data