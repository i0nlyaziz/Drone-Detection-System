# Model Weights

The trained weights aren't committed to this repo directly — they're excluded in `.gitignore` since `.pt` files are large.

## Download

- **best.pt** — [Download from Releases](https://github.com/i0nlyaziz/Drone-Detection-System/releases/download/v1.0/best.pt)

## Using the weights

1. Download `best.pt` from the link above and place it in this `weights/` folder.
2. `main.py` loads `best.pt` directly — no export step is required.
3. Update the model path in `main.py` if you place the file somewhere other than `weights/`.`.