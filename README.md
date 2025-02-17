# OnPoint Smart Pellet Gun Shooting Targets
A small project I began to work on during January 2023. This project was started based off of my interest in Airsoft but lack of accessibility to Airsoft fields around me.
I thought if I found the right spot and had responsive shooting targets I could set up CQB (Close Quarters Combat) scenarios and compete with my friends to get the best score/time.
This birthed the idea of OnPoint, a desktop application that wirelessly communicated with any number of Raspberry Pi Pico devices on the same network.

## The Targets
I never got out of the prototype phase with these but my working prototype at the time was a cone with a medium sized LED light sticking out of the top. The Raspberry Pi Pico was taped into the cone with a small accelerometer chip tucked inside.
The accelerometer would retrieve force information applied to it which I would then calibrate to a weak hit from an Airsoft pellet which meant any reasonable gas-powered or electric airsoft gun would set it off properly. The whole "smart" part of these targets
comes from the light up top and their wireless communication. The RGB LED would flash either Red, Blue, or White (with varied frequencies). Each color and pulse meant something different about the target which forced the trainee to think critically before pulling the trigger.
If the trainee shot a blue target they would lose a point which prevents them from gaining a perfect score, if they shot a red target then they would gain a point. My favorite part was the white light. If the LED was white it would either pulse slowly or rapidly, slow
means the target is friendly and fast meant the target is an enemy. This aspect of the target was put in place to sharpen the trainee's threat recognition skills and reaction time. I found this to be really fun and keep you on your toes when running through CQB scenarios with
these targets. Below are some photos of the prototypes.
(IMAGE)

## The Server
The other half of this project was the server application that would be run on a Windows/MacOS computer. I developed this in Xojo because I liked it's WYSIWIG style at the time, going forward I would probably not use Xojo. The server application would scan all subnets of
its IP Address to find the smart shooting targets connected to the same local network. At this stage in development I had the WiFi connectivity hardcoded into the targets but I was planning on making a configuration aspect for them to connect to any available local network
provided by the server. Once the scanned targets were found you could tweak each target individually or just randomize it. Once the targets were set up to the users configuration, they would get sent a start command where they enter their active mode. In active mode they
listen to the accelerometer for any hits where they will then send the hit information back to the server. The server parses this info and then adds/removes points from the score and keeps a timer running the entire time. Once all combatant targets were hit the timer stops and
the user could view their time/score/stats. Attached below are some screenshots of the server application.
![Screenshot of the Server Application](https://i.imgur.com/IHogT4c.png)
![Screenshot of the help page demonstrating some basic info about the mode you chose and rules about the targets behaviors](https://i.imgur.com/bLWEnMf.gif)

## What I Learned
This was the second project I did that integrated Raspberry Pis. This was also my first time working with wireless communication via an albeit basic but useful UDP connection. Soldering was a fun new challenge not to mention figuring out the best physical form
for these shooting targets. My favorite part about this project the mixture of physical knowledge and expertise alongside the programming. Understanding how to manipulate data from the accelerometer was a headache for about a week but once I got it dialed in it was the
greatest relief. All in all, I realized that I can and will enjoy working with both my hands and my brain on projects and when they're driven by passion they are all the more fun to do.
