
import SimpleITK as sitk
import glob
import os
from os.path import join

def threshold(input_dir, output_dir, threshold):
    image_list = os.listdir(input_dir)
    for file in image_list:
        file_name = os.path.join(input_dir, file)
        img = sitk.ReadImage(file_name, sitk.sitkInt16)
        seg_mask = img>threshold
        seg_image = img*sitk.Cast(seg_mask,img.GetPixelID())
        seg_image = sitk.Cast(seg_mask,sitk.sitkUInt8)
        seg_image = sitk.RescaleIntensity(seg_image,0,255)
        sitk.WriteImage(seg_image,join(output_dir,file.split('.')[0]+"_predicted.png"))
