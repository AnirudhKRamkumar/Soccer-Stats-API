import sklearn, matplotlib
import pandas as pd
import sklearn.model_selection

df = pd.read_csv('EUR_gca_2023-2024_individual.csv')
df2 = pd.read_csv('EUR_defense_2023-2024_individual.csv')
df3 = pd.read_csv('EUR_shooting_2023-2024_individual.csv')
df4 = pd.read_csv('EUR_passing_types_2023-2024_individual.csv')

# pd.set_option('display.max_columns', 23)

df = pd.concat([df, df2, df3, df4])

df = df.drop(columns=['Player', 'Comp', 'Nation', 'Squad', 'Age', '90s']).rename(columns={"Types PassLive": "SCA PassLive", "Types PassDead": "SCA PassDead", "Types TO": "SCA TO", "Types Sh": "SCA Sh", "Types Fld": "SCA Fld", "Types Def": "SCA Def", "Types PassLive.1": "GCA PassLive", "Types PassDead.1": "GCA PassDead", "Types TO.1": "GCA TO", "Types Sh.1": "GCA Sh", "Types Fld.1": "GCA Fld", "Types Def.1": "GCA Def"})
df["Position 2"] = df['Position 2'].fillna("None")

# print(df.head)

le = sklearn.preprocessing.LabelEncoder()
print(df.columns.tolist())
uniquevals = df["Position 1"].unique()
le.fit(uniquevals)
le.transform(uniquevals)

encoder = sklearn.preprocessing.OneHotEncoder(sparse_output=False, handle_unknown='ignore')
pos2_encoded = encoder.fit_transform(df[["Position 2"]])
encoded_columns = encoder.get_feature_names_out(["Position 2"])
pos2_df = pd.DataFrame(pos2_encoded, columns=encoded_columns, index=df.index)
df = pd.concat([df, pos2_df], axis=1)
df = df.drop(columns=["Position 2"])

Xcol = df.columns.drop("Position 1").tolist()
X = pd.concat([df[Xcol], pos2_df], axis=1)
y = df["Position 1"]


# pd.reset_option('display.max_columns')
Xtrain, Xtest, ytrain, ytest = sklearn.model_selection.train_test_split(X, y, test_size=0.25, random_state=42)
print(Xtrain, Xtest, ytrain, ytest)
hgbclassifier = sklearn.ensemble.HistGradientBoostingClassifier(random_state=42, max_depth=None, class_weight='balanced')
hgbclassifier.fit(Xtrain, ytrain)

predictions = hgbclassifier.predict(Xtest)

print(predictions)

accuracy = sklearn.metrics.accuracy_score(ytest, predictions)
print(f"Accuracy: {accuracy:.2f}")
print(sklearn.metrics.confusion_matrix(ytest, predictions, normalize='true'))

