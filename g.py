from ultralytics import YOLO
model = YOLO('runs/segment/train/weights/best.pt')

conter = 10
#for i in range(54):
#    file_path = f"D:/Cancer/manifest-1705128020168/Lung-PET-CT-Dx/Lung_Dx-A0001/04-04-2007-NA-Chest-07990/3.000000-5mm-41315/1-{str(conter)}.jpg"
#    model.predict(file_path, save=True, imgsz=640)
#    conter = conter+1

file_path = f"D:/Cancer/manifest-1705128020168/Lung-PET-CT-Dx/Lung_Dx-A0001/04-04-2007-NA-Chest-07990/3.000000-5mm-41315/1-{str(64)}.jpg"
#model.predict(file_path, save=True, imgsz=640, project="proj", name="trest")
model.predict(file_path, show_conf=False, save=True, imgsz=640, project="predictions", save_crop=True)