### CONSTANTS START
def _CONST(NAME):
    if NAME == 'REP_RULES':
        return {    
            "([0123456789])" : " ",
            "([\n\t\0\ufeff])" : " ",
            "([:.,\?!])" : " ",
            "([♪$\"])" : " ",
            "-->|<i>|</i>" : " ",
            "--| -|- |->" : " ",
            " - " : " ",
            "([\(\[\{]).*?([\}\)\]])" : " "
        }
    if NAME == 'P_OUT':
        return 'OUT.csv'
    if NAME == 'PARQ_COPMR':
        return 'GZIP'
    if NAME == 'DEF_DTYPE':
        return 'int32'
    if NAME == 'PATH_DIR':
        return os.path.expanduser("~") + '/.MyApps/moVdata/'

    return None
### CONSTANTS END





### ARGS_HANDLING FUNC START
def ARGS_HANDLING():

    if len(sys.argv) < 2:
        print("WRONG ARGUMANT")
        print("TYPE  -h or help  TO USE MANUAL")
        exit(1)

    MC = sys.argv[1].lower()    # main command

    if MC == '-h' or MC == '--help' or MC == 'help':
        HELP()
        
    if MC == '-p' or MC == '--process' or MC == 'process':
        if len(sys.argv) == 3:
            PROCESS(sys.argv[2])
    
    if MC == '-a' or MC == '--add' or MC == 'add':
        if len(sys.argv) == 4:
            ADD(sys.argv[2], sys.argv[3])
    
    if MC == '-b' or MC == '--backup' or MC == 'backup':
        BACKUP()

    print("WRONG ARGUMANT")
    print("TYPE  -h or help  TO USE MANUAL")
    exit(1)
    
### ARGS_HANDLING FUNC END


### HELP FUNC START
def HELP():

    print("{-h or help or --help}       :               printing this tutorials.")
    print("{-p or process or --process} {SRT_FILE}:     making a csv file of srt's words.")
    print("{-a or add or --add}         {CSV} {TXT}:    adding new movie words to DB.")
    print("{-b or backup or --backup}   {PATH_BK_FILE}: maiking a backup of DB.")

    exit(0)
### HELP FUNC END


### PROCESS FUNC START
def PROCESS(SRT_FILE):
    
    Name    = input('Enter movie\'s Name: ')
    file    = open(SRT_FILE, 'r').read().lower()

    REP_RULES = _CONST('REP_RULES')
    for rule in REP_RULES:
        file = re.sub(rule, REP_RULES[rule], file)
    

    words   = file.split()

    OUT = ''    

    ret     = pandas.Series(dtype = _CONST('DEF_DTYPE'))
    ret.index.name = 'WORDS'
    ret.name = Name
    
    for W in words:
        OUT += W + '\n'
        if W.isprintable == False:
            continue
        if W in ret:
            ret[W] += 1
        else:
            ret[W] = 1

    open(Name + '.txt', 'w').write(OUT)
    ret.sort_index().fillna(0).to_csv(Name + ".csv")

    exit(0)
### PROCESS FUNC END


### ADD FUNC START
def ADD(CSV_FILE, TXT_FILE):

    DB_check()
    open(_CONST('PATH_DIR') + 'TEXTS/' + TXT_FILE, 'w').write(open(TXT_FILE, 'r').read())


    ww = pandas.read_csv(CSV_FILE, index_col = 0)
    WORDS = pandas.read_parquet(_CONST('PATH_DIR') + 'WORDS.parquet')
    DB = pandas.read_parquet(_CONST('PATH_DIR') + 'MOVIES.parquet')

    
    Name    = ww.columns[0]
    print("Movie's name is: " + Name)
    
    Year    = input('Enter movie\'s Year: ')
    while Year.isdigit() == False:
        Year = input('WRONG input for YEAR\nEnter movie\'s Year again: ')
    Time    = input('Enter movie\'s Time (in minutes): ')
    while Time.isdigit() == False:
        Time = input('WRONG input for TIME\nEnter movie\'s Time again (in minutes): ')
    Genre  = input('Enter movie\'s Genres: ')


    DB.loc[Name, 'UNIQUE'] = len(ww.index)
    DB.loc[Name, 'ALL'] = ww[Name].sum()
    
    DB.loc[Name, 'YEAR'] = int(Year)
    DB.loc[Name, 'TIME'] = int(Time)

    for gen in Genre.upper().split(' '):
        DB.loc[Name, gen] = int(1)
    
    
    for word in ww.index:
        WORDS.loc[word, Name] = ww.loc[word, Name]
    

    WORDS   = WORDS.sort_values('WORDS').fillna(0).astype(_CONST('DEF_DTYPE'))
    DB      = DB.fillna(0).astype(_CONST('DEF_DTYPE'))

    DB.to_parquet(_CONST('PATH_DIR') + 'MOVIES.parquet', compression = _CONST('PARQ_COPMR'))
    WORDS.to_parquet(_CONST('PATH_DIR') + 'WORDS.parquet', compression = _CONST('PARQ_COPMR'))

    exit(0)
### ADD FUNC END

### BACKUP FUNC START
def BACKUP():

    from shutil import copyfile  as cp

    cp(_CONST('PATH_DIR') + 'WORDS.parquet', 'WORDS.parquet.bk')
    cp(_CONST('PATH_DIR') + 'MOVIES.parquet', 'MOVIES.parquet.bk')

    exit(0)
### BACKUP FUNC END




### DB_check FUNC START
##  this function check is DB avalibale or create it
def DB_check():

    # import os
    # import pandas

    if os.path.isdir(_CONST('PATH_DIR')) == False:
        os.makedirs(_CONST('PATH_DIR'))

    if os.path.isdir(_CONST('PATH_DIR') + 'TEXTS/') == False:
        os.makedirs(_CONST('PATH_DIR') + 'TEXTS/')

    if os.path.exists(_CONST('PATH_DIR') + 'WORDS.parquet') == False:
        df = pandas.DataFrame()
        df.index.name = 'WORDS'
        df.to_parquet(_CONST('PATH_DIR') + 'WORDS.parquet', compression = _CONST('PARQ_COPMR'))

    if os.path.exists(_CONST('PATH_DIR') + 'MOVIES.parquet') == False:
        df = pandas.DataFrame()
        df.index.name = 'MOVIES'
        df.to_parquet(_CONST('PATH_DIR') + 'MOVIES.parquet', compression = _CONST('PARQ_COPMR'))

    return

### DB_check FUNC END




##### NON FUNC PART

try:
    import fastparquet  as FASTPARQUET
    import pandas       as pandas
    import sys          as sys
    import os           as os
    import re           as re
except ImportError as e:
    print(e)
    print("This project needs pandas sys os re shutil fastparquet pakages.")
    exit(2)

if __name__ == '__main__':
    ARGS_HANDLING()

exit(0)
##### NON FUNC PART