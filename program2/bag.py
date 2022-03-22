from collections import defaultdict
from goody import type_as_str

class Bag:
    
    def __init__(self, iterable = []):
        self.dic = defaultdict(int)
        for x in iterable:
            self.dic[x] += 1
#             if x not in self.dic:
#                 self.dic[x] = 1
#             else:
#                 self.dic[x] += 1
                
    def __repr__(self):
        lis = str([x for x,y in self.dic.items() for _ in range(y)])
        return f"Bag({lis})"
    
    def __str__(self):
        s = "" 
        for x in self.dic:
            s += "".join(f"{x}[{self.dic[x]}],")
        return f"Bag({s.rstrip(',')})"
    
    def __len__(self):
        count = 0
        for x,y in self.dic.items():
            count += y
        return count
                
    def unique(self):
        count = 0
        for x in self.dic:
            count += 1
        return count
    
    def __contains__(self, arg):
        if arg in self.dic:
            return True
        return False  
    
    def count(self, arg):
        if arg in self.dic:
            return self.dic[arg]
        else:
            return 0
        
    def add(self, arg):
        if arg not in self.dic:
            self.dic[arg] = 1
        else:
            self.dic[arg] += 1  

    def __add__(self, arg):
        d = defaultdict(int)
        if not isinstance(arg, (Bag)):
            raise TypeError
        for k,v in self.dic.items():
            d[k] += v
        for kk,vv in arg.dic.items():
            d[kk] += vv
        lis = [k for k, v in d.items() for _ in range(v)]
        return Bag(lis)
        
    def remove(self, arg):
        if arg not in self.dic:
            raise ValueError
        else:
            if self.dic[arg] >= 1:
                self.dic[arg] -= 1
            if self.dic[arg] == 0:
                del self.dic[arg]
        
    def __eq__(self, arg):
        if not isinstance(arg, Bag):
            return False
        else:
            if self.dic == arg.dic:
                return True
            else:
                return False
            
    def __ne__(self, arg):
        if self.__eq__(arg):
            return False
        else:
            return True

    def __iter__(self):
        
        def gen(x):
            for k, v in x.items():
                for _ in range(v):
                    yield k
        return gen(dict(self.dic))


if __name__ == '__main__':
    #driver tests
    import driver
    driver.default_file_name = 'bscp21W20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
