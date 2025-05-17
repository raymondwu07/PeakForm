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
    print(average, count)
    return (average/count)

def pullup_ecc_vs_con(con_ratio, ecc_ratio): # checks difference between concentric and eccentric ratio - if too eccentric changes too fast then return false
    return ecc_ratio > 0.96*con_ratio
    
def pullup_left_vs_right(leftAngle, rightAngle): # if one side's angle open is much different the return false
    return abs(leftAngle - rightAngle) <= 0.09 * max(leftAngle, rightAngle)

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

def check_ratio(angles):
    starts, stops = find_eccentric(angles)
    starts_ecc, stops_ecc = starts, stops
    starts_con, stops_con = [0], []
    for i in range(len(starts)):
        starts_con.append(stops_ecc[i])
        stops_con.append(starts_ecc[i])
    del starts_con[-1]
        

    print(starts_ecc, len(starts_ecc), stops_ecc, len(stops_ecc))
    ecc_ratio = get_average_ratio(start=starts_ecc, stop=stops_ecc, angles=angles)
    print(starts_con, len(starts_con), stops_con, len(stops_con))
    con_ratio = get_average_ratio(start=starts_con, stop=stops_con, angles=angles)

    return pullup_ecc_vs_con(con_ratio, ecc_ratio)







model = YOLO("yolo11n-pose.pt") # n/x, n = nano, x = more complex

results = model.predict(source="/Users/raymondwu/codingprograms/everythingelsenrn/python/dot/other/videos/pullups8.MOV", show=True)

#keypoints shape: [2, 17, 3], 3 --> [x,y,confidence]
#print(results[0].keypoints.shape) # 5-10, shoulder to elbow to wrist, left right 
#X/Y size [nframes, 6 (lrlrlr)(s --> e --> w)]

x, y = get_coords_pullups(results)
nframes = len(results)
leftShoulders, rightShoulders = get_shoulders_coords(nframes, x, y)
leftElbows, rightElbows = get_elbows_coords(nframes, x, y)
leftWrists, rightWrists = get_wrists_coords(nframes, x, y)
left_angles = get_all_angles_pullups(nframes, leftShoulders, leftElbows, leftWrists)
right_angles = get_all_angles_pullups(nframes, rightShoulders, rightElbows, rightWrists)

print(check_ratio(left_angles))