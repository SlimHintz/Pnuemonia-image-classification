
# Identifying Pneumonia From Chest X-ray Images 
### Using ensemble classification and transfer learning to implement pneumonia triage


**Authors**: [Tim Hintz](mailto:tjhintz@gmail.com), [Nick
Subic](mailto:bagnine@gmail.com)


![img](./images/doctor-research.jpg)

## Overview

We built a light-weight, ensemble, voting-classifier using 3 transfer learning models (VGG16, DenseNet121, MobileNetV2) to predict the presence of pneumonia from x-rays of childrens (age 1-5) chests. Given the use case, we optimised for both recall and accuracy. Initially, we optimised for recall and acheived a test prediciton containing no false negatives. However, we also wanted to insure that medical professionals weren't being inundated with false positives so we included accuracy as an evaluation metric.

Summary of key findings:
- Accuracy: 0.9038

- Recall: 0.9897

- AUC: 0.9691

![img](./images/roccurve.png)


## Healthcare Problem

X-rays are a widely accessible imaging technique that can be used to diagnose pneumonia. However, years of training are required for someone to make an accurate diagnosis. We built a convolutional neural network that can classify images of pneumonia with 90% accuracy and could be run on nothing more than a smart-phone. We optimised recall to minimise the number of false negatives. We propose implementing automated image classification in low income communities with access to x-rays that will aid medical professionals by better allocating their time and resources.

## Data

Our dataset contains 5,863 X-Ray images, downloaded from Kaggle. The images were taken from pediatric patients from 1 to 5 years old in Guangzhou, China and contain instances of both bacterial and viral pneumonia.

The set is split into three groups-
1. A training set consisting of 5216 images, 3875 with pneumonia and 1341 healthy
2. A test set consisting of 624 images, 390 with pneumonia and 234 healthy
3. A validation set consisting of 16 images, with 8 each with pneumonia and healthy


We addressed class imbalance via image augmentation and weighting each class by their inverse frequency. However, image augmentation did not perform as well as class weighting so we only used class weighting in our final models.


![img](./images/classimbalance.png)


We visually inspected 3 by 2 random batches of images from our training data. It’s not clear which class images belong to without the aid of labels. I’ll draw your attention to the cloudiness of the lateral distal portions of the lungs in the pneumonia images and the clear negative space that is present in the chest cavities of normal images. 

![img](./images/normVSpneu.png)


If we compare the mean pixel intensity between the two groups, where more red here represents a higher average pixel intensity in pneumonia chest x-rays, we can see that on average, pneumonia images have far brighter lungs. This is due to scarificaton and fluid build up in the lungs due to the infection.

![img](./images/averageDifference.png)


Now that we have developed some intuition where the images are most different from eachother, let's look at how much interclass difference there is. To do this, we looked at the standard deviation for pixel intensity for each class and then, similar to before, we fond the difference between the two and plotted it.

![img](./images/standardDiff.png)



## Methodology

For preprocessing, we resized each image to 224x224 pixels and ran models both after converting them to greyscale and as a 3d tensor array.  We calculated the inverse frequency of each class in our training data to use as class weights in our models. 

We used an Adam optimizer which uses an adaptive learning rate with stochastic gradient descent. We chose to use it because of its speed training and evaluating new models, but given more time would switch to an SGD optimizer with step decay in the learning rate.

We created a convoluted neural network consisting of 8 alternating convolution and max pooling layers, followed by a flattening layer and 3 densely connected layers interspersed with regularization layers to reduce overfit. We chose Recall as our target metric to avoid potentially deadly false negatives, but because of the class imbalance our early models were able to achieve 100% recall, albeit with 100s of false positives. As we continued to develop our models, we added Accuracy and AUC in order to reduce false positives and produce an overall better model. 


### VGG16: Make it AlexNet, but better
![img](./images/vgg16.png)


