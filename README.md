# CyberNews

**`How I Built The One Cyber News Aggregator To Rule Them All`**
   </br>

## 📜 The Why
So many things happen in infosec every day that it’s hard to keep up. It can be even harder to know what matters. I sure know I was overwhelmed when Google started serving me more infosec content than a human can consume in a lifetime. But keeping up is a must, especially here. Can’t stay ahead of the curve if you’re missing out, right?

   </br>

## 📜 The What
CyberNews is a news aggregator from different websites that cover cybersecurity, including Dark Reading, CSO Online, Security Week, and more. CyberNews can analyze and cluster headlines together, giving a saliency score according to the number of mentions in the media.

   </br>

## 📜 The How
CyberNews starts with a simple script that aggregates RSS feeds from six main sources. The RSS feeds are then processed by SpaCy to extract the entities in each headline, and by SKLearn to perform an initial clustering of headlines together. Then, large clusters are processed again by weighting the entities and re-clustering them. The end result is every headline from every news source clustered according to its subject, making it easy to skim the news and find the important topics.

   </br>

## 📜 The Challenges
From a Python perspective, this was extremely challenging. First, getting to work with NLP and clustering algorithms, which to be honest - I didn’t really know anything about. Luckily, the third-party libraries available do an incredible job of making these tools accessible. From a content perspective, tuning the clustering algorithm was a huge task, and it’s still not perfect. I tried so many variations trying to tune the algorithm by weighting entities, adjusting the sensitivity, using different vectoring algorithms, different models, different libraries…and still haven’t gotten it to work perfectly.

   </br>

## 📜 The Lessons
This project, with the number of iterations it went through, was (and still is…) an exercise in picking things up and persisting until it works. Trying different approaches. Going through the door would’ve been using ChatGPT - but 3.5 isn’t smart enough, and 4 is expensive. So through the window we go with open source NLP libraries and clustering algorithms. These were some of the advanced Python libraries I’ve ever worked with, and it gave me a lot of confidence in my abilities to write complex scripts.

   </br>

