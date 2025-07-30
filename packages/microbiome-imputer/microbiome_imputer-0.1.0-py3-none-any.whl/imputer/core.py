import numpy as np
import pandas as pd
import tensorflow as tf
import json
import os

def load_feature_categories(json_path):
    with open(json_path, "r") as f:
        feature_dict = json.load(f)
    return feature_dict["low_features"], feature_dict["high_features"]

def impute_category_features(model, data_subset):
    if data_subset.shape[1] == 0:
        return data_subset
    imputed = model.predict(data_subset)
    imputed[imputed < 0] = 0
    return pd.DataFrame(imputed, columns=data_subset.columns, index=data_subset.index)

def run_imputation(input_csv, output_csv, base_path):
    feature_json = os.path.join(base_path, "feature_categories.json")
    model_low_path = os.path.join(base_path, "models", "dae_model_low.h5")
    model_high_path = os.path.join(base_path, "models", "dae_model_high.h5")

    low_features, high_features = load_feature_categories(feature_json)

    test_data = pd.read_csv(input_csv)
    test_data.set_index("sample_id", inplace=True)
    original_features = test_data.columns.tolist()
    all_expected_features = set(low_features + high_features)

    for feature in all_expected_features:
        if feature not in test_data.columns:
            test_data[feature] = 0.0

    test_data = test_data[list(test_data.columns)]
    test_data = np.log1p(test_data)

    dae_low = tf.keras.models.load_model(model_low_path)
    dae_high = tf.keras.models.load_model(model_high_path)

    imputed_low = impute_category_features(dae_low, test_data[low_features])
    imputed_high = impute_category_features(dae_high, test_data[high_features])
    untouched = [f for f in original_features if f not in (low_features + high_features)]
    untouched_df = test_data[untouched]

    final_df = pd.concat([imputed_low, imputed_high, untouched_df], axis=1)
    final_df = final_df[original_features]
    final_df = np.expm1(final_df)

    final_df.to_csv(output_csv)
    print(f"✅ Imputed data saved to {output_csv}")
