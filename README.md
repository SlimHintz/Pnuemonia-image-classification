
# Identifying Pnuemonia From Chest X-ray Images 
### Using ensemble classification and transfer learning to implement pneuomonia triage


**Authors**: [Tim Hintz](mailto:tjhintz@gmail.com), [Nick
Subic](mailto:bagnine@gmail.com)


![img](./images/doctor-research.jpg)

## Overview

We build a light-weight, ensemble, voting classifier using 3 transfer learning models to predict the presence of pneumonia from x-rays of childrens chest ages 1-5. 

Summary of key findings:
- Accuracy:
- Recall: 
- AUC:

## Healthcare Problem

Pneumonia is the leading cause of death among children across the globe. Pneumonia is a respiratory disease of the lungs usually caused by viral or bacterial infections. The World Health Organization estimated that in 2017 pneuomonia killed 800,000 children under the age of five, or 15% of all deaths of children in that age range. In addition, epidemiologists suggest that of the children that die of pneumonia every year, 45% of those are due to poor living conditions, specifically air quality. Since air quality has been linked to socioeconomic status, the present study built a statistical model using convolutional neural networks in order to aid in the diagnosis of pneumonia. 

X-rays are a widely accessible imaging technique used to diagnose pneumonia but a lot of trianing is required for a medical professional to reliably diagnose the disase. We were able to run our nerual network on a relatively low powered 2018 MacBook Air. We propose that implementing rapid image classification in low income communities could aid medical professionals in better allocating their time and resources.


## Data

Our dataset contains 5,863 X-Ray images, downloaded from Kaggle. The images were taken from pediatric patients from 1 to 5 years old in Guangzhou, China and contain instances of both bacterial and viral pneumonia.

The set is split into three groups-
1. A training set consisting of 5216 images, 3875 with pneumonia and 1341 healthy
2. A test set consisting of 624 images, 390 with pneumonia and 234 healthy
3. A validation set consisting of 16 images, with 8 each with pneumonia and healthy


We addressed class imbalance via image augmentation and weighting each class by their inverse frequency. However, image augmentation did not perform as well as class weighting so we only used class weighting in our final models.


![img](./images/classimbalance.png)


Looking at 3 examples from each class, the differences are subtle. But we hope that by then end of this section you will be able to accurately identify pneumonia chest x-rays from normal ones. Pay close attention to the definition of the chest cavity in Normal images and the blurred lung area in pneumonia patients

![img](./images/normVSpneu.png)


If we compare the mean pixel intensity between the two groups, where a higher value here represents a higher average pixel intensity in pneumonia chest x-rays, we can see that on average, pneumonia images have far brighter lungs. This is due to scarificaton and fluid build up in the lungs due to the infection.

![img](./images/averageDifference.png)


Now that we have developed some intuition where the images are most different from eachother, let's look at how much interclass difference there is. To do this, we looked at the standard deviation for pixel intensity for each class and then, similar to before, we fond the difference between the two and plotted it.

![img](./images/standardDiff.png)



## Methodology

For preprocessing, we resized each image to 224x224 pixels and ran models both after converting them to greyscale and as a 3d tensor array.  We calculated the inverse frequency of each class in our training data to use as class weights in our models. 

We used an Adam classifer which uses an adaptive learning rate with stochastic gradient descent. 

We created a convoluted neural network consisting of 8 alternating convolution and max pooling layers, followed by a flattening layer and 3 densely connected layers interspersed with regularization layers. Using our target metric- Recall- along with Accuracy and AUC we were able to tune our model to avoid over predicting pneumonia while still avoiding a potentially life-threatening false negative. 

### VGG16: make it Alexnet, but better
![img](./images/vgg16.png)


image [source](https://neurohive.io/en/popular-networks/vgg16/)


It's impossible for us to talk about image classfication tasks, particularly when it comes to transfer learning, without paying respect to Alexnet. Alexnet was really the first model that took advantage of GPU processing to implement a deep learning task. VGG16 replaces so of Alexnets enormous central kernel filters and replaces them with multiple streamlined 3x3 filters (see image). This model is a pain to train even with transfer learning due to it's size (with weights and nodes ~500mb). But yeilded amazing results in our use case.


### Densenet Archetecture, an unconventional take on image classification.
![img](./images/densenet.png)

image source: [Hashmi et al., 2020: Efficient Pneumonia Detection in Chest Xray Images Using Deep Transfer Learning](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7345724/#app1-diagnostics-10-00417)


As we were learning about image classfication, we continuously read that convolutions were king. This made sense. A sliding filter that could pick out features in in the image via [convolutions](https://en.wikipedia.org/wiki/Convolution#Visual_explanation)l. However, we saw Densenet, an almost entriely densley connected network, outperform primarily convolutional neural networks. Indeed, in the present study, we found that of the three models we tested, Densenet121 performed the best. In light of the performance, we included in Densenet in our stacked classifier.


### Mobilenet, a light weight multipurpose image recognition archetecture
![img](./images/mobilenet.png)



image source: [Hashmi et al., 2020: Efficient Pneumonia Detection in Chest Xray Images Using Deep Transfer Learning](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7345724/#app1-diagnostics-10-00417)


MobilenetV2 ustilizes [depth-wise convolutions](https://medium.com/@zurister/depth-wise-convolution-and-depth-wise-separable-convolution-37346565d4ec) and linear bottlenecks between convolution blocks to maximise classification on RGB images. We selected this archetecture because it had previously been used very effectively in this classfication task, it took the same dimensional input as vgg16 and densenet121 but also it is very lightweight. Initially being designed to run on mobile devices, we wanted to use a model that, by itself could have accuracy, recall and also run on low powered computers.


## Results

### Vgg16

Vgg16 was our largest model by far. It took 3x the time to converge. After regularizing the dense connections using dropout, we acheived:

Accuracy: 
Recall: 
AUC:

### Densenet121

Considering this model was unconventional for image classification we were surprised that it worked so efffectively in our use case:

Accuracy
Recall:
AUC:

### MobileNetV2 

Our fastest model was less effective overall but could be deployed on older, less powerful computers so we were very pleased with the results:

Accuracy:
Recall:
AUC

### Ensemble Voting Classfier

We used soft voting between our three models and after experimenting, we optimised the probability threshold to be 0.65 from 0.5 which increased our accuracy to 0.90 from 0.87 and didn't decrease our recall.

Accuracy:
Recall:
AUC:

![img](./images/ensemblecmatrix.png)


![img](./images/roccurve.png)


## Discussion and Conclusions

We are happy with the results of our model given the 1 week time constraint we were under. However, from reading the literature, using an 

## Repository Structure

```
├── Index.ipynb
├── README.md
├── images
├── notebooks
│   ├── EDA
│   └── modelling
└── src
    ├── data
    └── modules
```
