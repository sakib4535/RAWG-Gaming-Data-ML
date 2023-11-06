import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import f_oneway
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer


data = pd.read_excel('game_data_new.xlsx')

X = data[['reviews_text_count', 'metacritic', 'playtime', 'suggestions_count']]
y = data['rating']



print("Basic Information about the Dataset:")
print(data.info())


print("\nSample Data (first 5 rows):")
print(data.head())


print("\nMissing Values:")
print(data.isnull().sum())


##########################################################################


# Handling missing values using a simple imputer
X = X.replace([np.inf, -np.inf], np.nan)
X = X.dropna()


X = sm.add_constant(X)


model = sm.OLS(y[X.index], X).fit()
summary = model.summary()




# Calculate Mean Squared Error (MSE)
y_pred = model.predict(X)
mse = mean_squared_error(y[X.index], y_pred)

# Chi-Square Test
contingency_table = pd.crosstab(data['reviews_text_count'], data['playtime'])
chi2, p, _, _ = chi2_contingency(contingency_table)

# ANOVA Test
groups = data.groupby('metacritic')['suggestions_count'].apply(list)
f_statistic, p_value = f_oneway(*groups)



# Print the results
print("Summary Statistics:")
print(summary)
print("\nMean Squared Error (MSE):", mse)
print("\nChi-Square Test (reviews_text_count vs. playtime):")
print("Chi-Square Value:", chi2)
print("p-value:", p)
print("\nANOVA Test (metacritic vs. suggestions_count):")
print("F-statistic:", f_statistic)
print("p-value:", p_value)



# Convert the 'released' column to datetime
data['released'] = pd.to_datetime(data['released'])

# EDA: Create visualizations

# Distribution of Ratings
plt.figure(figsize=(12, 6))
sns.histplot(data['rating'], bins=20, kde=True)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

# Correlation heatmap
correlation_matrix = data.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

# Scatter plot of Metacritic vs. Ratings
plt.figure(figsize=(10, 6))
sns.scatterplot(x='metacritic', y='rating', data=data)
plt.title('Scatter Plot of Metacritic vs. Ratings')
plt.xlabel('Metacritic Score')
plt.ylabel('Rating')
plt.show()

# Pairplot to visualize relationships between numerical variables
sns.pairplot(data[['rating', 'reviews_text_count', 'metacritic', 'playtime', 'suggestions_count']])
plt.suptitle('Pairplot of Numerical Variables')
plt.show()




X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train = X_train.dropna()
y_train = y_train[X_train.index]  # Update y_train accordingly
X_test = X_test.dropna()
y_test = y_test[X_test.index]  # Update y_test accordingly

# Replace missing values with the mean of each column
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)



rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)


dt_regressor = DecisionTreeRegressor(random_state=42)
dt_regressor.fit(X_train, y_train)


rf_predictions = rf_regressor.predict(X_test)
dt_predictions = dt_regressor.predict(X_test)


def evaluate_model(predictions, model_name):
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f'{model_name} Model:')
    print(f'Mean Squared Error (MSE): {mse:.2f}')
    print(f'R-squared (R2) Score: {r2:.2f}\n')


def create_model_visualizations(model, model_name):
    feature_names = list(X.columns)
    feature_importances = model.feature_importances_

    # Feature Importances Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importances, y=feature_names)
    plt.title(f'{model_name} - Feature Importances')
    plt.xlabel('Feature Importance')
    plt.ylabel('Features')
    plt.show()

    # Actual vs. Predicted Plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_test, y=rf_predictions)
    plt.title(f'{model_name} - Actual vs. Predicted Ratings')
    plt.xlabel('Actual Ratings')
    plt.ylabel('Predicted Ratings')
    plt.show()

# Visualizations for Random Forest
create_model_visualizations(rf_regressor, 'Random Forest')

# Visualizations for Decision Tree
create_model_visualizations(dt_regressor, 'Decision Tree')