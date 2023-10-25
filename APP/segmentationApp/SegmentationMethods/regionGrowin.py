import SimpleITK as sitk
import glob
import os
from os.path import join

def regionGrowing(input_dir, output_dir, seed,lower,upper,multiplier):
    image_list = os.listdir(input_dir)
    for file in image_list:
        file_name = os.path.join(input_dir, file)
        img = sitk.ReadImage(file_name, sitk.sitkInt16)
        seg = sitk.Image(img.GetSize(), sitk.sitkUInt8)
        seg.CopyInformation(img)
        seg[seed] = 1
        #seg = sitk.BinaryDilate(seg, 3)
        seg = sitk.ConnectedThreshold(img, seedList=[seed], lower=lower, upper=upper)
        seg = sitk.ConfidenceConnected(img, seedList=[seed],
                                   numberOfIterations=1,
                                   multiplier=multiplier,
                                   initialNeighborhoodRadius=2,
                                   replaceValue=1)
        seg_image = img*sitk.Cast(seg,img.GetPixelID())

        seg_image = sitk.Cast(seg,sitk.sitkUInt8)
        seg_image = sitk.RescaleIntensity(seg_image,0,255)

        sitk.WriteImage(seg_image,join(output_dir,file.split('.')[0]+"_predicted.png"))

