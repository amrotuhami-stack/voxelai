#!/usr/bin/env python3
"""
Train CEPHMark-Net on Unified Cephalometric Dataset

Usage:
    python train_cephalometric.py --epochs 100 --backbone resnet50
    python train_cephalometric.py --resume --weights logs/weights/best_weights.h5
"""

import os
import sys
import argparse
from pathlib import Path

# Add CEPHMark-Net to path
CEPHMARK_DIR = Path(__file__).parent / "models" / "CEPHMark-Net"
sys.path.insert(0, str(CEPHMARK_DIR))

def main():
    parser = argparse.ArgumentParser(description="Train CEPHMark-Net on unified cephalometric dataset")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size")
    parser.add_argument("--backbone", type=str, default="resnet50", 
                        choices=["resnet50", "resnet34", "resnet18", "vgg16", "vgg19", "darknet53"],
                        help="Backbone network")
    parser.add_argument("--lr", type=float, default=0.0001, help="Learning rate")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    parser.add_argument("--weights", type=str, default=None, help="Path to weights for resume")
    parser.add_argument("--dataset", type=str, default=None, help="Path to dataset")
    
    args = parser.parse_args()
    
    # Import TensorFlow
    import tensorflow as tf
    print(f"TensorFlow version: {tf.__version__}")
    print(f"GPU available: {len(tf.config.list_physical_devices('GPU')) > 0}")
    
    # Update config
    from config import cfg
    cfg.NUM_LANDMARKS = 19  # Unified 19 landmarks
    cfg.TRAIN.EPOCHS = args.epochs
    cfg.TRAIN.OPTIMIZER = tf.keras.optimizers.Adam(learning_rate=args.lr)
    
    # Set dataset path
    if args.dataset:
        dataset_path = args.dataset
    else:
        dataset_path = str(Path(__file__).parent / "datasets" / "cephalometric_unified")
    
    print("\n" + "="*60)
    print("CEPHALOMETRIC LANDMARK DETECTION TRAINING")
    print("="*60)
    print(f"\nDataset: {dataset_path}")
    print(f"Backbone: {args.backbone}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print(f"Learning rate: {args.lr}")
    print(f"Landmarks: {cfg.NUM_LANDMARKS}")
    
    # Load unified dataset
    from data.unified_dataset import Dataset
    
    train_data = Dataset(
        name="unified", 
        mode="train", 
        batch_size=args.batch_size, 
        shuffle=True,
        dataset_path=dataset_path
    )
    
    val_data = Dataset(
        name="unified", 
        mode="val", 
        batch_size=args.batch_size, 
        shuffle=False,
        dataset_path=dataset_path
    )
    
    print(f"\nTrain batches: {len(train_data)}")
    print(f"Val batches: {len(val_data)}")
    
    # Create network
    from network.model import Network
    
    network = Network(
        backbone_name=args.backbone,
        freeze_backbone=False,
        backbone_weights="imagenet" if not args.resume else None
    )
    
    # Load weights if resuming
    if args.resume and args.weights:
        print(f"\nLoading weights from: {args.weights}")
        network.model.load_weights(args.weights)
    
    # Create output directory
    output_dir = CEPHMARK_DIR / "logs" / "unified_19landmarks"
    output_dir.mkdir(parents=True, exist_ok=True)
    weights_dir = output_dir / "weights"
    weights_dir.mkdir(parents=True, exist_ok=True)
    
    # Training
    from train import train
    from valid import valid
    from utils import save_statistics
    from paths import Paths
    
    # Override paths
    Paths.logs_root_path = str(output_dir)
    
    print("\n" + "="*60)
    print("STARTING TRAINING...")
    print("="*60 + "\n")
    
    best_mre = float('inf')
    
    for epoch in range(1, args.epochs + 1):
        print(f"\n{'='*40}")
        print(f"Epoch {epoch}/{args.epochs}")
        print(f"{'='*40}")
        
        # Train
        train_data.dataset.shuffle()
        from train import train_on_batch
        train_stats = train_on_batch(train_data, network, cfg.TRAIN.OPTIMIZER)
        train_results = tf.reduce_mean(tf.stack(train_stats), axis=0)
        
        train_mre = float(train_results[cfg.NUM_LANDMARKS + 1])
        print(f"\n[Train] MRE: {train_mre:.3f}mm")
        
        # Validate every 5 epochs
        if epoch % 5 == 0 or epoch == 1:
            from valid import valid_on_batch
            val_stats = valid_on_batch(val_data, network)
            val_results = tf.reduce_mean(tf.stack(val_stats), axis=0)
            val_mre = float(val_results[cfg.NUM_LANDMARKS])
            print(f"[Val] MRE: {val_mre:.3f}mm")
            
            # Save best model
            if val_mre < best_mre:
                best_mre = val_mre
                network.model.save_weights(str(weights_dir / "best_weights.h5"))
                print(f"✅ New best model saved! MRE: {val_mre:.3f}mm")
        
        # Save checkpoint every 10 epochs
        if epoch % 10 == 0:
            network.model.save_weights(str(weights_dir / f"epoch_{epoch}.h5"))
            print(f"💾 Checkpoint saved: epoch_{epoch}.h5")
    
    # Save final model
    network.model.save_weights(str(weights_dir / "final_weights.h5"))
    print(f"\n✅ Training complete! Best MRE: {best_mre:.3f}mm")
    print(f"Weights saved to: {weights_dir}")


if __name__ == "__main__":
    main()
