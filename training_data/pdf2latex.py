import pdf2image
from PIL import Image
import numpy as np
import texify.inference
import texify.model.model
import texify.model.processor
import texify.settings

print('Import complete')

THRESHOLD = 200
PADDING = 25

print('Loading models')
model = texify.model.model.load_model()
processor = texify.model.processor.load_processor()

with open('output.tex', 'w', encoding='utf-8') as file:
    for i in range(24, 638): # 24
        print(f'Converting page {i+1}')
        image, = pdf2image.convert_from_path('APMASK-book.pdf', first_page=i, last_page=i)
        image = np.array(image.convert('L'))[128:2220]
        
        print(f'Finding image slices from page {i+1}')
        image_slices = list()

        start = 0
        active = False

        for row in range(image.shape[0]):
            if start == 0 and (image[row, :] <= THRESHOLD).any():
                start = row
            
            elif start > 0 and (image[row:min(row+15, image.shape[0]), :] > THRESHOLD).all():
                left = 0
                right = 0

                while (image[start:row, :left+1] > THRESHOLD).all():
                    left += 1

                while (image[start:row, right-1:] > THRESHOLD).all():
                    right -= 1

                if image[start:row, left:right].shape[1] > 0:
                    new_image = 255*np.ones((2*PADDING + row - start, 2*PADDING + right - left + image.shape[1]), np.uint8)
                    new_image[PADDING:-PADDING, PADDING:-PADDING] = image[start:row, left:right]

                    image_slices.append(Image.fromarray(new_image).convert('L'))
                else:
                    print('Skipping paragraph')
                
                start = 0
        
        if len(image_slices) > 0:
            print(f'Converting {len(image_slices)} paragaphs')
            paragraphs = texify.inference.batch_inference(image_slices, model, processor)
            file.write('\n'.join(paragraphs) + '\n\n')
        else:
            print('No paragraphs found')

print('Done!')
