
import re,os.path


class DataTriple(object):
    """
    Base Data class
    """

    def __init__(self, data):
        self.raw_data_ = data

    def getData(self):
        return self.raw_data_


class Subject(DataTriple):
    """
    Predicate instance class
    """

    def __init__(self, data):
        DataTriple.__init__(self,data)
        self.url=re.sub("^<","",re.sub(">$","",self.raw_data_))
    def getData(self):
        return self.url

class Object(DataTriple):
    """
    Object instance class
    """

    def __init__(self, data):
        DataTriple.__init__(self,data)
        self.type,self.lang,self.data=None,None,None
        # typed Data
        if (re.match("\^\^",self.raw_data_)):

            datas=self.raw_data_.split("^^")
            self.data=re.sub("\"","",datas[0])
            self.type=re.sub("^<","",re.sub(">$","",datas[1]))

        # lang Data
        if(re.match("\".+\"@[\w]+",self.raw_data_)):
            datas=self.raw_data_.split("@")

            if(len(datas) > 2):
                datas=["@".join(datas[0:-1]),datas[-1]]
            self.lang=re.sub("\"","",datas[1])
            self.data=re.sub("\"","",datas[0])
        if re.match("^<.+>$",self.raw_data_):
            self.data=re.sub("^<","",re.sub(">$","",self.raw_data_))
    def getData(self):
        return {"data":self.data,"type":self.type,"lang":self.lang}

class Predicate(DataTriple):
    """
    Predicate instance class
    """

    def __init__(self, data):
        DataTriple.__init__(self,data)
        self.url=re.sub("^<","",re.sub(">$","",self.raw_data_))

    def getData(self):
        return self.url


class Triple(object):
    """
    Class that store a rdf triple
    """

    def __init__(self, string_line, delimiter=" "):
        # Some pretreatment
        self.raw_ = re.sub(".$", "", string_line).strip()

        # Split the triple string
        self.datas = self.raw_.split(delimiter)

        # Missing or wrong Delimiter
        if(len(self.datas) < 3):
            print("Format Error with the string : " + self.raw_)
            self = None

        # Case like <subjectURI>[delimiter]<predicateURI>[delimiter]"Le[delimiter]chien<[delimiter]de[delimiter]Paco"@fr
        if (len(self.datas) > 3):
            self.datas = [self.datas[0], self.datas[1],
                          " ".join(self.datas[2:len(self.datas)])]
        #print(self.datas)
        # Instantiate each triple parts
        self.subject_ = Subject(self.datas[0])
        self.predicate_ = Predicate(self.datas[1])
        self.object_ = Object(self.datas[2])

    def get_subject(self):
        """
        Subject instance getter
        """
        return self.subject_

    def get_predicate(self):
        """
        Predicate instance getter
        """
        return self.predicate_

    def get_object(self):
        """
        Object instance getter
        """
        return self.object_

    def __repr__(self):
        return "\tsubject:{0} \n\t predicate:{1} \n\t object:{2}".format(self.subject_.getData(),self.predicate_.getData(),self.object_.getData())

class TripleRdfFileIterator(object):
    """docstring for TripleParser."""
    def __init__(self, filename,delimiter=" "):
        self.delimiter_=delimiter
        if not os.path.isfile(filename):
            print("The file {0} you want to work with don't exists !!".format(filename))
            return False
        self.data_file=open(filename,'r')

    def __iter__(self):
        return self
    def __next__(self):
        line=self.data_file.readline()
        if line:
            return Triple(line, self.delimiter_)
        else:
            return False
