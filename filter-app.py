import tkinter as tk
from tkinter import filedialog, Canvas, Button, Scale
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import numpy as np
import colorsys

class ImageFilterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Filter App")
        self.canvas = Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.image = None
        self.filtered_image = None
        
        button_frame = tk.Frame(master)
        button_frame.pack()

        self.load_button = Button(button_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT)

        self.filter_buttons = [
            Button(button_frame, text="Blur", command=self.apply_blur),
            Button(button_frame, text="Sharpen", command=self.apply_sharpen),
            Button(button_frame, text="Contour", command=self.apply_contour),
            Button(button_frame, text="Edge Enhance", command=self.apply_edge_enhance),
            Button(button_frame, text="Apply Hue", command=self.apply_hue),
            Button(button_frame, text="Apply Saturation", command=self.apply_saturation),
        ]
        
        for button in self.filter_buttons:
            button.pack(side=tk.LEFT)

        self.saturation_scale = Scale(master, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Saturation")
        self.saturation_scale.set(1)
        self.saturation_scale.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path).convert("RGBA")
            self.show_image(self.image)

    def show_image(self, img):
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def apply_blur(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.BLUR)
            self.show_image(self.filtered_image)

    def apply_sharpen(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.SHARPEN)
            self.show_image(self.filtered_image)

    def apply_contour(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.CONTOUR)
            self.show_image(self.filtered_image)

    def apply_edge_enhance(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            self.show_image(self.filtered_image)

    def apply_hue(self):
        if self.image:
            hue_shift = 30
            self.filtered_image = self.change_hue(self.image, hue_shift)
            self.show_image(self.filtered_image)

    def apply_saturation(self):
        if self.image:
            saturation_factor = self.saturation_scale.get()
            enhancer = ImageEnhance.Color(self.image)
            self.filtered_image = enhancer.enhance(saturation_factor)
            self.show_image(self.filtered_image)

    def change_hue(self, img, hue_shift):
        img = img.convert("RGB")
        data = np.array(img)
        hsv = np.empty(data.shape, dtype=np.float32)
        r, g, b = data[..., 0] / 255.0, data[..., 1] / 255.0, data[..., 2] / 255.0
        hsv[..., 0], hsv[..., 1], hsv[..., 2] = colorsys.rgb_to_hsv(r, g, b)
        hsv[..., 0] = (hsv[..., 0] + hue_shift / 360) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hsv[..., 0], hsv[..., 1], hsv[..., 2])
        rgb = np.empty(data.shape, dtype=np.uint8)
        rgb[..., 0], rgb[..., 1], rgb[..., 2] = r * 255, g * 255, b * 255
        return Image.fromarray(rgb)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()
