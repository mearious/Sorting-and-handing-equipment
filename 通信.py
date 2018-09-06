
# Main Module Example
#
# When your OpenMV Cam is disconnected from your computer it will either run the
# main.py script on the SD card (if attached) or the main.py script on
# your OpenMV Cam's internal flash drive.

from pyb import Pin, Timer, udelay, LED
import sensor, image, time,math

def led_control(name,stime):
    #亮灯和间隔时间
    led = LED(name) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.
    led.on()
    time.sleep(stime)
    led.off()
    time.sleep(stime)

def pwm_control(A1,A2,B1,B2,C1,C2):
    PWM1.pulse_width_percent(A1)
    PWM2.pulse_width_percent(A2)
    PWM3.pulse_width_percent(B1)
    PWM4.pulse_width_percent(B2)
    PWM5.pulse_width_percent(C1)
    PWM6.pulse_width_percent(C2)
# 为了使色彩追踪效果真的很好，你应该在一个非常受控制的照明环境中。
green_threshold     = (30, 79, -59, -18, -128, 127)
black_threshold     = (0, 41, -17, 16, -25, 19)
yellow_threshold    = (74, 88, -5, 14, 34, 127)
pingpang_threshold  = (67, 78, -3, 23, 16, 64)
#设置绿色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,
# maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。如果是灰度图，则只需
#设置（min, max）两个数字即可。

# You may need to tweak the above settings for tracking green things...
# Select an area in the Framebuffer to copy the color settings.
tim1 = Timer(2, freq=1000) # Frequency in Hz
tim2 = Timer(4, freq=1000) # Frequency in Hz
# tim3 = Timer(1, freq=1000) # Frequency in Hz
# 生成1kHZ方波，使用TIM4，channels 1 and 2分别是 50% 和 75% 占空比。

PWM1 = tim1.channel(3, Timer.PWM, pin=Pin("P4"))
PWM2 = tim1.channel(4, Timer.PWM, pin=Pin("P5"))
PWM3 = tim1.channel(1, Timer.PWM, pin=Pin("P6"))
PWM4 = tim2.channel(1, Timer.PWM, pin=Pin("P7"))
PWM5 = tim2.channel(2, Timer.PWM, pin=Pin("P8"))
PWM6 = tim2.channel(3, Timer.PWM, pin=Pin("P9"))



sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
#关闭白平衡。白平衡是默认开启的，在颜色识别中，需要关闭白平衡。
clock = time.clock() # Tracks FPS.

pin0 = Pin('P0', Pin.IN, Pin.PULL_UP)
pin1 = Pin('P1', Pin.IN, Pin.PULL_UP)

old_angle=0

while(True):
  while(True):
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]
    ratio=0
    K=0
    flag=0
    flag3=0
    Most=1.4   ########角度最小
    Least=1.6 ########角度最大
    X=120      ########第一次进的X
    led_control(1,0)
    led_control(2,0)

##########################################复位

    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.03)
    blobs = img.find_blobs([green_threshold],pixels_threshold =80,area_threshold=80)
    if blobs:
    #如果找到了目标颜色
        for b in blobs:
        #迭代找到的目标颜色区域
            # Draw a rect around the blob.
            img.draw_rectangle(b[0:4]) # rect
            #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            #在目标颜色区域的中心画十字形标记
            print(b[5], b[6])
            #输出目标物体中心坐标
            #print(b[7])
            A.append(b[5])
            B.append(b[6])
            C.append(b[7])
    if len(A)<1:
       # PWM1.pulse_width_percent(60)
       # PWM2.pulse_width_percent(0)
        break
    if len(A)>1:
        break

    if C[0]<Most:
       ratio=30
    if C[0]>Least:
       ratio=-30

    if B[0]<215:
        pwm_control(0,0,75,0,0,70)

    elif A[0]>20:
        pwm_control(100,0,0,0,0,0)
    else:
        pwm_control(0,0,0,0,0,0)
###############################################################

    if pin0.value()==0:
        K=K+1
    else:
        K=K

    while(pin0.value()==0):
        pass
###############################第一题
    while(K==1):
        led_control(1,50)
        while(pin1.value()==0):
            while(pin1.value()):
                led_control(1,0)
                pwm_control(0,0,0,82,95,0)
                time.sleep(3250)
                pwm_control(0,100,0,0,0,0)
                time.sleep(6800)
                pwm_control(100,0,0,0,0,0)
                time.sleep(2000)
                pwm_control(0,0,80,0,0,75)
                time.sleep(1600)
                pwm_control(0,100,0,0,0,0)
                time.sleep(3500)
                pwm_control(0,0,0,75,80,0)
                time.sleep(1000)
                pwm_control(0,0,80,0,0,75)
                time.sleep(1000)
                pwm_control(100,0,0,0,0,0)
                time.sleep(1500)
                pwm_control(0,0,0,75,80,0)
                time.sleep(1500)
                pwm_control(0,100,0,0,0,0)
                time.sleep(2800)
                pwm_control(0,0,0,75,80,0)
                time.sleep(700)
                pwm_control(0,0,0,0,0,0)
                break
                if pin0.value()==0 or pin1.value()==0:
                    break
                else:
                    pass
        if pin0.value()==0:
            K=K+1
        else:
            K=K
        while(pin0.value()==0):
            pass

