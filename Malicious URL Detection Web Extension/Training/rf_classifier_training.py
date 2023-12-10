import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

df = pd.read_csv('Malicious URL Detection Web Extension/Dataset/Dataset_Features.csv')

#Assigning features and target variable
X = df.drop(['label', 'url'], axis=1)
y = df['label']

#Splitting training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Training classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

#Make predictions
y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Random Forest - Model Accuracy:", accuracy)
print("Random Forest - Classification Report:\n", report)
print("Random Forest - Confusion Matrix:\n", conf_matrix)

joblib.dump(rf_classifier, 'rf_model.pkl')