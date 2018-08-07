# Blob Detection Example
#
# 这个例子展示了如何使用find_blobs函数来查找图像中的颜色色块。这个例子特别寻找深绿色的物体。

import time,math
from pyb import Pin, Timer
import sensor, image, time

# 为了使色彩追踪效果真的很好，你应该在一个非常受控制的照明环境中。
black_threshold   = (0, 25, -2, 24, -128, 55)
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

PWM1.pulse_width_percent(0)
PWM2.pulse_width_percent(0)
PWM3.pulse_width_percent(0)
PWM4.pulse_width_percent(0)
PWM5.pulse_width_percent(0)
PWM6.pulse_width_percent(0)


sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
#关闭白平衡。白平衡是默认开启的，在颜色识别中，需要关闭白平衡。
clock = time.clock() # Tracks FPS.

while(True):
  while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot()

    blobs = img.find_blobs([black_threshold],pixels_threshold =20,area_threshold=30 ,roi = (79, 15, 220, 189))
    #find_blobs(thresholds, invert=False, roi=Auto),thresholds为颜色阈值，
    #是一个元组，需要用括号［ ］括起来。invert=1,反转颜色阈值，invert=False默认
    #不反转。roi设置颜色识别的视野区域，roi是一个元组， roi = (x, y, w, h)，代表
    #从左上顶点(x,y)开始的宽为w高为h的矩形区域，roi不设置的话默认为整个图像视野。
    #这个函数返回一个列表，[0]代表识别到的目标颜色区域左上顶点的x坐标，［1］代表
    #左上顶点y坐标，［2］代表目标区域的宽，［3］代表目标区域的高，［4］代表目标
    #区域像素点的个数，［5］代表目标区域的中心点x坐标，［6］代表目标区域中心点y坐标，
    #［7］代表目标颜色区域的旋转角度（是弧度值，浮点型，列表其他元素是整型），
    #［8］代表与此目标区域交叉的目标个数，［9］代表颜色的编号（它可以用来分辨这个
    #区域是用哪个颜色阈值threshold识别出来的）。
    A=[]
    B=[]
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
            A.append(b[5])
            B.append(b[6])
    if len(A)<3:
       break

    if len(B)<3:
       break

    if (B[1]-B[2])<-5.0:
       PWM1.pulse_width_percent(90)
       PWM2.pulse_width_percent(0)

    elif (B[1]-B[2])>5.0:
       PWM1.pulse_width_percent(90)
       PWM2.pulse_width_percent(0)

    if (A[1]-A[2])<-5:
       PWM1.pulse_width_percent(90)
       PWM1.pulse_width_percent(0)
       PWM1.pulse_width_percent(90)
       PWM1.pulse_width_percent(0)

    elif (A[1]-A[2])>5:
       PWM1.pulse_width_percent(0)
       PWM1.pulse_width_percent(90)
       PWM1.pulse_width_percent(0)
       PWM1.pulse_width_percent(90)

    if (B[1]-B[2])>-5 and (B[1]-B[2])<5:
       if (A[1]-A[2])>-5 and (A[1]-A[2])<5:
          if A[0]>A[1]:
             PWM1.pulse_width_percent(90)
             PWM1.pulse_width_percent(0)
             PWM1.pulse_width_percent(90)
             PWM1.pulse_width_percent(0)

    if (B[1]-B[2])>-5 and (B[1]-B[2])<5:
       if (A[1]-A[2])>-5 and (A[1]-A[2])<5:
          if A[0]<A[1]:
             PWM1.pulse_width_percent(0)
             PWM1.pulse_width_percent(90)
             PWM1.pulse_width_percent(0)
             PWM1.pulse_width_percent(90)

    if (B[1]-B[2])>-5 and (B[1]-B[2])<5:
       if (A[1]-A[2])>-5 and (A[1]-A[2])<5:
          if B[0]>B[1]:
             PWM1.pulse_width_percent(90)
             PWM1.pulse_width_percent(0)

    if (B[1]-B[2])>-5 and (B[1]-B[2])<5:
       if (A[1]-A[2])>-5 and (A[1]-A[2])<5:
          if B[0]<B[1]:
             PWM1.pulse_width_percent(0)
             PWM1.pulse_width_percent(90)

    print(A)
    print(B)
    A.clear()
    B.clear()
    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.


