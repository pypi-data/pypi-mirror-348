import csv
import glob
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from skimage import measure
from scipy import spatial
from sklearn.model_selection import train_test_split
from tifffile import imread, imwrite
from tqdm import tqdm

from .utils import normalizeFloatZeroOne


def SegFreeMovieLabelDataSet(
    image_dir,
    csv_dir,
    save_dir,
    static_name,
    static_label,
    csv_name_diff,
    crop_size,
    gridx=1,
    gridy=1,
    normPatch=False,
    tshift=0,
    normalizeimage=True,
    dtype=np.uint8,
):

    raw_path = os.path.join(image_dir, "*tif")
    Csv_path = os.path.join(csv_dir, "*csv")
    files_raw = glob.glob(raw_path)
    files_raw.sort
    filesCsv = glob.glob(Csv_path)
    filesCsv.sort
    Path(save_dir).mkdir(exist_ok=True)
    total_categories = len(static_name)

    for fname in files_raw:

        name = os.path.basename(os.path.splitext(fname)[0])

        for csvfname in filesCsv:
            count = 0
            Csvname = os.path.basename(os.path.splitext(csvfname)[0])

            for i in range(0, len(static_name)):
                event_name = static_name[i]
                trainlabel = static_label[i]
                classfound = Csvname == csv_name_diff + event_name + name
                if classfound:
                    print(Csvname)
                    image = imread(fname).astype(dtype)
                    if not normPatch and normalizeimage:
                        image = normalizeFloatZeroOne(
                            image.astype(dtype), 1, 99.8, dtype=dtype
                        )
                    dataset = pd.read_csv(csvfname)
                    time = dataset[dataset.keys()[0]][1:]
                    y = dataset[dataset.keys()[1]][1:]
                    x = dataset[dataset.keys()[2]][1:]

                    # Categories + XYHW + Confidence
                    for (key, t) in time.items():

                        SimpleMovieMaker(
                            t,
                            y[key],
                            x[key],
                            image,
                            crop_size,
                            gridx,
                            gridy,
                            total_categories,
                            trainlabel,
                            name + event_name + str(count),
                            save_dir,
                            normPatch,
                            tshift,
                        )
                        count = count + 1


def SegFreeMovieLabelDataSet4D(
    image_dir,
    csv_dir,
    save_dir,
    static_name,
    static_label,
    csv_name_diff,
    crop_size,
    gridx=1,
    gridy=1,
    normPatch=False,
    tshift=0,
    normalizeimage=True,
    dtype=np.uint8,
):

    raw_path = os.path.join(image_dir, "*tif")
    Csv_path = os.path.join(csv_dir, "*csv")
    files_raw = glob.glob(raw_path)
    files_raw.sort
    filesCsv = glob.glob(Csv_path)
    filesCsv.sort
    Path(save_dir).mkdir(exist_ok=True)
    total_categories = len(static_name)

    for fname in files_raw:

        name = os.path.basename(os.path.splitext(fname)[0])

        for csvfname in filesCsv:
            count = 0
            Csvname = os.path.basename(os.path.splitext(csvfname)[0])

            for i in range(0, len(static_name)):
                event_name = static_name[i]
                trainlabel = static_label[i]
                classfound = Csvname == csv_name_diff + event_name + name
                if classfound:
                    print(Csvname)
                    image = imread(fname).astype(dtype)
                    dataset = pd.read_csv(csvfname)
                    time = dataset[dataset.keys()[0]]
                    z = dataset[dataset.keys()[1]]
                    y = dataset[dataset.keys()[2]]
                    x = dataset[dataset.keys()[3]]

                    # Categories + XYHW + Confidence
                    for (key, t) in time.items():

                        SimpleMovieMaker4D(
                            normalizeimage,
                            t,
                            z[key],
                            y[key],
                            x[key],
                            image,
                            crop_size,
                            gridx,
                            gridy,
                            total_categories,
                            trainlabel,
                            name + event_name + str(count),
                            save_dir,
                            normPatch,
                            tshift,
                            dtype,
                        )
                        count = count + 1


def SimpleMovieMaker(
    time,
    y,
    x,
    image,
    crop_size,
    gridx,
    gridy,
    total_categories,
    trainlabel,
    name,
    save_dir,
    normPatch,
    tshift,
    dtype,
):

    sizex, sizey, size_tminus, size_tplus = crop_size

    imagesizex = sizex * gridx
    imagesizey = sizey * gridy

    shiftNone = [0, 0]
    AllShifts = [shiftNone]

    time = time - tshift
    if time > 0:
        for shift in AllShifts:

            newname = name + "shift" + str(shift)
            Event_data = []

            Label = np.zeros([total_categories + 6])

            newcenter = (y - shift[1], x - shift[0])
            if (
                x + shift[0] > sizex / 2
                and y + shift[1] > sizey / 2
                and x + shift[0] + int(imagesizex / 2) < image.shape[2]
                and y + shift[1] + int(imagesizey / 2) < image.shape[1]
                and time > size_tminus
                and time + size_tplus + 1 < image.shape[0]
            ):
                crop_xminus = x - int(imagesizex / 2)
                crop_xplus = x + int(imagesizex / 2)
                crop_yminus = y - int(imagesizey / 2)
                crop_yplus = y + int(imagesizey / 2)
                # Cut off the region for training movie creation
                region = (
                    slice(int(time - size_tminus), int(time + size_tplus + 1)),
                    slice(
                        int(crop_yminus) + shift[1], int(crop_yplus) + shift[1]
                    ),
                    slice(
                        int(crop_xminus) + shift[0], int(crop_xplus) + shift[0]
                    ),
                )
                # Define the movie region volume that was cut
                crop_image = image[region]
                if normPatch:
                    crop_image = normalizeFloatZeroOne(
                        crop_image, 1, 99.8, dtype=dtype
                    )
                seglocationx = newcenter[1] - crop_xminus
                seglocationy = newcenter[0] - crop_yminus
                Label[total_categories] = seglocationx / sizex
                Label[total_categories + 1] = seglocationy / sizey
                Label[total_categories + 2] = (size_tminus) / (
                    size_tminus + size_tplus
                )
                Label[total_categories + 3] = 1
                Label[total_categories + 4] = 1
                Label[total_categories + 5] = 1

                # Write the image as 32 bit tif file
                if (
                    crop_image.shape[0] == size_tplus + size_tminus + 1
                    and crop_image.shape[1] == imagesizey
                    and crop_image.shape[2] == imagesizex
                ):

                    imwrite(
                        (save_dir + "/" + newname + ".tif"),
                        crop_image.astype("float32"),
                    )
                    Event_data.append([Label[i] for i in range(0, len(Label))])
                    if os.path.exists(save_dir + "/" + (newname) + ".csv"):
                        os.remove(save_dir + "/" + (newname) + ".csv")
                    writer = csv.writer(
                        open(save_dir + "/" + (newname) + ".csv", "a")
                    )
                    writer.writerows(Event_data)


