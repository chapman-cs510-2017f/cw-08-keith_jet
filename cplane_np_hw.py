import cplane_np as c_np
import numpy as np
from cplane_np import ArrayComplexPlane
import matplotlib.pyplot as plt

class JuliaPlane(ArrayComplexPlane):    
    def __init__(self, c):

        
        self.xmin = -1
        self.xmax = 1
        self.xlen = 2000
        self.ymin = -1
        self.ymax = 1
        self.ylen = 2000
        self.fs =[]
        
        self.c=c
        self.__initplane__()         
        
    def __initplane__(self):
        #print("init plane as:")
        super().__initplane__() #call parent method
        #print(self.plane)
        fv = np.vectorize(julia(self.c))
        self.plane=fv(self.plane)
        #print("plane transformed as:")
        #print(self.plane)

    def refresh(self):
        """Regenerate complex plane.
        Populate self.plane with new points (x + y*1j), using
        the stored attributes of xmax, xmin, xlen, ymax, ymin,
        and ylen to set plane dimensions and resolution. Reset
        the attribute fs to an empty list so that no functions 
        are transforming the fresh plane.
        """        
        self.fs = []
        self.__initplane__()
     
    def toCSV(self, filename):
        f = open(filename, "a")
        f.write(filename+"\n")
        f.write("Paratemters:")
        f.write("\n")
        f.write('c='+str(self.c)+"\n")
        f.write("xmin="+str(self.xmin)+"\n")
        f.write("xmax="+str(self.xmax)+"\n")
        f.write("xlen="+str(self.xlen)+"\n")
        f.write("ymin="+str(self.ymin)+"\n")
        f.write("ymax="+str(self.ymax)+"\n")
        f.write("ylen="+str(self.ylen)+"\n")
        f.write("\n")
        f.write("\n")
        f.write("The array of the transformed plane by Julia:\n")        
        for i in range(0, len(self.plane)):
            rowval=''
            for j in range(0, len(self.plane[i])):
                rowval=rowval+str(self.plane[i][j])+','
            rowval=rowval[:-1] #get rid of last ','
            f.write(rowval)
            f.write("\n")
        
        f.close()
        
    def fromCSV(self, filename):
        #read paramets from CSV file and reset the plane to match the settings in the file
        f = open(filename,"r")
        #ignore the file header
        f.readline()
        f.readline()
        #get c
        r=f.readline()
        self.c=complex(r[2:])

        r=f.readline()
        self.xmin=int(r[5:])
        
        r=f.readline()
        self.xmax=int(r[5:])
        
        r=f.readline()
        self.xlen=int(r[5:])
        
        r=f.readline()
        self.ymin=int(r[5:])
        
        r=f.readline()
        self.ymax=int(r[5:])

        r=f.readline()
        self.ylen=int(r[5:])
        
        #  refresh the plane array to the values stored in the .csv file directly.
        self.refresh(self.c)
   
    def show(self):
        plt.imshow(self.plane, interpolation = 'bicubic', cmap =('viridis'), extent = (self.xmin,self.xmax,self.ymin,self.ymax) )
        plt.title('c='+str(self.c))
        plt.show()
        
def julia(c):
    '''
    This function returns a function specified by the following algorithm:
    1. The returned function should take one complex parameter z as an input, and return one positive integer as an output.
    2. If the input number z has a magnitude abs(z) larger than 2, the function should output the integer 1.
    3. Otherwise, set a counter n=1.
    4. Increment n by 1, then transform the input z according to the formula z = z**2 + c.
        Check the resulting magnitude abs(z): If the magnitude now exceeds 2, then return the value of n;
        If the magnitude does not yet exceed 2, repeat this step.
    5. If the positive integer max is reached before the magnitude of z exceeds 2, the preceding loop should abort 
        and return the output integer 0.
    
    input parameters:
        c: a complex
        maxnumber: an optional positive integer, if it is reached before the magnitude of z exceeds 2, the preceding loop should abort 
        and return the output integer 0
        
    return:
        return a function with complex z as an input and return one postive interger as an output
        
        
   Examples of use of this function:

    >>> f1 = julia(c,100)
    >>> f2 = f1(z)
    '''
    def magnitude(z):
        n=0
        if abs(z)>2:
            #print("init abs(z)>2")
            return 1
        else:
            n=1
        
        while abs(z) < 2:            
            z=z**2+c
            n +=1
        return n
    
    return magnitude


#jp=JuliaPlane(1+0.5*1j)

#print("write para and transformed plane to CSV file")
#jp.toCSV("jp.csv")

#print("ream para and transformed plane from CSV file")
#jp.fromCSV("jp.csv")

#print("refresh the plane with para from CSV file")
#print(jp.plane)

'''
print("what happen when refreh by c=0.5+0.5*1j")
jp.refresh(0.5+0.5*1j)
print(jp.plane)

print("what happen when c=0")
jp=JuliaPlane(0+0*1j)

'''
#f1=julia(-0.01-0.01*1j,100)
#print(f1)

#f2=f1(1+2*1j)
#print(f2)