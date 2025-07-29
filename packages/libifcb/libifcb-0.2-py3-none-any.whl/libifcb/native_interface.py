#!/bin/python3

# Copyright 2025, A Baldwin
#
# This file is part of libifcb.
#
# libifcb is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libifcb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with libifcb.  If not, see <http://www.gnu.org/licenses/>.

'''
sample.py

An interface for image data from the IFCB sensor
'''

import argparse
import os
import re
import csv
import struct
import json
from PIL import Image
from PIL.TiffImagePlugin import ImageFileDirectory_v2
import numpy as np
from .utils import to_snake_case


def extract_images(target, no_metadata = False):
    header_lines = ""
    with open(target + ".hdr") as f:
        header_lines = f.readlines()
    metadata = header_file_to_dict(header_lines)
    #print(metadata)

    adc_format_map = list(csv.reader([metadata["adc_file_format"]], skipinitialspace=True))[0]
    image_map = []
    outputs = []


    if not no_metadata:
        with open(target + ".json", "w") as f:
            json.dump(metadata, f, ensure_ascii=False)
        outputs.append(target + ".json")
    with open(target + ".adc") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=adc_format_map, skipinitialspace=True)
        adc_data = []
        for row in reader:
            adc_data_row = {}
            for key in row:
                adc_data_row[to_snake_case_ifcb_preprocess(key)] = row[key]
            adc_data.append(adc_data_row)
        with open(target + ".roi", "rb") as imagefile:
            for row in adc_data:
                #print(row)
                imagefile.seek(int(row["start_byte"]))
                height = int(row["roi_height"])
                width = int(row["roi_width"])
                imdata = imagefile.read(height * width)
                if (height * width > 0):
                    imdata_reform = np.reshape(np.frombuffer(imdata, dtype=np.uint8), (height, width))
                    image = Image.fromarray(imdata_reform, "L")
                    image_package = {"metadata": row, "image": image}
                    image_map.append(image_package)
                    im_metadata = {}
                    for col_key in row:
                        #sanitised_col_key = re.sub(r"[^A-Za-z0-9_-]", "", col_key) # not neccesary now we do sanitization earlier
                        #print(sanitised_col_key)
                        #print(row[col_key])
                        im_metadata[col_key] = row[col_key]
                    trigger_number = str(row["trigger_number"])
                    if not no_metadata:
                        with open(target + "_TN" + trigger_number + ".json", "w") as f:
                            json.dump(im_metadata, f, ensure_ascii=False)
                        outputs.append(target + "_TN" + trigger_number + ".json")
                    image.save(target + "_TN" + trigger_number + ".tiff", "TIFF")
                    outputs.append(target + "_TN" + trigger_number + ".tiff")
    return outputs

class TriggerEvent:
    def __init__(self, raw, rois):
        self.raw = raw
        self.rois = rois

class ROIList(list):
    def __init__(self, roi_fp):
        self.__roi_fp = roi_fp
        self.__definitions = []
    def append(self, value):
        raise RuntimeException("ROIList is indented to be read only")
    def _append_roi(self, definition):
        self.__definitions.append(definition)
    def __setitem__(self, index, value):
        raise RuntimeException("ROIList is read only")
    def __getitem__(self, index, value):
        raise RuntimeException("ROIList is read only")
    def __len__(self):
        return len(self.__definitions)
    # Returns X,Y of ROI (this data isn't really useful but it's something someone might want to extract)
    def get_offset(self, index):
        cdef = self.__definitions[index]
        return (cdef[3], cdef[4])
    def __iter__(self):
        self.__iter_idx = 0
        return self
    def __next__(self):
        self.__iter_idx += 1
        if self.__iter_idx > len(self.__definitions):
            raise StopIteration
        return self.__getitem__(self.__iter_idx-1)
    def __getitem__(self, index):
        cdef = self.__definitions[index]
        if cdef is None:
            return None
        self.__roi_fp.seek(cdef[0])
        imdata = self.__roi_fp.read(cdef[1] * cdef[2])
        imdata_reform = np.reshape(np.frombuffer(imdata, dtype=np.uint8), (cdef[2], cdef[1]))
        image = Image.fromarray(imdata_reform, "L")
        return image

