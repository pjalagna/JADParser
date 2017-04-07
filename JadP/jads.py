# file jads.py
class S:
    """
pja 4-7-2017 original

class 
data
CGrid (current grid)
Fin - process file name
behaviors
debug() test till '.'
NewGrid => grid to CGrid (current grid)
SetFileName
Load
Save
DisplayGrid
GenType
InsertLoc
ClearLoc

test as
import jads
js = jads.S()
js.debug()

    """
    def __init__(self):
		""" prep """
		self.CGrid = ''
		self.Fin = ''
		self.fh = '' # file handle
	#end init
	
    def SetFileName(self):
	    self.Fin = raw_input("File Name? ")
	#end SetFileName
    def Save(self):
	    if (self.Fin == ''):
	        print("Set file name first")
	    else:
	        fh = open(self.Fin,'w')
	        fh.write(self.CGrid)
	        fh.close()
	    #endif
	#end save
    def Load(self):
	    if (self.Fin == ''):
	        print("Set file name first")
	    else:
	        fh = open(self.Fin,'r')
	        self.CGrid = fh.read() # entire file
	        fh.close() 
	    #endif
	#end save
    def help(self):
        ans = """
debug() test till '.'
NewGrid => grid to CGrid (current grid)
SetFileName
Load
Save
DisplayGrid
GenType
InsertLoc
ClearLoc

        """
        print(ans)
    #end help
    def debug(self):
		""" forth outer loop """
		inc = raw_input('>? ')
		while (inc != '.'):
			if (inc == 'NewGrid'):
				self.NewGrid()
				print("done")
			elif (inc == "DisplayGrid"):
				self.DisplayGrid()
				print('done')
			elif (inc == "Save"):
				self.Save()
				print('done')
			elif (inc == "Load"):
				self.Load()
				print('done')
			elif (inc == "SetFileName"):
				self.SetFileName()
				print('done')
			elif (inc == "help"):
				self.help()
				print('done')
			else:
				print('did not understand command ' + inc.__str__() + ' seek help')
			#endif
			inc = raw_input('>? ')
		#wend
	#end debug

    def NewGrid(self):
        t1 = """
<html>
  <head>
    <title> gridWork </title>
  </head>
  <body>
    <form name='f1' method='GET'>
        """
        t2 = """
      <input type='submit' name='s1' value='GO'/>
    </form>
  </body>

</html>
        """
        ap = "ABCDEFGHI"
        ans = "<table name='gridBox' border='3'>\n"
        ans = ans + "<tr>\n" 
        for c in range(0,8):
            for r in range(0,8):
                b1 = "<td id='" + ap[c] + r.__str__() + "'></td>\n"
                ans = ans + b1
            #end for-r
            ans = ans + "</tr>\n<tr>\n"
        #end for c
        ans = ans + "</tr>\n</table>"
        self.CGrid = t1 + ans + t2
	#end NewGrid

    def DisplayGrid(self):
        print("\n*********** GRID ************\n")
        print(self.CGrid.__str__())
        print("\n*********** GRID ************\n")
	#end DisplayGrid

