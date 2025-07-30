import argparse
import os
from .core import run_imputation

def main():
    parser = argparse.ArgumentParser(description="Microbiome Imputation Tool")
    parser.add_argument("input", help="Path to input CSV file with microbiome data")
    parser.add_argument("output", help="Path to save the imputed output CSV")

    args = parser.parse_args()
    base_path = os.path.dirname(__file__)
    run_imputation(args.input, args.output, base_path)
