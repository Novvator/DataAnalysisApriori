Programming Project 2 – Ανακάλυψη Γνώσης από Βάσεις Δεδομένων

•	Loading data 
Καθώς όλα τα αρχεία του dataset ακολουθούν ένα κανόνα κατά τον οποίο ξεκινούν με μερικές σειρές που περιλαμβάνουν πληροφορίες για το email document αποφάσισα να χρησιμοποιώ ως document το καθένα από την σειρά που αναφέρει “Lines :x” και κάτω

•	Data pre-processing
Η προεξεργασία των δεδομένων αποτελείται από τα εξής βήματα:
1.	Αφαίρεση punctuation με χρήση του string.punctuation
2.	Tokenization με την ntlk.word_tokenize() όπου χωρίζεται το έγγραφο σε λέξεις
3.	word.lower() για να αποφευχθούν τα κεφαλαία γράμματα και word.isalpha() για να αποφευχθούν λέξεις που περιέχουν χαρακτήρες που δεν είναι στο αγγλικό αλφάβητο
4.	Stemming με τον αλγόριθμο Porter έτσι ώστε να γίνει ένα απλό stemming για να ανιχνευθεί πιο εύκολα η ουσία των λέξεων και όχι κάθε αυτόνομη λέξη
5.	Αφαίρεση stop words μέσα από τα δεδομένα του ntlk
Preprocessed_text_data είναι μια λίστα python που κάθε στοιχείο της περιέχει τις λέξεις από ένα έγγραφο της συλλογής

•	Storing pre-processed data
Object serialization με το pickle για αποθήκευση των δεδομένων

•	Top-K words
Για την εύρεση Top-K words χρησιμοποιήθηκε το TF-IDF επειδή είναι απλό στον υπολογισμό και πιο effective σε σχέση με άλλα numerical statistics, με την TfidfVectorizer() από το sklearn

![image](https://user-images.githubusercontent.com/50420240/219849416-e8cfcc5f-a71b-454d-91f0-8c8265f4c5e5.png)

•	Apriori Association Rules
Για την εύρεση των association rules χρησιμοποιήθηκε η βιβλιοθήκη mlxtend.
Με το TransactionEncoder() μετατρέπουμε κάθε document σε ένα transaction με κάθε λέξη σαν ένα item. Έπειτα το μετατρέπουμε σε pandas dataframe για να εφαρμόσουμε τον αλγόριθμο Apriori για να παράγουμε τους κανόνες
Παρακάτω έχουμε τα αποτελέσματα με χρήση διαφορετικών support και confidence thresholds:

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


Παρατηρούμε ότι αυξάνοντας το support παίρνουμε μικρότερη συλλογή από κανόνες που μπορεί να κάνει την διαδικασία γρηγορότερη αλλά μπορεί να χάσουμε σημαντικές συσχετίσεις. Αυξάνοντας το confidence παίρνουμε μεγαλύτερη ακρίβεια στους κανόνες μας καθώς φαίνεται ότι η σχέση μεταξύ του αριστερού και δεξιού μέλους είναι ισχυρή, με κόστος όμως τον περιορισμό των δεδομένων.
Για παράδειγμα ο κανόνας would, write -> article έχει confidence=0.74, lift=1.69 που δείχνει ότι είναι από τους πιο ισχυρούς κανόνες αλλά λόγω του support=0.17 δεν εμφανίζεται στο τελευταίο run.
Επίσης παρατηρούμε οτι το articl -> write είναι ο πιο ισχυρός κανόνας. Αυτό συμβαίνει όμως επειδή πολλά έγγραφα περιέχουν τις εξής γραμμές:

![image](https://user-images.githubusercontent.com/50420240/219849468-f0eb22f4-fa2e-4556-8958-882279cc144e.png)


Επομένως αν αυτό δεν είναι επιθυμητό αποτέλεσμα, θα μπορούσε στο preprocessing να αφαιρείται αυτό το κομμάτι από κάθε έγγραφο.
