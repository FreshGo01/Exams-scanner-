import sqlite3
import time
from ultralytics import YOLO
import cv2
import scaner
import json

# Connect to the SQLite3 database
conn = sqlite3.connect('../database.sqlite')
cursor = conn.cursor()
model = YOLO("best.pt")

# Function to retrieve data from the database


def retrieve_data():
    cursor.execute('SELECT * FROM answer')
    rows = cursor.fetchall()
    return rows

# Function to update data when no answer sheet is found


def update_data_notfound(answer_id):
    message = "Not found answer sheet"
    cursor.execute('UPDATE answer SET status = ? WHERE id = ?',
                   (message, answer_id))
    conn.commit()

# Function to update data when an answer sheet is found and process the results


def update_data_found(answer_id, exam_id, filePath):
    message = ""

    correct_answer_str = get_exam_correct_answer(exam_id)
    try:
        correct_answer_list = json.loads(correct_answer_str)
    except json.JSONDecodeError:
        message = "Error decoding JSON"
        cursor.execute(
            'UPDATE answer SET status = ? WHERE id = ?', (message, answer_id))
        conn.commit()
        return

    try:
        answer = scaner.scan(filePath)
    except Exception as e:
        print(e)
        message = f"Error while scanning, Please delete the file and try again."
        cursor.execute(
            'UPDATE answer SET status = ? WHERE id = ?', (message, answer_id))
        conn.commit()
        return

    print(f"Correct answer: {correct_answer_list}")
    print(f"Answer: {answer}")

    # Convert the list of dictionaries to a single dictionary
    correct_answer_dict = {}
    for d in correct_answer_list:
        correct_answer_dict.update(d)

    # Add missing keys to correct_answer_dict
    for key in answer:
        if key not in correct_answer_dict:
            correct_answer_dict[key] = []

    # Calculate the score
    score = 0
    total_questions = len(correct_answer_dict)

    for key in answer:
        if answer[key] == correct_answer_dict[key]:
            score += 1

    # Update the database with the score and status
    message = f"Successfully graded answer sheet. Score: {
        score}/{total_questions}"
    cursor.execute('UPDATE answer SET status = ?, score = ? WHERE id = ?',
                   (message, score, answer_id))
    conn.commit()

# Function to get the correct answers for an exam


def get_exam_correct_answer(exam_id):
    cursor.execute('SELECT * FROM exam WHERE id = ?', (exam_id,))
    row = cursor.fetchone()
    return row[3]

# Function to detect answers in images and process accordingly


def detectAnswer(detections, answer_id, exam_id, filePath):
    if len(detections) > 0:
        print("Detections found:")
        update_data_found(answer_id, exam_id, filePath)
    else:
        print("No detections found.")
        update_data_notfound(answer_id)


# Continuous loop to process and update data every second
try:
    while True:
        data = retrieve_data()
        for row in data:
            if row[3] == "Waiting for grading":
                exam_id = row[5]
                answer_id = row[0]
                filePath = '../uploads/' + row[2]
                results = model(filePath, conf=0.9)
                detections = results[0].boxes if hasattr(
                    results[0], 'boxes') else []
                detectAnswer(detections, answer_id, exam_id, filePath)
        # break  # Remove this break if you want the loop to run continuously
        time.sleep(1)  # Wait for 1 second before repeating
except KeyboardInterrupt:
    print("Process interrupted by user.")
finally:
    conn.close()
