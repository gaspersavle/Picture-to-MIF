import numpy as np
import matplotlib.pyplot as plt
import cv2

filename = "mordo.jpeg"
samoime = filename.split(".")
slika = cv2.resize(cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2RGB),[64,64])
crnobela = cv2.cvtColor(slika,cv2.COLOR_RGB2GRAY)
rdeca,zelena,modra = cv2.split(slika)

plt.figure()
plt.title("Original")
plt.imshow(slika)

plt.figure()
plt.title("Crnobela")
plt.imshow(crnobela)


def header (file,width):
    file.write("WIDTH="+str(width)+ ";" + "\n")
    file.write("DEPTH=4096;" + "\n")
    file.write("ADDRESS_RADIX=DEC;"+ "\n")
    file.write("DATA_RADIX=BIN;"+ "\n")
    file.write("CONTENT BEGIN"+ "\n")

barve = []
svetlosti = []
rezultat_r = np.zeros((64,64))
rezultat_g = np.zeros((64,64))
rezultat_b = np.zeros((64,64))

for vrstica in range(64):
    for stolpec in range(64):
        
        neored = (int(rdeca[vrstica,stolpec]))//64
        red = str(np.binary_repr(neored,2))
        rezultat_r[vrstica,stolpec] = neored
        
        neogreen = (int(zelena[vrstica,stolpec]))//64
        green = str(np.binary_repr(neogreen,2))
        rezultat_g[vrstica,stolpec] = neogreen
        
        neoblue = (int(modra[vrstica,stolpec]))//64
        blue = str(np.binary_repr(neoblue,2))
        rezultat_b[vrstica,stolpec] = neoblue
        

            
        barve.append(red+green+blue)
        svetlosti.append(np.binary_repr(crnobela[vrstica,stolpec],8))
rezultat = cv2.merge([rezultat_r,rezultat_g,rezultat_b])

plt.figure()
plt.title("Rezultat")
plt.imshow(rezultat)




barvefile = open("./slike/barve_"+samoime[0]+".mif", "w+")
svetlostifile = open("./slike/svetlosti_"+samoime[0]+".mif","w+")
header(barvefile,6)
header(svetlostifile,8)

for indeks, element in enumerate(barve):
    barvefile.write(str(indeks) + " : " + element + ";" +"\n")
   
for vrsta, element in enumerate(svetlosti):
    svetlostifile.write(str(vrsta) + " : " + element + ";" +"\n")

barvefile.write("END;")
svetlostifile.write("END;")

barvefile.close
svetlostifile.close

print(barve[1621])
print(svetlosti[1621])
print(rezultat[23,20])
print(rezultat.shape)
print("The shape of colour: ", len(barve))
print(barve[0])

plt.show()








