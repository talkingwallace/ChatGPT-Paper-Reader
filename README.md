## CHATGPT-PAPER-READER📝 

This repository provides a simple interface that utilizes the gpt-3.5-turbo model to read academic papers in PDF format locally. You can use it to help you summarize papers, create presentation slides, or simply fulfill tasks assigned by your supervisor.

## How Does This Work
Considering the following issues with using ChatGPT to read complete academic papers:

- The ChatGPT model itself has a context window size of 4096 tokens, making it unable to process the entire paper directly.
- It is easy to forget the context when dealing with long texts.

This repository attempts to solve these problems when using the OpenAI interface in the following ways:

- Splitting a PDF paper into multiple parts for reading and generating a summary of each part. When reading each part, it will refer to the context of the previous part within the token limit.
- Combining the summaries of each part to generate a summary of the entire paper. This can partially alleviate the forgetting problem when reading with ChatGPT.
- Before reading the paper, you can set the questions you are interested in the prompt. This will help ChatGPT focus on the relevant information when reading and summarizing, resulting in better reading performance.

By default, the initalized prompt will ask ChatGPT to focus on these points:
- Who are the authors?
- What is the process of the proposed method?
- What is the performance of the proposed method? Please note down its performance metrics.
- What are the baseline models and their performances? Please note down these baseline methods.
- What dataset did this paper use?
  
These questions are designed for research articles in the field of computer science.
After finishing reading the paper, you can ask questions using 'question()' interface, it will anwser your question based on the summaries of each part.

## Example: Read AlexNet Paper

### Summarize AlexNet
```python
from gpt_reader.pdf_reader import PaperReader, BASE_POINTS

print('Key points to focus while reading: {}'.format(BASE_POINTS))

api_key = 'Your key'
session = PaperReader(api_key, points_to_focus=BASE_POINTS)  # You can set your key points 
summary = session.read_pdf_and_summarize('./alexnet.pdf')

print(summary)
```

```
# console print
reading pdf finished
page: 0, part: 0
page: 0, part: 1
page: 1, part: 0
page: 1, part: 1
page: 2, part: 0
page: 2, part: 1
page: 3, part: 0
page: 3, part: 1
page: 4, part: 0
page: 4, part: 1
page: 5, part: 0
page: 5, part: 1
page: 6, part: 0
page: 6, part: 1
page: 7, part: 0
page: 7, part: 1
page: 8, part: 0
page: 8, part: 1
```

> reply: The paper presents a deep convolutional neural network architecture that was trained to classify 1.2 million high-resolution images in the ImageNet LSVRC-2010 contest into 1000 different classes. The network achieved top-1 and top-5 error rates of 37.5% and 17.0%, respectively, which is considerably better than the previous state-of-the-art. The authors used non-saturating neurons and a very efficient GPU implementation of the convolution operation to make training faster. They also employed a recently-developed regularization method called "dropout" to reduce overfitting in the fully-connected layers. The paper discusses the importance of large datasets for object recognition and the need for models with a large learning capacity. The authors entered a variant of this model in the ILSVRC-2012 competition and achieved a winning top-5 test error rate of 15.3%, compared to 26.2% achieved by the second-best entry. The paper also discusses the advantages of using convolutional neural networks (CNNs) for image recognition, including their ability to make strong and mostly correct assumptions about the nature of images, and the challenges of applying CNNs to high-resolution images. The authors describe the architecture of their CNN, which contains eight layers with weights, and the techniques they used to combat overfitting, including data augmentation and dropout. The paper provides qualitative evaluations of their CNN architecture and suggests future work, including using very large and deep convolutional nets on video sequences. The paper also lists references cited in the paper, including papers on image recognition challenges, object recognition, handwritten digit recognition, and convolutional networks and their applications in vision.


### Ask some questions

```python
session.question('Authors of this paper?')
```

