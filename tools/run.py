import decode
import encode

def main():
    mode=input('モードを選択してください（1: エンコード, 2: デコード）: ')
    if mode == '1':
        encode.main()
    elif mode == '2':
        decode.main()
if __name__ == '__main__':
    main()