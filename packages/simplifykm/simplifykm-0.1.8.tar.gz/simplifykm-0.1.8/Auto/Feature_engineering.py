# import pandas as pd
# import numpy as np
# from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, MinMaxScaler

# class AutoClean:
#     def __init__(self, path: str):
#         self.df = pd.read_csv(path)
#         print(self.df)
#         print(f"✅ Data loaded successfully!")

#     def get_df(self):
#         return self.df.copy()

#     def handle_missing_values(self):
#         df = self.df.copy()
        
#         missing_value_percent = (df.isnull().sum() / len(df) * 100).reset_index()
#         missing_value_percent.columns = ["column", "missing_percent"]
#         print("Missing Values (%):")
#         print(missing_value_percent)
#         to_drop = missing_value_percent[missing_value_percent["missing_percent"] > 50]["column"].tolist()
#         df.drop(columns=to_drop, inplace=True)

#         num_cols = df.select_dtypes(include=["int64", "float64"]).columns
#         cat_cols = df.select_dtypes(include="object").columns
#         if len(num_cols) > 0:
#             df[num_cols] = SimpleImputer(strategy="mean").fit_transform(df[num_cols])
#         if len(cat_cols) > 0:
#             df[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df[cat_cols])
        
#         print("-"*40)
#         print(f"Dropped columns: {to_drop}")
#         print("-"*40)
#         print(df.isnull().sum())
#         print("✅ Missing value handling successful.")
#         self.df = df
#         return self

#     def encoding(self, encoding_type="label", ordinal_mapping=None, max_unique=10):
#         df = self.df.copy()
#         cat_cols = df.select_dtypes(include="object").columns

#         if encoding_type == "label":
#             for col in cat_cols:
#                 df[col] = LabelEncoder().fit_transform(df[col].astype(str))
#             print("✅ Label encoding applied.")

#         elif encoding_type == "onehot":
#             df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
#             print("✅ One-hot encoding applied.")

#         elif encoding_type == "ordinal":
#             if ordinal_mapping is None:
#                 ordinal_mapping = {
#                     col: sorted(df[col].dropna().unique())
#                     for col in cat_cols if df[col].nunique() <= max_unique
#                 }
#                 print("Auto ordinal mapping:")
#                 for col, order in ordinal_mapping.items():
#                     print(f"   {col}: {order}")

#             oe = OrdinalEncoder(categories=[ordinal_mapping[col] for col in ordinal_mapping])
#             df[list(ordinal_mapping.keys())] = oe.fit_transform(df[list(ordinal_mapping.keys())].astype(str))
#             print("✅ Ordinal encoding applied.")

#         else:
#             raise ValueError("❌ encoding_type must be 'label', 'onehot', or 'ordinal'")

#         self.df = df
#         return self

#     def handle_outliers(self, method="trim", threshold=1.5, show_boxplots=True, columns=None):
#         df = self.df.copy()
#         num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    
#         if columns:
#             invalid_cols = [col for col in columns if col not in num_cols]
#             if invalid_cols:
#                 raise ValueError(f"❌ Invalid numeric columns: {invalid_cols}")
#             num_cols = columns
    
#         if show_boxplots:
#             print("📊 Displaying boxplots for selected numerical features:")
#             for col in num_cols:
#                 plt.figure(figsize=(6, 4))
#                 sns.boxplot(x=df[col])
#                 plt.title(f"Boxplot for '{col}'")
#                 plt.xlabel(col)
#                 plt.show()
    
#         for col in num_cols:
#             Q1 = df[col].quantile(0.25)
#             Q3 = df[col].quantile(0.75)
#             IQR = Q3 - Q1
#             lower_bound = Q1 - threshold * IQR
#             upper_bound = Q3 + threshold * IQR
    
#             if method == "trim":
#                 before = df.shape[0]
#                 df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
#                 after = df.shape[0]
#                 print(f"✅ Trimmed outliers from '{col}': {before - after} rows dropped")
    
#             elif method == "cap":
#                 df[col] = df[col].apply(
#                     lambda x: lower_bound if x < lower_bound else upper_bound if x > upper_bound else x
#                 )
#                 print(f"✅ Capped outliers in '{col}' using IQR method.")
    
#             else:
#                 raise ValueError("❌ Method must be 'trim' or 'cap'.")
    
#         self.df = df
#         print("✅ Outlier handling completed.")
#         return self


# class Scaler:
#     def __init__(self, df, target_column):
#         self.df = df.copy()
#         self.target_column = target_column
#         self.X = self.df.drop(columns=[target_column])
#         self.y = self.df[target_column]
#         self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

#     def split(self, test_size=0.2, random_state=42):
#         self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
#             self.X, self.y, test_size=test_size, random_state=random_state
#         )
#         print(f"✅ Data split: {self.X_train.shape[0]} train rows, {self.X_test.shape[0]} test rows")
#         return self

#     def scaler(self, method="standard"):
#         if method == "standard":
#             scaler = StandardScaler()
#         elif method == "minmax":
#             scaler = MinMaxScaler()
#         else:
#             raise ValueError("❌ scaler type must be 'standard', or 'minmax'")

