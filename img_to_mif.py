import numpy as np
import cv2
import argparse
import os

parser = argparse.ArgumentParser(description='Image to MIF conversion')
parser.add_argument('--indir', type=str, required=True,
                    help='Input directory containing images')
parser.add_argument('--outdir', type=str, required=True,
                    help='Output directory containing MIF files')
parser.add_argument('--out_depth_c', type=int, required=False, default=6,
                    help='Coulour resolution (in bits) of the processed colour file')
parser.add_argument('--out_depth_l', type=int, required=False, default=8,
                    help='Luminosity resolution (in bits) of the processed luminosity file')
parser.add_argument('--adr_encoding', type=str, required=False, default='DEC',
                    help='Encoding type of the adress colum (BIN, DEC, HEX, ...)', choices=['BIN', 'DEC', 'HEX'])
parser.add_argument('--data_encoding', type=str, required=False, default='BIN',
                    help='Encoding type of the data (BIN, DEC, HEX, ...)', choices=['BIN', 'DEC', 'HEX'])
parser.add_argument('--out_height', type=int, required=False, default=64,
                    help='Height of output image')
parser.add_argument('--out_width', type=int, required=False, default=64,
                    help='Width of output image')
args = parser.parse_args()

class ImgToMIF():
    def __init__(self, args):
        self.args = args
        self.imgheight = args.out_height
        self.imgwidth = args.out_width
        self.outdir = args.outdir
        self.colwidth = args.out_depth_c
        self.lumwidth = args.out_depth_l
        self.imgs = []
        self.names = []

        self.LoadIMGs()
        self.ProcessIMGs()
        
    def LoadIMGs(self):
        directory = args.indir
        filenames = sorted(os.listdir(directory))

        for file in filenames:
            print(f"Found file: {file}")
            self.imgs.append(cv2.imread(os.path.join(directory, file)))
            self.names.append(file.split("."))
    
    def ProcessIMGs(self):
        for index, img in enumerate(self.imgs):
            img = cv2.resize(img, [self.imgheight, self.imgwidth])
            r, g, b = cv2.split(img)
            bw = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

            clrs = []
            lums = []

            out_r = np.zeros((self.imgheight,self.imgwidth))
            out_g = np.zeros((self.imgheight,self.imgwidth))
            out_b = np.zeros((self.imgheight,self.imgwidth))

            chwidth = int(self.colwidth/3)

            for row in range(self.imgheight):
                for col in range(self.imgwidth):
                    
                    red = (int(r[row,col]))//64
                    red = str(np.binary_repr(red,chwidth))
                    out_r[row,col] = red
                    
                    green = (int(g[row,col]))//64
                    green = str(np.binary_repr(green,chwidth))
                    out_g[row,col] = green
                    
                    blue = (int(b[row,col]))//64
                    blue = str(np.binary_repr(blue,chwidth))
                    out_b[row,col] = blue
                    

                        
                    clrs.append(red+green+blue)
                    lums.append(np.binary_repr(bw[row,col],self.lumwidth))

            colfile = open(self.outdir+"cols_"+self.names[index][0]+".mif", "w+")
            lumfile = open(self.outdir+"lums_"+self.names[index][0]+".mif","w+")

            self.header(colfile, self.colwidth, depth=(self.imgheight*self.imgwidth))
            self.header(lumfile, self.lumwidth, depth=(self.imgheight*self.imgwidth))

            for i, col in enumerate(clrs):
                colfile.write(str(i) + " : " + col + ";" + "\n")

            for j, lum in enumerate(clrs):
                colfile.write(str(j) + " : " + lum + ";" + "\n")

            colfile.write("END;")
            lumfile.write("END;")

            colfile.close
            lumfile.close

            print(f"Finished processing file: {self.names[index][0]}.{self.names[index][1]}")


    def header (self, file,width,depth):
        file.write("WIDTH="+str(width)+ ";" + "\n")
        file.write("DEPTH="+str(depth)+ ";" + "\n")
        file.write("ADDRESS_RADIX=DEC;"+ "\n")
        file.write("DATA_RADIX=BIN;"+ "\n")
        file.write("CONTENT BEGIN"+ "\n")

if __name__ == "__main__":
    ImgToMIF(args)











