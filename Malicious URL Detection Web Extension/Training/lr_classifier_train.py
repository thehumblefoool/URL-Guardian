import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

df = pd.read_csv('Malicious URL Detection Web Extension/Dataset/Dataset_Features.csv')

#Assigning features and target variable
X = df.drop(['label', 'url'], axis=1)
y = df['label']

#Splitting training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Training classifier
logistic_classifier = LogisticRegression(random_state=42)
logistic_classifier.fit(X_train, y_train)

#Make predictions
y_pred_lr = logistic_classifier.predict(X_test)

accuracy_lr = accuracy_score(y_test, y_pred_lr)
report_lr = classification_report(y_test, y_pred_lr)
conf_matrix_lr = confusion_matrix(y_test, y_pred_lr)

print("Logistic Regression - Model Accuracy:", accuracy_lr)
print("Logistic Regression - Classification Report:\n", report_lr)
print("Logistic Regression - Confusion Matrix:\n", conf_matrix_lr)

joblib.dump(logistic_classifier, 'lr_model.pkl')
