# file tDef.py table def parser
def logg(msg):
    print(msg)
    j = raw_input('? ')
#end logg
def doComment():
    # capture and print comment
    # /* already captured
    global fi,nds
    fo = fi.ioxGet()
    aa = fi.ftill('*/')
    sd = fi.fpword()
    bo = sd[2]
    # needs work 
#end doComment

"""
jadT :-
[[ 0 ]] pword jd ! ...
[[ 1 ]] jd=/* doComment tail. 
[[ 2 ]] jd=TABLE doTable tail. 
[[ 3 ]] js=@endend ercode 'ended' ! .
[[ 4 ]] ercode 'bad token jadT'  .
;
"""
def jadT():
    #[[ 00 ]] init
    global nds
    nds = {}
    nds['kn'] = {}
    nds['kix'] = 0
    nds['tn'] = {}
    nds['tix'] = 0
    import fioiClass
    global fi
    fi = fioiClass.fio(filename)
    fi.fwhite()
    jadt = 0 # tail marker
    while (jadt == 0):
        # [[ 0 ]]
        nds['jd'] = fi.fpword()
        if (nds['jd'][1] == '/*'):
            doComment()
            #tail .
        elseif ( nds['jd'][1] == 'TABLE'):
            doTable()
            # tail .
        elseif ( nds['jd'][1] == '@endend'):
            nds['ercode'] = 'ended'
            jadt = -1 # break
        else:
            nds['ercode'] = 'bad token at jadT'
            logg(nds['ercode'])
            jadt = -1 # break
        #endif
    #wend
    return(nds)
#end jadT
"""

doTable :-
[[ 1 ]] pword tn[+tix] ! table2 .
;
"""
def doTable():
   global fi,nds
   # [[ 1 ]]
   nds['tix'] = nds['tix'] + 1
   dot = fi.fpword()
   nds['tn'][nds['tix']] = {}
   nds['tn'][nds['tix']]['tname'] = dot[1]
   table2()
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
    wht2 = 0
    while (wht2 == 0):
        #[[0]]
        j2 = fi.fpword()
        #[[1]]
        if (j2[1] == '/*'):
            doComment()
            #loop
        #[[2]]
        elseif (j2[1] == "'''"):
            nds['tn'][nds['tix']['desc'] = getDesc()
            #loop
        elseif (j2[1] == "(("):
            getKeys()
            table3()
            wht2 = -1 #break
        else:
            nds['ercode'] = 'bad token table2'
            logg(nds['ercode'])
            wht2 = -2 #break
        #endif
    #wend
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
    whgetK = 0
    while ( whgetK == 0 ):
        nds['j'] = fi.fpword()
        if (nds['j'][1] == ','):
            #loop
        elseif (nds['j'][1] == ")" ):
            getTags()
            whgetK = -1 #break
        else:
            nds['kix'] = nds['kix'] + 1
            nds['kn'][nds['kix']] = {}
            nds['kn'][nds['kix']]['name'] = nds['j'][1]
            getKeyData()
            #loop
        #endif
    #wend
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
    whgetKD = 0
    while (whgetKD == 0):
        nds['kd'] = fi.fpword()
        if ( nds['kd'][1] == '/*'):
            doComment()
            #loop
        elseif ( nds['kd'][1] == "'''"):
            getDesc()
            #loop
        elseif (nds['kd'][1] == ','):
            fi.setIOX(nds['kd'][0]) # pushback
            whgetKD = -1 #break
        elseif (nds['kd'][1] == ')'):
            fi.setIOX(nds['kd'][0]) # pushback
            whgetKD = -1 #break
         else:
            nds['ercode'] = 'bad token table2'
            logg(nds['ercode'])
            whgetKD = -1 # break
        #endif
    #wend
#end getKeyData
                      
                      
"""
getFK :- /* of t.c {( t.c = v )}
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
        pword gfk6 ! =) . 
[[ 2 ]] ercode 'bad token at gfk3' ! .
;
getTags :- "(" na ''' /* , ) ; */
[[ 1 ]] pword j ! ...
[[ 2 ]] j[1] ',' = tail. 
[[ 3 ]] j[1] ")"= pword =; tn++ .
[[ 4 ]] j[1] tagn[tix+] ! gettTagData tail.
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
[[ 1 ]] pword gfk3 ! '.' gfk3split
        tagN[tagIX][fklovt] ! tagN[tagIX][fklovc] !
        pword gfk4 ! gfk4== 
        pword gfk5 ! tagN[tagIX][fklovV] !
        pword gfk6 ! =) . 
[[ 2 ]] ercode 'bad token at gfk3' ! .
;

"""

