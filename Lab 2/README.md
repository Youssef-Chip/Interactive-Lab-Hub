# Interactive Prototyping: The Clock of Pi
**NAMES OF COLLABORATORS HERE**
Youssef Hassan (yh2443), Jonathan Tumalle (jrt285)

**Note: I didn't have my own Pi.**

Does it feel like time is moving strangely during this semester?

For our first Pi project, we will pay homage to the [timekeeping devices of old](https://en.wikipedia.org/wiki/History_of_timekeeping_devices) by making simple clocks.

It is worth spending a little time thinking about how you mark time, and what would be useful in a clock of your own design.

**Please indicate anyone you collaborated with on this Lab here.**
Be generous in acknowledging their contributions! And also recognizing any other influences (e.g. from YouTube, Github, Twitter) that informed your design. 

## Prep

1. ### Set up your Lab 2 Github

At the start of lab Wednesday, ensure you have the latest lab content by updating your forked repository. 

**📖 [Follow the step-by-step guide for safely updating your fork](pull_updates/README.md)**

This guide covers how to pull updates without overwriting your completed work, handle merge conflicts, and recover if something goes wrong.


2. ### Get Kit and Inventory Parts
Take inventory of the kit parts that you have, and note anything that is missing:

***Update your [parts list inventory](partslist.md)***

3. ### Prepare your Pi for lab this week
[Follow these instructions](prep.md) to download and burn the image for your Raspberry Pi before lab Wednesday.




## Overview
For this assignment, you are going to 

A) [Connect to your Pi](#part-a)  

B) [Try out cli_clock.py](#part-b) 

C) [Set up your RGB display](#part-c)

D) [Try out clock_display_demo](#part-d) 

E) [Modify the code to make the display your own](#part-e)

F) [Make a short video of your modified barebones PiClock](#part-f)

G) [Sketch and brainstorm further interactions and features you would like for your clock for Part 2.](#part-g)

## The Report
This readme.md page in your own repository should be edited to include the work you have done. You can delete everything but the headers and the sections between the \*\*\***stars**\*\*\*. Write the answers to the questions under the starred sentences. Include any material that explains what you did in this lab hub folder, and link it in the readme.

Labs are due on Sunday midnight. Make sure this page is linked to on your main class hub page.

## Part A. 
### Connect to your Pi
Just like you did in the lab prep, ssh on to your pi. Once you get there, create a Python environment (named venv) by typing the following commands.

```
ssh pi@<your Pi's IP address>
...
pi@raspberrypi:~ $ python -m venv venv
pi@raspberrypi:~ $ source venv/bin/activate
(venv) pi@raspberrypi:~ $ 

```
### Setup Personal Access Tokens on GitHub
Set your git name and email so that commits appear under your name.
```
git config --global user.name "Your Name"
git config --global user.email "yourNetID@cornell.edu"
```

The support for password authentication of GitHub was removed on August 13, 2021. That is, in order to link and sync your own lab-hub repo with your Pi, you will have to set up a "Personal Access Tokens" to act as the password for your GitHub account on your Pi when using git command, such as `git clone` and `git push`.

Following the steps listed [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) from GitHub to set up a token. Depends on your preference, you can set up and select the scopes, or permissions, you would like to grant the token. This token will act as your GitHub password later when you use the terminal on your Pi to sync files with your lab-hub repo.


## Part B. 
### Try out the Command Line Clock
Clone your own lab-hub repo for this assignment to your Pi and change the directory to Lab 2 folder (remember to replace the following command line with your own GitHub ID):

```
(venv) pi@raspberrypi:~$ git clone https://github.com/<YOURGITID>/Interactive-Lab-Hub.git
(venv) pi@raspberrypi:~$ cd Interactive-Lab-Hub/Lab\ 2/
```
Depends on the setting, you might be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you just set up as the password instead of your account one!

Check if the directory has clone sucessfully, you should see the Interactive-Lab-Hub under the home directory listed:
```
(venv) pi@raspberrypi:~ $ ls
Bookshelf      Documents            Music     Public                 venv
create_img.sh  Downloads            pi-apps   screen_boot_script.py  Videos
Desktop        Interactive-Lab-Hub  Pictures  Templates
(venv) pi@raspberrypi:~ $
```


Install the packages from the requirements.txt and run the example script `cli_clock.py`:

```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ pip install -r requirements.txt
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ python cli_clock.py 
02/24/2021 11:20:49
```

The terminal should show the time, you can press `ctrl-c` to exit the script.
If you are unfamiliar with the Python code in `cli_clock.py`, have a look at [this Python refresher](https://hackernoon.com/intermediate-python-refresher-tutorial-project-ideas-and-tips-i28s320p). If you are still concerned, please reach out to the teaching staff!


## Part C. 
### Set up your RGB Display
We have asked you to equip the [Adafruit MiniPiTFT](https://www.adafruit.com/product/4393) on your Pi in the Lab 2 prep already. Here, we will introduce you to the MiniPiTFT and Python scripts on the Pi with more details.

<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="200" />

The Raspberry Pi 5 has a variety of interfacing options. When you plug the pi in the red power LED turns on. Any time the SD card is accessed the green LED flashes. It has standard USB ports and HDMI ports. Less familiar it has a set of 20x2 pin headers that allow you to connect a various peripherals.

<img src="https://maker.pro/storage/g9KLAxU/g9KLAxUiJb9e4Zp1xcxrMhbCDyc3QWPdSunYAoew.png" height="400" />

To learn more about any individual pin and what it is for go to [pinout.xyz](https://pinout.xyz/pinout/3v3_power) and click on the pin. Some terms may be unfamiliar but we will go over the relevant ones as they come up.

### Hardware (you have already done this in the prep)

From your kit take out the display and the [Raspberry Pi 5](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.raspberrypi.com%2Fproducts%2Fraspberry-pi-5%2F&psig=AOvVaw330s4wIQWfHou2Vk3-0jUN&ust=1757611779758000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCPi1-5_czo8DFQAAAAAdAAAAABAE)

Line up the screen and press it on the headers. The hole in the screen should match up with the hole on the raspberry pi.

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/087/539/medium640/adafruit_products_4393_quarter_ORIG_2019_10.jpg?1579991932" height="200" />
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/861/original/adafruit_products_image.png" height="200">
</p>

### Testing your Screen

The display uses a communication protocol called [SPI](https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/) to speak with the raspberry pi. We won't go in depth in this course over how SPI works. The port on the bottom of the display connects to the SDA and SCL pins used for the I2C communication protocol which we will cover later. GPIO (General Purpose Input/Output) pins 23 and 24 are connected to the two buttons on the left. GPIO 22 controls the display backlight.

To show you the IP and Mac address of the Pi to allow connecting remotely we created a service that launches a python script that runs on boot. For the following steps stop the service by typing ``` sudo systemctl stop piscreen.service --now```. Othwerise two scripts will try to use the screen at once. You may start it again by typing ``` sudo systemctl start piscreen.service --now```

We can test it by typing 
```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ python screen_test.py
```

You can type the name of a color then press either of the buttons on the MiniPiTFT to see what happens on the display! You can press `ctrl-c` to exit the script. Take a look at the code with
```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ cat screen_test.py
```

#### Displaying Info with Texts
You can look in `screen_boot_script.py` for how to display text on the screen!

#### Displaying an image

You can look in `image.py` for an example of how to display an image on the screen. Can you make it switch to another image when you push one of the buttons?

\*\*\***Include a picture of your own Raspberry Pi displaying the piscreen.service with your unique MAC address. Additionally, please provide another picture showing the successful completion of the screen test.**\*\*\*

<img width="367" height="430" alt="Screenshot 2026-09-10 at 3 36 10 PM" src="https://github.com/user-attachments/assets/5bf568af-9b66-45ca-af39-4e202c2080b7" />


<img width="577" height="526" alt="Screenshot 2026-09-19 at 2 07 25 PM" src="https://github.com/user-attachments/assets/52eb5d73-3919-4939-a47d-06394d89f42b" />


## Part D. 
### Set up the Display Clock Demo
Work on `screen_clock.py`, try to show the time by filling in the while loop (at the bottom of the script where we noted "TODO" for you). You can use the code in `cli_clock.py` and `stats.py` to figure this out.

### How to Edit Scripts on Pi
Option 1. One of the ways for you to edit scripts on Pi through terminal is using [`nano`](https://linuxize.com/post/how-to-use-nano-text-editor/) command. You can go into the `screen_clock.py` by typing the follow command line:
```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ nano screen_clock.py
```
You can make changes to the script this way, remember to save the changes by pressing `ctrl-o` and press enter again. You can press `ctrl-x` to exit the nano mode. There are more options listed down in the terminal you can use in nano.

Option 2. Another way for you to edit scripts is to use VNC on your laptop to remotely connect your Pi. Try to open the files directly like what you will do with your laptop and edit them. Since the default OS we have for you does not come up a python programmer, you will have to install one yourself otherwise you will have to edit the codes with text editor. [Thonny IDE](https://thonny.org/) is a good option for you to install, try run the following command lines in your Pi's ternimal:

  ```
  pi@raspberrypi:~ $ sudo apt install thonny
  pi@raspberrypi:~ $ sudo apt update && sudo apt upgrade -y
  ```

Now you should be able to edit python scripts with Thonny on your Pi.

Option 3. A nowadays often preferred method is to use Microsoft [VS code to remote connect to the Pi](https://www.raspberrypi.com/news/coding-on-raspberry-pi-remotely-with-visual-studio-code/). This gives you access to a fullly equipped and responsive code editor with terminal and file browser.  

Pro Tip: Using tools like [code-server](https://coder.com/docs/code-server/latest) you can even setup a VS Code coding environment hosted on your raspberry pi and code through a web browser on your tablet or smartphone! 

## Part E. Read Part 2. Sketch and brainstorm further interactions and features you would like for your clock.

One potential source of ideas might be thinking about other clocks and timekeeping devices for inspiration.

Another might be novel units of time. How do you measure a year? [In daylights? In midnights? In cups of coffee?](https://www.youtube.com/watch?v=wsj15wPpjLY)

We strongly discourage literal digital or analog clock display: Be creative.


** Insert ideas, sketches, [Verplank diagrams](https://ccrma.stanford.edu/courses/250a-fall-2004/IDSketchbok.pdf)), storyboards for your ideas **

<img width="3595" height="2461" alt="clock_storyboard" src="https://github.com/user-attachments/assets/d0e3d398-2da1-42bc-89a2-9fa0b75bec6e" />

The user looks at the screen and instantly knows where they are in the day by observing the position of the Sun or Moon relative to the horizon and the resulting color of the screen.


**Put the names of the people you gave feedback to here. (Even better, add links to their repos here!)**


1- Sirapop Umnakkittikul & Feiyu Zhou: https://github.com/Morinzzz/Interactive-Lab-Hub

My feedback to them: I think the “Egg” is a very creative way to make a clock that measures a year and I really like the story that you gave to your character. However I do think if it weren’t for the text below your storyboard, I would’ve been a bit confused about how you were gonna make the clock measure a year. Additionally, I really love the Pomodoro timer option that you introduced, I think it’s a very useful feature that I would definitely use.


I think your storyboard for your second clock idea is much clearer and I was able to understand how the clock works. My only feedback is that I would prefer to use your first clock just because the idea that the clock can speak might creep me out sometimes.

2- Viktor Radev: https://github.com/LaboriouslyExquisite/Interactive-Lab-Hub/blob/Fall2026/Lab%202/README.md

My feedback to Viktor: I think this is a fantastic design and a very creative way to make a clock very fun to use, which isn't something I thought I would need, but I'm glad you made it possible. I have 2 possible critiques, unless I misunderstood your storyboard: First one: who picks the suit for the hour, is it randomly decided or is the user picking it? If it's the latter, I think it could turn a bit tedious for the user eventually, if its the former, would it also be possible for the user to keep switching suits? Second one: since the items per spiderman only go up to 12, how would you tell the difference between AM and PM? Is it possible to make your storyboard a bit clearer to address these questions?


3- Jonathan Tumalle: https://github.com/jontumalle/Interactive-Lab-Hub/blob/Lab2a/Lab%202/README.md

My feedback to JT: I really like this idea for multiple reasons: first off, I learned that the ISS actually passes over 16 times a day, which I didn't know, and more impressively, that someone built an API for tracking it. This is why I think your clock design is very impressive because it's based on a real-time phenomenon that you can check for yourself if you are a stargazer. My only critique is I would make more panels in the storyboard showing more stages of what it would like when the ISS is passing and when the user is waiting for it.


# Lab 2 Part 2

## Prep 

1. Pick up remaining parts for kit on Wednesday lab class. Check the updated [parts list inventory](partslist.md) and let the TA know if there is any part missing.

2. Look at and give feedback on the Part E. for at least 3 other people in the class and get 3 people to comment on your Part E!)
**Put the feedback for your ideas here.**

1- Sirapop Umnakkittikul:


I really like how this concept brings nature into the clock. Seeing the Sun or Moon move across the screen relative to the horizon makes the whole experience feel warmer and more grounded. It creates a stronger sense of connection to the natural cycle of the day, rather than just reading abstract numbers. The way the position of the Sun or Moon changes based on the actual time of day is especially thoughtful. It’s not just a fixed or hard-coded placement, it genuinely reflects where those celestial bodies would be, which makes the design feel more intentional and immersive. Combined with the shifting screen colors, it lets the user instantly sense their place in the day in a calm, intuitive way.


2- Viktor Radev:

Overall I like your design as it follows the idea of the coffee mug where for time tracking you would note when you last drank coffee to tell you how long before you should get another one assuming it's still day time outside. Instead of literally pasting the time you want to show the user the position of the moon and the earth in relation to their geo-spatial location to inform them whether or not the sun will be rising or setting to give them some idea as to what time of day it is. Instead of using time in the quantifiable sense, you will inform the user based on the sense of the heavenly bodies of the moon and the sun. Some things that I think might be a problem come up when we talk about individuals who are located far away from the equator, which is that they usually have daytime and night time for much longer than your typical 12hr day time and 12night time cycle. How could you include additional information in your program to account for this issue? Could giving them a countdown on when the moon and the sun be helpful information, so that they can plan around that, as apposed to just showing the moon and the suns position? Is there some way you could integrate how the cycle of time is changing for the person, such as showing them when the lunar and the summer solstice will occur? These are just a few things that come to mind just from seeing your Verplank design.


3- Jonathan Tumalle

I do like the animation for the sun and moon and making it intuitive on what it’s measuring. One thing that might be cool is for maybe it also knowing if you’re outside or not and give you a measure of vitamin D accumulated from the week if that’s possible. Gives user an incentive to go outside

## Update your Lab Hub

[Update your Lab Hub](pull_updates/README.md) to get the latest content and requirements for Part 2.

## Modify the barebones clock to make it your own

Start small, pick just one element of your overall idea, just to show you have a handle on the code and components.

\*\*\***Put a copy of your code in your Lab 2 Github repo.**\*\*\*

**Please see ```barebone_clock.py```**

## Make a short video of your modified barebones PiClock

\*\*\***Take a video of your barely modified PiClock.**\*\*\*




https://github.com/user-attachments/assets/8f14c532-9354-4d4e-91dd-c1ea7d411ccf


This is a sped up version of the clock where 1 second => 1 hour. It starts at midnight.



After you edit and work on the scripts for Lab 2, the files should be upload back to your own GitHub repo! You can push to your personal github repo by adding the files here, commiting and pushing.

```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ git add .
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ git commit -m 'your commit message here'
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ git push
```

After that, Git will ask you to login to your GitHub account to push the updates online, you will be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you set up in Part A as the password instead of your account one! Go on your GitHub repo with your laptop, you should be able to see the updated files from your Pi!

## Now, make your own PiClock

Do take advantage of having done the previous iteration to refine and simplify your design.

** Insert any updates ideas, sketches, [Verplank diagrams](https://ccrma.stanford.edu/courses/250a-fall-2004/IDSketchbok.pdf))!, storyboards for your ideas **



Updated storyboard with the additional feature:

<img width="671" height="537" alt="Screenshot 2026-09-19 at 2 27 22 PM" src="https://github.com/user-attachments/assets/773588b5-5a2c-4f22-8fab-b9dba2898351" />




\*\*\***Put a copy of your code in your Lab 2 Github repo.**\*\*\*


**Please see ```complete_clock.py```**


\*\*\***Take a video of your PiClock.**\*\*\*



https://github.com/user-attachments/assets/c418f87e-f76c-4f5f-8923-b07bb9732feb

This is a sped up version of the clock where 1 second => 1 hour. It starts at midnight.



https://github.com/user-attachments/assets/80d10ea2-69fe-4e35-8d79-fe8170cbe299

This is a video of the clock working in real time, where the user can hold the button on "pin 23" to see what time it is.



As always, make sure you document contributions and ideas from others (and AI) explicitly in your writeup.

You are permitted (but not required) to work in groups and share a turn in; you are expected to make equal contribution on any group work you do, and N people's group project should look like N times the work of a single person's lab.  Make sure the page for the group turn in is linked to your personal Interactive Lab Hub page. 


