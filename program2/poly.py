
class Poly:
    # coefficient is value and power is key
    
    def __init__(self, *tup):
        
        self.ar = tup

        self.terms = {}
        for x,y in tup: 
            if x != 0: self.terms[y] = x
        
        for x, y in tup:
            assert isinstance(x, (int, float)) and isinstance(y, (int)), "Not int or float"
            assert y >= 0, "Power is less than 0"
        
        
        i = iter(tup)
        try:
            current = next(i)[1]
            while True:
                nex = next(i)
                if nex[1] >= current:
                    raise AssertionError
        except StopIteration:
            return
        
    def __repr__(self):
        string = "Poly("
        s = sorted(self.terms, reverse = True)
        for x in s:
            string += "("+ str(self.terms[x]) + ", " + str(x) + ")" + ", "
        string = string.rstrip(", ")
        return string + ")"
    
    def __str__(self):
        string = ""
        s = sorted(self.terms, reverse = True)
#         print(self.terms)
        if self.terms == {}: return "0"
        else:
            for x in s:
                if x == 0: 
                    if self.terms[x] > 0: string += str(self.terms[x])
                    else: 
                        if len(s) == 1:
                            string += str(self.terms[x])
                        else:
                            string = string.rstrip(" + ")
                            string += " - " + str(self.terms[x]).lstrip("-")
                elif x == 1: 
                    if self.terms[x] > 1: string += str(self.terms[x]) + "x" + " + "
                    elif self.terms[x] == 1: string += "x" + " + "
                    else: 
                        string = string.rstrip(" + ")
                        if self.terms[x] == -1: string += " - " + "x" + " + "
                        else:
                            if string == "": string += str(self.terms[x]) + "x" +  " + "
                            else: string += " - " + str(self.terms[x]).lstrip("-") + "x" + " + "
                else:
                    if self.terms[x] > 1: string += str(self.terms[x]) + "x^" + str(x) +  " + "
                    elif self.terms[x] == 1: string += "x^" + str(x) + " + "
                    else: 
                        string = string.rstrip(" + ")
                        if self.terms[x] == -1: 
                            if string == "": string += "-x^" + str(x) + " + "
                            else: string += " - " +  "x^" + str(x) +  " + "
                        else:
                            if string == "": string += str(self.terms[x]) + "x^" + str(x) +  " + "
                            else: string += " - " + str(self.terms[x]).lstrip("-") + "x^" + str(x) +  " + "
        return string.rstrip(" + ")
          
                
    def __bool__(self):
        if self.__str__() != "0": return True
        else: return False
       
        
    def __len__(self):
        if self.__str__() =='0': return 0
        return max([i for i,j in self.terms.items()])
        
                
    def __call__(self, arg):
        count = 0
        for k,v in self.terms.items():
            mult = arg ** k
            count += mult * v
        return count

    def __iter__(self):
        for k,v in self.terms.items():
            yield (v,k)


    def __getitem__(self, arg):
        if arg < 0: raise TypeError
        if arg not in self.terms: return 0
        return self.terms[arg]
    
    def __setitem__(self, power, coef):
        if not isinstance(power,int) or power<0:
            raise TypeError
        if coef ==0:
            try:
                del self.terms[power]
            except:
                pass
        else:
            self.terms[power] = coef
        
    def __delitem__(self,arg):
        if not isinstance(arg,int) or arg<0:
            raise TypeError
        try:
            del self.terms[arg]
        except KeyError:
            pass
        
    def _add_term(self, coef, power):
        if not isinstance(coef, (int, float)) and not isinstance(power, int) and power < 0:
            raise TypeError
        elif power not in self.terms and coef != 0:
            self.terms[power] = coef
        elif power in self.terms:
            self.terms[power] += coef
            if self.terms[power] == 0:
                del self.terms[power]
                
    def __pos__(self):
        tu = ((v,k) for k,v in self.terms.items())
        c = tuple(tu)
        return Poly(*c)
    
    def __neg__(self):
        tu = ((-v,k) for k,v in self.terms.items())
        c = tuple(tu)
        return Poly(*c)
    
    def __abs__(self):
        tu = ((abs(v),k) for k,v in self.terms.items())
        c = tuple(tu)
        return Poly(*c)
    
    def differentiate(self):
        cc = {}
        c = self.terms.copy()
        for coef,power in c.items():
            power *=coef
            coef-=1
            cc[coef] = power
        a = tuple((v,k) for k,v in cc.items() if k>=0 )
        return Poly(*a)
    
    def integrate(self,arg=0):
        cc = {}
        c = self.terms.copy()
        for power,coef in c.items():
            power +=1
            coef = coef/power
            cc[power] = coef
        cc[0] = arg
        a = tuple((v,k) for k,v in cc.items() if k>=0 )
        
        return Poly(*a)
        
    def def_integrate(self,lower,upper):
        a = self.integrate()
        return a.__call__(upper) - a.__call__(lower)
    
    
    def __add__(self,right):
        pol = Poly()
        if isinstance(right,int):
            pol._add_term(right,0)
            for power,coef in self.terms.items():
                pol._add_term(coef,power)
        elif isinstance(right,Poly):
            for power,coef in right.terms.items():
                pol._add_term(coef,power)
            for power,coef in self.terms.items():
                pol._add_term(coef,power)
        else:
            raise TypeError
        return pol
        
        
    def __radd__(self,left):
        return self + left
    
    
    def __sub__(self,right):
        return self.__add__(-right)
        
            
    def __rsub__(self,right):
        return -self + right
    
    
    def __mul__(self,right):
        pol = Poly()
        a = 0
        b = 0
        if isinstance(right,Poly):
            for power,coef in self.terms.items():
                
                for p,c in right.terms.items():
                    a = coef *c
                    b = p + power
                    pol._add_term(a,b)
        elif isinstance(right,int):
            for power,coef in self.terms.items():
                a = coef * right
                b = power
                pol._add_term(a,b)
        else:
            raise TypeError
        return pol
                    
    
    def __rmul__(self,right):
        return self * right

    
    def __pow__(self,right):
        pol = Poly(*self.ar)
        if right == 1:
            return self
        elif right ==0:
            return 1
        elif right == 2:
            return pol.__mul__(pol)
        elif right < 0:
            raise TypeError
        else:
            for i in range(1, right + 1):
                if i%2==0:
                    pol = pol.__mul__(pol)
            return pol.__mul__(pol)
        
    def __eq__(self, arg):
        if self.__str__() == arg.__str__(): return True
        elif not isinstance(arg, (Poly, int, float)): raise TypeError
        else: return False
        
    def __lt__(self, arg):
        if isinstance(self, Poly) and isinstance(arg, Poly):
            for p,c in self.terms.items():
                for pp,cc in arg.terms.items():
                    if p < pp: return True
                    elif p == pp:
                        if c < cc: return True
                        else: return False
                    else: return False
                    break 
        elif isinstance(arg, (int, float)) and isinstance(self, Poly):
            if 0 in self.terms:
                num = self.terms[0]
                if num < arg: return True
                else: return False
#         elif isinstance(self, (int, float)) and isinstance(arg, Poly):
#             if 0 in arg.terms:
#                 if self.arg[0] < self: return True
#                 else: return False
        elif not isinstance(arg, (Poly, int, float)): raise TypeError
        
   
    def __gt__(self, arg):
        if not isinstance(arg, (Poly, int, float)): raise TypeError
        else: 
            if self.__lt__(arg): return False
            else: return True


    
if __name__ == '__main__':
    #Simple tests before running driver
    #Put your own test code here to test Poly before doing bsc tests
    #Debugging problems with tests is simpler

#     print('Start of simple tests')
#     p = Poly((3,2),(-2,1),(4,0))
#     print('  For Polynomial: 3x^2 - 2x + 4')
#     print('  str(p):',p)
#     print('  repr(p):',repr(p))
#     print('  len(p):',len(p))
#     print('  p(2):',p(2))
#     print('  list collecting the iterator results:', [t for t in p])
#     print('  p+p:',p+p)
#     print('  p+2:',p+2)
#     print('  p*p:',p*p)
#     print('  p*2:',p*2)
#     print('End of simple tests\n\n')
    
    import driver
    driver.default_file_name = 'bscp22W20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()     
