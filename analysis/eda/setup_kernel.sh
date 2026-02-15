#!/bin/bash
# Setup script for Datathon EDA Template
# This creates a conda environment and registers it as a Jupyter kernel

echo "Creating conda environment for Datathon EDA..."
conda create -n datathon-eda python=3.9 -y

echo "Activating environment..."
source activate datathon-eda

echo "Installing required packages..."
pip install pandas numpy matplotlib seaborn scipy jupyter ipykernel

echo "Registering kernel with Jupyter..."
python -m ipykernel install --user --name datathon-eda --display-name "Python 3 (Datathon EDA)"

echo "✓ Setup complete!"
echo ""
echo "To use this kernel:"
echo "1. Open the notebook in Jupyter"
echo "2. Go to Kernel > Change Kernel > Python 3 (Datathon EDA)"
echo ""
echo "Or activate the environment and run:"
echo "  conda activate datathon-eda"
echo "  jupyter notebook"

