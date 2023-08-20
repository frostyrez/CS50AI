# Traffic

Design an AI that identifies which traffic sign appears in a photograph.

<img width="500" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/91b7720a-b3de-4dfe-8830-753a5876b63a">

## Outline

- The [German Traffic Sign Recognition Benchmark](https://benchmark.ini.rub.de/?section=gtsrb&subsection=news) (GTSRB) dataset contains thousands of images spanning 43 different kinds of road signs.

<p align="center">
<img width="500" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/64acb093-fd4e-4216-8346-1f912e6651d3">
</p>

- Once the data is loaded, resized, and separated into training and test data, the training data is fed into a compiled convolutional neural network model built using TensorFlow.
- Various combinations of convolutional, pooling, and dense layers are used.
- Initially, few layers are built, with few filters within each layer. These lead to accuracies of 80%+, but various improvements are explored.
- Increasing the number of filters in each successive convolutional layer was shown to have better accuracy than keeping a constant number.
- However, this had the inverse effect on the trio of stacked dense layers once the network was flattened.
- Dropout was shown to also improve the accuracy of the model.
- The following configuration was eventually found which seemed to strike a satisfactory balance between computational time and accuracy:

<img width="700" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/4eca3dc6-1451-4b5d-8c59-889fc7c11427">

## Usage
`python traffic.py gtsrb [model.h5]`
  
`[model.h5]` optional argument which allows for saving of the model.