class ROIReader:
    # header = {}
    # adc_data = []
    # __adc_format_map = {}
    __close_adc = False
    __close_roi = False

    def __to_snake_case_ifcb_preprocess(self, str_in):
        # A quick fix for some questionable variable naming from old IFCB models
        str_inter = str_in.replace("MCC", "MCC_")
        str_inter = str_inter.replace("ROI", "ROI_")
        str_inter = str_inter.replace("ADC", "ADC_")
        str_inter = str_inter.replace("DAC", "DAC_")
        str_inter = str_inter.replace("DAQ", "DAQ_")
        str_inter = str_inter.replace("PMT", "PMT_")
        str_inter = str_inter.replace("TCP", "TCP_")
        str_inter = str_inter.replace("ROI", "ROI_")
        str_inter = str_inter.replace("UV", "UV_")
        str_inter = str_inter.replace("HKTRIGGER", "HK_Trigger_")
        str_inter = str_inter.replace("grabtimestart", "Grab_Time_Start")
        str_inter = str_inter.replace("grabtimeend", "Grab_Time_End")
        str_inter = str_inter.replace("STartPoint", "Start_Point")
        str_inter = str_inter.replace("trigger", "Trigger")
        str_inter = str_inter.replace("volt", "Volt")
        str_inter = str_inter.replace("high", "High")
        str_inter = str_inter.replace("grow", "Grow")
        return to_snake_case(str_inter)

    def __header_file_to_dict(self, lines):
        o_dict = {}
        for line in lines:
            m = re.search("^([^:]+):\\s?", line)
            if m is not None: # Only needed for very old IFCB data that might be mangled
                key = self.__to_snake_case_ifcb_preprocess(m.group(1))
                value = line[len(m.group(0)):]
                o_dict[key] = value.rstrip()
        return o_dict

    def __init__(self, hdr_fp, adc_fp, roi_fp):
        close_hdr = False
        if type(hdr_fp) == str:
            hdr_fp = open(hdr_fp, "r")
            close_hdr = True
        if type(adc_fp) == str:
            adc_fp = open(adc_fp, "r")
            close_adc = True
        if type(roi_fp) == str:
            roi_fp = open(roi_fp, "rb")
            self.__close_roi = True
        self.__roi_fp = roi_fp

        header_lines = hdr_fp.readlines()
        if close_hdr:
            hdr_fp.close()
        self.header = self.__header_file_to_dict(header_lines)
        self.__adc_format_map = list(csv.reader([self.header["adc_file_format"]], skipinitialspace=True))[0]

        self.adc_data = []
        reader = csv.DictReader(adc_fp, fieldnames=self.__adc_format_map, skipinitialspace=True)
        for row in reader:
            adc_data_row = {}
            for key in row:
                adc_data_row[self.__to_snake_case_ifcb_preprocess(key)] = row[key]
            self.adc_data.append(adc_data_row)
        if close_adc:
            hdr_fp.close()

        trigger_list = {}
        self.rows = ROIList(roi_fp)
        self.rois = ROIList(roi_fp)
        for adc_row in self.adc_data:
            tn = adc_row["trigger_number"]
            if tn not in trigger_list:
                trigger_list[tn] = {}
                trigger_list[tn]["rois"] = ROIList(roi_fp)
            trigger_list[tn]["raw_properties"] = adc_row
            if int(adc_row["roi_x"]) != 0:
                roi_def = (int(adc_row["start_byte"]),int(adc_row["roi_width"]),int(adc_row["roi_height"]),int(adc_row["roi_x"]),int(adc_row["roi_y"]))
                trigger_list[tn]["rois"]._append_roi(roi_def)
                self.rois._append_roi(roi_def)
                self.rows._append_roi(roi_def)
            else:
                self.rows._append_roi(None)

        self.triggers = []
        for trigger_idx in trigger_list.keys():
            trigger_def = trigger_list[trigger_idx]
            te = TriggerEvent(trigger_def["raw_properties"], trigger_def["rois"])
            self.triggers.append(te)
