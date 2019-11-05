# BeatBot

## Inspiration
Who would not want to have a DJ for their small conducted house events? Who would not want to enjoy their own public gatherings instead of worrying about the songs to set in a playlist? While you are having a party or public gathering in your house, there are so many things to carry out and not every time you can afford to have professional DJ even for small gatherings...Right? So,our group thought of creating an application to take care for setting the mood by playing songs for any event or gathering arrangement conducted by you which helps in alleviating one of the main event planning worries. Phew! Now you can enjoy your event or party without worrying about the songs to play

## What it does
BeatBot, a full-stack application using python framework and Deep learning basically helps you to play the songs based on event or public gathering held in your house. It is your personal AI-DJ which activates when you upload image of the event. It classifies the event based on the picture you uploaded. For now we have 5 classes into which our model classifies the uploaded image which are as follows:

Birthday gatherings
Christmas gatherings
Halloween party
EDM parties
Wedding parties
How we built it
We built this project by using the following pipeline:

Hand curated the image data from the internet for each class. Around 300 images per class were collected to implement primitive idea of project.
Trained a ResNet34 Deep Learning model (Transfer Learning) on the collected data using fastai library. The model was trained with the goal to achieve scene-based classification.
Based on the prediction of the model, it calls the Spotify API and searches songs using specific tags related to the predicted event and plays the song.
At the same time, it also calls GIPHY API and displays dynamic gifs related to the predicted event on our web application.
Challenges we ran into
Not able to collect more data and create more classes for multiclass classification given the time constraint
Working with Web API of Spotify was kind of a challenge. Basically we wanted to search the term on spotify and play the songs relating to term. The search term are tags which we defined based on the predicted label obtained from the model classification. It was challenging to integrate and play the predicted label songs on our application
Integrating FastAI implemented model weights with the django framework and predict the uploaded image
Accomplishments that we're proud of
This project was made from scratch, starting from data collection, training model, creating web application and integrating the Spotify API (for playing song related to search from the model predicted tag). Tried to turn a rather abstract idea into a real time working web application and would be working to create mobile application further

## What we learned
Integrating FastAI implemented model with web application framework (Django)
Usage of Web API of Spotify for our web application
Integrating Giphy API with our web application
What's next for BeatBot
Collect more data for model classification
Include more classes such as sports gatherings,calm/peaceful gatherings,etc
Create mobile app where user can take a real time image/video and our project pipeline flows from that

## Built With
computer-vision
css
deep-learning
django
fastai
giphy
html
javascript
machine-learning
python
spotify
