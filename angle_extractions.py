from ultralytics import YOLO
import math
def getAngle(shoulder, elbow, wrist):
    dot_prod_x = (shoulder[0] - elbow[0])*(wrist[0] - elbow[0])
    dot_prod_y = (shoulder[1] - elbow[1])*(wrist[1] - elbow[1])

    mag1 = math.sqrt(((shoulder[0] - elbow[0])**2)+((shoulder[1] - elbow[1])**2))
    mag2 = math.sqrt(((wrist[0] - elbow[0])**2)+((wrist[1] - elbow[1])**2))

    dot_prod = dot_prod_x + dot_prod_y
    mag = mag1*mag2
    angle = (math.acos((dot_prod)/(mag)))*(180/math.pi)

    return angle

def getRatio(angle1, angle2): # used for calculating ratio of 2 consecutive frames, for baseline ratio comparison
    return (angle2/angle1)

def pullup_ecc_vs_conc(ratio, angle1, angle2): # calc angle diff for 1 arm, takes angle of 1 frame and 1 following frame, takes ratio of eccentric - if much faster then return false
    return (angle1/angle2) < (ratio*0.9)
    
def pullup_left_vs_right(leftAngle, rightAngle): # if one side's angle open is much different the return false
    return abs(leftAngle - rightAngle) <= 0.08 * max(leftAngle, rightAngle)

def find_eccentric(angles, streak=4):
    starts = []
    stops = []
    eccentric = False
    increase_count = 0
    decrease_count = 0

    for i in range(1, len(angles)):
        diff = angles[i] - angles[i - 1]

        if not eccentric:
            if diff > 0:
                increase_count += 1
                if increase_count >= streak:
                    starts.append(i - streak + 1)
                    eccentric = True
                    decrease_count = 0  # reset
            else:
                increase_count = 0
        else:
            if diff < 0:
                decrease_count += 1
                if decrease_count >= streak:
                    stops.append(i - streak + 1)
                    eccentric = False
                    increase_count = 0  # reset
            else:
                decrease_count = 0

    if eccentric:
        stops.append(len(angles) - 1)

    return starts, stops


def get_coords_pullups(results):
    nframes = len(results)
    X = [[] for _ in range(nframes)]
    Y = [[] for _ in range(nframes)]

    for idx, result in enumerate(results):
        keypoints = result.keypoints.data

        X[idx]=[keypoints[0, 5, 0].item(), keypoints[0, 6, 0].item(), keypoints[0, 7, 0].item(), keypoints[0, 8, 0].item(), keypoints[0, 9, 0].item(), keypoints[0, 10, 0].item()]
        Y[idx]=[keypoints[0, 5, 1].item(), keypoints[0, 6, 1].item(), keypoints[0, 7, 1].item(), keypoints[0, 8, 1].item(), keypoints[0, 9, 1].item(), keypoints[0, 10, 1].item()]

    return X, Y

def print_coords_pullups(results):
    for result in enumerate(results):
        keypoints = result.keypoints.data
        
        print("Left Shoulder")
        print(f"X: {keypoints[0, 5, 0]}, Y: {keypoints[0, 5, 1]}")
        print("Right Shoulder")
        print(f"X: {keypoints[0, 6, 0]}, Y: {keypoints[0, 6, 1]}")


        print("Left Elbow")
        print(f"X: {keypoints[0, 7, 0]}, Y: {keypoints[0, 7, 1]}")
        print("Right Elbow")
        print(f"X: {keypoints[0, 8, 0]}, Y: {keypoints[0, 8, 1]}")
        print("Left Wrist")
        print(f"X: {keypoints[0, 9, 0]}, Y: {keypoints[0, 9, 1]}")
        print("Right Wrist")
        print(f"X: {keypoints[0, 10, 0]}, Y: {keypoints[0, 10, 1]}")

def print_angles_pullups(results, X, Y):
    for i in range(len(results)):
        left_s1 = [X[i][0], Y[i][0]]
        left_e1 = [X[i][2], Y[i][2]]
        left_w1 = [X[i][4], Y[i][4]]

        right_s1 = [X[i][1], Y[i][1]]
        right_e1 = [X[i][3], Y[i][3]]
        right_w1 = [X[i][5], Y[i][5]]
        print(f"{i} - Left arm angle: {getAngle(left_s1, left_e1, left_w1)}")
        print(f"{i} - Right arm angle: {getAngle(right_s1, right_e1, right_w1)}")

def get_shoulders_coords(nframes, X, Y):
    leftShoulders = []
    rightShoulders = []

    for i in range(nframes):
        leftShoulders.append([X[i][0], Y[i][0]])
        rightShoulders.append([X[i][1], Y[i][1]])

    return leftShoulders, rightShoulders
    
def get_elbows_coords(nframes, X, Y):
    leftElbows = []
    rightElbows = []

    for i in range(nframes):
        leftElbows.append([X[i][2], Y[i][2]])
        rightElbows.append([X[i][3], Y[i][3]])

    return leftElbows, rightElbows

def get_wrists_coords(nframes, X, Y):
    leftWrists = []
    rightWrists = []

    for i in range(nframes):
        leftWrists.append([X[i][4], Y[i][4]])
        rightWrists.append([X[i][5], Y[i][5]])

    return leftWrists, rightWrists

def get_all_angles_pullups(nframes, shoulders, elbows, wrists): # use for both left or right
    angles = []
    for i in range(nframes):
        angles.append(getAngle(shoulders[i], elbows[i], wrists[i]))

    return angles



model = YOLO("yolo11n-pose.pt") # n/x, n = nano, x = more complex

results = model.predict(source="/Users/raymondwu/codingprograms/everythingelsenrn/python/dot/other/videos/pullups6.mp4", show=True)

#keypoints shape: [2, 17, 3], 3 --> [x,y,confidence]
#print(results[0].keypoints.shape) # 5-10, shoulder to elbow to wrist, left right 
#X/Y size [nframes, 6 (lrlrlr)(s --> e --> w)]

x, y = get_coords_pullups(results)
nframes = len(results)
leftShoulders, rightShoulders = get_shoulders_coords(nframes, x, y)
leftElbows, rightElbows = get_elbows_coords(nframes, x, y)
leftWrists, rightWrists = get_wrists_coords(nframes, x, y)
angles = get_all_angles_pullups(nframes, leftShoulders, leftElbows, leftWrists)
starts , stops = find_eccentric(angles)
