"""
Main entry point for the project.

This script provides a command-line interface for running
training, evaluation, and inference tasks.
"""

import argparse
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

from src.data import load_data
from src.model import create_model
from src.train import train_model
from src.evaluate import evaluate_model


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="${project_name} - AI model training and evaluation"
    )
    
    parser.add_argument(
        "--mode",
        choices=["train", "evaluate", "infer"],
        default="train",
        help="Operation mode: train, evaluate, or infer"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config.yaml",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
        help="Directory containing the dataset"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save outputs"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the script."""
    args = parse_args()
    
    print(f"Running in {args.mode} mode")
    print(f"Using config: {args.config}")
    print(f"Data directory: {args.data_dir}")
    print(f"Output directory: {args.output_dir}")
    
    # Load data
    train_data, val_data = load_data(args.data_dir)
    
    # Create model
    model = create_model()
    
    if args.mode == "train":
        # Train model
        train_model(model, train_data, val_data, args.output_dir)
    elif args.mode == "evaluate":
        # Evaluate model
        metrics = evaluate_model(model, val_data)
        print(f"Evaluation metrics: {metrics}")
    elif args.mode == "infer":
        # Inference mode (to be implemented)
        print("Inference mode not yet implemented")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
