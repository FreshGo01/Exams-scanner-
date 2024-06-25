# =====================================================================================
# anser sheet scanner conclusion to use
# =====================================================================================

# import the necessary packages
from imutils.perspective import four_point_transform
import cv2
import argparse
from imutils import contours
import numpy as np
import imutils
import traceback


def load_and_preprocess_image(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(
                f"Cannot find or open the file: {image_path}")
        image = imutils.resize(image, width=1600)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)
        gradient = cv2.morphologyEx(
            edged, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
        return image, gray, gradient
    except Exception as e:
        raise RuntimeError(f"Error in load_and_preprocess_image: {str(e)}")


def find_document_contour(gradient):
    try:
        cnts = cv2.findContours(
            gradient.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        docCnt = None
        if len(cnts) > 0:
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if len(approx) >= 4 and len(approx) <= 6:
                    docCnt = approx
                    break
        if docCnt is None:
            raise ValueError("Document contour not found")
        return docCnt
    except Exception as e:
        raise RuntimeError(f"Error in find_document_contour: {str(e)}")


def get_top_down_view(image, gray, docCnt):
    try:
        paper = four_point_transform(image, docCnt.reshape(4, 2))
        warped = four_point_transform(gray, docCnt.reshape(4, 2))
        return paper, warped
    except Exception as e:
        raise RuntimeError(f"Error in get_top_down_view: {str(e)}")


def extract_conner_markers(cnts, thresh):
    try:
        connerCnts = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ratio = w / float(h)
            cntAr = cv2.contourArea(c)
            if (ratio >= 0.9 and ratio <= 1.1) and (cntAr > 1000):
                mask = np.zeros(thresh.shape, dtype='uint8')
                cv2.drawContours(mask, [c], -1, 255, -1)
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                filledArea = cv2.countNonZero(mask)
                percentage_filled = (filledArea / float(cntAr)) * 100
                if percentage_filled > 70:
                    connerCnts.append(c)
        # print('connerCnts:', len(connerCnts))
        return connerCnts
    except Exception as e:
        raise RuntimeError(f"Error in extract_conner_markers: {str(e)}")


def detect_rotation(warped, connerCnts):
    try:
        topZoneImage = warped.shape[0] // 3
        topMaker = [c for c in connerCnts if cv2.boundingRect(c)[
            1] < topZoneImage]
        # print('topMaker:', len(topMaker))
        if len(topMaker) == 1:
            return True
        return False
    except Exception as e:
        raise RuntimeError(f"Error in detect_rotation: {str(e)}")


def find_all_rectangles(cnts, thresh):
    try:
        all_rectangles = []
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
        # print('all_rectangles:', len(all_rectangles))
        return all_rectangles
    except Exception as e:
        raise RuntimeError(f"Error in find_all_rectangles: {str(e)}")


def find_rectangles(all_rectangles):
    try:
        rectangles = []
        for c in all_rectangles:
            x, y, w, h = cv2.boundingRect(c)

            ratio = w / float(h)

            area = cv2.contourArea(c)

            if not (0.9 <= ratio <= 1.1) and area > 100:
                rectangles.append(c)
        # print('rectangles:', len(rectangles))
        return rectangles
    except Exception as e:
        raise RuntimeError(f"Error in find_rectangles: {str(e)}")


def find_horizontal_rectangles_and_vertical_rectangles(rectangles):
    try:
        horizontal_rectangles = []
        vertical_rectangles = []
        for c in rectangles:
            x, y, w, h = cv2.boundingRect(c)

            ratio = w / float(h)

            area = cv2.contourArea(c)

            if ratio > 1.1 and area > 100 and area < 500:
                # print('ratio: ', ratio, 'area: ', area, 'horizontal')
                horizontal_rectangles.append(c)
            elif ratio < 0.9 and area > 100 and area < 500:
                # print('ratio: ', ratio, 'area: ', area, 'vertical')
                vertical_rectangles.append(c)
        # print('horizontal_rectangles:', len(horizontal_rectangles))
        # print('vertical_rectangles:', len(vertical_rectangles))
        return horizontal_rectangles, vertical_rectangles
    except Exception as e:
        raise RuntimeError(
            f"Error in find_horizontal_rectangles_and_vertical_rectangles: {str(e)}")


def find_bubbles_in_zone(cnts, min_x, max_x, min_y, max_y):
    try:
        bubbles = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            area = cv2.contourArea(c)

            if min_x < x < max_x and min_y < y < max_y:
                # print('area: ', area)
                if area > 10:
                    bubbles.append(c)
        # print('bubbles:', len(bubbles))
        return bubbles
    except Exception as e:
        raise RuntimeError(f"Error in find_bubbles_in_zone: {str(e)}")


def process_bubbles(bubbles, thresh, horizontal_rectangles, paper):
    try:
        answers = {}
        horizontal_rectangles = sorted(
            horizontal_rectangles, key=lambda x: x[0][0][1])
        for (i, row) in enumerate(horizontal_rectangles):
            # print('i: ', i, 'row: ', row)
            # find the bubbles 5 bubbles that have the nearest y coordinate to the row
            bubbles_in_row = []
            for bubble in bubbles:
                if abs(bubble[0][0][1] - row[0][0][1]) < 20:
                    bubbles_in_row.append(bubble)
            # print(len(bubbles_in_row))

            # sort the bubbles by x coordinate
            bubbles_in_row = sorted(bubbles_in_row, key=lambda x: x[0][0][0])

            # draw bubbles in row and put the number of the row
            # output = paper.copy()
            # for j, bubble in enumerate(bubbles_in_row):
            #     cv2.drawContours(output, [bubble], -1, (0, 255, 0), 2)
            #     cv2.putText(output, str(
            #         j+1), (bubble[0][0][0], bubble[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # cv2.putText(output, str(
            #     i+1), (row[0][0][0], row[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # cv2.imshow('bubbles_in_row', imutils.resize(output, height=1000))
            # cv2.waitKey(0)

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
            # add the answer to the answers dictionary 0: A, 1: B, 2: C, 3: D, 4: E
            answers[str(i+1)] = []
            for j, bubble in enumerate(bubbles_in_row):
                if j in bubbles_filled:
                    answers[str(i+1)].append(chr(65+j))
        return answers
    except Exception as e:
        raise RuntimeError(f"Error in process_bubbles: {str(e)}")


def scan(image_path):
    try:
        image, gray, gradient = load_and_preprocess_image(image_path)
        docCnt = find_document_contour(gradient)
        paper, warped = get_top_down_view(image, gray, docCnt)
        thresh = cv2.threshold(
            warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        connerCnts = extract_conner_markers(cnts, thresh)

        if detect_rotation(warped, connerCnts):
            warped = cv2.rotate(warped, cv2.ROTATE_180)
            thresh = cv2.rotate(thresh, cv2.ROTATE_180)
            paper = cv2.rotate(paper, cv2.ROTATE_180)

        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        all_rectangles = find_all_rectangles(cnts, thresh)
        rectangles = find_rectangles(all_rectangles)
        horizontal_rectangles, vertical_rectangles = find_horizontal_rectangles_and_vertical_rectangles(
            rectangles)
        if len(horizontal_rectangles) != 25 or len(vertical_rectangles) != 5:
            raise ValueError(
                f"Found {len(horizontal_rectangles)} horizontal rectangles and {len(vertical_rectangles)} vertical rectangles, please check the image again.")

        # # draw horizontal rectangles
        # output = paper.copy()
        # cv2.drawContours(output, horizontal_rectangles, -1, (0, 255, 0), 2)
        # cv2.imshow('horizontal_rectangles', imutils.resize(output, height=650))

        # draw vertical rectangles
        # output = paper.copy()
        # cv2.drawContours(output, vertical_rectangles, -1, (0, 255, 0), 2)
        # cv2.imshow('vertical_rectangles', imutils.resize(output, height=650))

        max_x = max([cv2.boundingRect(c)[0] for c in vertical_rectangles])
        min_x = min([cv2.boundingRect(c)[0] for c in vertical_rectangles]) - 5
        max_y = max([cv2.boundingRect(c)[1]
                    for c in horizontal_rectangles]) + 20
        min_y = min([cv2.boundingRect(c)[1]
                    for c in horizontal_rectangles]) - 20
        # print('min_x: ', min_x, 'max_x: ', max_x,
        #       'min_y: ', min_y, 'max_y: ', max_y)

        # draw zones
        # output = paper.copy()
        # cv2.rectangle(output, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
        # cv2.imshow('zone', imutils.resize(output, height=650))

        # print('cnts:', len(cnts))
        bubbles = find_bubbles_in_zone(cnts, min_x, max_x, min_y, max_y)
        if len(bubbles) != 125:
            raise ValueError(
                f"Found {len(bubbles)} bubbles, please check the image again.")

        # draw bubbles
        # output = paper.copy()
        # for i, bubble in enumerate(bubbles):
        #     cv2.drawContours(output, [bubble], -1, (0, 255, 0), 2)
        #     cv2.putText(output, str(
        #         i+1), (bubble[0][0][0], bubble[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # cv2.imshow('bubble', imutils.resize(output, height=1000))

        answers = process_bubbles(
            bubbles, thresh, horizontal_rectangles, paper)

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # validate the answers that correct format 1 question must max 5 answers
        for key in answers:
            if len(answers[key]) > 5:
                raise ValueError(
                    "Found more than 5 answers, please check the image again.")

        return (answers)

    except Exception as e:
        raise RuntimeError(f"Error: {str(e)}")