def SimpleMovieMaker4D(
    normalizeimage,
    time,
    z,
    y,
    x,
    image,
    crop_size,
    gridx,
    gridy,
    total_categories,
    trainlabel,
    name,
    save_dir,
    normPatch,
    tshift,
    dtype,
):

    sizex, sizey, size_tminus, size_tplus = crop_size

    imagesizex = sizex * gridx
    imagesizey = sizey * gridy

    shiftNone = [0, 0]
    AllShifts = [shiftNone]

    time = time - tshift

    image = image[:, z, :, :]
    if normalizeimage:
        image = normalizeFloatZeroOne(
            image.astype(dtype), 1, 99.8, dtype=dtype
        )

    if time > 0:

        for shift in AllShifts:

            newname = name + "shift" + str(shift)
            Event_data = []

            Label = np.zeros([total_categories + 6])
            Label[trainlabel] = 1

            newcenter = (y - shift[1], x - shift[0])
            if (
                x + shift[0] > sizex / 2
                and y + shift[1] > sizey / 2
                and x + shift[0] + int(imagesizex / 2) < image.shape[2]
                and y + shift[1] + int(imagesizey / 2) < image.shape[1]
                and time > size_tminus
                and time + size_tplus + 1 < image.shape[0]
            ):
                crop_xminus = x - int(imagesizex / 2)
                crop_xplus = x + int(imagesizex / 2)
                crop_yminus = y - int(imagesizey / 2)
                crop_yplus = y + int(imagesizey / 2)
                # Cut off the region for training movie creation
                region = (
                    slice(int(time - size_tminus), int(time + size_tplus + 1)),
                    slice(
                        int(crop_yminus) + shift[1], int(crop_yplus) + shift[1]
                    ),
                    slice(
                        int(crop_xminus) + shift[0], int(crop_xplus) + shift[0]
                    ),
                )
                # Define the movie region volume that was cut
                crop_image = image[region]
                if normPatch:
                    crop_image = normalizeFloatZeroOne(
                        crop_image, 1, 99.8, dtype=dtype
                    )

                seglocationx = newcenter[1] - crop_xminus
                seglocationy = newcenter[0] - crop_yminus
                Label[total_categories] = seglocationx / sizex
                Label[total_categories + 1] = seglocationy / sizey
                Label[total_categories + 2] = (size_tminus) / (
                    size_tminus + size_tplus
                )
                Label[total_categories + 3] = 1
                Label[total_categories + 4] = 1
                Label[total_categories + 5] = 1

                # Write the image as 32 bit tif file
                if (
                    crop_image.shape[0] == size_tplus + size_tminus + 1
                    and crop_image.shape[1] == imagesizey
                    and crop_image.shape[2] == imagesizex
                ):

                    imwrite(
                        (save_dir + "/" + newname + ".tif"),
                        crop_image.astype("float32"),
                    )
                    Event_data.append([Label[i] for i in range(0, len(Label))])
                    if os.path.exists(save_dir + "/" + (newname) + ".csv"):
                        os.remove(save_dir + "/" + (newname) + ".csv")
                    writer = csv.writer(
                        open(save_dir + "/" + (newname) + ".csv", "a")
                    )
                    writer.writerows(Event_data)


def loadResizeImgs(im, size):

    w, h = im.size
    if w < h:
        im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    elif w > h:
        im = im.crop(((w - h + 1) / 2, 0, (w + h) / 2, h))

    return np.array(im.resize(size, Image.BILINEAR))


def Folder_to_oneat(
    dir, trainlabel, trainname, total_categories, size, save_dir
):

    Label = np.zeros([total_categories])

    count = 0

    files = sorted(glob.glob(dir + "/" + "*.png"))
    for i in tqdm(range(len(files))):
        file = files[i]
        try:
            Event_data = []

            img = Image.open(file)
            img = loadResizeImgs(img, size)
            Name = str(trainname) + os.path.basename(os.path.splitext(file)[0])
            image = normalizeFloatZeroOne(img.astype("uint16"), 1, 99.8)
            Label[trainlabel] = 1
            imwrite(
                (save_dir + "/" + Name + str(count) + ".tif"),
                image.astype("uint16"),
            )
            Event_data.append([Label[i] for i in range(0, len(Label))])
            if os.path.exists(save_dir + "/" + Name + str(count) + ".csv"):
                os.remove(save_dir + "/" + Name + str(count) + ".csv")
            writer = csv.writer(
                open(save_dir + "/" + Name + str(count) + ".csv", "a")
            )
            writer.writerows(Event_data)
            count = count + 1
        except Exception as e:
            print("[WW] ", str(e))
            continue


