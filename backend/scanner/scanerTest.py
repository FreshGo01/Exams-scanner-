# =====================================================================================
# anser sheet scanner
# =====================================================================================

# import the necessary packages
from imutils.perspective import four_point_transform
import cv2
import argparse
from imutils import contours
import numpy as np
import imutils

image_path = 'test_image/LINE_ALBUM_25667_9.jpg'

image = cv2.imread(image_path)
image = imutils.resize(image, width=1600)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200, None, 3, False)
gradient = cv2.morphologyEx(
    edged, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))

# cv2.imshow('edged', edged)
# cv2.imshow('gradient', gradient)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# find contours in the edge map, then initialize
# the contour that corresponds to the document
cnts = cv2.findContours(gradient.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# draw the contours on the image
# cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)
# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

docCnt = None

# ensure that at least one contour was found
if len(cnts) > 0:
    # sort the contours according to their size in
    # descending order
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # loop over the sorted contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points,
        # then we can assume we have found the paper
        if len(approx) >= 4 and len(approx) <= 6:
            docCnt = approx
            break

# show the contour of the paper
# cv2.drawContours(image, [docCnt], -1, (0, 255, 0), 2)
# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# apply a four point perspective transform to both the
# original image and grayscale image to obtain a top-down
# birds eye view of the paper
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))

