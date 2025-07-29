# import required libraries
import cv2
import os
import importlib.resources as pkg_resources
import PyFaceCrop
import tempfile
import shutil
# Function to extract and return the Haarcascade file path
def get_haarcascade_path(filename):
    """Get the file path for Haarcascade files."""
    try:
        # Use pkg_resources to get the resource path
        with pkg_resources.path(PyFaceCrop, f'haarcascades/{filename}') as p:
            # Create a temporary directory to copy the Haarcascade file
            temp_dir = tempfile.mkdtemp()  # Create a temp directory
            temp_file_path = os.path.join(temp_dir, filename)
            
            # Copy the Haarcascade file to the temp directory
            shutil.copy(p, temp_file_path)

            print(f"Resolved path for {filename}: {temp_file_path}")  # Debugging output
            return temp_file_path
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        raise
        
class FaceCrop:
    # read the input image 
    def __init__(self, root_folder, destination_folder,interval_seconds=0,padding=0):
        # self.rootfolder = "../Samples/"
        self.rootfolder = root_folder
        self.destination_folder = destination_folder
        self.interval_seconds = interval_seconds  # Time interval in seconds
        self.padding = padding
    

    def generate(self):
        self.loadVideos()

    def crop_frame(self, frame, user_dir):
        img = frame
        # convert to grayscale of each frames
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        eye_cascade = cv2.CascadeClassifier(get_haarcascade_path("haarcascade_eye.xml"))
        # read the haarcascade to detect the faces in an image
        face_cascade = cv2.CascadeClassifier(get_haarcascade_path("haarcascade_frontalface_default.xml"))

        # detects faces in the input image
        faces = face_cascade.detectMultiScale(
            gray, 1.3, 5, flags=cv2.CASCADE_SCALE_IMAGE)

        # print(user_dir)
        usernameFolder = user_dir.split("_")[0]
        usernameFile = user_dir.split("_")[1]
        # print(usernameFile+" File")

        # loop over all detected faces
        if len(faces) > 0:
            for i, (x, y, w, h) in enumerate(faces):
                #face = img[y-20:y+20 + h, x-20:x+20 + w]
                padding = self.padding
                start_x = max(x - padding, 0)
                start_y = max(y - padding, 0)
                end_x = min(x + w + padding, img.shape[1])
                end_y = min(y + h + padding, img.shape[0])
                face = img[start_y:end_y, start_x:end_x]
                
                roi_gray = img[y:y + h, x:x + w]
                roi_color = img[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                # print(f"Eyes Count{len(eyes)}")
                for (ex, ey, ew, eh) in eyes:
                    #face = img[y:y+50 + h+50, x:x+50 + w+50]
                    # cv2.rectangle(
                    #     img, (x, y), (x + w+100, y + h+100), (0, 255, 255), 0)
                    if not os.path.exists(f"{self.destination_folder}/{usernameFolder}"):
                        os.makedirs(
                            f'{self.destination_folder}/{usernameFolder}', exist_ok=True)
                    # Save Images
                    cv2.imwrite(
                        f'{self.destination_folder}/{usernameFolder}/{usernameFile}.jpg', face)

    def loadVideos(self):
        try:
            # videorootfolder = "../Samples/Videos"
            videorootfolder = self.rootfolder
            for dir in os.listdir(videorootfolder):
                # set video file path of input video with name and extension
                print(f"{videorootfolder}/{dir}")
                vid = cv2.VideoCapture(f"{videorootfolder}/{dir}")
                
                fps = vid.get(cv2.CAP_PROP_FPS)
                if fps == 0:
                    print(f"Could not determine FPS for {videorootfolder}/{dir}. Skipping...")
                    continue

                frame_interval = int(fps * self.interval_seconds)  # 1 frame per second


                # for frame identity
                index = 0
                frame_id = 0
                
                while (True):
                    # Extract images
                    ret, frame = vid.read()
                    # end of frames
                    if not ret:
                        break
                    
                    if frame_interval > 0:
                        if frame_id % frame_interval == 0:
                            self.crop_frame(frame, f"{dir.split('.')[0]}_{index}")
                            index += 1
                    else:
                        self.crop_frame(frame, f"{dir.split('.')[0]}_{index}")
                        index += 1    

                    frame_id += 1                 
        except Exception as e:
            print(e.args)