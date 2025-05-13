import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from sklearn.cluster import KMeans

# باز کردن عکس
def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        process_image(file_path)

# نوار پیشرفت
def process_image(image_path):
    progress_label = tk.Label(window, text="... در حال پردازش")
    progress_label.grid(row=3, column=0 , padx= (100,210) , pady=(10,10))

    progress_bar = ttk.Progressbar(window, mode='indeterminate', length=300)
    progress_bar.grid(row=4, column=0 , padx=(100,210) , pady=(0,20))

    progress_bar.start()

    window.after(100, lambda: detect_color_palette(image_path, progress_bar, progress_label))

# تشخیص طیف رنگی
def detect_color_palette(image_path, progress_bar, progress_label):
    # RGB تبدیل به
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    c_img = img.copy()
    c_img = np.reshape(c_img, (-1, 3))

    # خوشه‌بندی با الگوریتم کی-مینز برای یافتن رنگ‌های غالب
    kmeans = KMeans(n_clusters=7 , random_state=2 , n_init=10)
    kmeans.fit_predict(c_img)

    centers = kmeans.cluster_centers_.astype(int)

    per = np.array(np.unique(kmeans.labels_, return_counts=True)[1], dtype=np.float32)
    per = per / c_img.shape[0]

    dom = [[per[ix], centers[ix]] for ix in range(kmeans.n_clusters)]
    DOM = sorted(dom, reverse=True)

    color_p = np.zeros((50, 500, 3)).astype(int)

    start = 0
    for ix in range(kmeans.n_clusters):
        width = int(DOM[ix][0] * color_p.shape[1])
        end = start + width
        color_p[:, start:end, :] = DOM[ix][1]
        start = end

    #ایجاد یک تصویر و شی عکس برای طیف رنگی
    palette_image = Image.fromarray(color_p.astype(np.uint8))
    palette_photo = ImageTk.PhotoImage(palette_image)

    # ساخت قالب برای نمایش طیف رنگی
    palette_frame = tk.Frame(window, bg='#333333')
    palette_frame.grid(row=5, column=0 , padx= (0,210) , pady=(15,20))

    palette_label = tk.Label(palette_frame, image=palette_photo, bd=0)
    palette_label.image = palette_photo
    palette_label.pack(padx=5, pady=5)

    # پایان دادن نوار پیشرفت و برچسب
    progress_bar.stop()
    progress_bar.destroy()
    progress_label.destroy()

    # نمایش عکس منتخب
    selected_image = Image.open(image_path)
    selected_image = selected_image.resize((500, 350), Image.ANTIALIAS)
    selected_photo = ImageTk.PhotoImage(selected_image)

    selected_frame = tk.Frame(window, bg='#333333')
    selected_frame.grid(row=2, column=0, padx=(0, 210), pady=(15, 0))

    selected_label = tk.Label(selected_frame, image=selected_photo, bd=0)
    selected_label.image = selected_photo
    selected_label.pack(padx=5, pady=5)

# اجرای برنامه اصلی
window = ctk.CTk()
window.title("تشخیص طیف رنگی عکس")

# دکمه برای انتخاب عکس
open_button = ctk.CTkButton(window, text="انتخاب عکس", font=('Calibri' , 17), command=open_image, hover=True)
open_button.grid(row=1, column=0, padx=(130, 170) , pady=(15,0), sticky="w")

# تنظیم کردن موقعیت پنجره در هنگام بازشدن
window_width = 408
window_height = 415
display_width = window.winfo_screenwidth()
display_height = window.winfo_screenheight()
left = int(display_width / 2 - window_width / 2)
top = int(display_height / 2 - window_height / 2)
window.geometry(f'{window_width}x{window_height}+{left}+{top}')
window.resizable(False, False)

# وارد کردن آرم برای برنامه و اجرای برنامه
window.iconbitmap('F:/anaconda/project/ax/icon.ico')
window.mainloop()