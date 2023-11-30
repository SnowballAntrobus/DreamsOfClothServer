from segment_anything import sam_model_registry, SamPredictor
import cv2
from io import BytesIO
import numpy as np

class UploadedImage:
    #TODO: change to not be hardcoded based on env created in init script instead
    sam_checkpoint = "models/sam_vit_h_4b8939.pth"
    model_type = "vit_h"
    device = "cuda"

    input_point = np.array([[600, 500]])
    input_label = np.array([1])
    imageData: BytesIO
    predictor: SamPredictor = None
    masks: any

    def __init__(self, imageData: BytesIO):
        self.imageData = imageData

    #TODO func that checks size of image

    def readImage(self):
        nparr = np.frombuffer(self.imageData.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def createImageEmbedding(self):
        sam = sam_model_registry[self.model_type](checkpoint=self.sam_checkpoint)
        sam.to(device=self.device)

        predictor = SamPredictor(sam)
        predictor.set_image(self.readImage())
        self.predictor = predictor

    # func that gets mask with points
    def predictMasks(self):
        if self.predictor != None:
            masks, scores, logits = self.predictor.predict(
                point_coords=self.input_point,
                point_labels=self.input_label,
                multimask_output=True,
            )
            self.masks = masks
        else:
            print("Error: Predictor was not set")

    def getMaskByteStream(self):
        for i, binary_mask in enumerate(self.masks):
            image = np.zeros_like(binary_mask, dtype=np.uint8)
            image[binary_mask != 0] = 255
            cv2.imwrite(f'{i}.png', image)
            retval, buffer = cv2.imencode('.png', image)
            byte_stream = BytesIO(buffer)
            #return byte_stream

    

