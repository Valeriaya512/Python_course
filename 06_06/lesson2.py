## 課程內容：自訂function

n = 10
print(n)

#以下是內建屬性
print(__name__)
print(__file__)
print(__doc__)
print(__package__)


#================================================
#自訂命名function
def main():  #自訂命名function main()
    print("這裡是main function的命名空間")
    print(n)

if __name__ == '__main__':
    n = 10  #n為文件變數，使用範圍：這個整個文件
    #print(n)
    main()  #呼叫main()，執行裡的程式區塊

#================================================
def main():
    n = 5  #n為區域變數，使用範圍僅在main裡
    print("這裡是main function的命名空間")
    print(n)

if __name__ == '__main__':
    main()  #呼叫main()，執行裡的程式區塊
    print(n)  #無法找到n，n只能用在main function運作

#================================================
n = 0
def main():
    print("這裡是main function的命名空間")
    print(n)

if __name__ == '__main__':
    main()
    print(n)

#================================================