def Midog_to_oneat(
    midog_folder,
    annotation_file,
    event_type_name_label,
    all_ids,
    crop_size,
    save_dir,
):

    rows = []
    annotations = {}
    id_to_tumortype = {
        id: list(k for k in all_ids if id in all_ids[k])[0]
        for id in range(1, 406)
    }
    with open(annotation_file) as f:
        data = json.load(f)

        # categories = {cat["id"]: cat["name"] for cat in data["categories"]}
        total_categories = len(event_type_name_label.keys())
        for row in data["images"]:
            file_name = row["file_name"]
            image_id = row["id"]
            width = row["width"]
            height = row["height"]
            tumortype = id_to_tumortype[image_id]

            for annotation in [
                anno
                for anno in data["annotations"]
                if anno["image_id"] == image_id
            ]:
                box = annotation["bbox"]
                cat = annotation["category_id"]

                rows.append([image_id, width, height, box, cat, tumortype])
            annotations[file_name] = rows

    count = 0
    for tumortype, ids in zip(list(all_ids.keys()), list(all_ids.values())):

        for image_id in ids:

            file_path = midog_folder + "/" + f"{image_id:03d}.tiff"
            Name = os.path.basename(os.path.splitext(file_path)[0])

            img = imread(file_path)
            image = normalizeFloatZeroOne(img.astype("uint16"), 1, 99.8)
            image_annotation_array = annotations[Name + ".tiff"]
            image_id += 1

    for image_annotation in image_annotation_array:

        Label = np.zeros([total_categories + 5])
        Event_data = []
        (
            image_id,
            image_width,
            image_height,
            box,
            cat,
            tumortype,
        ) = image_annotation
        Name = str(image_id)
        x0, y0, x1, y1 = box
        height = y1 - y0
        width = x1 - x0
        x = (x0 + x1) // 2
        y = (y0 + y1) // 2
        # if cat == 1 then it is mitosis if cat == 2 it is hard negative
        if cat == 2:
            trainlabel = (
                event_type_name_label[tumortype] + total_categories // 2
            )
        if cat == 1:
            trainlabel = event_type_name_label[tumortype]
        ImagesizeX, ImagesizeY = crop_size
        crop_Xminus = x - int(ImagesizeX / 2)
        crop_Xplus = x + int(ImagesizeX / 2)
        crop_Yminus = y - int(ImagesizeY / 2)
        crop_Yplus = y + int(ImagesizeY / 2)
        region = (
            slice(int(crop_Yminus), int(crop_Yplus)),
            slice(int(crop_Xminus), int(crop_Xplus)),
        )

        crop_image = image[region]

        Label[trainlabel] = 1
        Label[total_categories] = 0.5
        Label[total_categories + 1] = 0.5
        Label[total_categories + 2] = width / ImagesizeX
        Label[total_categories + 3] = height / ImagesizeY
        Label[total_categories + 4] = 1

        count = count + 1
        if (
            crop_image.shape[0] == ImagesizeY
            and crop_image.shape[1] == ImagesizeX
        ):
            imwrite(
                (save_dir + "/" + Name + str(count) + ".tif"),
                crop_image.astype("float32"),
            )
            Event_data.append([Label[i] for i in range(0, len(Label))])
            if os.path.exists(save_dir + "/" + Name + str(count) + ".csv"):
                os.remove(save_dir + "/" + Name + str(count) + ".csv")
            writer = csv.writer(
                open(save_dir + "/" + Name + str(count) + ".csv", "a")
            )
            writer.writerows(Event_data)


def Midog_to_oneat_simple(
    midog_folder,
    annotation_file,
    event_type_name_label,
    all_ids,
    crop_size,
    save_dir,
):

    rows = []
    annotations = {}
    id_to_tumortype = {
        id: list(k for k in all_ids if id in all_ids[k])[0]
        for id in range(1, 406)
    }
    with open(annotation_file) as f:
        data = json.load(f)

        total_categories = len(event_type_name_label.keys())
        for row in data["images"]:
            file_name = row["file_name"]
            image_id = row["id"]
            width = row["width"]
            height = row["height"]
            tumortype = id_to_tumortype[image_id]

            for annotation in [
                anno
                for anno in data["annotations"]
                if anno["image_id"] == image_id
            ]:
                box = annotation["bbox"]
                cat = annotation["category_id"]

                rows.append([image_id, width, height, box, cat, tumortype])
            annotations[file_name] = rows

    count = 0
    for tumortype, ids in zip(list(all_ids.keys()), list(all_ids.values())):

        for image_id in ids:

            file_path = midog_folder + "/" + f"{image_id:03d}.tiff"
            Name = os.path.basename(os.path.splitext(file_path)[0])

            img = imread(file_path)
            image = normalizeFloatZeroOne(img.astype("uint16"), 1, 99.8)
            image_annotation_array = annotations[Name + ".tiff"]
            image_id += 1

    for image_annotation in image_annotation_array:

        Label = np.zeros([total_categories])
        Event_data = []
        (
            image_id,
            image_width,
            image_height,
            box,
            cat,
            tumortype,
        ) = image_annotation
        Name = str(image_id)
        x0, y0, x1, y1 = box
        height = y1 - y0
        width = x1 - x0
        x = (x0 + x1) // 2
        y = (y0 + y1) // 2
        # if cat == 1 then it is mitosis if cat == 2 it is hard negative
        if cat == 2:
            trainlabel = (
                event_type_name_label[tumortype] + total_categories // 2
            )
        if cat == 1:
            trainlabel = event_type_name_label[tumortype]
        ImagesizeX, ImagesizeY = crop_size
        crop_Xminus = x - int(ImagesizeX / 2)
        crop_Xplus = x + int(ImagesizeX / 2)
        crop_Yminus = y - int(ImagesizeY / 2)
        crop_Yplus = y + int(ImagesizeY / 2)
        region = (
            slice(int(crop_Yminus), int(crop_Yplus)),
            slice(int(crop_Xminus), int(crop_Xplus)),
        )

        crop_image = image[region]

        Label[trainlabel] = 1

        count = count + 1
        if (
            crop_image.shape[0] == ImagesizeY
            and crop_image.shape[1] == ImagesizeX
        ):
            imwrite(
                (save_dir + "/" + Name + str(count) + ".tif"),
                crop_image.astype("float32"),
            )
            Event_data.append([Label[i] for i in range(0, len(Label))])
            if os.path.exists(save_dir + "/" + Name + str(count) + ".csv"):
                os.remove(save_dir + "/" + Name + str(count) + ".csv")
            writer = csv.writer(
                open(save_dir + "/" + Name + str(count) + ".csv", "a")
            )
            writer.writerows(Event_data)


