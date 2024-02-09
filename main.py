from Spiders import umei,jb9

if __name__ == '__main__':
    test = 'jb9'
    match test:
        case 'umei':
            umei.mainProcess()
        case 'jb9':
            jb9.mainProcess()
        case _:
            print("未指定程序")