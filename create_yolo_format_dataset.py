import os.path

import cv2
import json
import glob
from pprint import pprint



if __name__ == '__main__':
    is_train = False
    mode = "train" if is_train else "val"
    root = "data/football_{}".format(mode)
    output_path = "../football/football_yolo"
    videos_paths = list(glob.iglob("{}/*/*.mp4".format(root)))
    anno_paths = list(glob.iglob("{}/*/*.json".format(root)))

    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    if not os.path.isdir(os.path.join(output_path, "images")):
        os.mkdir(os.path.join(output_path, "images"))
        os.mkdir(os.path.join(output_path, "labels"))
    if not os.path.isdir(os.path.join(output_path,"images",mode)):
        os.mkdir(os.path.join(output_path,"images",mode))
        os.mkdir(os.path.join(output_path, "labels",mode))


    for video_id, (video_path, anno_path) in enumerate(zip(videos_paths, anno_paths)):
        counter = 1
        video = cv2.VideoCapture(video_path)
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))


        with open(anno_path, "r") as json_file:
            json_data = json.load(json_file)

        image_width = json_data["images"][0]["width"]
        image_height = json_data["images"][0]["height"]



        while video.isOpened():
            flag, frame = video.read()

            if not flag:
                break
            cv2.imwrite(os.path.join(output_path,"images",mode,"{}_{}.jpg".format(video_id +1,counter)),frame)
            objects =  [item for item in json_data["annotations"] if item["image_id"] == counter and item["category_id"] >=2]

            with open(os.path.join(output_path, "labels",mode,"{}_{}.txt".format(video_id +1,counter)), "w") as txt_file:
                for obj in objects:
                    bbox = obj["bbox"]
                    xmin , ymin, width, height = bbox
                    xmin /= image_width
                    ymin /= image_height
                    width /= image_width
                    height /= image_height
                    x_cent = xmin + width/2
                    y_cent = ymin + height/2

                    if obj["category_id"] == 3:
                        cls = 0
                    else:
                        cls = 1
                    txt_file.write("{} {:06f} {:06f} {:06f} {:06f}\n".format(cls, x_cent, y_cent, width, height))
            counter += 1