image [source](https://neurohive.io/en/popular-networks/vgg16/)


It's impossible for us to talk about image classfication tasks, particularly when it comes to transfer learning, without paying respect to AlexNet. AlexNet was really the first model that took advantage of GPU processing to implement a deep learning task. VGG16 replaced Alexnets enormous central kernel filters with multiple streamlined 3x3 filters (see image). This model is a pain to train even with transfer learning due to it's size (with weights and nodes the model size was  ~500mb). However, VGG16 yeilded amazing results in our use case.


### Densenet121 Architecture, an unconventional take on image classification.
![img](./images/densenet.png)

image source: [Hashmi et al., 2020: Efficient Pneumonia Detection in Chest Xray Images Using Deep Transfer Learning](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7345724/#app1-diagnostics-10-00417)


As we were learning about image classfication, we continuously read that convolutions were king. This made sense. A sliding filter that could pick out features in in the image via [convolutions](https://en.wikipedia.org/wiki/Convolution#Visual_explanation)l. However, we saw [Densenet](https://towardsdatascience.com/understanding-and-visualizing-densenets-7f688092391a), an almost entriely densley connected network, outperform primarily convolutional neural networks. Indeed, in the present study, we found that of the three models we tested, Densenet121 performed the best. In light of the performance, we included in Densenet in our stacked classifier.


### Mobilenet, a light weight multipurpose image recognition architecture
![img](./images/mobilenet.png)



image source: [Hashmi et al., 2020: Efficient Pneumonia Detection in Chest Xray Images Using Deep Transfer Learning](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7345724/#app1-diagnostics-10-00417)


MobilenetV2 ustilizes [depth-wise convolutions](https://medium.com/@zurister/depth-wise-convolution-and-depth-wise-separable-convolution-37346565d4ec) and linear bottlenecks between convolution blocks to maximise classification on RGB images. We selected this architecture because it had previously been used effectively in this classfication task, it took the same dimensional input as VGG16 and DenseNet121 but also it is very lightweight. Initially being designed to run on mobile devices, we wanted to use a model that, by itself could have accuracy, recall and also run on low powered computers.


## Results

### Homemade CNN

Accuracy: 0.7901

Recall: 0.9769

Auc: 0.8848

![img](./images/homemadeconf.png)

![img](./images/homemaderoc.png)

Our homemade model had good recall but was far to sensitive. Having 122 false positives would do little to ease congestion of health care workers. The specificty of this model was 0.5. Since computing time was a limiting factor in our project, we set out to utilize pre trained models to improve our accuracy. 

### VGG16

VGG16 was our largest model by far. It took 3x the time to converge. After regularizing the dense connections using dropout, we achieved:

Accuracy: 0.8830

Recall: 0.9897

AUC: 0.9480

### Densenet121

Considering this model was unconventional for image classification we were surprised that it worked so efffectively in our use case:

Accuracy: 0.8734 

Recall: 0.9923

AUC: 0.9044

### MobileNetV2 

Thogh MobileNetV2 was our fastest model to converge by far, it was less effective overall. However, it could be deployed on older, less powerful computers so we were very pleased with the results:

Accuracy: 0.8814

Recall: 0.9795

AUC: 0.9485

### Ensemble Voting Classfier

We wrote our own soft voting classifier. After experimenting with classification thresholds, we optimised the probability threshold to be 0.65 from 0.5 which increased our accuracy to 0.90 from 0.87 and didn't decrease our recall.

Accuracy: 0.9038

Recall: 0.9897

AUC: 0.9691

![img](./images/ensemblecmatrix.png)


![img](./images/roccurve.png)


### Looking at False Negatives and False Positives:

![img](./images/fp_fn_diff.png)


We repeated some of the earlier EDA steps to try and figure out what why we were getting so many false positives. When we compare the difference between the two images we can see again the areas highlighted in red. These red areas indicate brighter regions within the lungs that were typical of the positive case. The cause for these blurred regions is unclear but could be due to movement during the x-ray procedures. 

## Discussion and Conclusions

We are happy with the results of our model given the 1 week time constraint we were under. However, from reading the literature, using an optimiser with an adaptive learning rate does not always give the best results. It does speed up the time to converge, but can also lead get trapped in local minima. Therefore, if we had more time and access to more powerful computers, we would use stochastic gradient descent with a very low learning rate (alpha ~ 0.0001) with stepped learning decay and run 100 epochs per model. 

In addition, we would like to train a multiclassfication model. The positive class has both viral and bacterial pneumonia cases. We understand tht bacterial cases are often more severe. Therefore we would like to indicate whether a particular infection is bacterial or viral. Even if the classifier's accuracy drops, the possibility that false positives could be reduced by more accurately predicting healthy patients versus pneumonia, even if it's the incorrect type of pneumonia, would be an overall improvement.

Finally, here we used wrote a soft voting classifier simililar to the scikit learn implementation. In the future we are interested in building a stacked classifier that uses backpropagation to assign weights to the output of each model in the classifier.

## Repository Structure

```
├── Pneumonia Classification.ipynb     <- A complete walkthrough of our project
├── README.md       <-
├── images          <- Images used in this README
├── notebooks       
│   ├── EDA         <- Exploratory Data Analysis
│   └── modelling   <- Model Prototyping 
└── src
    ├── data        <- Image Data
    └── modules     <- Custom eda, preprocessing and graphing functions
```
