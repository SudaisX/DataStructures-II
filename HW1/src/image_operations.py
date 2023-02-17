from src.myimage import *

def remove_channel(src: MyImage, red: bool = False, green: bool = False,
                   blue: bool = False) -> MyImage:
    """Returns a copy of src in which the indicated channels are suppressed.
    Suppresses the red channel if no channel is indicated. src is not modified.
    Args:
    - src: the image whose copy the indicated channels have to be suppressed.
    - red: suppress the red channel if this is True.
    - green: suppress the green channel if this is True.
    - blue: suppress the blue channel if this is True.
    Returns:
    a copy of src with the indicated channels suppressed.
    """

    #creating src image's copy
    copyImg = MyImage((src.size[0], src.size[1]))

    #iterating over the copy image
    for x in range(src.size[1]):
        for y in range(src.size[0]):
            # Extracting RGB values of a pixel at (x, y) coordinate
            r, g, b = src.get(x,y)

            # Suppresses the red channel if no channel is indicated / Although im confused how do I tackle if we want to supress no channel
            r = 0 if (not red and not green and not blue) else r

            # Check if any channel has been indicated to supress
            r = 0 if red else r
            g = 0 if green else g
            b = 0 if blue else b

            # Sets the copy image with supressed channel(s)
            copyImg.set(x, y, (r, g, b))

    return copyImg

def rotations(src: MyImage) -> MyImage:
    """Returns an image containing the 4 rotations of src.
    The new image has twice the dimensions of src. src is not modified.
    Args:
    - src: the image whose rotations have to be stored and returned.
    Returns:
    an image twice the size of src and containing the 4 rotations of src.
    """
    #creating src image's copy
    copyImg = MyImage((src.size[0]*2, src.size[1]*2))

    for x in range(src.size[0]):
        for y in range(src.size[1]):
            rgbPixel=src.get(x, y)  # Get the current rgbPixel position values without rotation

            # Rotating the current pixel of the image
            topRight =      (x                      , src.size[0] + y)          # No rotation 
            bottomRight =   (src.size[0] + y        , src.size[1]*2 - x - 1)    # 90 degree rotation
            bottomLeft =    (src.size[0]*2 -x - 1   , src.size[0] - y -1)       # 180 degree rotation
            topLeft =       (src.size[0] - y - 1    , x)                        # 270 degrees rotation

            copyImg.set(topRight[0]     , topRight[1]     , rgbPixel)         # Copy the rgbPixel to the top right without rotation
            copyImg.set(bottomRight[0]  , bottomRight[1]  , rgbPixel)         # Copy the rgbPixel to the bottom right with 90 degrees rotation
            copyImg.set(bottomLeft[0]   , bottomLeft[1]   , rgbPixel)         # Copy the rgbPixel to the bottom right with 180 degrees rotation
            copyImg.set(topLeft[0]      , topLeft[1]      , rgbPixel)         # Copy the rgbPixel to the bottom left with 270 degrees rotation

    return copyImg

def apply_mask(src: MyImage, maskfile: str, average: bool = True) -> MyImage:
    """Returns an copy of src with the mask from maskfile applied to it.
    maskfile specifies a text file which contains an n by n mask. It has the
    following format:
    - the first line contains n
    - the next n^2 lines contain 1 element each of the flattened mask
    Args:
    - src: the image on which the mask is to be applied
    - maskfile: path to a file specifying the mask to be applied
    - average: if True, averaging should to done when applying the mask
    Returns:
    an image which the result of applying the specified mask to src.
    """

    copyImg = MyImage((src.size[0], src.size[1]))
    newImg = MyImage((src.size[0], src.size[1]))

    # Saving maskfile's contents into a 2d list
    with open(maskfile) as maskFile:
        maskFileContents = [int(i) for i in maskFile] # get all the contents of the maskFile into a flat list
        maskSize = maskFileContents[0]                # extract 0th element from the maskFileContents list = size
        mask = [[maskFileContents[j+1] for j in range(i*maskSize, (i+1)*maskSize)] for i in range(maskSize)]

    # Turning img into grayscale
    for x in range(src.size[1]):
        for y in range(src.size[0]):
            rgbAvg = sum(src.get(x,y))//3               # Extracting avg RGB values of a pixel at (x, y) coordinate
            copyImg.set(x, y, (rgbAvg, rgbAvg, rgbAvg)) # replace the value of each channel at the pixel with the average channel value at the pixel

    # Implementing Mask
    for x in range(src.size[1]):
        for y in range(src.size[0]):
            weightedSum = 0
            maskWeights = 0

            # Finding masked values for every pixel in the image
            for maskX in range(maskSize):
                for maskY in range(maskSize):
                    try:
                        weightedSum += mask[maskX][maskY] * copyImg.get(maskX + (x - maskSize//2), maskY + (y - maskSize//2))[0] # To calculate weighted sum
                        maskWeights += mask[maskX][maskY] # To calculate weighted average if average=true

                    except: # Skips invalid pixel values / to deal with out of border pixels
                        continue

            # If average=true then convert to weighted average
            if average: 
                weightedSum = weightedSum//maskWeights 

            # 0 - 255 Boundry
            weightedSum = 255 if weightedSum > 255 else weightedSum
            weightedSum = 0 if weightedSum < 0 else weightedSum

            # Set the masked pixel to the new image
            newImg.set(x, y, (weightedSum, weightedSum, weightedSum))

    return newImg


# copyImg = MyImage.open("C:/Users/sudai/OneDrive - Habib University/University/Spring 22/Data Structures II (CS 201)/DataStructures-II/HW1/images/pool.jpg", False)
# copyImg.show()
# copyImg = remove_channel(copyImg)
# copyImg.show()

# copyImg = MyImage.open("C:/Users/sudai/OneDrive - Habib University/University/Spring 22/Data Structures II (CS 201)/DataStructures-II/HW1/images/hu-logo.png", False)
# copyImg.show()
# copyImg = rotations(copyImg)
# copyImg.show()

# img = MyImage.open("C:/Users/sudai/OneDrive - Habib University/University/Spring 22/Data Structures II (CS 201)/DataStructures-II/HW1/images/campus.jpeg", False)
# # img.show()
# img = apply_mask(img, "C:/Users/sudai/OneDrive - Habib University/University/Spring 22/Data Structures II (CS 201)/DataStructures-II/HW1/masks/mask-blur.txt", True)
# img.show()