##############################第二题
    while(K==2):
        led_control(2,50)
        while(pin1.value()==0):
            while(pin1.value()):
                X=68
                while(flag==0):####第一步：向下后向右     57 68    106 64    103  157    290
                    clock.tick() # Track elapsed milliseconds between snapshots().
                    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.03)
                    blobs = img.find_blobs([green_threshold],pixels_threshold =80,area_threshold=80)
                    if blobs:
                    #如果找到了目标颜色
                        for b in blobs:
                        #迭代找到的目标颜色区域
                            # Draw a rect around the blob.
                            img.draw_rectangle(b[0:4]) # rect
                            #用矩形标记出目标颜色区域
                            img.draw_cross(b[5], b[6]) # cx, cy
                            #在目标颜色区域的中心画十字形标记
                            #print(b[5], b[6])
                            #输出目标物体中心坐标
                            #print(b[7])
                            A.append(b[5])
                            B.append(b[6])
                            C.append(b[7])
                    if len(A)<1:
                        break
                    if len(A)>2:
                        break

                    print(A)
                    print(B)
                    print(C)
                    print(1)
                    if C[0]<Most:
                       ratio=10
                    if C[0]>Least:
                       ratio=-10

                    if B[0]>83:
                        pwm_control(0,0,0,70,85,0)#####pwm_control(0,0,0,77,80+ratio,0)
                    elif A[0]<40:
                        pwm_control(0,90,0,0,0,0)
                    elif A[0]>85:
                        pwm_control(90,0,0,0,0,0)
                    else:
                        pwm_control(0,0,0,0,0,0)
                        flag=flag+1
                    A.clear()
                    B.clear()
                    C.clear()

                while(flag==1):##################第二步：向左后向后
                    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.03)
                    blobs = img.find_blobs([green_threshold],pixels_threshold =80,area_threshold=80)
                    if blobs:
                    #如果找到了目标颜色
                        for b in blobs:
                        #迭代找到的目标颜色区域
                            # Draw a rect around the blob.
                            img.draw_rectangle(b[0:4]) # rect
                            #用矩形标记出目标颜色区域
                            img.draw_cross(b[5], b[6]) # cx, cy
                            #在目标颜色区域的中心画十字形标记
                            #print(b[5], b[6])
                            #输出目标物体中心坐标
                            #print(b[7])
                            A.append(b[5])
                            B.append(b[6])
                            C.append(b[7])
                    if len(A)<1:
                        break
                    if len(A)>2:
                        break

                    if C[0]<Most:
                       ratio=20
                    if C[0]>Least:
                       ratio=-20

                    if A[0]<15:
                        pwm_control(90,0,0,0,0,0)
                    elif B[0]<165:
                        pwm_control(0,0,72+ratio,0,0,70)
                    else:
                        pwm_control(0,0,0,0,0,0)
                        flag=flag+1
                    print(A)
                    print(B)
                    print(C)
                    print(2)
                    A.clear()
                    B.clear()
                    C.clear()
                while(flag==2):##################第三步：向右后向前在向左
                    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.05)
                    blobs = img.find_blobs([green_threshold],pixels_threshold =80,area_threshold=80)
                    if blobs:
                    #如果找到了目标颜色
                        for b in blobs:
                        #迭代找到的目标颜色区域
                            # Draw a rect around the blob.
                            img.draw_rectangle(b[0:4]) # rect
                            #用矩形标记出目标颜色区域
                            img.draw_cross(b[5], b[6]) # cx, cy
                            #在目标颜色区域的中心画十字形标记
                            #print(b[5], b[6])
                            #输出目标物体中心坐标
                            #print(b[7])
                            A.append(b[5])
                            B.append(b[6])
                            C.append(b[7])
                    if len(A)<1:
                        break
                    if len(A)>2:
                        break

                    if C[0]<Most:
                       ratio=20
                    if C[0]>Least:
                       ratio=-20

                    if A[0]<290:
                        pwm_control(0,100,0,0,0,0)
                    else:
                        pwm_control(0,0,0,70,85,0)
                        time.sleep(1900)
                        pwm_control(100,0,0,0,0,0)
                        time.sleep(3000)
                        flag=flag+1
                    print(A)
                    print(B)
                    print(C)
                    print(3)
                    A.clear()
                    B.clear()
                    C.clear()
                while(flag==3):###############第四步：向左后向后
                    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.05)
                    blobs = img.find_blobs([green_threshold],pixels_threshold =80,area_threshold=80)
                    if blobs:
                    #如果找到了目标颜色
                        for b in blobs:
                        #迭代找到的目标颜色区域
                            # Draw a rect around the blob.
                            img.draw_rectangle(b[0:4]) # rect
                            #用矩形标记出目标颜色区域
                            img.draw_cross(b[5], b[6]) # cx, cy
                            #在目标颜色区域的中心画十字形标记
                            #print(b[5], b[6])
                            #输出目标物体中心坐标
                            #print(b[7])
                            A.append(b[5])
                            B.append(b[6])
                            C.append(b[7])
                    if len(A)<1:
                        break
                    if len(A)>2:
                        break

                    if C[0]<Most:
                       ratio=20
                    if C[0]>Least:
                       ratio=-20

                    if A[0]>100:
                        pwm_control(100,0,0,0,0,0)
                    elif B[0]<157:
                        pwm_control(0,0,75,0,0,70)
                    else:
                        flag=flag+1
                    print(A)
                    print(B)
                    print(C)
                    print(4)
                    A.clear()
                    B.clear()
                    C.clear()
                while(flag==4):##############第五步：向左后向前
                    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.05)
                    blobs = img.find_blobs([green_threshold],pixels_threshold =80,area_threshold=80)
                    if blobs:
                    #如果找到了目标颜色
                        for b in blobs:
                        #迭代找到的目标颜色区域
                        # Draw a rect around the blob.
                            img.draw_rectangle(b[0:4]) # rect
                            #用矩形标记出目标颜色区域
                            img.draw_cross(b[5], b[6]) # cx, cy
                            #在目标颜色区域的中心画十字形标记
                            #print(b[5], b[6])
                            #输出目标物体中心坐标
                            #print(b[7])
                            A.append(b[5])
                            B.append(b[6])
                            C.append(b[7])
                    if len(A)<1:
                        break
                    if len(A)>2:
                        break

                    if C[0]<Most:
                       ratio=20
                    if C[0]>Least:
                       ratio=-20

                    if A[0]>X+5:
                        pwm_control(100,0,0,0,0,0)
                    elif B[0]>23:
                        pwm_control(0,0,0,70,85,0)
                    else:
                        flag=flag+1
                    print(A)
                    print(B)
                    print(C)
                    print(5)
                    A.clear()
                    B.clear()
                    C.clear()
                while(flag==5):#############第六步：向后向左再开始检验
                    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.05)
                    blobs = img.find_blobs([green_threshold],pixels_threshold =80,area_threshold=80)
                    if blobs:
                    #如果找到了目标颜色
                        for b in blobs:
                        #迭代找到的目标颜色区域
                            # Draw a rect around the blob.
                            img.draw_rectangle(b[0:4]) # rect
                            #用矩形标记出目标颜色区域
                            img.draw_cross(b[5], b[6]) # cx, cy
                            #在目标颜色区域的中心画十字形标记
                            #print(b[5], b[6])
                            #输出目标物体中心坐标
                            #print(b[7])
                            A.append(b[5])
                            B.append(b[6])
                            C.append(b[7])
                    if len(A)<1:
                        break
                    if len(A)>2:
                        break

                    if C[0]<Most:
                       ratio=20
                    if C[0]>Least:
                       ratio=-20

                    if B[0]<157:
                        pwm_control(0,0,73,0,0,70)
                    elif A[0]>18:
                        pwm_control(90,0,0,0,0,0)
                    else:
                        blobs = img.find_blobs([black_threshold],pixels_threshold =30,area_threshold=30,roi=(20,25,138,151))
                        if blobs:
                        #如果找到了目标颜色
                            for b in blobs:
                            #迭代找到的目标颜色区域
                                # Draw a rect around the blob.
                                img.draw_rectangle(b[0:4]) # rect
                                #用矩形标记出目标颜色区域
                                img.draw_cross(b[5], b[6]) # cx, cy
                                #在目标颜色区域的中心画十字形标记
                                #print(b[5], b[6])
                                #输出目标物体中心坐标
                                #print(b[7])
                                D.append(b[5])
                                E.append(b[6])

                        if len(D)>0:
                            flag=0
                            X=D[0]
                        else:
                            pwm_control(0,0,0,0,0,0)
                    print(A)
                    print(B)
                    print(C)
                    print(D)
                    print(E)
                    print(6)
                    A.clear()
                    B.clear()
                    C.clear()
                    D.clear()
                    E.clear()
        if pin0.value()==0:
            K=K+1
        else:
            K=K
        while(pin0.value()==0):
            pass

#######################################第三题
    while(K==3):
        led_control(3,50)
        while(pin1.value()==0):
            while(pin1.value()):
                while(flag3==0):###########
                    pass
            if pin0.value()==0 or pin1.value()==0:
                break

            else:
                pass
        if pin0.value()==0:
            K=K+1
        else:
            K=K
        while(pin0.value()==0):
            pass

#####################################第四题
    while(K==4):
        led_control(2,50)
        led_control(3,50)
        while(pin1.value()==0):
            while(pin1.value()):
                led_control(2,0)
                led_control(3,0)
                clock.tick() # Track elapsed milliseconds between snapshots().
                img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.1)
                if pin0.value()==0 or pin1.value()==0:
                    break
                else:
                    pass
        if pin0.value()==0:
            K=K+1
        else:
            K=K
        while(pin0.value()==0):
            pass

    if K==5:
        K=0



    print(A)
    print(B)
    print(C)
    A.clear()
    B.clear()
    C.clear()
    D.clear()
    E.clear()
    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while