def MovieLabelDataSet(
    image_dir,
    seg_image_dir,
    csv_dir,
    save_dir,
    static_name,
    static_label,
    csv_name_diff,
    crop_size,
    gridx=1,
    gridy=1,
    tshift=0,
    normalizeimage=True,
    dtype=np.uint8,
):

    raw_path = os.path.join(image_dir, "*tif")
    Seg_path = os.path.join(seg_image_dir, "*tif")
    Csv_path = os.path.join(csv_dir, "*csv")
    files_raw = glob.glob(raw_path)
    files_raw.sort
    filesSeg = glob.glob(Seg_path)
    filesSeg.sort
    filesCsv = glob.glob(Csv_path)
    filesCsv.sort
    Path(save_dir).mkdir(exist_ok=True)
    total_categories = len(static_name)

    for fname in files_raw:
        name = os.path.basename(os.path.splitext(fname)[0])
        for i in range(0, len(static_name)):
                event_name = static_name[i]
                trainlabel = static_label[i]
                Csvname = csv_name_diff + event_name + name
                csvfname = os.path.join(csv_dir, Csvname + '.csv')
                if os.path.exists(csvfname):
                            print(Csvname)
                            count = 0
                            image = imread(os.path.join(image_dir,fname)).astype(dtype)
                            segimage = imread(os.path.join(seg_image_dir,fname)).astype("uint16")
                            dataset = pd.read_csv(csvfname)
                            time = dataset[dataset.keys()[0]]
                            y = dataset[dataset.keys()[1]]
                            x = dataset[dataset.keys()[2]]

                            # Categories + XYHW + Confidence
                            for (key, t) in time.items():

                                MovieMaker(
                                    t,
                                    y[key],
                                    x[key],
                                    image,
                                    segimage,
                                    crop_size,
                                    gridx,
                                    gridy,
                                    total_categories,
                                    trainlabel,
                                    name + event_name + str(count),
                                    save_dir,
                                    tshift,
                                    normalizeimage,
                                    dtype,
                                )
                                count = count + 1
                            image = None
                            segimage = None

def VolumeLabelDataSet(
    image_dir,
    seg_image_dir,
    csv_dir,
    save_dir,
    static_name,
    static_label,
    csv_name_diff,
    crop_size,
    gridx=1,
    gridy=1,
    gridz=1,
    tshift=0,
    normalizeimage=True,
    dtype=np.uint8,
):

    files_raw =  os.listdir(image_dir)

    Path(save_dir).mkdir(exist_ok=True)
    total_categories = len(static_name)

    for fname in files_raw:
        name = os.path.basename(os.path.splitext(fname)[0])
        for i in range(0, len(static_name)):
                event_name = static_name[i]
                trainlabel = static_label[i]
                Csvname = csv_name_diff + event_name + name
                csvfname = os.path.join(csv_dir, Csvname + '.csv')
                if os.path.exists(csvfname):
                    print(Csvname)
                    count = 0
                    image = imread(os.path.join(image_dir,fname)).astype(dtype)
                    segimage = imread(os.path.join(seg_image_dir,fname)).astype("uint16")
                    dataset = pd.read_csv(csvfname)
                    time = dataset[dataset.keys()[0]]
                    z = dataset[dataset.keys()[1]]
                    y = dataset[dataset.keys()[2]]
                    x = dataset[dataset.keys()[3]]

                    # Categories + XYZHW + Confidence
                    for (key, t) in time.items():

                        VolumeMaker(
                            t,
                            z[key],
                            y[key],
                            x[key],
                            image,
                            segimage,
                            crop_size,
                            gridx,
                            gridy,
                            gridz,
                            total_categories,
                            trainlabel,
                            name + event_name + str(count),
                            save_dir,
                            tshift,
                            normalizeimage,
                            dtype,
                        )
                        count = count + 1
                    image = None
                    segimage = None