if len(A)<3:
   if B[1]<189:
      PWM1.pulse_width_percent(0)
      PWM2.pulse_width_percent(60)
   if B[1]>189:
      PWM1.pulse_width_percent(60)
      PWM2.pulse_width_percent(0)
   else:
      PWM1.pulse_width_percent(0)
      PWM2.pulse_width_percent(0)

   if A[1]>278:
      PWM3.pulse_width_percent(50)
      PWM4.pulse_width_percent(0)
      PWM5.pulse_width_percent(50)
      PWM6.pulse_width_percent(0)
   if A[1]<278:
      PWM3.pulse_width_percent(0)
      PWM4.pulse_width_percent(50)
      PWM5.pulse_width_percent(0)
      PWM6.pulse_width_percent(50)
   else:
      PWM1.pulse_width_percent(0)
      PWM2.pulse_width_percent(0)
   break

if(C[0]>2.9):
   PWM3.pulse_width_percent(0)
   PWM4.pulse_width_percent(0)
   PWM5.pulse_width_percent(40)
   PWM6.pulse_width_percent(0)

elif(C[0]<2.8):
   PWM3.pulse_width_percent(0)
   PWM4.pulse_width_percent(0)
   PWM5.pulse_width_percent(0)
   PWM6.pulse_width_percent(40)

if B[1]==B[2]+15 :
   if A[1]<A[2]:
      PWM3.pulse_width_percent(60)
      PWM4.pulse_width_percent(0)
      PWM5.pulse_width_percent(60)
      PWM6.pulse_width_percent(0)

   elif A[1]>A[2]:
      PWM3.pulse_width_percent(0)
      PWM4.pulse_width_percent(60)
      PWM5.pulse_width_percent(0)
      PWM6.pulse_width_percent(60)

   else:
      PWM3.pulse_width_percent(0)
      PWM4.pulse_width_percent(0)
      PWM5.pulse_width_percent(0)
      PWM6.pulse_width_percent(0)

else:
   if B[1]>B[2]+15:
      PWM1.pulse_width_percent(0)
      PWM2.pulse_width_percent(80)

   elif B[1]<B[2]+15:
      PWM1.pulse_width_percent(80)
      PWM2.pulse_width_percent(0)

   else:
      PWM1.pulse_width_percent(0)
      PWM2.pulse_width_percent(0)

blobs = img.find_blobs([red_threshold],pixels_threshold =50,area_threshold=50)
#find_blobs(thresholds, invert=False, roi=Auto),thresholds为颜色阈值，
#是一个元组，需要用括号［ ］括起来。invert=1,反转颜色阈值，invert=False默认
#不反转。roi设置颜色识别的视野区域，roi是一个元组， roi = (x, y, w, h)，代表
#从左上顶点(x,y)开始的宽为w高为h的矩形区域，roi不设置的话默认为整个图像视野。
#这个函数返回一个列表，[0]代表识别到的目标颜色区域左上顶点的x坐标，［1］代表
#左上顶点y坐标，［2］代表目标区域的宽，［3］代表目标区域的高，［4］代表目标
#区域像素点的个数，［5］代表目标区域的中心点x坐标，［6］代表目标区域中心点y坐标，
#［7］代表目标颜色区域的旋转角度（是弧度值，浮点型，列表其他元素是整型），
#［8］代表与此目标区域交叉的目标个数，［9］代表颜色的编号（它可以用来分辨这个
#区域是用哪个颜色阈值threshold识别出来的）。
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
        a.append(b[5])
        b.append(b[6])
