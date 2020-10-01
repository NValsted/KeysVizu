from kivy.graphics import Canvas, Translate, Fbo, ClearColor, \
    ClearBuffers, Scale

import glob
import cv2
import re

from .cleanup_util import clean_directory

class VideoManager():
    img_counter = 0
    meta_data = {"width" : 1920,
                 "height": 1080,
                 "FPS"   : 30.0,
                 "fourcc": cv2.VideoWriter_fourcc(*'XVID')}

    def __init__(self,tmp_imgs_path,**kwargs):
        self.tmp_imgs_path = tmp_imgs_path
        for k,v in kwargs.items():
            self.meta_data[k] = v

        self.compute_derived_meta_data()

    def compute_derived_meta_data(self):
        self.meta_data["WH_ratio"] = self.meta_data["width"] // self.meta_data["height"]
        self.meta_data["refresh_rate"] = 1 / self.meta_data["FPS"]
        
    def add_image(self,widget):
        filename = f"tmp_{self.img_counter}.png"
        output_size = (self.meta_data["width"], self.meta_data["height"])
        
        if self.meta_data["WH_ratio"] != widget.width // widget.height:
            raise Exception("W/H ratio does not match")
        
        img_scale = self.meta_data["width"] / widget.width

        if widget.parent is not None:
            canvas_parent_index = widget.parent.canvas.indexof(widget.canvas)
            if canvas_parent_index > -1:
                widget.parent.canvas.remove(widget.canvas)
    
        fbo = Fbo(size=output_size, with_stencilbuffer=True)

        with fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()
            Scale(img_scale, -img_scale, img_scale)
            Translate(-widget.x, -widget.y - widget.height, 0)

        fbo.add(widget.canvas)
        fbo.draw()
        fbo.texture.save(self.tmp_imgs_path+filename, flipped=False)
        fbo.remove(widget.canvas)
        
        if widget.parent is not None and canvas_parent_index > -1:
            widget.parent.canvas.insert(canvas_parent_index, widget.canvas)

        self.img_counter += 1 

    def clean_tmp_imgs(self):
        clean_directory(self.tmp_imgs_path)
        self.img_counter = 0

    def export_video(self,output_path):
        source_imgs = glob.glob(f"{self.tmp_imgs_path}*.png")
        source_imgs.sort(key=lambda f: int(re.sub('\D', '', f)))
        
        video = cv2.VideoWriter(output_path,
                                self.meta_data["fourcc"],
                                self.meta_data["FPS"],
                                ( self.meta_data["width"],
                                self.meta_data["height"] )
                                )
        
        for img in source_imgs:
            video.write(cv2.imread(img))

        cv2.destroyAllWindows()
        video.release()

        self.clean_tmp_imgs()

    

def main():
    pass

if __name__ == '__main__':
    main()