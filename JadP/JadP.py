# file jadP.py table def parser
""" JadT - asks for filename """
import time
global ts
ts = time
def ask(token):
    j = raw_input(token+ "? ")
    return(j)
#ask
def pword():
    # adds logg to fetch
    global fi
    j = fi.fpword()
    logg('pword = (' + j.__str__() + ')')
    return(j)
#end pword
def logg(msg):
    global ts
    print("(" + ts.asctime() + ")[" + msg + ']')
    j = raw_input('? ')
#end logg
def doComment():
    # capture and print comment
    # /* already captured
    global fi,nds
    fo = fi.fioxGet()
    aa = fi.ftill('*/')
    sd = pword()
    bo = sd[2]
    # position at fo
    fi.fh.seek(fo)
    # rd = read for bo-fo
    rd = fi.fh.read(bo-fo)
    # print rd
    print (rd) # prints trailing */
    # position at bo
    fi.fioxSet(bo)
    # needs work 
#end doComment
def getDesc():
    # capture and return description
    # beginning '''  already captured
    global fi,nds
    logg('getDesc')
    fo = fi.fioxGet()
    aa = fi.ftill("'''")
    sd = pword()
    bo = sd[0] # before '''
    bo1 = sd[2] # after '''
    # position at fo
    fi.fh.seek(fo)
    # rd = read for bo-fo
    rd = fi.fh.read(bo-fo)
    # position at bo
    fi.fioxSet(bo1)
    return(rd) 
#end getDesc

"""
jadT :-
[[ 1 ]] init
        jadT2 
        return(nds)
        .
;

jadT2 :-
[[ 0 ]] pword jd ! ...
[[ 1 ]] jd=/* doComment tail. 
[[ 2 ]] jd=TABLE doTable tail. 
[[ 3 ]] js=@endend ercode 'ended' ! .
[[ 4 ]] ercode 'bad token jadT'  .
;
"""

def jadT():
    #[[ 1 ]] init
    global nds
    logg('begin jadT')
    nds = {}
    nds['tn'] = {}
    nds['tix'] = 0
    nds['kix'] = 0
    import fioiClass
    global fi
    filename = ask('filename')
    fi = fioiClass.fio(filename)
    fi.fwhite()
    jadT2
    return(nds)
#end jadT

def jadT2():
    logg('begin jadT2')
    jadt = 0 # tail marker
    while (jadt == 0):
        # [[ 0 ]]
        nds['jd'] = pword()
        if (nds['jd'][1] == '/*'):
            doComment()
            #tail .
        elif ( nds['jd'][1] == 'TABLE' ) :
            doTable()
            # tail .
        elif ( nds['jd'][1] == '@endend'):
            nds['ercode'] = 'ended'
            jadt = -1 # break
        else:
            nds['ercode'] = 'bad token at jadT'
            logg(nds['ercode'])
            jadt = -1 # break
        #endif
    #wend
    logg('end jadT2')

#end jadT
"""

doTable :-
[[ 1 ]] pword tn[+tix] ! table2 .
;
"""
def doTable():
   global fi,nds
   logg('begin doTable')
   # [[ 1 ]]
   nds['tix'] = nds['tix'] + 1
   dot = pword()
   nds['tn'][nds['tix']] = {}
   nds['tn'][nds['tix']]['tname'] = dot[1]
   logg('nds ' + nds.__str__() )
   table2()
   logg('end doTable')
#end doTable
"""
table2 :-
[[ 0 ]] pword j2 ! ...
[[ 1 ]] j2=/* getComment tail.
[[ 2 ]] j2=''' getDesc tdesc ! tail. 
[[ 3 ]] j2=(( getKeys table3 .
[[ 4 ]] ercode 'bad token table2' ! fail .
;
"""
def table2():
    global fi,nds
    logg('begin Table2')
    wht2 = 0
    while (wht2 == 0):
        #[[0]]
        j2 = pword()
        #[[1]]
        if (j2[1] == '/*'):
            doComment()
            #loop
        #[[2]]
        elif (j2[1] == "'''"):
            nds['tn'][nds['tix']]['desc'] = getDesc()
            logg('nds ' + nds.__str__() )
            #loop
        elif (j2[1] == "(("):
            getKeys()
            #pja  -- table3()
            wht2 = -1 #break
        else:
            nds['ercode'] = 'bad token table2'
            logg(nds['ercode'])
            wht2 = -2 #break
        #endif
    #wend
    logg('end Table2')
#end table2
        
"""
getKeys :-
[[ 1 ]] pword j ! ...
[[ 2 ]] j[1] ',' = tail. 
[[ 3 ]] j[1] ")"= getTags .
[[ 4 ]] j[1] kn[+kix] ! getKeyData tail.
;
"""
def getKeys():
    global fi,nds
    logg('begin getKeys')
    whgetK = 0
    while ( whgetK == 0 ):
        nds['j'] = pword()
        if (nds['j'][1] == ','):
            nop = 0 # syntax filler
            #loop
        elif (nds['j'][1] == ")" ):
            #--pja -- getTags()
            whgetK = -1 #break
        else:
            nds['kix'] = nds['kix'] + 1
            nds['tn'][nds['tix']]['kn'] = {}
            nds['tn'][nds['tix']]['kn'][nds['kix']] = {}
            nds['tn'][nds['tix']]['kn'][nds['kix']]['name'] = nds['j'][1]
            logg('nds ' + nds.__str__() )
            getKeyData()
            #loop
        #endif
    #wend
    logg('end getKeys')
