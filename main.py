from Spiders import umei,jb9
from cmnFunc import myFunc as mf

if __name__ == '__main__':
    test = 'jb9'
    match test:
        case 'test':
            mf.testProscess()
        case 'umei':
            umei.mainProcess()
        case 'jb9':
            jb9.saveFromDbProscess()
        case _:
            print("未指定程序")