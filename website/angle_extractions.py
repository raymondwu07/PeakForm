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

def get_average_ratio(start, stop, angles): # calculates average ratio across all reps for either concentric/eccentric movement, for baseline ratio comparison
    average = 0
    count = 0
    for j in range(len(start)):
        for i in range(start[j], stop[j], 1):
            average += (angles[i]/angles[i+1])
            count+=1
    return (average/count)

def pullup_ecc_vs_con(con_ratio, ecc_ratio): # checks difference between concentric and eccentric ratio - if too eccentric changes too fast then return false
    return ecc_ratio > 0.96*con_ratio
    
def pullup_left_vs_right(leftAngle, rightAngle): # if one side's angle open is much different the return false
    return abs(leftAngle - rightAngle) <= 0.09 * max(leftAngle, rightAngle)

def squat_align_check(nose, shoulder, ankle):
    if nose[0] < ankle[0]:
        angle = getAngle(shoulder, ankle, [0, ankle[1]]) # 3rd coord is the corner of screen, at height of ankle
    else: # else, do opposite side, facing left/right etc
        angle = getAngle(shoulder, ankle, [9999, ankle[1]]) # 3rd coord is the corner of screen, at height of ankle

    if angle > 105 or angle < 75:
        return False
    else:
        return True

def bentover_check(shoulder, hip, ankle): 
    return getAngle(shoulder, hip, ankle) > 40

def kneecave_check(left_knee, right_knee, left_ankle, right_ankle): # if knee distance is closer than ankle, then knee caving must be occuring (MUST BE FRONT ON)
    return abs(left_knee[0]-right_knee[0]) > abs(left_ankle[0]-right_ankle[0]) # abs to allow right left error


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

def get_coords_squat(results): # squat coords - lrlr... shoulder, hip, knee, ankle, nose
    nframes = len(results)
    X = [[] for _ in range(nframes)]
    Y = [[] for _ in range(nframes)]

    for idx, result in enumerate(results):
        keypoints = result.keypoints.data

        X[idx]=[keypoints[0, 5, 0].item(), keypoints[0, 6, 0].item(), keypoints[0, 11, 0].item(), keypoints[0, 12, 0].item(), keypoints[0, 13, 0].item(), keypoints[0, 14, 0].item(), keypoints[0, 15, 0].item(), keypoints[0, 16, 0].item(), keypoints[0, 0, 0].item()]
        Y[idx]=[keypoints[0, 5, 1].item(), keypoints[0, 6, 1].item(), keypoints[0, 11, 1].item(), keypoints[0, 12, 1].item(), keypoints[0, 13, 1].item(), keypoints[0, 14, 1].item(), keypoints[0, 15, 1].item(), keypoints[0, 16, 1].item(), keypoints[0, 0, 1].item()]

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

def get_hip_coords(nframes, X, Y): 
    leftHips = []
    rightHips = []

    for i in range(nframes):
        leftHips.append([X[i][2], Y[i][2]]) 
        rightHips.append([X[i][3], Y[i][3]])

    return leftHips, rightHips

def get_knee_coords(nframes, X, Y): 
    leftKnees = []
    rightKnees = []

    for i in range(nframes):
        leftKnees.append([X[i][4], Y[i][4]]) 
        rightKnees.append([X[i][5], Y[i][5]])

    return leftKnees, rightKnees

def get_ankle_coords(nframes, X, Y): 
    leftAnkles = []
    rightAnkles = []

    for i in range(nframes):
        leftAnkles.append([X[i][6], Y[i][6]]) 
        rightAnkles.append([X[i][7], Y[i][7]])

    return leftAnkles, rightAnkles

def get_nose_coords(nframes, X, Y): 
    noses = []

    for i in range(nframes):
        noses.append([X[i][8], Y[i][8]]) 

    return noses

def get_all_angles(nframes, shoulders, elbows, wrists): # use for both left or right
    angles = []
    for i in range(nframes):
        angles.append(getAngle(shoulders[i], elbows[i], wrists[i]))

    return angles

def check_ratio(angles):
    starts, stops = find_eccentric(angles)
    starts_ecc, stops_ecc = starts, stops
    starts_con, stops_con = [0], []
    for i in range(len(starts)):
        starts_con.append(stops_ecc[i])
        stops_con.append(starts_ecc[i])
    del starts_con[-1]
        


    ecc_ratio = get_average_ratio(start=starts_ecc, stop=stops_ecc, angles=angles)
    con_ratio = get_average_ratio(start=starts_con, stop=stops_con, angles=angles)

    return pullup_ecc_vs_con(con_ratio, ecc_ratio)

def pullup_left_vs_right_all(left_angles, right_angles): # ASSUMING STRAIGHT ON VIEW
    for i in range(len(left_angles)):
        if not pullup_left_vs_right(left_angles[i], right_angles[i]):
            return False


model = YOLO("yolo11x-pose.pt") # n/x, n = nano, x = more complex

results = model.predict(source="/Users/raymondwu/codingprograms/trainer/project-input/Barbell Squat Side View.mp4", show=True, save=True)

"""#keypoints shape: [2, 17, 3], 3 --> [x,y,confidence]
#print(results[0].keypoints.shape) # 5-10, shoulder to elbow to wrist, left right 
#X/Y size [nframes, 6 (lrlrlr)(s --> e --> w)]

x, y = get_coords_pullups(results)
nframes = len(results)
leftShoulders, rightShoulders = get_shoulders_coords(nframes, x, y)
leftElbows, rightElbows = get_elbows_coords(nframes, x, y)
leftWrists, rightWrists = get_wrists_coords(nframes, x, y)
left_angles = get_all_angles(nframes, leftShoulders, leftElbows, leftWrists)
right_angles = get_all_angles(nframes, rightShoulders, rightElbows, rightWrists)

print(check_ratio(left_angles))
print(pullup_left_vs_right_all(left_angles, right_angles)) """

squat_x, squat_y = get_coords_squat(results)

