import numpy as np
from glob import glob
import os 

import shutil
import logging
from constants import IMAGE_FOLDER, IMAGE_NAME, PROCESSED_IMAGES,PDF_NAME, ROOT, UPLOAD_FOLDER, WATER_MARK_PATH
from helper import checker,number, oneD_to_threeD
import fpdf
from pathlib import Path
import imageio.v3 as iio
import imageio
from PIL import Image


class Pdf_maker:
    def __init__(self):
        
        self.errors = []

        

    def take_images(self):
        
        images_folder = IMAGE_FOLDER
            
        cwd  = ROOT
        all_images = os.path.join(cwd,images_folder)
    
        processed_images = PROCESSED_IMAGES
        checker(processed_images)
        directory  = os.path.join(cwd,processed_images)

    
        paths = os.listdir(all_images)
        paths.sort()
        print(paths)
        for i,path in enumerate(paths):
            path = os.path.join(all_images,path)

            if path.split('.')[-1] not in ['png', 'jpg', 'jpeg']:
                continue

            
            image = iio.imread(path)[:,:,:3]         
            
            row,col,_ =image.shape              
            print(image.shape)
            if row < 800 and col < 650:
                color = (255,255,255)
                pad = np.full((1128,800, 3), color, dtype=np.uint8)
                center_x = abs(1128 - row )//2
                center_y = abs(800 - col)//2
                logging.debug((row,col))
            
                pad[center_x:center_x + row, center_y:center_y + col] = image
                image = pad
            else:
                image = Image.fromarray(image).resize((800, 1128))
            
            
         
            extension = path.strip().split('.')[-1]
           
            imageio.imwrite(f'{directory}/{IMAGE_NAME}-{i}.{extension}',image)      

        print('All images taken successfully')
        return directory


    def qualityoptimizer(self):
        directory = self.take_images()

        watermark_path =   WATER_MARK_PATH
        
        waterMarkImage = iio.imread(watermark_path)[:,:,0]          

        waterMarkImage =Image.fromarray(waterMarkImage).resize((800, 1128))  
        paths = os.listdir(directory)
        paths.sort(key = number)
        
        for path in paths:
            
            
            img_path = os.path.join(directory,path)


            raw_image = iio.imread(img_path)[:,:,:3]     
            gray_mark = 255-np.array(waterMarkImage)
            
            
              
            gray_mark =gray_mark//10
            
            gray = oneD_to_threeD(gray_mark)
            
            b,g,r = raw_image[:,:,0],raw_image[:,:,1],raw_image[:,:,2]                      
            red = oneD_to_threeD(r)                                
            blue = oneD_to_threeD(b)
            green = oneD_to_threeD(g)
            
            filtered_image = np.where(((red > gray) & (green > gray) & (blue > gray)),raw_image - gray,raw_image)

            imageio.imwrite(img_path,filtered_image)   
                            
        return glob(os.path.join(ROOT,f"{PROCESSED_IMAGES}/*"))
    
    def generate_file_structure(self) -> None:
        try:
            print('Creating structure ... ')
            
            os.mkdir(f'/{ROOT}/processed_images')
            Path(f'/{ROOT}/static/pdf').mkdir(parents=True, exist_ok=True)
            os.mkdir(f'/{ROOT}/static/images')
           
        except:
            pass
            
        finally:
            print('Structure already there')

    def pdfmaker(self) -> bool:
        try:
            self.generate_file_structure()
            print('Generating pdf wait for a while')
            pdf = fpdf.FPDF()
            paths = self.qualityoptimizer()
            paths.sort(key = number)
            for i in range(len(paths)):
                pdf.add_page()
                pdf.image(paths[i],0,0,210,290)
            

            path = UPLOAD_FOLDER

            pdf.output(f"{path}/{PDF_NAME}","F")
            
            print('Pdf generation done')

            return True
        except Exception as ex:
            print('Sorry Pdf could not be generated')
            self.errors.append(ex)
            return False
            
maker = Pdf_maker()
maker.pdfmaker()