def VolumeMaker(
    time,
    z,
    y,
    x,
    image,
    segimage,
    crop_size,
    gridx,
    gridy,
    gridz,
    total_categories,
    trainlabel,
    name,
    save_dir,
    tshift,
    normalizeimage,
    dtype,
):

    sizex, sizey, sizez, size_tminus, size_tplus = crop_size

    imagesizex = sizex * gridx
    imagesizey = sizey * gridy
    imagesizez = sizez * gridz
    shiftNone = [0, 0, 0]

    AllShifts = [shiftNone]

    time = time - tshift
    if normalizeimage:
        image = normalizeFloatZeroOne(
            image.astype(dtype), 1, 99.8, dtype=dtype
        )
    if time > size_tminus:

        # slice the images
    
        currentsegimage = segimage[int(time), :].astype("uint16")
        image_props = getHWD(
            x, y, z, currentsegimage, imagesizex, imagesizey, imagesizez
        )
        if image_props is not None:
            height, width, depth, center, seg_label = image_props
            smallimage = CreateVolume(
                image, size_tminus, size_tplus, int(time)
            )

            for shift in AllShifts:

                newname = name + "shift" + str(shift)
                Event_data = []
                newcenter = center
                x = center[2]
                y = center[1]
                z = center[0]

                Label = np.zeros([total_categories + 8])
                Label[trainlabel] = 1

                # T co ordinate
                Label[total_categories + 3] = (size_tminus) / (
                    size_tminus + size_tplus
                )
                if (
                    x > sizex / 2
                    and z > sizez / 2
                    and y > sizey / 2
                    and z + int(imagesizez / 2) < image.shape[1]
                    and y + int(imagesizey / 2) < image.shape[2]
                    and x + int(imagesizex / 2) < image.shape[3]
                    and time > size_tminus
                    and time + size_tplus + 1 < image.shape[0]
                ):
                    crop_xminus = x - int(imagesizex / 2)
                    crop_xplus = x + int(imagesizex / 2)
                    crop_yminus = y - int(imagesizey / 2)
                    crop_yplus = y + int(imagesizey / 2)
                    crop_zminus = z - int(imagesizez / 2)
                    crop_zplus = z + int(imagesizez / 2)
                    region = (
                        slice(0, smallimage.shape[0]),
                        slice(int(crop_zminus), int(crop_zplus)),
                        slice(int(crop_yminus), int(crop_yplus)),
                        slice(int(crop_xminus), int(crop_xplus)),
                    )

                    # Define the movie region volume that was cut
                    crop_image = smallimage[region]
                    seglocationx = newcenter[2] - crop_xminus
                    seglocationy = newcenter[1] - crop_yminus
                    seglocationz = newcenter[0] - crop_zminus

                    Label[total_categories] = seglocationx / sizex
                    Label[total_categories + 1] = seglocationy / sizey
                    Label[total_categories + 2] = seglocationz / sizez
                    if height >= imagesizey:
                        height = 0.5 * imagesizey
                    if width >= imagesizex:
                        width = 0.5 * imagesizex
                    if depth >= imagesizez:
                        depth = 0.5 * imagesizez
                    # Height
                    Label[total_categories + 4] = height / imagesizey
                    # Width
                    Label[total_categories + 5] = width / imagesizex
                    # Depth
                    Label[total_categories + 6] = depth / imagesizez

                    Label[total_categories + 7] = 1
                    # Write the image as 32 bit tif file
                    if (
                        crop_image.shape[0] == size_tplus + size_tminus + 1
                        and crop_image.shape[1] == imagesizez
                        and crop_image.shape[2] == imagesizey
                        and crop_image.shape[3] == imagesizex
                    ):

                        imwrite(
                            (save_dir + "/" + newname + ".tif"),
                            crop_image.astype("float32"),
                        )
                        Event_data.append(
                            [Label[i] for i in range(0, len(Label))]
                        )
                        if os.path.exists(save_dir + "/" + (newname) + ".csv"):
                            os.remove(save_dir + "/" + (newname) + ".csv")
                        writer = csv.writer(
                            open(save_dir + "/" + (newname) + ".csv", "a")
                        )
                        writer.writerows(Event_data)
    crop_image = None
    currentsegimage = None
    smallimage = None


def MovieMaker(
    time,
    y,
    x,
    image,
    segimage,
    crop_size,
    gridx,
    gridy,
    total_categories,
    trainlabel,
    name,
    save_dir,
    tshift,
    normalizeimage,
    dtype,
):

    sizex, sizey, size_tminus, size_tplus = crop_size

    imagesizex = sizex * gridx
    imagesizey = sizey * gridy

    shiftNone = [0, 0]
    AllShifts = [shiftNone]

    time = time - tshift
    if normalizeimage:
        image = normalizeFloatZeroOne(
            image.astype(dtype), 1, 99.8, dtype=dtype
        )
    if time > size_tminus:
        currentsegimage = segimage[int(time), :].astype("uint16")
        image_props = getHW(x, y, currentsegimage, imagesizex, imagesizey)
        if image_props is not None:
            height, width, center, seg_label = image_props
            for shift in AllShifts:

                newname = name + "shift" + str(shift)
                Event_data = []
                newcenter = (center[0] - shift[1], center[1] - shift[0])
                x = center[1]
                y = center[0]

                Label = np.zeros([total_categories + 6])
                Label[trainlabel] = 1
                # T co ordinate
                Label[total_categories + 2] = (size_tminus) / (
                    size_tminus + size_tplus
                )
                smallimage = CreateVolume(
                    image, size_tminus, size_tplus, int(time)
                )

                if (
                    x + shift[0] > sizex / 2
                    and y + shift[1] > sizey / 2
                    and x + shift[0] + int(imagesizex / 2) < image.shape[2]
                    and y + shift[1] + int(imagesizey / 2) < image.shape[1]
                    and time > size_tminus
                    and time + size_tplus + 1 < image.shape[0]
                ):
                    crop_xminus = x - int(imagesizex / 2)
                    crop_xplus = x + int(imagesizex / 2)
                    crop_yminus = y - int(imagesizey / 2)
                    crop_yplus = y + int(imagesizey / 2)
                    region = (
                        slice(0, smallimage.shape[0]),
                        slice(
                            int(crop_yminus) + shift[1],
                            int(crop_yplus) + shift[1],
                        ),
                        slice(
                            int(crop_xminus) + shift[0],
                            int(crop_xplus) + shift[0],
                        ),
                    )
                    # Define the movie region volume that was cut
                    crop_image = smallimage[region]

                    seglocationx = newcenter[1] - crop_xminus
                    seglocationy = newcenter[0] - crop_yminus

                    Label[total_categories] = seglocationx / sizex
                    Label[total_categories + 1] = seglocationy / sizey
                    if height >= imagesizey:
                        height = 0.5 * imagesizey
                    if width >= imagesizex:
                        width = 0.5 * imagesizex
                    # Height
                    Label[total_categories + 3] = height / imagesizey
                    # Width
                    Label[total_categories + 4] = width / imagesizex
                    Label[total_categories + 5] = 1
                    # Write the image as 32 bit tif file
                    if (
                        crop_image.shape[0] == size_tplus + size_tminus + 1
                        and crop_image.shape[1] == imagesizey
                        and crop_image.shape[2] == imagesizex
                    ):

                        imwrite(
                            (save_dir + "/" + newname + ".tif"),
                            crop_image.astype("float32"),
                        )
                        Event_data.append(
                            [Label[i] for i in range(0, len(Label))]
                        )
                        if os.path.exists(save_dir + "/" + (newname) + ".csv"):
                            os.remove(save_dir + "/" + (newname) + ".csv")
                        writer = csv.writer(
                            open(save_dir + "/" + (newname) + ".csv", "a")
                        )
                        writer.writerows(Event_data)
    image = None
    segimage = None
    crop_image = None
    currentsegimage = None
    smallimage = None