#         self.X_train = scaler.fit_transform(self.X_train)
#         self.X_test = scaler.transform(self.X_test)
#         print(f"✅ Applied {method} scaling")
#         return self

#     def get_data(self):
#         return self.X_train, self.X_test, self.y_train, self.y_test

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns


class AutoClean:
    def __init__(self, path: str):
        self.df = pd.read_csv(path)
        print(self.df.head())
        print(f"✅ Data loaded successfully!")

    def get_df(self):
        return self.df.copy()

    def handle_missing_values(self):
        df = self.df.copy()

        # Show % missing
        missing_value_percent = (df.isnull().sum() / len(df) * 100).reset_index()
        missing_value_percent.columns = ["column", "missing_percent"]
        print("🕳 Missing Values (%):")
        print(missing_value_percent)

        # Drop columns with >50% missing
        to_drop = missing_value_percent[missing_value_percent["missing_percent"] > 50]["column"].tolist()
        df.drop(columns=to_drop, inplace=True)

        # Impute numeric and categorical
        num_cols = df.select_dtypes(include=["int64", "float64"]).columns
        cat_cols = df.select_dtypes(include="object").columns

        if len(num_cols) > 0:
            df[num_cols] = SimpleImputer(strategy="mean").fit_transform(df[num_cols])

        if len(cat_cols) > 0:
            df[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df[cat_cols])

        print("-" * 40)
        print(f"🧹 Dropped columns: {to_drop}")
        print("🔍 Remaining nulls:")
        print(df.isnull().sum())
        print("✅ Missing value handling completed.")
        self.df = df
        return self

    def encoding(self, encoding_type="label", ordinal_mapping=None, max_unique=10):
        df = self.df.copy()
        cat_cols = df.select_dtypes(include="object").columns

        if encoding_type == "label":
            for col in cat_cols:
                df[col] = LabelEncoder().fit_transform(df[col].astype(str))
            print("✅ Label encoding applied.")

        elif encoding_type == "onehot":
            df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
            print("✅ One-hot encoding applied.")

        elif encoding_type == "ordinal":
            if ordinal_mapping is None:
                ordinal_mapping = {
                    col: sorted(df[col].dropna().unique())
                    for col in cat_cols if df[col].nunique() <= max_unique
                }
                print("ℹ️ Auto ordinal mapping:")
                for col, order in ordinal_mapping.items():
                    print(f"   {col}: {order}")

            oe = OrdinalEncoder(categories=[ordinal_mapping[col] for col in ordinal_mapping])
            df[list(ordinal_mapping.keys())] = oe.fit_transform(df[list(ordinal_mapping.keys())].astype(str))
            print("✅ Ordinal encoding applied.")

        else:
            raise ValueError("❌ encoding_type must be 'label', 'onehot', or 'ordinal'")

        self.df = df
        return self

    def handle_outliers(self, method="trim", threshold=1.5, show_boxplots=True, columns=None):
        df = self.df.copy()
        num_cols = df.select_dtypes(include=["int64", "float64"]).columns

        if columns:
            invalid_cols = [col for col in columns if col not in num_cols]
            if invalid_cols:
                raise ValueError(f"❌ Invalid numeric columns: {invalid_cols}")
            num_cols = columns

        if show_boxplots:
            print("📊 Displaying boxplots for numerical features:")
            for col in num_cols:
                plt.figure(figsize=(6, 4))
                sns.boxplot(x=df[col])
                plt.title(f"Boxplot for '{col}'")
                plt.xlabel(col)
                plt.show()

        for col in num_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            if method == "trim":
                before = df.shape[0]
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
                after = df.shape[0]
                print(f"✅ Trimmed outliers from '{col}': {before - after} rows removed")

            elif method == "cap":
                df[col] = df[col].apply(
                    lambda x: lower_bound if x < lower_bound else upper_bound if x > upper_bound else x
                )
                print(f"✅ Capped outliers in '{col}' using IQR method.")

            else:
                raise ValueError("❌ Method must be 'trim' or 'cap'.")

        self.df = df
        print("✅ Outlier handling completed.")
        return self


class Scaler:
    def __init__(self, df, target_column):
        # ✅ Fix: allow AutoClean object too
        if hasattr(df, "get_df"):
            df = df.get_df()
        self.df = df.copy()
        self.target_column = target_column
        self.X = self.df.drop(columns=[target_column])
        self.y = self.df[target_column]
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def split(self, test_size=0.2, random_state=42):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state
        )
        print(f"✅ Data split: {self.X_train.shape[0]} train rows, {self.X_test.shape[0]} test rows")
        return self

    def scaler(self, method="standard"):
        if method == "standard":
            scaler = StandardScaler()
        elif method == "minmax":
            scaler = MinMaxScaler()
        else:
            raise ValueError("❌ scaler type must be 'standard' or 'minmax'")

        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)
        print(f"✅ Applied {method} scaling")
        return self

    def get_data(self):
        return self.X_train, self.X_test, self.y_train, self.y_test
