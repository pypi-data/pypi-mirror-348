import pandas as pd
import numpy as np
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

def run_imputation(input_file, output_file, base_path):
    test_data = pd.read_csv(input_file)
    test_data.set_index("sample_id", inplace=True)

    original_features = test_data.columns.tolist()

    feature_json = os.path.join(base_path, "feature_categories.json")
    model_low_path = os.path.join(base_path, "models", "dae_model_low.h5")
    model_high_path = os.path.join(base_path, "models", "dae_model_high.h5")

    low_features, high_features = load_feature_categories(feature_json)
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
    untouched_features = [f for f in original_features if f not in (low_features + high_features)]
    untouched_df = test_data[untouched_features]

    final_imputed_df = pd.concat([imputed_low, imputed_high, untouched_df], axis=1)
    final_imputed_df = final_imputed_df[original_features]
    final_imputed_df = np.expm1(final_imputed_df)

    final_imputed_df.to_csv(output_file)
    print("✅ Final imputed data saved to:", output_file)