> reply: The authors of this paper are Alex Krizhevsky, Ilya Sutskever, and Geoffrey E. Hinton from the University of Toronto.


```python
session.question('Describe the proposed method in details.')
```

> reply：The proposed method is based on a large, deep convolutional neural network that is trained with stochastic gradient descent using techniques like weight decay, momentum, and dropout for regularization.  The network consists of eight layers (five convolutional and three fully-connected) with the output layer consisting of a 1000-way softmax to produce a distribution over 1000 class labels.  The authors used a ReLU activation function and local response normalization to improve training speed, and overlapping pooling to improve generalization.  They also reduced overfitting by augmenting the training data with techniques like image translations, horizontal reflections, and altering the intensities of the RGB channels in training images using PCA.  The proposed method was trained on subsets of the ImageNet dataset used in the ILSVRC-2010 and ILSVRC-2012 competitions, which contain roughly 1.2 million training images, 50,000 validation images, and 150,000 testing images. By using a large, deep convolutional neural network with various optimization strategies, the proposed method achieved top-5 error rates of 16.4% and 15.3% on the ILSVRC-2012 validation and test sets, respectively, outperforming the previous state-of-the-art results.
> 

```python
session.question('What dataset does this paper use for experiment?')
```

> reply: The authors used subsets of the ImageNet dataset used in the ILSVRC-2010 and ILSVRC-2012 competitions for their experiments. These subsets contain approximately 1.2 million training images, 50,000 validation images, and 150,000 testing images.

```python
session.question('What metrics does this paper use to evaluate the performace?')
```

> reply: The paper evaluated the performance of their proposed method using Top-1 and Top-5 error rates on the validation and test sets of the ILSVRC-2010 and ILSVRC-2012 image recognition challenges. The Top-1 error rate measures the percentage of images for which the predicted class label is not the correct label, while the Top-5 error rate measures the percentage of images for which the correct label is not among the five most probable labels predicted by the model.

```python
session.question('Summarize this paper and your anwsers above, then translate the result into Chinese')
```
> reply: 这篇论文的作者是来自Toronto大学的Alex Krizhevsky、Ilya Sutskever和Geoffrey E. Hinton。该论文提出了一种基于卷积神经网络的深度学习方法，该方法在 ImageNet LSVRC-2010 和 ImageNet LSVRC-2012 图像识别挑战中达到了最佳结果。\n\n该方法使用了一系列技术来优化性能，包括使用ReLU激活函数和局部响应归一化等方法提高训练速度，使用重叠池化等方法提高泛化能力。为了减少过拟合，该方法还使用了数据增强技术，如图像平移、水平反射和使用PCA修改训练图像的RGB通道强度。作者在多个GPU上使用随机梯度下降进行训练，通过调整学习速率和使用权重衰减、动量和dropout等技术来优化性能。\n\n用于实验的数据集是 ImageNet LSVRC-2010 和 ImageNet LSVRC-2012 数据集的子集，其中包括大约120万个训练图像、5万个验证图像和15万个测试图像。该方法相比之前的最佳结果，达到了 更好的Top-1错误率和Top-5错误率。作者使用这两个错误率来评估性能，Top-1错误率表示预测的类别不是正确标签的百分率，而Top-5错误率表示真实标签不在模型预测的五个最可能标签中的百分率。

## GUI Interface
![alt](webui.png)
1. Install gradio in your python environment.
```
pip install gradio
```
2. Run gui.py. The link to the web page is output in the console.
```
python gui.py
```
![alt](console.png)
3. Fill in your API_KEY in the appropriate places on the web page and upload the required analysis PDF file. After you wait for the program to finish analyzing, you can switch to the second TAB and ask the program questions about the PDF.

## TODO

- This demo still needs to be improved to support longer articles. Articles of more than 10 pages have the possibility to exceed the token limit during processing.
- You may exceed the token limit when asking questions.
- More prompt tuning needed to let it outputs stable results.
- Imporve summary accuracies
