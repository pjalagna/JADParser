# file name SQClass.py version 1-30-2013
# need to incorporate the meta table sqlite_master perhaps "SQmeta {type} {name}"
# CREATE TABLE sqlite_master(
#  type text,
#  name text,
#  tbl_name text,
#  rootpage integer,
#  sql text
# );
# pja - 11-3-12 - SQCSVLoad(dbna,csvFile)
#                 CSV files MUST follow the following format
#                 a) line 1 must contain the names of the key elements
#                 b) line 2 must contain the names of the tag elements
#                 c) no column can contain a comma
class SQC:
    """ DAO type class for i/f with sqlite databases """
    def __init__(self,dbna):
        """ connect and remember name """
        import sqlite3
        self.dh = sqlite3.Connection(dbna)
        self.cursor = self.dh.cursor()
        self.dbna = dbna
    # end def init
    def SQClose(self):
        self.cursor.close()
        self.dh.close
    # end def
    def hasRecords(self,dt):
        """ rets yes or no """
        mx = dt.__str__()
        # # print ('dt(' + mx.__str__() + ")")
        if ( mx.__str__() == "None"):
            ans = "no"
        else:
            ans = 'yes'
        #end if
        return(ans)
    # end def hasRecords
    def SQX(self, stmt):
        """ executes sql commands return is ?? """
        self.cursor = self.dh.cursor()
        self.drec = self.cursor.execute(stmt)
        self.dh.commit()
        ans = self.drec
        return(ans)
    # end def sqx
    def SQRead1(self,stmt):
        """ -- """
        self.cursor = self.dh.cursor()
        self.drec = self.cursor.execute(stmt)
        dt = self.drec.fetchone()
        self.cursor.close()
        return(dt)
    # end def SQRead1
    def SQReadFirst(self,stmt):
        """ -- """
        self.cursor = self.dh.cursor()
        self.drec = self.cursor.execute(stmt)
        dt = self.drec.fetchone()
        # check type of dt if nonetype close cursor
        return(dt)
    # end def SQReadFirst
    def SQReadNext(self):
        """ = """
        dt = self.drec.fetchone()
        # check type of dt if nonetype close cursor
        return(dt)
    # end def SQReadNext
    def SQReadAll(self,stmt):
        """ -- """
        self.cursor = self.dh.cursor()
        self.drec = self.cursor.execute(stmt)
        dt = self.drec.fetchall()
        self.cursor.close()
        return(dt)
    # end def SQReadAll
# end class