#end getKeys
                      
"""
getKeyData :-
[[ 1 ]] pword kd ! ...
[[ 2 ]] kd=/* doComment tail. 
[[ 3 ]] kd=''' getDesc kn[kix]['desc'] ! tail.
[[ 4 ]] kd=of getFK kn[kix]['fk'] ! tail.
[[ 5 ]] kd=, pushback .
[[ 6 ]] kd=) pushback .
[[ 7 ]] ercode 'bad token getKeyData' ! .
;
"""
def getKeyData():
    global fi,nds
    logg('begin getKeyData')
    whgetKD = 0
    while (whgetKD == 0):
        nds['kd'] = pword()
        if ( nds['kd'][1] == '/*'):
            doComment()
            #loop
        elif ( nds['kd'][1] == "'''"):
            nds['tn'][nds['tix']]['kn'][nds['kix']]['desc']  = getDesc()
            #loop
        elif ( nds['kd'][1] == "of"):
            getPFK()
        elif (nds['kd'][1] == ','):
            fi.setIOX(nds['kd'][0]) # pushback
            whgetKD = -1 #break
        elif (nds['kd'][1] == ')'):
            fi.fioxSet(nds['kd'][0]) # pushback
            whgetKD = -1 #break
        else:
            nds['ercode'] = 'bad token table2'
            logg(nds['ercode'])
            whgetKD = -1 # break
        #endif
    #wend
    logg('end getKeyData')
#end getKeyData
                      
                      
"""
getPFK :- /* of t.c {( t.c = v )}
[[ 1 ]] pword gfk ! ...
[[ 2 ]] '.' gfkSplit kn[kix][fkt] ! kn[kix][fkc] ! getFK2 .
;
getFK2 :-
[[ 1 ]] pword gfk2 ! ...
[[ 2 ]] gfk2=( gfk3 .
[[ 3 ]] pushback .
;
gfk3 :-
[[ 1 ]] pword gfk3 ! '.' gfk3split
        kn[kix][fklovt] ! kn[kix][fklovc] !
        pword gfk4 ! gfk4== 
        pword gfk5 ! kn[kix][fklovV] !
        pword gfk6 ! =) 
        pword gfk7 ! =; . 
[[ 2 ]] ercode 'bad token at gfk3' ! .
;

"""
def getPFK():
    #of t.c {( t.c = v )}
    # '.' gfkSplit
    global fi,nds
    logg('begin getPFK')
    r = pword()
    # split at '.'
    j = r[1].split('.')
    nds['tn'][nds['tix']]['kn'][nds['kix']]['pfkTable'] = j[0]
    nds['tn'][nds['tix']]['kn'][nds['kix']]['pfkCol'] = j[1]
    #{( t.c = v )} aka getPFK2
    m = pword()
    if (m[1] == "("):
        n = pword()
        n2 = n[1].split('.')
        nds['tn'][nds['tix']]['kn'][nds['kix']]['pfkLTable'] = n2[0]
        nds['tn'][nds['tix']]['kn'][nds['kix']]['pfkLCol'] = n2[1]
        n3 = pword()
        if (n3[1] != '='):
            #err bad format
        else:
            n4 = pword()
            nds['tn'][nds['tix']]['kn'][nds['kix']]['pfkLVal'] = n4[1]
        #endif
        n5 = pword()
        if (n5[1] != ')'):
            #er bad format
            nds['ercode'] = 'bad token getPFK expected ")" '
            logg(nds['ercode'])
            nop = -1
        else:
            nop = 1
        #endif
    else:
        #pushback
        fi.setIOX(m[0])
    #endif
#end getPFK
"""

getTags :- "(" na ''' /* , ) ; */
[[ 1 ]] pword j ! ...
[[ 2 ]] j[1] ',' = tail. 
[[ 3 ]] j[1] =")" pword =; .
[[ 4 ]] j[1] tagn[+tix] ! gettTagData tail.
;
getTagData :-
[[ 1 ]] pword tagD ! ...
[[ 2 ]] tagD=/* doComment tail. 
[[ 3 ]] tagD=''' getDesc tagN[tagIX]['desc'] ! tail.
[[ 4 ]] tagD=of getTagFK tagN[tagIX]['fk'] ! tail.
[[ 5 ]] tagD=, pushback .
[[ 6 ]] tagD=) pushback .
[[ 7 ]] ercode 'bad token getTagData' ! .
;
getTagFK :- /* of t.c {( t.c = v )}
[[ 1 ]] pword gfk ! ...
[[ 2 ]] '.' gfkSplit tagN[tagIX][fkt] ! tagN[tagIX][fkc] ! getTagFK2 .
;
getTagFK2 :-
[[ 1 ]] pword gfk2 ! ...
[[ 2 ]] gfk2=( gfkT3 .
[[ 3 ]] pushback .
;
gfkT3 :-
[[ 1 ]] pword gft3 ! '.' gft3split
        tagN[tagIX][fklovt] ! tagN[tagIX][fklovc] !
        pword gft4 ! gft4== 
        pword gft5 ! tagN[tagIX][fklovV] !
        pword gft6 ! =) 
        pword gft7 ! =; . 
[[ 2 ]] ercode 'bad token at gft3' ! .
;

"""

