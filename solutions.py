class ParseException(Exception):
    pass

class network:
    def __init__(self):
        self.event_numbers = 0
        self.events = {} # {"alice":1,"Bob":2}
        self.relations = {} # {0:[],1:[0],2:[3,4]}
        self.tables = {} # {1:[0.001,0.999]}

    def calpro(self,TF_table:list)->float:
        '''
        here TF_table is a list [True,False,False,True,True]
        cal pro from table return a float number
        '''
        result = float(1)
        for i in range(self.event_numbers):
            str_index = ""
            for j in self.relations[i]:
                if TF_table[j]:
                    str_index += "1"
                else :
                    str_index += "0"
            if TF_table[i]:
                str_index += "0"
            else:
                str_index += "1"
            index = int(str_index,2)
            temp = float(self.tables[i][index])
            result = result*temp
        return result

class problem:
    def __init__(self):
        self.event_name = ""
        self.conditions = {} # {"event1":True,"event2":False}
        self.string = ""
    def __str__(self):
        return self.string

def read_network(content:str)->network:
    l = content.split("\n\n")
    event_numbers = int(l[0])
    n = network()
    n.event_numbers = event_numbers
    for index,name in enumerate(l[1].split(" ")):
        if index>=event_numbers:
            raise ParseException
        n.events[name] = index
        n.relations[index] = []
    for i,line in enumerate(l[2].split("\n")):
        for j,value in enumerate(line.split(" ")):
            if value=="1" and i!=j :
                n.relations[j] += [i]
            if j>=event_numbers:
                raise ParseException
        if i >= event_numbers:
            raise ParseException
    try:
        for i in range(event_numbers):
            n.tables[i] = l[3+i].split()
    except:
        raise ParseException
    return n

def read_queries(content:str)->list():
    result = []
    for line in content.split("\n\n"):
        p = problem()
        p.string = line
        blocks = line.split(" ")
        for index,block in enumerate(blocks):
            if index == 0:
                p.event_name = block[2:]
            elif index == 1:
                if block!="|":
                    raise ParseException
            else:
                s = block[:-1].split("=")
                if s[1]=="true":
                    p.conditions[s[0]] = True
                elif s[1]=="false":
                    p.conditions[s[0]] = False
                else:
                    raise ParseException
        result.append(p)
    return result

def solute(bayes:network,question:problem)->(float,float):
    true_value = float(0)
    false_value = float(0)
    denominator = float(0)
    random_value_len = len(bayes.events)-len(question.conditions)
    for i in range(pow(2,random_value_len)):
        seq = bin(i)[2:].rjust(random_value_len,"0")
        table = []
        start = 0
        for event_name in bayes.events:
            if event_name in question.conditions:
                table.append(question.conditions[event_name])
            else :
                if seq[start] == "0":
                    table.append(False)
                else:
                    table.append(True)
                start += 1
        r = bayes.calpro(table)
        denominator += r
        if table[bayes.events[question.event_name]]==True:
            true_value += r
        else:
            false_value += r
    return (round(true_value/denominator,4),round(false_value/denominator,4))

if __name__=="__main__":
    try:
        with open("burglarnetwork.txt","r") as f:
            bayes_network = read_network(f.read())
        with open("burglarqueries.txt","r") as f:
            prolems = read_queries(f.read())
    except ParseException:
        print("parse burglarnetwork.txt failed")
        exit(0)
    for i in prolems:
        # a is true,while b is false
        (a,b)=solute(bayes_network,i) # a,b is two float number
        print(str(i)+" ===> ("+str(a)+","+str(b)+")")