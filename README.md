Data Mining with Apriori in Python

•	Loading data 
All the files from the dataset follow a rule in which they start with some information about the email document. I decided to use only information after the 'Lines: x' line, where x are the lines in the given document. This way I will extract only the content of the email

•	Data pre-processing

1.	Removal of punctuation using string.punctiation
2.	Tokenization with nltk.word_tokenize() which splits each document to words
3.	word.lower() to avoid processing capital letters and word.isalpha() to avoid words that include characters which are not in the english alphabet
4.	Stemming with the Porter algorithm so that we focus on the meaning of each word and not each seperate word
5.	Removal of stop words by using data from nltk
Preproccesed_text data is now a python list where each item is a document from the collection

•	Storing pre-processed data
Object serialization with pickle for storing data

•	Top-K words
TF-IDF was used for finding the Top-K words of the dataset because it is easy to calculate and more effective than other numerical statistics. TfidVectorized() from sklearn was used

![image](https://user-images.githubusercontent.com/50420240/219849416-e8cfcc5f-a71b-454d-91f0-8c8265f4c5e5.png)

•	Apriori Association Rules
Mlxtend librady was used for the creation of the association rules. Using TransactionEncoder() we convert each document to a transaction in which every word is an item. Then we convert it to a Pandas DataFrame so that we can apply the Apriori algorithm and generate rules using different support and confidence thresholds:

Support: 0.12 Confidence: 0.6

![image](https://user-images.githubusercontent.com/50420240/219849431-4c8d5b67-9b21-4e4c-ba37-e415ee5fbb33.png)


Support: 0.12 Confidence: 0.7

![image](https://user-images.githubusercontent.com/50420240/219849438-323b08f9-d8c7-4395-8b0c-c20467358caf.png)


Support: 0.15 Confidence: 0.6

![image](https://user-images.githubusercontent.com/50420240/219849447-35c25e89-f4a2-4e09-83d0-0867d63a4505.png)


Support: 0.15 Confidence: 0.7

![image](https://user-images.githubusercontent.com/50420240/219849454-8fdf405d-3e4b-49b6-9f14-bcc7871d8b59.png)

	
Support: 0.2 Confidence: 0.6

![image](https://user-images.githubusercontent.com/50420240/219849459-17e18bc6-dc7e-4165-89b9-e47c19d2b454.png)


By incrementing support we get a smaller fraction of the collection which can make the whole process faster but we might eliminate strong rules. By incrementing confidence we get better accuracy on the generated rules as the connection between the antecedents and the consequents is stronger, at the cost of the reduction of the generated data.
For example, the would, write -> articl rule has a confidence of 0.74 and a lift of 1.69 which makes it one of the top strongest rules but its support of 0.17 makes it so that it does not appear during the last run.
We can also observe that the strongest rule is articl -> write. After checking the data manually we can confirm that this happens because a huge number of the documents include these lines:

![image](https://user-images.githubusercontent.com/50420240/219849468-f0eb22f4-fa2e-4556-8958-882279cc144e.png)


If this is not a desired effect, we could have removed these lines during the pre-process.
