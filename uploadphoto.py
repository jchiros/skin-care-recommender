import cv2
import dlib
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Skin Care Recommender")
root.config(bg="#194F54") 

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

result_label = tk.Label(right_frame, text="Skin Care Recommender", font=("Helvetica", 16))
result_label.pack(pady=10)

output_label = tk.Label(right_frame, text="", font=("Helvetica", 12))
output_label.pack(pady=5)


image_canvas = tk.Canvas(left_frame, width=720, height=640)
image_canvas.pack(pady=10)


prod_reco = {
    '(0-2)': {
        'Male': '\nAveeno Baby Daily Moisturizing Lotion',
        'Female': '\nAveeno Baby Daily Moisturizing Lotion',
    },
    '(4-6)': {
        'Male': '\nChild-friendly sunscreen: Banana Boat Kids Sport Tear-Free SPF 50',
        'Female': '\nChild-friendly sunscreen: Banana Boat Kids Sport Tear-Free SPF 50',
    },
    '(8-12)': {
        'Male': '\nEvereden Kids Face Wash',
        'Female': '\nEvereden Kids Face Wash',
    },
    '(15-20)': {
        'Male': '\nCleanser: Cetaphil Gentle Skin Cleanser \n\nMoisturizer: Cetaphil Daily Facial Moisturizer \n\nSunscreen: Garnier Skin Naturals Sun Control Moisturizer SPF 15',
        'Female': '\nCleanser: Garnier Micellar Cleansing Water Blue \n\nMoisturizer: Myra Smooth Glow Facial Moisturizer \n\nSunscreen: Lotus Herbals Safe Sun Block Cream SPF 30',
    },
    '(25-32)': {
        'Male': '\nCleanser: La Roche-Posay Effaclar Medicated Gel Cleanser \n\nMoisturizer: Neutrogena Hydro Boost Water Gel \n\nSunscreen: Jack Black Double-Duty Face Moisturizer SPF 20',
        'Female': '\nCleanser: CeraVe Hydrating Facial Cleanser \n\nMoisturizer: CeraVe Facial Moisturizing Lotion PM \n\nSunscreen: EltaMD UV Clear Broad-Spectrum SPF 46',
    },
    '(38-43)': {
        'Male': '\nAnti-aging Serum: CeraVe Skin Renewing Vitamin C Serum \n\nMoisturizer: Neutrogena Rapid Wrinkle Repair Night Moisturizer \n\nSunscreen: EltaMD UV Clear Broad-Spectrum SPF 46',
        'Female': '\nAnti-aging Serum: SkinCeuticals C E Ferulic \n\nMoisturizer: CeraVe Facial Moisturizing Lotion PM \n\nSunscreen: Supergoop! Unseen Sunscreen SPF 40',
    },
    '(48-53)': {
        'Male': '\nCleanser: Cetaphil Gentle Skin Cleanser \n\nMoisturizer: Nivea Men Maximum Hydration Moisturizing Face Cream \n\nSunscreen: Sun Bum Mineral SPF 30 Sunscreen Spray',
        'Female': '\nCleanser: CeraVe Hydrating Facial Cleanser \n\nMoisturizer: Olay Regenerist Micro-Sculpting Cream \n\nSunscreen: La Roche-Posay Anthelios Melt-in Milk Sunscreen SPF 60',
    },
    '(60-100)': {
        'Male': "\nCleanser: Jack Black Pure Clean Daily Facial \n\nMoisturizer: CeraVe PM Facial Moisturizing Lotion \n\nSunscreen: EltaMD UV Daily Broad-Spectrum SPF 40",
        'Female': '\nCleanser: Neutrogena Ultra Gentle Hydrating Cleanser \n\nMoisturizer: Global Anti-Aging Cell Power Creme \n\nSunscreen: Neutrogena Age Shield Face Sunscreen SPF 110',
    }
}

image_pil = None
canvas_item_id = None


def display_image_with_annotations(image, annotations):
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    image_canvas.create_image(0, 0, anchor=tk.NW, image=image)
    image_canvas.image = image

    annotations_label = tk.Label(right_frame, text=annotations, font=("Helvetica", 12))
    annotations_label.pack(pady=10)

def select_image():
    global image_pil
    global canvas_item_id

    if canvas_item_id is not None:
        image_canvas.delete(canvas_item_id)

    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        img = cv2.resize(img, (720, 640))
        frame = img.copy()

        age_weights = "age_deploy.prototxt"
        age_config = "age_net.caffemodel"
        age_Net = cv2.dnn.readNet(age_config, age_weights)

        ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
                   '(25-32)', '(38-43)', '(48-53)', '(60-100)']
        model_mean = (78.4263377603, 87.7689143744, 114.895847746)

        gender_weights = "gender_deploy.prototxt"
        gender_config = "gender_net.caffemodel"
        gender_Net = cv2.dnn.readNet(gender_config, gender_weights)

        genderList = ['Male', 'Female']

        fH = img.shape[0]
        fW = img.shape[1]

        Boxes = []
        mssg = 'Face Detected'

        face_detector = dlib.get_frontal_face_detector()
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector(img_gray)

        if not faces:
            mssg = 'No face detected'
            result_label.config(text=mssg)
        else:
            for face in faces:
                x = face.left()
                y = face.top()
                x2 = face.right()
                y2 = face.bottom()

                box = [x, y, x2, y2]
                Boxes.append(box)
                cv2.rectangle(frame, (x, y), (x2, y2),
                              (00, 200, 200), 2)

            for box in Boxes:
                face = frame[box[1]:box[3], box[0]:box[2]]

                blob = cv2.dnn.blobFromImage(
                    face, 1.0, (227, 227), model_mean, swapRB=False)

                age_Net.setInput(blob)
                age_preds = age_Net.forward()
                age = ageList[age_preds[0].argmax()]

                gender_Net.setInput(blob)
                gender_preds = gender_Net.forward()
                gender = genderList[gender_preds[0].argmax()]

                recommendation = prod_reco.get(age, {}).get(gender, 'Unknown')
                result_label.config(text=f"\n\nRecommended Products:\n {recommendation}", font=("Helvetica", 18))

                cv2.putText(frame, f'{mssg}: {age}, {gender}', (box[0], box[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

                img_with_annotations = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_with_annotations = Image.fromarray(img_with_annotations)
                img_with_annotations = ImageTk.PhotoImage(img_with_annotations)
                canvas_item_id = image_canvas.create_image(0, 0, anchor=tk.NW, image=img_with_annotations)
                image_canvas.image = img_with_annotations

button_frame = tk.Frame(left_frame)
button_frame.pack(pady=10)

button = tk.Button(button_frame, text="Select Image", command=select_image)
button.grid(row=0, column=0, padx=10, pady=10)

root.mainloop()