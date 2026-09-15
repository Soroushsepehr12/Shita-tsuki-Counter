import cv2
import mediapipe as mp
import numpy as np
import time
vidsource = 0 
COLOR_NEON_GREEN = (50, 255, 50)
COLOR_NEON_BLUE = (255, 200, 50)
COLOR_WARNING = (50, 50, 255)
state = {
    'l_ready': False,
    'r_ready': False,
    'last_punched_arm': None,
    'last_punch_time': 0.0,
    'last_seen_time': time.time(),
    }
def inguard(wrist, elbow, guard, vis):
    ty, by, lx, rx = guard
    return(
        vis
        and (ty < wrist.y < by)
        and (wrist.y < elbow.y)
        and (lx < wrist.x < rx)
    )
def inpunch(wrist, elbow, punch, angle, vis):
    ty, by, lx, rx = punch
    return(
        vis
        and(ty < wrist.y < by)
        and (lx < wrist.x < rx)
        and (80 < angle < 130)
        and (wrist.z < elbow.z)
    )
def calculateangle(a, b,c):
    v1 = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    v2 = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
    v1n = np.linalg.norm(v1)
    v2n =  np.linalg.norm(v2)
    if v1n == 0 or v2n == 0:
        return 0.0
    cosine_angle = np.dot(v1, v2) / (v1n * v2n)
    return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
def getzone(lsh, rsh, lh, rh, eyey,w, h):
    avgshy = (lsh.y + rsh.y) / 2.0
    avghy = (lh.y + rh.y) / 2.0
    span = avghy - avgshy
    guard = avgshy + span * 0.25
    punch = avgshy + span * 0.75
    shleft = min(lsh.x, rsh.x)
    shright = max(lsh.x, rsh.x)
    shoulderwidth = shright - shleft
    padx = shoulderwidth  * 0.15
    leftx = shleft - padx
    rightx = shright + padx
    guardn = (eyey, guard, leftx, rightx)
    punchn = (guard, punch, leftx, rightx)
    def pixels(zone):
        top, bottom, lx, rx = zone
        x1, y1 = int(lx * w), int(top*h)
        x2, y2 = int(rx* w), int(bottom * h)
        x1,y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        return (x1, y1, x2, y2)
    return punchn, pixels(punchn), guardn, pixels(guardn)
def checkp(state, side, isg, isp, currtime):
    readyk = 'l_ready' if side == 'LEFT' else 'r_ready'
    if isg:
        state[readyk] = True
    tslp = currtime - state['last_punch_time']
    if tslp <= 0.4:
        return False
    isr = state[readyk]
    diffarm = state['last_punched_arm'] != side
    if isp and isr and diffarm:
        state[readyk] = False
        state['last_punched_arm'] = side
        state['last_punch_time'] = currtime
        return True
    return False
def main():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    cap = cv2.VideoCapture(vidsource)
    punch_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        currtime = time.time()
        hitf = (currtime -  state['last_punch_time']) < 0.2
        overlay = frame.copy()
       
        darkbg = (30, 30, 30)
        results = pose.process(rgb)
        if results.pose_landmarks:
            h, w, _ = frame.shape
            lm = results.pose_landmarks.landmark
            l_sh, l_el, l_wr = lm[11], lm[13], lm[15]
            r_sh, r_el, r_wr = lm[12], lm[14], lm[16]
            l_hip, r_hip = lm[23], lm[24]
            l_eye, r_eye = lm[2], lm[5]
            eye_y = (l_eye.y + r_eye.y) / 2.0
            cv2.line(frame, (int(l_sh.x*w), int(l_sh.y*h)), (int(l_el.x * w),int(l_el.y*h)), (200, 200, 200), 2)
            cv2.line(frame, (int(l_el.x*w), int(l_el.y*h)), (int(l_wr.x * w),int(l_wr.y*h)), (200, 200, 200), 2)
            cv2.line(frame, (int(r_sh.x*w), int(r_sh.y*h)), (int(r_el.x * w),int(r_el.y*h)), (200, 200, 200), 2)
            cv2.line(frame, (int(r_el.x*w), int(r_el.y*h)), (int(r_wr.x * w),int(r_wr.y*h)), (200, 200, 200), 2)
            
            punchn, px, guardn, gx = getzone(l_sh, r_sh, l_hip, r_hip, eye_y, w, h)
            gx1, gy1, gx2, gy2 = gx
            px1, py1, px2, py2 = px
            cv2.rectangle(frame, (gx1, gy1), (gx2, gy2), (255,0,0), 3)
            anglel = calculateangle(l_wr, l_el, l_sh)
            angler = calculateangle(r_wr, r_el, r_sh)
            cv2.putText(frame, "GUARD ZONE", (gx1, gy1 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1, cv2.LINE_AA)
            guardl = inguard(l_wr, l_el, guardn, True)
            guardr = inguard(r_wr, r_el, guardn, True)
            punchl = inpunch(l_wr, l_el, punchn, anglel, True)
            punchr = inpunch(r_wr, r_el, punchn, angler, True)
            l_col = COLOR_NEON_GREEN if guardl else (COLOR_NEON_BLUE if punchl else COLOR_WARNING)
            r_col = COLOR_NEON_GREEN if guardr else (COLOR_NEON_BLUE if punchr else COLOR_WARNING)
            cv2.circle(frame, (int(l_wr.x*w), int(l_wr.y*h)), 6, l_col, -1)
            cv2.circle(frame, (int(r_wr.x*w), int(r_wr.y*h)), 6, r_col, -1)
            zonec = COLOR_NEON_GREEN if hitf else COLOR_NEON_BLUE
            cv2.rectangle(overlay, (px1, py1), (px2, py2), zonec,-1)
            cv2.rectangle(frame, (px1, py1), (px2, py2), zonec, 3)
            cv2.putText(frame, "PUNCH ZONE", (px1, py1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1, cv2.LINE_AA)
            alpha = 0.3 if not hitf else 0.6
            cv2.addWeighted(overlay, alpha, frame,1 - alpha, 0, frame)
            if state['l_ready']:
                lx, ly = int(l_wr.x*w), int(l_wr.y*h)
                cv2.circle(frame, (lx, ly), 22, COLOR_NEON_GREEN, 3)
                cv2.putText(frame, "READY", (lx -25, ly - 28), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1, cv2.LINE_AA)
            if state['r_ready']:
                rx, ry = int(r_wr.x*w), int(r_wr.y*h)
                cv2.circle(frame, (rx, ry), 22, COLOR_NEON_GREEN, 3)
                cv2.putText(frame, "READY", (rx -25, ry - 28), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1, cv2.LINE_AA)
            if checkp(state, 'LEFT', guardl, punchl, currtime):
                punch_count += 1
            elif checkp(state, 'RIGHT', guardr, punchr, currtime):
                punch_count += 1
            cv2.rectangle(frame, (10, 20), (220, 80), darkbg, -1)
            cv2.putText(frame, "PUNCHES", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, str(punch_count), (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1, cv2.LINE_AA)
        cv2.imshow("Mediapipe counter", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
main()