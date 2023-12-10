import pandas as pd
import joblib

from config import rf_model_path, lr_model_path, xgb_model_path

feature_names = [
    'count_specialchar',
    'count_sensitive_words',
    'using_shortener',
    'has_at_symbol',
    'count_double_slash',
    'count_dash_symbol',
    'count_multiple_subdomains',
    'url_length',
    'https',
    'contains_ip_address',
    'url_entropy',
    'numchar_classification'
]

rf_model = joblib.load(rf_model_path)
xgb_model = joblib.load(xgb_model_path)
lr_model = joblib.load(lr_model_path)

#RF
rf_feature_importances = rf_model.feature_importances_

#XGB
xgb_feature_importances = xgb_model.feature_importances_

#LF
lr_coefficients = lr_model.coef_[0]
total_lr_importance = abs(lr_coefficients).sum()
normalized_lr_coefficients = abs(lr_coefficients) / total_lr_importance

rf_feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance (Random Forest)': rf_feature_importances})
xgb_feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance (XGBoost)': xgb_feature_importances})
normalized_lr_feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Normalized Coefficient (Logistic Regression)': normalized_lr_coefficients})

#Merge
final_df = rf_feature_importance_df.merge(xgb_feature_importance_df, on='Feature').merge(normalized_lr_feature_importance_df, on='Feature')

#Sort
final_df = final_df.sort_values(by=['Importance (Random Forest)', 'Importance (XGBoost)', 'Normalized Coefficient (Logistic Regression)'], ascending=False)

final_df.to_csv('Feature Importance.csv', index=False)
