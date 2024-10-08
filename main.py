# -*- coding: utf-8 -*-
"""Copy_of_Copy_of_hand_gesture.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sIjzfYLPXJ_b_qhy2a3kXM8xaN3k7Rtq
"""

!pip install mediapipe

import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import mediapipe as mp

# from google.colab import drive
# drive.mount('/content/drive')

# import zipfile
# # from google.colab import drive

# # drive.mount('/content/drive/')

# zip_ref = zipfile.ZipFile("/content/drive/MyDrive/hand gesture dataset1/MP_DATA-75.zip", 'r')
# zip_ref.extractall("/tmp")
# zip_ref.close()



mp_holistic=mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def mediapipe_detection(image,model):
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    image.flags.writeable=False
    results=model.process(image)
    image.flags.writeable=True
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    return image,results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION) # Draw face connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS) # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw right hand connections

def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                             )
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                             )
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             )
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             )

cap=cv2.VideoCapture(0) #laptop webcam
# cap=cv2.VideoCapture(1) #mobile
# cap=cv2.VideoCapture(2) #mobile2
with mp_holistic.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret,frame=cap.read()

        image,results=mediapipe_detection(frame,holistic)

        draw_styled_landmarks(image,results)
        cv2.imshow('OpenCV Feed',image)
        if cv2.waitKey(10) & 0xFF == ord('q'or'Q'):
                break
    cap.release()
    cv2.destroyAllWindows()

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

"""#### DATA_PATH=os.path.join("MP_DATA")

"""

actions=np.array(['Bye','Hello','How Are You','I Love You',"I'm Fine",'No','Yes',])
no_sequences = 75 #change according to your sequence
sequence_length = 30

7*75*30

15750*1662

# for action in actions:
#     for sequence in range(no_sequences): #change according to your sequence
#         try:
#             os.makedirs(os.path.join(DATA_PATH,action,str(sequence)))
#         except:
#                 pass

# cap=cv2.VideoCapture(2) #laptop webcam
# # cap=cv2.VideoCapture(1) #mobile

# y=['Hello','Yes','No' ,'I Love You','Bye','How are you',"I'm fine"]
# i=0

# with mp_holistic.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5) as holistic:
#     for action in actions:
#         cv2.putText(image,f"please change your action to ",(75,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3,cv2.LINE_AA)
#         cv2.putText(image,f"{action} ",(125,250),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),5,cv2.LINE_AA)
#         cv2.imshow('OpenCV Feed', image)
#         cv2.waitKey(5000)
#         for sequence in range(15,no_sequences): #change according to u

#             for frame_num in range(sequence_length):

#                     ret,frame=cap.read()
#                     image,results=mediapipe_detection(frame,holistic)
#                     draw_styled_landmarks(image,results)

#                     if frame_num==0:
#                             cv2.putText(image,"Please reset your pose",(100,200),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
#                             cv2.putText(image,f"the frame no is {frame_num} the sequence is {sequence+7-no_sequences}",(2,20),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),1,cv2.LINE_AA)
#                             cv2.putText(image,f"action : {action}",(75,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
#                             cv2.imshow('OpenCV Feed', image)
#                             cv2.waitKey(2500)
#                     else:

#                         cv2.putText(image,f"the frame no is {frame_num} the sequence is {sequence+7-no_sequences}",(2,20),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),1,cv2.LINE_AA)
#                         cv2.putText(image,f"action : {action}",(75,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
#                         cv2.imshow('OpenCV Feed', image)

#                     keypoints=extract_keypoints(results)
#                     npy_path=os.path.join(DATA_PATH,action,str(sequence),str(frame_num))
#                     np.save(npy_path,keypoints)

#                     if cv2.waitKey(10) & 0xFF == ord('q'or'Q'):
#                             break
#     cap.release()
#     cv2.destroyAllWindows()

# cap.release()
 #cv2.destroyAllWindows()

from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

label_map={label:num for num,label in enumerate(actions)}

y=enumerate(actions)
for label,num in y:
    print(num,label)

label_map={label:num for num,label in enumerate(actions)}

print(label_map)

sequences, labels = [], []
for action in actions:
    for sequence in range(0,no_sequences):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])
    # for sequence in range(45,75):
    #     for frame_num in range(sequence_length):
    #         res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
    #         window.append(res)
    #     sequences.append(window)
    #     labels.append(label_map[action])

np.array(sequences).shape

np.array(labels).shape

X = np.array(sequences)

X.shape

y = to_categorical(labels).astype(int)

y

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.5)

y_test.shape

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense,Dropout,Flatten
from tensorflow.keras.callbacks import TensorBoard

log_dir=os.path.join('Logs')
tb_callback=TensorBoard(log_dir=log_dir)

print(actions.shape[0])

model=Sequential()
model.add(LSTM(64,return_sequences=True,activation="relu",input_shape=(30,1662)))
model.add(LSTM(128,return_sequences=True,activation="relu"))
model.add(LSTM(64,return_sequences=False,activation="relu"))
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(actions.shape[0],activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# model.fit(X_train,y_train,epochs=200,callbacks=[tb_callback])

model.summary()

res = model.predict(X_test)

actions[np.argmax(res[2])]

actions[np.argmax(y_test[4])]

model.save("handGes2.h5")

model.load_weights('handGes1.h5')

from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
yhat = model.predict(X_test)
ytrue = np.argmax(y_test, axis=1).tolist()
yhat = np.argmax(yhat, axis=1).tolist()
multilabel_confusion_matrix(ytrue, yhat)

accuracy_score(ytrue, yhat)

colors = [(245,117,16), (117,245,16), (16,117,245)]
def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

    return output_frame

# plt.figure(figsize=(18,18))
# plt.imshow(prob_viz(res, actions, image, colors))

# 1. New detection variables
sequence = []
sentence = []
threshold = 0.8

cap = cv2.VideoCapture(0)
# Set mediapipe model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():

        # Read feed
        ret, frame = cap.read()

        # Make detections
        image, results = mediapipe_detection(frame, holistic)
        print(results)

        # Draw landmarks
        draw_styled_landmarks(image, results)

        # 2. Prediction logic
        keypoints = extract_keypoints(results)
#         sequence.insert(0,keypoints)
#         sequence = sequence[:30]
        sequence.append(keypoints)
        sequence = sequence[-30:]

        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            print(actions[np.argmax(res)])


        #3. Viz logic
            if res[np.argmax(res)] > threshold:
                if len(sentence) > 0:
                    if actions[np.argmax(res)] != sentence[-1]:
                        sentence.append(actions[np.argmax(res)])
                else:
                    sentence.append(actions[np.argmax(res)])

            if len(sentence) > 5:
                sentence = sentence[-5:]

            # Viz probabilities
            image = prob_viz(res, actions, image, colors)

        cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
        cv2.putText(image, ' '.join(sentence), (3,30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Show to screen
        cv2.imshow('OpenCV Feed', image)

        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



