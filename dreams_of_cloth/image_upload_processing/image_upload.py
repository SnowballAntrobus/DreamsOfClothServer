from segment_anything import sam_model_registry, SamPredictor
import cv2
from io import BytesIO
import numpy as np

class UploadedImage:
    #TODO: maybe change to not be hardcoded path
    sam_checkpoint = "models/sam_vit_h_4b8939.pth"
    model_type = "vit_h"
    device = "cuda"

    points_data_present: bool
    box_data_present: bool
    positive_points: np.ndarray
    negative_points: np.ndarray
    input_box: np.ndarray
    imageData: BytesIO
    predictor: SamPredictor = None
    masks: any

    def __init__(self, imageData, points_data_present: bool, box_data_present: bool, positive_points: np.ndarray, negative_points: np.ndarray, input_box: np.ndarray):
        if not points_data_present and not box_data_present:
            raise ValueError("Input box and points can't both be null")
        self.box_data_present = box_data_present
        self.points_data_present = points_data_present
        
        self.imageData = imageData

        if points_data_present and positive_points.size == 0:
            self.positive_points = np.array([], dtype=int).reshape((0, 2))
        elif points_data_present:
            self.positive_points = positive_points

        if points_data_present and negative_points.size == 0:
            self.negative_points = np.array([], dtype=int).reshape((0, 2))
        elif points_data_present:
            self.negative_points = negative_points

        if box_data_present:
            self.input_box = input_box

    def isImageTooLarge(self, image):
        height, width = image.shape[:2]
        print(f"Width: {width}, Height: {height}")
        #TODO: Change this so it is not the exact size my phone happens to return a thumbnail as instead find smallest size that produces good results
        if not width == 640 or not height == 852:
            raise ValueError("The image is not the exact size expected")


    def readImage(self):
        nparr = np.frombuffer(self.imageData.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #TODO: Remove this write when we are confident in the process
        cv2.imwrite('from_mobile.png', image)
        self.isImageTooLarge(image)
        return image

    def createImageEmbedding(self):
        sam = sam_model_registry[self.model_type](checkpoint=self.sam_checkpoint)
        sam.to(device=self.device)

        predictor = SamPredictor(sam)
        predictor.set_image(self.readImage())
        self.predictor = predictor

    def predictMasks(self):
        if self.predictor == None:
            print("Error: Predictor was not set")
            return
        
        if self.points_data_present:
            points = np.concatenate((self.positive_points, self.negative_points), axis=0)
            pos_lables = np.ones(self.positive_points.shape[0])
            neg_lables = np.zeros(self.negative_points.shape[0])
            lables = np.concatenate((pos_lables, neg_lables))
        else:
            points = None
            lables = None

        if self.box_data_present:
            masks, scores, logits = self.predictor.predict(
                point_coords=points,
                point_labels=lables,
                box=self.input_box[None, :],
                multimask_output=True,
            )
            self.masks = zip(masks, scores)
            return
        
        masks, scores, logits = self.predictor.predict(
            point_coords=points,
            point_labels=lables,
            multimask_output=True,
        )
        self.masks = zip(masks, scores)

    def getMaskByteStream(self):
        binary_mask = max(self.masks, key=lambda x: x[1])[0]
        image = np.zeros_like(binary_mask, dtype=np.uint8)
        image[binary_mask != 0] = 255
        retval, buffer = cv2.imencode('.png', image)
        byte_stream = BytesIO(buffer)
        return byte_stream

    

