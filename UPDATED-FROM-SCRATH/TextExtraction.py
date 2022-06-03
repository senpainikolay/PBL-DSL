import cv2
import numpy as np 
from  ImgTextReaderFc import read_test_from_image
 

class TextSelectorFromImage:
    def __init__(self):

        # Create point matrix get coordinates of mouse click on image 
        self.point_matrix = np.zeros((2,2),np.int) 

        self.counter = 0  

            # Read image
        self.bool_selected = False

        self.current_coords = np.zeros((2,2),np.int)


    def mousePoints(self, event,x,y,flags,params):
        #global self.counter
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point_matrix[self.counter] = x,y
            self.counter = self.counter + 1 


    def run(self,image_path):
        img = cv2.imread(image_path) 
        while True:

            if self.bool_selected:
                self.current_coords =  self.point_matrix
                self.point_matrix = np.zeros((2,2),np.int) 
                self.counter = 0
                self.bool_selected = False
                cv2.waitKey(1000)
                cv2.destroyAllWindows()

                break

            for x in range (0,2):
                cv2.circle(img,(self.point_matrix[x][0],self.point_matrix[x][1]),3,(0,255,0),cv2.FILLED)

            if self.counter == 2:
                starting_x = self.point_matrix[0][0]
                starting_y = self.point_matrix[0][1]

                ending_x = self.point_matrix[1][0]
                ending_y = self.point_matrix[1][1]
         

                # Cropping image
                img_cropped = img[starting_y:ending_y, starting_x:ending_x]
                cv2.imshow("ROI", img_cropped)  
                cv2.rectangle(img, (starting_x, starting_y), (ending_x, ending_y), (0, 255, 0), 3)  
                print(self.point_matrix)
                print(   read_test_from_image(img_cropped)  )
                self.bool_selected = True 


     
            # Showing original image
            cv2.imshow("Original Image ", img)
            # Mouse click event on original image
            cv2.setMouseCallback("Original Image ", self.mousePoints)
            # Printing updated point matrix
            #print(self.point_matrix)
            # Refreshing window all time
            cv2.waitKey(1)  
