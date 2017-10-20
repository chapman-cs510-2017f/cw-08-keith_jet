###
# Name: Keith, Jianhua 
# Course: CS510 Fall 2017
# Assignment: Classwork 5
# Date: 10-2017
###

import numpy as np
import pandas as pd


from abscplane import AbsComplexPlane


class ArrayComplexPlane(AbsComplexPlane):
    """
    
    A complex plane is a 2D grid of complex numbers, having
    the form (x + y*1j), where 1j is the unit imaginary number in
    Python, and one can think of x and y as the coordinates for
    the horizontal axis and the vertical axis of the plane, 
    respectively. Recall that (1j)*(1j) == -1. Also recall that 
    the FOIL rule for multiplication still works:
        (x + y*1j)*(v + w*1j) = (x*v - y*w + (x*w + y*v)*1j)
    You can check these results in an interpreter.
    
    We will explore several implementations for a complex plane in
    this course, so we wish to have an abstract interface that
    is independent of any particular implementation.
    
    In addition to generating the 2D grid of numbers (x + y*1j),
    we wish to easily support transformations of the plane with
    arbitrary complex functions f. The class attribute self.plane
    should store a 2D grid of numbers (x + y*1j) such that the
    parameter x ranges from self.xmin to self.xmax with self.xlen
    total points, while the parameter y ranges from self.ymin to
    self.ymax with self.ylen total points. The class attribute
    self.fs should store a list of functions that are being applied
    in order to each point of the complex plane, initially empty. 
    The method self.apply(self,f) should take a function f that transforms 
    a complex number into another complex number and map that function 
    over the complex plane to produce the grid of numbers f(x + y*1j),
    adding the function f to the list self.fs in the process. If the
    method apply is called multiple times with different functions, then
    self.fs should record the ordered sequence of functions, and self.plane
    should contain the final output after applying the entire sequence
    of functions. The method self.refresh should regenerate the complex
    plane and clear all functions that transform the plane. The method
    self.zoom should reset the parameters for the 2D grid of points and
    regenerate the grid, reapplying all collected functions to each point.
    
    Note that it may be advantageous to define other methods for your
    implementation that are not specified here. By convention, "private"
    methods should be named with a double underscore (e.g., __mymethod)
    to hide it from the user interface. Helper methods that you define
    should be made private in this manner to keep the interface clean.
    
    Attributes:
        xmax (float) : maximum horizontal axis value
        xmin (float) : minimum horizontal axis value
        xlen (int)   : number of horizontal points
        ymax (float) : maximum vertical axis value
        ymin (float) : minimum vertical axis value
        ylen (int)   : number of vertical points
        plane        : stored complex plane implementation
        fs (list[function]) : function sequence to transform plane
    """ 
     
    def __init__(self, xmin, xmax, xlen, ymin, ymax, ylen):
        self.xmin = xmin
        self.xmax = xmax
        self.xlen = xlen
        self.ymin = ymin
        self.ymax = ymax
        self.ylen = ylen
        self.fs =[]
        self.__initplane__() #init plane 
   
    def __initplane__(self):
        '''
        init the complex plane by average distance of X and Y
        '''
        
        
        ##use numpy to add the 2D grid in an array
        x=np.linspace(self.xmin,self.xmax,self.xlen)
        y=np.linspace(self.ymin,self.ymax,self.ylen)
        xx, yy = np.meshgrid(x,y)
        self.plane = xx + yy*1j
        #self.df = pd.DataFrame(xx+(1j)*yy, index=y, columns=x)
        #print(self.df)
        #self.df = pd.DataFrame(self.plane, index=y, columns=x) ---not worked

        
        '''
        add the 2D grid in a list in list  *****---- use list to generate 2D plane (just for comparsion with numpy)---------------
        #self.plane = []
        #xunit = (self.xmax - self.xmin)/(self.xlen - 1)
        #yunit = (self.ymax - self.ymin)/(self.ylen - 1)
        #self.plane = [[(self.xmin + i*xunit)+(self.ymin + j*yunit)*1j for i in range(self.xlen)]for j in range(self.ylen)]
        '''
        
        '''
        The following get a list, not list in list as required
        for i in range(self.xlen):
            for j in range(self.ylen):
                self.plane.append((self.xmin + i*xunit)+(self.ymin + j*yunit)*1j)
        '''
       

    def refresh(self):
        """Regenerate complex plane.
        Populate self.plane with new points (x + y*1j), using
        the stored attributes of xmax, xmin, xlen, ymax, ymin,
        and ylen to set plane dimensions and resolution. Reset
        the attribute fs to an empty list so that no functions 
        are transforming the fresh plane.
        """
        self.__initplane__()
        self.fs = []
   
    def apply(self, fun):
        """Add the function f as the last element of self.fs. 
        Apply f to every point of the plane, so that the resulting
        value of self.plane is the final output of the sequence of
        transformations collected in the list self.fs.
        """
        
        #self.plane = fun(self.plane)
        
        # use numpy vectorize 
        fv = np.vectorize(fun)
        self.plane = fv(self.plane)
        self.fs.append(fun)
    
    def zoom(self,xmin,xmax,xlen,ymin,ymax,ylen):
        """Reset self.xmin, self.xmax, and self.xlen.
        Also reset self.ymin, self.ymax, and self.ylen.
        Regenerate the plane with the new range of the x- and y-axes,
        then apply all transformations in fs in the correct order to
        the new points so that the resulting value of self.plane is the
        final output of the sequence of transformations collected in
        the list self.fs.
        """
        #init the plane
        self.xmin = xmin
        self.xmax = xmax
        self.xlen = xlen
        self.ymin = ymin
        self.ymax = ymax
        self.ylen = ylen
        self.__initplane__()
        
        # use numpy vectorize 
        if len(self.fs) > 0:
            for fun in self.fs:
                fv = np.vectorize(fun)
                self.plane=fv(self.plane)
        else:
            print("no fun applied")
        
        
        '''
        ----------use funtions list-----
        if len(self.fs) > 0:
            for fun in self.fs:
                self.plane = fun(self.plane)
        else:
            print("no fun applied")

'''
'''
def doubleplane(plane):
    # mulitple the grids
    for i in range(len(plane)):
        for j in range(len(plane[i])):
            plane[i][j] *=2
    return plane*2

def powerplane(plane):
    #mulitple the grids by iteself
    for i in range(len(plane)):
        for j in range(len(plane[i])):
            plane[i][j] =plane[i][j] * plane[i][j] 
    return plane**2
'''

'''
LCP = ArrayComplexPlane(1,4,3,2,5,3)
print("init plane")
print(LCP.plane)

print("double fun")
LCP.apply(doubleplane)
print(LCP.plane)

print("power fun")
LCP.apply(powerplane)
print(LCP.plane)

print("add 2")
#ff = lambda x: x+(1+1*1j)
ff = lambda x: x+2
LCP.apply(ff)
print(LCP.plane)


#print(LCP.fs)
'''