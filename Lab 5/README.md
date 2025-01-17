# Observant Systems

**NAMES OF COLLABORATORS HERE**

For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

## Prep

1. Spend about 10 Minutes doing the Listening exercise as described in [ListeningExercise.md](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2022/Lab%205/ListeningExercise.md)

2.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2022/Lab%202/prep.md), we offered the instruction at the bottom.

3.  Read about [OpenCV](https://opencv.org/about/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).

4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:
1. Pull the new Github Repo.(Please wait until thursday morning. There are still some incompatabilities to make the assignment work.)
1. Raspberry Pi
1. Webcam 

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show the filled out answers for the Contextual Interaction Design Tool.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)
B) [Fold](#part-b)
C) [Flight test](#part-c)
D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### OpenCV
A more traditional method to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python. We included 4 standard OpenCV examples: contour(blob) detection, face detection with the ``Haarcascade``, flow detection (a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (e.g. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example. 

The following command is a nicer way you can run and see the flow of the `openCV-examples` we have included in your Pi. Instead of `ls`, the command we will be using here is `tree`. [Tree](http://mama.indstate.edu/users/ice/tree/) is a recursive directory colored listing command that produces a depth indented listing of files. Install `tree` first and `cd` to the `openCV-examples` folder and run the command:

```shell
pi@ixe00:~ $ sudo apt install tree
...
pi@ixe00:~ $ cd openCV-examples
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```

The flow detection might seem random, but consider [this recent research](https://cseweb.ucsd.edu/~lriek/papers/taylor-icra-2021.pdf) that uses optical flow to determine busy-ness in hospital settings to facilitate robot navigation. Note the velocity parameter on page 3 and the mentions of optical flow.

Now, connect your webcam to your Pi and use **VNC to access to your Pi** and open the terminal. Use the following command lines to try each of the examples we provided:
(***it will not work if you use ssh from your laptop***)

```
pi@ixe00:~$ cd ~/openCV-examples/contours-detection
pi@ixe00:~/openCV-examples/contours-detection $ python contours.py
...
pi@ixe00:~$ cd ~/openCV-examples/face-detection
pi@ixe00:~/openCV-examples/face-detection $ python face-detection.py
...
pi@ixe00:~$ cd ~/openCV-examples/flow-detection
pi@ixe00:~/openCV-examples/flow-detection $ python optical_flow.py 0 window
...
pi@ixe00:~$ cd ~/openCV-examples/object-detection
pi@ixe00:~/openCV-examples/object-detection $ python detect.py
```

**\*\*\*Try each of the following four examples in the `openCV-examples`, include screenshots of your use and write about one design for each example that might work based on the individual benefits to each algorithm.\*\*\***

![Alt text](images/contours.png "Materials")
Contour Ideas: 

Contours your face shape and gives you a beauty Youtuber you can follow based on the calculations of the contours on your face.

![Alt text](images/facedetection.png "Materials")

Like this, images
![Alt text](images/faceCollage.jpg "Face Collage")

Face Detection
You can create a cool photo app where it detects faces and then it creates photo collages of the different face parts with other people who also used the app simultaneously. 

![Alt text](images/optical%20flow%20.png "Materials")
Optical Flow 
You can use this to create drawings with your fingers in a VR setting. 
Maybe you can use it to collaborate virtually with your teammates to ideate and prototype applications and services. 

![Alt text](images/ojbect-detection%20.png "Materials")
Object Detection
Use object detection to look at the different ingredients inside a fridge.
and then with that information, it can recommend recipes with the ingredients that you have inside the fridge. 


#### Filtering, FFTs, and Time Series data. 
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU or Microphone data stream could create a simple activity classifier between walking, running, and standing.

To get the microphone working we need to install two libraries. `PyAudio` to get the data from the microphone, `sciPy` to make data analysis easy, and the `numpy-ringbuffer` to keep track of the last ~1 second of audio. 
Pyaudio needs to be installed with the following comand:
``sudo apt install python3-pyaudio``
SciPy is installed with 
``sudo apt install python3-scipy`` 

Lastly we need numpy-ringbuffer, to make continues data anlysis easier.
``pip install numpy-ringbuffer``

Now try the audio processing example:
* Find what ID the micrpohone has with `python ListAvalibleAudioDevices.py`
    Look for a device name that includes `USB` in the name.
* Adjust the variable `DEVICE_INDEX` in the `ExampleAudioFFT.py` file.
    See if you are getting results printed out from the microphone. Try to understand how the code works.
    Then run the file by typing `python ExampleAudioFFT.py`



Using the microphone, try one of the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

You can use volumneSlow to set up threshold detections.
I used this variable to detect the volume sounds and had it so that when it passed a certain threshold, it printed the volumne number to the screen

```python
  while True:
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            if (volumneSlow > 100) :
                drawText = "Today's sleeping habits"
                draw.rectangle((0, 0, width, height), outline=0, fill=0)
                y = top
                draw.text((x, y), drawText + " \n" + str(volumneSlow), font=font, fill="#FFFFFF")
                y += font.getsize(drawText)[1]

               ### draw.text((x, y), "You snored. \n Severity : \n4.5 out of 10 \n" + str(volumneSlow), font=font, fill="#FFFFFF")
            disp.image(image, rotation)
            time.sleep(0.1)
```

https://user-images.githubusercontent.com/49267393/197420662-2633c7f7-798e-4aa9-a69e-7e15f362ffe4.mp4



### (Optional Reading) Introducing Additional Concepts
The following sections ([MediaPipe](#mediapipe) and [Teachable Machines](#teachable-machines)) are included for your own optional learning. **The associated scripts will not work on Fall 2022's Pi Image, so you can move onto part B.** However, you are welcome to try it on your personal computer. If this functionality is desirable for your lab or final project, we can help you get a different image running the last OS and version of python to make the following code work.

#### MediaPipe

A more recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Alt Text](mp.gif)

To get started, create a new virtual environment with special indication this time:

```
pi@ixe00:~ $ virtualenv mpipe --system-site-packages
pi@ixe00:~ $ source mpipe/bin/activate
(mpipe) pi@ixe00:~ $ 
```

and install the following.

```
...
(mpipe) pi@ixe00:~ $ sudo apt install ffmpeg python3-opencv
(mpipe) pi@ixe00:~ $ sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr25
(mpipe) pi@ixe00:~ $ pip3 install mediapipe-rpi3 pyalsaaudio
```

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(mpipe) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(mpipe) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py` lines 48-53. 

~~\*\*\*Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.\*\*\*~~

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)



#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple. However, its simplicity is very useful for experimenting with the capabilities of this technology.

![Alt Text](tm.gif)

To get started, create and activate a new virtual environment for this exercise with special indication:

```
pi@ixe00:~ $ virtualenv tmachine --system-site-packages
pi@ixe00:~ $ source tmachine/bin/activate
(tmachine) pi@ixe00:~ $ 
```

After activating the virtual environment, install the requisite TensorFlow libraries by running the following lines:
```
(tmachine) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ sudo chmod +x ./teachable_machines.sh
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ ./teachable_machines.sh
``` 

This might take a while to get fully installed. After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)

```
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tm_ppe_detection.py
```


(**Optionally**: You can train your own model, too. First, visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. Second, use the webcam on your computer to train a model. For each class try to have over 50 samples, and consider adding a background class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate, or export your model as a 'Tensorflow' model, and select 'Keras'. You will find an '.h5' file and a 'labels.txt' file. These are included in this labs 'teachable_machines' folder, to make the PPE model you used earlier. You can make your own folder or replace these to make your own classifier.)

~~**\*\*\*Whether you make your own model or not, include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.\*\*\***~~


*Don't forget to run ```deactivate``` to end the Teachable Machines demo, and to reactivate with ```source tmachine/bin/activate``` when you want to use it again.*


### Part B
### Construct a simple interaction.

* Pick one of the models you have tried, and experiment with prototyping an interaction.
* This can be as simple as the boat detector showen in a previous lecture from Nikolas Matelaro.
* Try out different interaction outputs and inputs.
* Fill out the ``Contextual Interaction Design Tool`` sheet.[Found here.]

(ThinkingThroughContextandInteraction.png)

What I did with the audio device was I set it up next to my bed.
I placed it so that it could detect noise at a close distance.
See images below for details on setup

![Alt text](images/stationed1.jpg "Materials")
![Alt text](images/stationed2.jpg "Materials")

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***

![Alt text](images/contextualinteractiondesigntool.jpg "Materials")
### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do?
It does what it is supposed to do when it detects audio in the background noise. 
If the audio also detects signs up coughing, wheezing, gagging, etc. then it would also be
able to diagnose for sleep apnea.

1. When does it fail?
It fails when there is too much noise in the background.
It would be hard to distinguish between a snore and a car engine.
It would also need to have good algorithms so that it won't distinguish any other noise
for wheezing or gagging for sleep apnea.

1. When it fails, why does it fail?
Because at the moment, we do not have any code that could distinguish the audio from the background, it would fail because it doesn't have the right code to distinguish between various different sounds. 

1. Based on the behavior you have seen, what other scenarios could cause problems? 
The rustling of the bed could also create unforeseen noises.
We would have to set up an appropriate threshold that could distinguish just the
sleep habits. 


**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
They would not be aware because they are sleeping.

1. How bad would they be impacted by a misclassification?
If the prototype gave out wrong results in respect to the sleeping habits, 
they might get stressed and try to fix those sleeping habits. 

1. How could change your interactive system to address this?
I think the only way to address this problem is to create a good algorithm
and set up a threshold so that it could detect the right sounds. 

1. Are there optimizations you can try to do on your sense-making algorithm.
Like mentioned in the previous question, optimize the threshold so that it may detect the right sounds

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
=> Detect sleeping habits 
For now, it will detect if it has a sleeping habit.
Better prototypes will be able to distinguish other habits as well. 

* What is a good environment for X?
=> A quiet bedroom with no noise

* What is a bad environment for X?
=> A bedroom in the city with a lot of noise (cars, people, etc.)

* When will X break?
=> If it runs out of battery or if the user accidentally knocks it out of 
where the device is positioned in 

* When it breaks how will X break?
=> The device will break as it will not be able to detect noises as well 
or the device physically falls and dismantles

* What are other properties/behaviors of X?
=> Detecting noises and displaying them on screen
=> Blinking lights to indicate that the device is functioning properly 

* How does X feel?
=> X just feels like an easy to use 

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***

--> This video will be included in the part2

### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***

In order to test how the device, I used video that had a recording of a mixture of snoring & sleep apnea noises.

![Alt text](images/screenshot.png "Materials")

I use these three components. 

![Alt text](images/IMG_7480.jpg "Materials")

The Pi keeps record of the volume. The webcam detects the noises. and the OLED screen lights if it detects signs of sleep apnea.


https://user-images.githubusercontent.com/49267393/198308215-7361116a-2445-493e-a0a4-3f2f31946816.mp4


In this video, I turned on a video that has sleep apnea noises along with snoring. 
The video shows the pi and the oled light up when it detects wheezing & coughing. 



https://user-images.githubusercontent.com/49267393/198308524-1fd44936-120b-4cb6-b97c-ad9b19c94ea2.mp4

In order to test it, I left the pi overnight, and slept through. 
I do not have sleep apnea. If it is working properly, then it should not light up during the night. 
And as I predicted, the screen remained black in the morning.

However, because I don't have sleep apnea, I don't know if the pi can successfully detect snoring, sleep apnea, and other sleeping habits like grinding teeth