def Readname(fname):

    return os.path.basename(os.path.splitext(fname)[0])


def ImageLabelDataSet(
    image_dir,
    seg_image_dir,
    csv_dir,
    save_dir,
    static_name,
    static_label,
    csv_name_diff,
    crop_size,
    gridx=1,
    gridy=1,
    tshift=0,
    dtype=np.uint8,
):

    raw_path = os.path.join(image_dir, "*tif")
    Seg_path = os.path.join(seg_image_dir, "*tif")
    Csv_path = os.path.join(csv_dir, "*csv")
    files_raw = glob.glob(raw_path)
    files_raw.sort
    filesSeg = glob.glob(Seg_path)
    filesSeg.sort
    filesCsv = glob.glob(Csv_path)
    filesCsv.sort
    Path(save_dir).mkdir(exist_ok=True)
    total_categories = len(static_name)

    for csvfname in filesCsv:
        print(csvfname)
        count = 0
        Csvname = os.path.basename(os.path.splitext(csvfname)[0])

        for fname in files_raw:

            name = os.path.basename(os.path.splitext(fname)[0])
            for Segfname in filesSeg:

                Segname = os.path.basename(os.path.splitext(Segfname)[0])

                if name == Segname:

                    for i in range(0, len(static_name)):
                        event_name = static_name[i]
                        trainlabel = static_label[i]
                        if Csvname == csv_name_diff + name + event_name:
                            image = imread(fname).astype(dtype)
                            image = normalizeFloatZeroOne(
                                image.astype(dtype), 1, 99.8, dtype=dtype
                            )
                            segimage = imread(Segfname)
                            dataset = pd.read_csv(csvfname)
                            time = dataset[dataset.keys()[0]][1:]
                            y = dataset[dataset.keys()[1]][1:]
                            x = dataset[dataset.keys()[2]][1:]

                            # Categories + XYHW + Confidence
                            for (key, t) in time.items():
                                ImageMaker(
                                    t,
                                    y[key],
                                    x[key],
                                    image,
                                    segimage,
                                    crop_size,
                                    gridx,
                                    gridy,
                                    total_categories,
                                    trainlabel,
                                    name + event_name + str(count),
                                    save_dir,
                                    tshift,
                                )
                                count = count + 1


def SegFreeImageLabelDataSet(
    image_dir,
    csv_dir,
    save_dir,
    static_name,
    static_label,
    csv_name_diff,
    crop_size,
    gridx=1,
    gridy=1,
    dtype=np.uint8,
):

    raw_path = os.path.join(image_dir, "*tif")
    Csv_path = os.path.join(csv_dir, "*csv")
    files_raw = glob.glob(raw_path)
    files_raw.sort
    filesCsv = glob.glob(Csv_path)
    filesCsv.sort
    Path(save_dir).mkdir(exist_ok=True)
    total_categories = len(static_name)

    for csvfname in filesCsv:
        print(csvfname)
        count = 0
        Csvname = os.path.basename(os.path.splitext(csvfname)[0])

        for fname in files_raw:

            name = os.path.basename(os.path.splitext(fname)[0])
            image = imread(fname).astype(dtype)

            image = normalizeFloatZeroOne(
                image.astype(dtype), 1, 99.8, dtype=dtype
            )
            for i in range(0, len(static_name)):
                event_name = static_name[i]
                trainlabel = static_label[i]
                if Csvname == csv_name_diff + name + event_name:
                    dataset = pd.read_csv(csvfname)
                    time = dataset[dataset.keys()[0]][1:]
                    y = dataset[dataset.keys()[1]][1:]
                    x = dataset[dataset.keys()[2]][1:]

                    # Categories + XYHW + Confidence
                    for (key, t) in time.items():
                        SegFreeImageMaker(
                            t,
                            y[key],
                            x[key],
                            image,
                            crop_size,
                            gridx,
                            gridy,
                            total_categories,
                            trainlabel,
                            name + event_name + str(count),
                            save_dir,
                        )
                        count = count + 1


def CreateVolume(patch, size_tminus, size_tplus, timepoint):
    starttime = timepoint - int(size_tminus)
    endtime = timepoint + int(size_tplus) + 1
    smallimg = patch[starttime:endtime, :]

    return smallimg


