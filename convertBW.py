#Patrick Connolly
"""
This program takes an image, converts it into a pure black or pure white bitmap,
then using an array of prime numbers takes the image and creates a unique number
corresponding to the original image.

Currently Decrypt is not working.
"""

from PIL import Image
import math

def encrypt(fileName):
    theImage = convertBW(fileName)
    width, height = getDimensions(theImage)
    
    #This takes a good chunk of time
    primeList = seive(width, height)

    calculateTheNumber(theImage, primeList, fileName)

    return None

def convertBW(fileName):
    original = Image.open(fileName)
    gray = original.convert("L")
    blackWhite = gray.point(lambda x: 0 if x<128 else 255, '1')
    return blackWhite
    
def getDimensions(theImage):
    width, height = theImage.size
    return width, height


def seive(width, height):
    primes = [2]
    pMax = width*height
    initVal = 0
    counter = 1.0
    start = 3
    while len(primes)<pMax:
        prime = True
        for i in range(len(primes)):
            if(start%primes[i]==0):
                prime = False
                break
            if(math.sqrt(start)>int(math.floor(primes[i]))):
                break
        if prime:
            primes.append(start)
            counter+=1
        start+=2
        if math.floor((counter/pMax)*100)>initVal:
            initVal = math.floor((counter/pMax)*100)
    return primes

def calculateTheNumber(theImage, primeList, fileName):
    width, height = getDimensions(theImage)
    theNumber = 1
    for i in range(height):
        for j in range(width):
            r = theImage.getpixel((j, i))
            if(r>127):
                theNumber = theNumber*primeList[width*i+width-1]
    f=open(fileName+".txt", 'w')
    f.write(str(theNumber))
    f.close()

def menu():
    print("Please enter a selection...")
    print("1.) Encrypt a picture")
    print("2.) Decrypt a picture")
    print("3.) Exit")
    theSelection = input("Enter your choice..:")[0]
    if(theSelection=='1' or theSelection == '2'):
        fileName = input("Enter the filename: ")
        if theSelection=='1':
            encrypt(fileName)
        elif theSelection=='2':
            decrypt(fileName)
        return True
    elif(theSelection=='3'):
        return False
    else:
        print("INVALID SELECTION, TRY AGAIN!")
        return True

def decrypt(fileName):
    textFile = fileName+".txt"
    img = Image.open(fileName)
    width, height = getDimensions(img)
    pList = seive(width, height)
    newImg = Image.new("1", (width, height), 0)
    text = open(textFile, 'r')
    txt = int(text.read())
    text.close()
    counter = 0
    countVal = 1000
    for i in range(height):
        for j in range(width):
            counter+=1
            if(counter>=countVal):
                counter = 0
                print(((i*width+j)/(width*height))*100)
            if(txt%pList[i*width+j]==0 and i*width+j<width*height):
                txt=txt//pList[i*width+j]
                newImg.putpixel((i, j), 1)
    newImg.save(textFile+".jpg", "JPEG")
            
    return None
        
def main():
    while(menu()):
        print("---------------------------------------------")
main()




















