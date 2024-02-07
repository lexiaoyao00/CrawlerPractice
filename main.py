from Spiders import umei

if __name__ == '__main__':
    test = 'umei'
    match test:
        case 'umei':
            umei.mainProcess()
        case _:
            print("未指定程序")