def createNPZ(
    save_dir,
    axes,
    save_name="oneat",
    save_name_val="oneatVal",
    expand=True,
    static=False,
    flip_channel_axis=False,
    train_size=0.95,
):

    data = []
    label = []

    raw_path = os.path.join(save_dir, "*tif")
    files_raw = glob.glob(raw_path)
    files_raw.sort
    NormalizeImages = [imread(fname) for fname in files_raw]

    names = [Readname(fname) for fname in files_raw]
    # Normalize everything before it goes inside the training
    for i in range(0, len(NormalizeImages)):

        n = NormalizeImages[i]

        blankX = n
        csvfname = save_dir + "/" + names[i] + ".csv"
        arr = []
        with open(csvfname) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            arr = list(reader)[0]
            arr = np.array(arr)

        blankY = arr
        blankY = np.expand_dims(blankY, -1)
        if expand:

            blankX = np.expand_dims(blankX, -1)

        data.append(blankX)
        label.append(blankY)

    dataarr = np.asarray(data)
    labelarr = np.asarray(label)
    if flip_channel_axis:
        np.swapaxes(dataarr, 1, -1)
    if static:
        try:
            dataarr = dataarr[:, 0, :, :, :]
        except ValueError:
            pass
    print(dataarr.shape, labelarr.shape)
    traindata, validdata, trainlabel, validlabel = train_test_split(
        dataarr,
        labelarr,
        train_size=train_size,
        shuffle=False,
    )
    save_full_training_data(save_dir, save_name, traindata, trainlabel, axes)
    save_full_training_data(
        save_dir, save_name_val, validdata, validlabel, axes
    )


def _raise(e):
    raise e


def ImageMaker(
    time,
    y,
    x,
    image,
    segimage,
    crop_size,
    gridX,
    gridY,
    total_categories,
    trainlabel,
    name,
    save_dir,
    tshift,
):

    sizeX, sizeY = crop_size

    ImagesizeX = sizeX * gridX
    ImagesizeY = sizeY * gridY

    shiftNone = [0, 0]
    AllShifts = [shiftNone]

    time = time - tshift
    if time < segimage.shape[0] - 1 and time > 0:
        currentsegimage = segimage[int(time), :].astype("uint16")

        image_props = getHW(x, y, currentsegimage, ImagesizeX, ImagesizeY)
        if image_props is not None:
            height, width, center, seg_label = image_props
            for shift in AllShifts:

                newname = name + "shift" + str(shift)
                newcenter = (center[0] - shift[1], center[1] - shift[0])
                Event_data = []

                x = center[1]
                y = center[0]
                Label = np.zeros([total_categories + 5])
                Label[trainlabel] = 1
                if (
                    x + shift[0] > sizeX / 2
                    and y + shift[1] > sizeY / 2
                    and x + shift[0] + int(ImagesizeX / 2) < image.shape[2]
                    and y + shift[1] + int(ImagesizeY / 2) < image.shape[1]
                ):
                    crop_Xminus = x - int(ImagesizeX / 2)
                    crop_Xplus = x + int(ImagesizeX / 2)
                    crop_Yminus = y - int(ImagesizeY / 2)
                    crop_Yplus = y + int(ImagesizeY / 2)

                    for tex in range(int(time) - 2, int(time) + 2):
                        newname = newname + str(tex)
                        region = (
                            slice(int(tex - 1), int(tex)),
                            slice(
                                int(crop_Yminus) + shift[1],
                                int(crop_Yplus) + shift[1],
                            ),
                            slice(
                                int(crop_Xminus) + shift[0],
                                int(crop_Xplus) + shift[0],
                            ),
                        )

                        crop_image = image[region]

                        seglocationx = newcenter[1] - crop_Xminus
                        seglocationy = newcenter[0] - crop_Yminus

                        Label[total_categories] = seglocationx / sizeX
                        Label[total_categories + 1] = seglocationy / sizeY

                        if height >= ImagesizeY:
                            height = 0.5 * ImagesizeY
                        if width >= ImagesizeX:
                            width = 0.5 * ImagesizeX

                        Label[total_categories + 2] = height / ImagesizeY
                        Label[total_categories + 3] = width / ImagesizeX
                        Label[total_categories + 4] = 1

                        if (
                            crop_image.shape[1] == ImagesizeY
                            and crop_image.shape[2] == ImagesizeX
                        ):
                            imwrite(
                                (save_dir + "/" + newname + ".tif"),
                                crop_image.astype("float32"),
                            )
                            Event_data.append(
                                [Label[i] for i in range(0, len(Label))]
                            )
                            if os.path.exists(
                                save_dir + "/" + (newname) + ".csv"
                            ):
                                os.remove(save_dir + "/" + (newname) + ".csv")
                            writer = csv.writer(
                                open(save_dir + "/" + (newname) + ".csv", "a")
                            )
                            writer.writerows(Event_data)


def SegFreeImageMaker(
    time,
    y,
    x,
    image,
    crop_size,
    gridX,
    gridY,
    total_categories,
    trainlabel,
    name,
    save_dir,
    tshift,
):

    sizex, sizey = crop_size

    ImagesizeX = sizex * gridX
    ImagesizeY = sizey * gridY

    shiftNone = [0, 0]
    AllShifts = [shiftNone]

    time = time - tshift
    if time < image.shape[0] - 1 and time > 0:

        for shift in AllShifts:

            newname = name + "shift" + str(shift)
            newcenter = (y - shift[1], x - shift[0])
            Event_data = []

            Label = np.zeros([total_categories + 5])
            Label[trainlabel] = 1
            if (
                x + shift[0] > sizex / 2
                and y + shift[1] > sizey / 2
                and x + shift[0] + int(ImagesizeX / 2) < image.shape[2]
                and y + shift[1] + int(ImagesizeY / 2) < image.shape[1]
            ):
                crop_Xminus = x - int(ImagesizeX / 2)
                crop_Xplus = x + int(ImagesizeX / 2)
                crop_Yminus = y - int(ImagesizeY / 2)
                crop_Yplus = y + int(ImagesizeY / 2)

                for tex in range(int(time) - 2, int(time) + 2):
                    newname = newname + str(tex)
                    region = (
                        slice(int(tex - 1), int(tex)),
                        slice(
                            int(crop_Yminus) + shift[1],
                            int(crop_Yplus) + shift[1],
                        ),
                        slice(
                            int(crop_Xminus) + shift[0],
                            int(crop_Xplus) + shift[0],
                        ),
                    )

                    crop_image = image[region]

                    seglocationx = newcenter[1] - crop_Xminus
                    seglocationy = newcenter[0] - crop_Yminus

                    Label[total_categories] = seglocationx / sizex
                    Label[total_categories + 1] = seglocationy / sizey
                    Label[total_categories + 2] = 1
                    Label[total_categories + 3] = 1
                    Label[total_categories + 4] = 1

                    if (
                        crop_image.shape[1] == ImagesizeY
                        and crop_image.shape[2] == ImagesizeX
                    ):
                        imwrite(
                            (save_dir + "/" + newname + ".tif"),
                            crop_image.astype("float32"),
                        )
                        Event_data.append(
                            [Label[i] for i in range(0, len(Label))]
                        )
                        if os.path.exists(save_dir + "/" + (newname) + ".csv"):
                            os.remove(save_dir + "/" + (newname) + ".csv")
                        writer = csv.writer(
                            open(save_dir + "/" + (newname) + ".csv", "a")
                        )
                        writer.writerows(Event_data)


