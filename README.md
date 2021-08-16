# Classification-verification-identification-using-eye-movement
## Introduction
The code in the repo is trying to solve a Kaggle competition "Eye Movements Verification and Identification Competition" (https://www.kaggle.com/c/emvic/data) [1]. The original problem is using the technique of eyeball tracking to see how efficient it is to identify different objects/participants by tracking their eyeball movemenets when responding to stimulus signals. More details, including the experimental detail, can be found in the URL above.
## Data Wrangling and Machine Learning Model
#### Data Wrangling
After importing files of training and test data into DataFrames, the DataFrames were examined to see if any value is missing from the cell. The dimensions of the DataFrames were checked. There is no value missing from the training or test data, so no futher action was taken.   
Not much information is provided in the description in the Kaggle problem [2] whether the cooridnates of eye balls alone is a good indicator for identification. Therefore, I generated two other sets of training and test data by substracting the coordinates, where X and Y coordinates and left and right eyes were handled separately, of two consecutive stimulated responses. The new DataFrame of diffence between responses provides information of relative movement of eyeballs.  
#### Machine Learning Model
This is a supervised classification problem and the dimesnion of data features (8192) is huge, so support vector machine (SVC) is pciked. The advantage of using SVC in this problem is that it is still effective as the number of training data points is less than that of the features [3]. Each feature was standardized before fed into SVC model for training.
## Results and Discussion
#### First Glance at Data
As the experiment suggests that the location of the stimulus signal starts to show up around the corner of screen after 20ms of blank screen, followed by 1600 ms of stimulation, I first looked at the data around the window. The patterns of the data, cooridnates of both eyes, seem to show a significant step during the window where stimulus point disappeared from screen around 1600ms, especially in the X coordinates. The figure below uses the first row of training data as an example to show if there is any significant change in response around 1600ms.
![Stimulus Point Disappeared from Middle](https://user-images.githubusercontent.com/30448897/129472519-5518504d-3578-4624-a8ec-6c713f526b0b.png)
It's also interesting to look into whether there is any pattern after 1600ms. The figure below also uses the first row of training data to show responses after 1600ms.
![Stimulus Points Showing on Corners](https://user-images.githubusercontent.com/30448897/129472533-46d0eb7d-9544-485a-b8ec-9762489d2630.png)
It looks like there is a noticeable change in coordinates after 1600ms at first glance. However, the amplitude of data in the first 1600ms is no less than that in the previous two figures, as shown below, so it's difficult to say that the observation above has any significane.
![Stimulus Showing in the Middle](https://user-images.githubusercontent.com/30448897/129472639-d7b903ab-96be-4f7b-9d1d-3f768d60ac78.png)
#### Correlation between Features
I next check the correlation between features to see if any range of the data trajectory. The figure below suggests that consecutive data of each eye show medium to high positive correlation.   
![original_heatmap](https://user-images.githubusercontent.com/30448897/129472994-aac7c136-0cd5-4833-bbc5-308d2b910156.png)   
One intesting findings on the figure above is the highly-correlated area between the y coordinates between left eye and right eye while x coordinates don't show this behavior. Closer look at the two regions of heatmap can be found below. It is expected that the Y coordinates of left and right eyes are highly correlated as (almost) everyone cannot decouple the synchroized vertical motion of eyes.   
Correlation of X|Correlation of Y
---|---|
![original_heatmap_two_eye_corr_x](https://user-images.githubusercontent.com/30448897/129473612-662598b9-faa3-4945-8361-4302c6f5b9b2.png)|![original_heatmap_two_eye_corr_y](https://user-images.githubusercontent.com/30448897/129473623-0b69669b-1ce5-4511-8902-64dd21bb075a.png)   

The heatmaps of the second set of data, the calculated difference between two consecutive responses, can be found below. The correlation between left and right eye or X and Y coordinate has been minimized in this new data set, as suggested by the heatmaps.
![diff_heatmap_3in1](https://user-images.githubusercontent.com/30448897/129495724-a1ce2c6a-e0f2-458e-9530-6f5b06d2c5c6.png)

#### Models and Prediction
The two sets of training data was fed to SVC model for taining. Two kernels, linear and RBF, were used. The competition has ended, so I am not able to verify my models. I instead compared the classified result obtained from RBF kernel to that from linear kernel, for both sets of test data to see what percentage the two kernel classify a test data point into the same object/participant. The comparision can be found in the table below.   
 Kernel| Original Data | Difference Data|
:------:|:-------------:|:--------:|
RBF/Linear|63.5%|46.9%|

The figures below also show the occurrence of inconsistency, grouped by user profile, for two sets of test data when compared with Linear kernel.
Origianl Data|Difference Data|
:---:|:---:|
![Devation between Linear and RBF kernel for original data set](https://user-images.githubusercontent.com/30448897/129496539-b1b8cb96-7b36-4b04-af0b-b72bbda22770.png)|![Devation between Linear and RBF kernel for Diff Data set](https://user-images.githubusercontent.com/30448897/129496542-bf2e3cb5-3f66-4db1-bcc5-375013efa806.png)

One can easily find that Object 1 has the highest occurrence of inconsistency in both data set. This might be worth investigating if one can obtain the accurate prediction for the test data in the future.   
I also compared predicted results between two data sets when the two models both use RBF kernel. The figure below suggests that the two models could generate significant outcomes, as only 51.5% of the results are identical between them. The object groups that show different outcomes are also spread across mutiple groups, which could indicate there is fundamental difference between the two SVC models from two different training data.
![Devation between Original and Diff Data sets](https://user-images.githubusercontent.com/30448897/129496784-44d860a5-7f69-4a00-bdcc-2fd809966e51.png)


## Reference
1. Eye Movements Verification and Identification Competition (https://www.kaggle.com/c/emvic/data) 
2. KASPROWSKI, P., OBER, J. 2004. Eye Movement in Biometrics, In Proceedings of Biometric Authentication Workshop, European Conference on Computer Vision in Prague 2004, LNCS 3087, Springer-Verlag.the IEEE/IARP International Conference on Biometrics (ICB), pp. 1-8.
3. Support Vector Machines https://scikit-learn.org/stable/modules/svm.html
