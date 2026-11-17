"""MediaPipe Face Mesh visualization. No emotion or mental-health inference."""
from io import BytesIO
import cv2,numpy as np
from PIL import Image
import mediapipe as mp
def analyze_photo(image_bytes):
 try: rgb=np.array(Image.open(BytesIO(image_bytes)).convert("RGB"))
 except Exception as e: raise RuntimeError("Could not read the captured photo. Please try again.") from e
 if rgb.shape[1]>1280:
  scale=1280/rgb.shape[1]; rgb=cv2.resize(rgb,(1280,int(rgb.shape[0]*scale)))
 mesh=mp.solutions.face_mesh
 draw=mp.solutions.drawing_utils
 spec=draw.DrawingSpec(color=(37,99,235),thickness=1,circle_radius=1)
 with mesh.FaceMesh(static_image_mode=True,max_num_faces=3,refine_landmarks=True,min_detection_confidence=.5) as detector:
  result=detector.process(rgb)
 out=rgb.copy(); faces=result.multi_face_landmarks or []
 for face in faces:
  draw.draw_landmarks(out,face,mesh.FACEMESH_CONTOURS,landmark_drawing_spec=spec,connection_drawing_spec=spec)
 return {"image":out,"faces":len(faces)}