def getHW(defaultX, defaultY, currentsegimage, imagesizex, imagesizey):

    properties = measure.regionprops(currentsegimage)
    centroids = [prop.centroid for prop in properties]
    labels = [prop.label for prop in properties]
    tree = spatial.cKDTree(centroids)
    
    DLocation = (defaultY, defaultX)
    distance_cell_mask, nearest_location = tree.query(DLocation)
    if distance_cell_mask < 0.5 * imagesizex:
        y = int(centroids[nearest_location][0])         
        x = int(centroids[nearest_location][1])
        SegLabel = labels[nearest_location]
        DLocation = (y, x)
    else:
        if (
        int(TwoDLocation[0]) < currentsegimage.shape[0]
        and int(TwoDLocation[1]) < currentsegimage.shape[1]
        and all(i >= 0 for i in DLocation)
        ):
          SegLabel = currentsegimage[int(DLocation[0]), int(DLocation[1])]

        else:
            SegLabel = -1  

    TwoDLocation = (defaultY, defaultX)
    if (
        int(TwoDLocation[0]) < currentsegimage.shape[0]
        and int(TwoDLocation[1]) < currentsegimage.shape[1]
    ):
        SegLabel = currentsegimage[int(TwoDLocation[0]), int(TwoDLocation[1])]
        for prop in properties:

            if SegLabel > 0 and prop.label == SegLabel:
                minr, minc, maxr, maxc = prop.bbox
                center = (defaultY, defaultX)
                height = abs(maxc - minc)
                width = abs(maxr - minr)
                return height, width, center, SegLabel

            if SegLabel == 0:

                center = (defaultY, defaultX)
                height = 0.5 * imagesizex
                width = 0.5 * imagesizey
                return height, width, center, SegLabel


def getHWD(
    defaultX,
    defaultY,
    defaultZ,
    currentsegimage,
    imagesizex,
    imagesizey,
    imagesizez,
):

    properties = measure.regionprops(currentsegimage)
    centroids = [prop.centroid for prop in properties]
    labels = [prop.label for prop in properties]
    tree = spatial.cKDTree(centroids)
    
    DLocation = (defaultZ, defaultY, defaultX)
    distance_cell_mask, nearest_location = tree.query(DLocation)
    if distance_cell_mask < 0.5 * imagesizex:
        z = int(centroids[nearest_location][0])         
        y = int(centroids[nearest_location][1])
        x = int(centroids[nearest_location][2])
        SegLabel = labels[nearest_location]
        DLocation = (z, y, x)
    else:
        if (
        int(DLocation[0]) < currentsegimage.shape[0] 
        and int(DLocation[1]) < currentsegimage.shape[1]
        and int(DLocation[2]) < currentsegimage.shape[2]
        and all(i >= 0 for i in DLocation)
        ):
           SegLabel = currentsegimage[int(DLocation[0]), int(DLocation[1]), int(DLocation[2])]
        else:
            SegLabel = -1   
    if (
        int(DLocation[0]) < currentsegimage.shape[0]
        and int(DLocation[1]) < currentsegimage.shape[1]
        and int(DLocation[2]) < currentsegimage.shape[2]
    ):
       
        for prop in properties:
            if SegLabel > 0 and prop.label == SegLabel:
                minr, minc, mind, maxr, maxc, maxd = prop.bbox
                center = (defaultZ, defaultY, defaultX)
                height = abs(maxc - minc)
                width = abs(maxr - minr)
                depth = abs(maxd - mind)
                return height, width, depth, center, SegLabel

            if SegLabel == 0 :

                center = (defaultZ, defaultY, defaultX)
                height = 0.5 * imagesizex
                width = 0.5 * imagesizey
                depth = 0.5 * imagesizez
                return height, width, depth, center, SegLabel


def save_full_training_data(directory, filename, data, label, axes):
    """Save training data in ``.npz`` format."""

    len(axes) == data.ndim or _raise(ValueError())
    np.savez(directory + filename, data=data, label=label, axes=axes)


def InterchangeTXY(TXYCSV, save_dir):

    dataset = pd.read_csv(TXYCSV)
    time = dataset[dataset.keys()[0]][1:]
    x = dataset[dataset.keys()[1]][1:]
    y = dataset[dataset.keys()[2]][1:]

    Event_data = []

    Name = os.path.basename(os.path.splitext(TXYCSV)[0])

    for (key, t) in time.items():

        Event_data.append([t, y[key], x[key]])

    writer = csv.writer(open(save_dir + "/" + (Name) + ".csv", "a"))
    writer.writerows(Event_data)