# show the original and scanned images
# cv2.imshow('Original', imutils.resize(image, height=650))
# cv2.imshow('Scanned', imutils.resize(warped, height=650))
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# apply Otsu's thresholding method to binarize the warped
# piece of paper
thresh = cv2.threshold(warped, 0, 255,
                       cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# cv2.imshow('thresh', thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# find contours in the thresholded image, then initialize
# the list of contours that correspond to questions
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# draw all contours
output = paper.copy()
cv2.drawContours(output, cnts, -1, (0, 255, 0), 2)
cv2.imshow('paper', output)
cv2.waitKey(0)

# find conner square marker for rotation (top-left, top-right, bottom-left) and marker infill is black
connerCnts = []
for c in cnts:
    # compute the bounding box of the contour, then use the
    # bounding box to derive the aspect ratio
    (x, y, w, h) = cv2.boundingRect(c)
    ratio = w / float(h)

    # contours area
    cntAr = cv2.contourArea(c)
    if (ratio >= 0.8 and ratio <= 1.1) and (cntAr > 1000):

        mask = np.zeros(thresh.shape, dtype='uint8')
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        filledArea = cv2.countNonZero(mask)

        # calculate the total number of non-zero pixels
        percentage_filled = (filledArea / float(cntAr)) * 100
        # print('percentage_filled: ', percentage_filled, 'ratio: ', ratio, 'cntAr: ', cntAr)

        if percentage_filled > 70:
            connerCnts.append(c)

# draw all conners
output = paper.copy()
cv2.drawContours(output, connerCnts, -1, (0, 255, 0), 2)
cv2.imshow('connerCnts', imutils.resize(output, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()

topZoneImage = warped.shape[0] // 3
# print('topZoneImage: ', topZoneImage)

topMaker = []
for c in connerCnts:
    (x, y, w, h) = cv2.boundingRect(c)
    if y < topZoneImage:
        topMaker.append(c)

print('topMaker: ', len(topMaker))
if len(topMaker) == 1:
    print('image is upside down')
    warped = cv2.rotate(warped, cv2.ROTATE_180)
    thresh = cv2.rotate(thresh, cv2.ROTATE_180)
    paper = cv2.rotate(paper, cv2.ROTATE_180)


# cv2.imshow('Scanned', imutils.resize(warped, height=650))
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# draw all contours
# output = paper.copy()
# cv2.drawContours(output, cnts, -1, (0, 255, 0), 2)
# cv2.imshow('paper', imutils.resize(output, height=1000))


all_rectangles = []

print('cnts: ', len(cnts))
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    contour_area = cv2.contourArea(c)

    if contour_area != 0:
        mask = np.zeros(thresh.shape, dtype="uint8")

        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)

        total = cv2.countNonZero(mask)

        percentage_filled = total / float(contour_area)

        if len(approx) >= 3 and len(approx) <= 6 and percentage_filled > 0.9 and cv2.contourArea(c) > 200:
            all_rectangles.append(approx)

# draw all contours
# output = paper.copy()
# cv2.drawContours(output, cnts, -1, (0, 255, 0), 2)
# cv2.imshow('paper', output)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# draw all rectangles
# output = paper.copy()
# cv2.drawContours(output, all_rectangles, -1, (0, 255, 0), 2)
# cv2.imshow('all_rectangles', imutils.resize(output, height=650))
# cv2.waitKey(0)
# cv2.destroyAllWindows()

print('all_rectangles: ', len(all_rectangles))

rectangles = []

for c in all_rectangles:
    x, y, w, h = cv2.boundingRect(c)

    ratio = w / float(h)

    area = cv2.contourArea(c)
    # print('ratio: ', ratio, 'area: ', area)

    if not (0.9 <= ratio <= 1.1) and area > 100:
        rectangles.append(c)

print('rectangles: ', len(rectangles))
# draw rectangles
output = paper.copy()
cv2.drawContours(output, rectangles, -1, (0, 255, 0), 2)
cv2.imshow('rectangles', imutils.resize(output, height=650))
cv2.waitKey(0)

horizontal_rectangles = []
vertical_rectangles = []

for c in rectangles:
    x, y, w, h = cv2.boundingRect(c)

    ratio = w / float(h)

    area = cv2.contourArea(c)

    if (area > 100) and (area < 500):
        if ratio > 1.1:
            # print('ratio: ', ratio, 'area: ', area, 'horizontal')
            horizontal_rectangles.append(c)
        elif ratio < 0.9:
            print('ratio: ', ratio, 'area: ', area, 'vertical')
            vertical_rectangles.append(c)

print('horizontal_rectangles: ', len(horizontal_rectangles))
print('vertical_rectangles: ', len(vertical_rectangles))


# draw horizontal rectangles
output = paper.copy()
cv2.drawContours(output, horizontal_rectangles, -1, (0, 255, 0), 2)
cv2.imshow('horizontal_rectangles', imutils.resize(output, height=650))

# draw vertical rectangles
output = paper.copy()
cv2.drawContours(output, vertical_rectangles, -1, (0, 255, 0), 2)
cv2.imshow('vertical_rectangles', imutils.resize(output, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()

# define zones to find the answer zones by vertical and horizontal rectangles
max_x = max([cv2.boundingRect(c)[0] for c in vertical_rectangles])
min_x = min([cv2.boundingRect(c)[0] for c in vertical_rectangles]) - 5

max_y = max([cv2.boundingRect(c)[1] for c in horizontal_rectangles]) + 20
min_y = min([cv2.boundingRect(c)[1] for c in horizontal_rectangles]) - 20
print('min_x: ', min_x, 'max_x: ', max_x, 'min_y: ', min_y, 'max_y: ', max_y)

# draw zones
output = paper.copy()
cv2.rectangle(output, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
cv2.imshow('zone', imutils.resize(output, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()

# find circles bubbles in the answer zones
bubbles = []
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    area = cv2.contourArea(c)

    if min_x < x < max_x and min_y < y < max_y:
        # print('area: ', area)
        if area > 10:
            bubbles.append(c)


# draw bubbles
output = paper.copy()
for i, bubble in enumerate(bubbles):
    cv2.drawContours(output, [bubble], -1, (0, 255, 0), 2)
    cv2.putText(output, str(
        i+1), (bubble[0][0][0], bubble[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

cv2.imshow('bubble', imutils.resize(output, height=1000))
cv2.waitKey(0)
cv2.destroyAllWindows()

print('bubbles: ', len(bubbles))


answers = {
    # '1': ['A', 'B'],
    # '2': ['C', 'D'],
}
# sort horizontal rectangles by y coordinate top to bottom
horizontal_rectangles = sorted(
    horizontal_rectangles, key=lambda x: x[0][0][1])

for (i, row) in enumerate(horizontal_rectangles):
    # print('i: ', i, 'row: ', row)
    # find the bubbles 5 bubbles that have the nearest y coordinate to the row
    bubbles_in_row = []
    for bubble in bubbles:
        if abs(bubble[0][0][1] - row[0][0][1]) < 20:
            bubbles_in_row.append(bubble)
    print(len(bubbles_in_row))

    # sort the bubbles by x coordinate
    bubbles_in_row = sorted(bubbles_in_row, key=lambda x: x[0][0][0])

    # draw bubbles in row and put the number of the row
    output = paper.copy()
    for j, bubble in enumerate(bubbles_in_row):
        cv2.drawContours(output, [bubble], -1, (0, 255, 0), 2)
        cv2.putText(output, str(
            j+1), (bubble[0][0][0], bubble[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(output, str(
        i+1), (row[0][0][0], row[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('bubbles_in_row', imutils.resize(output, height=1000))
    cv2.waitKey(0)

    # find the bubbles that has filled > 50% in the row
    bubbles_filled = []
    for (j, bubble) in enumerate(bubbles_in_row):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [bubble], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        percentage_filled = total / float(cv2.contourArea(bubble))
        if percentage_filled > 0.5:
            bubbles_filled.append(j)
    # print(bubbles_filled)
    # print('---------------------')

    # add the answer to the answers dictionary 0: A, 1: B, 2: C, 3: D, 4: E
    answers[str(i+1)] = []
    for j, bubble in enumerate(bubbles_in_row):
        if j in bubbles_filled:
            answers[str(i+1)].append(chr(65+j))


print(answers)
