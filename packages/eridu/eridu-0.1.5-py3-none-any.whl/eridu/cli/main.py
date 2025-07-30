"""Main CLI module for Eridu."""

import os
from collections import OrderedDict
from importlib import import_module
from pathlib import Path

import click
import pandas as pd
import requests
from tqdm import tqdm


class OrderedGroup(click.Group):
    """Custom Click Group that maintains order of commands in help."""

    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        self.commands = OrderedDict()

    def list_commands(self, ctx):
        """Return commands in the order they were added."""
        return self.commands.keys()


@click.group(cls=OrderedGroup)
@click.version_option()
def cli() -> None:
    """Eridu: Fuzzy matching people and company names for entity resolution using representation learning"""
    pass


@cli.command()
@click.option(
    "--url",
    default="https://storage.googleapis.com/data.opensanctions.org/contrib/sample/pairs-all.csv.gz",
    show_default=True,
    help="URL to download the pairs gzipped CSV file from",
)
@click.option(
    "--output-dir",
    default="./data",
    show_default=True,
    help="Directory to save the downloaded and extracted files",
)
def download(url: str, output_dir: str) -> None:
    """Download and convert the labeled entity pairs CSV file to Parquet format."""
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Get filename from URL
    filename = url.split("/")[-1]
    gz_path = output_dir_path / filename

    # Step 1: Download the file
    click.echo(f"Downloading {url} to {gz_path}")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))

    with open(gz_path, "wb") as f:
        with tqdm(total=total_size, unit="B", unit_scale=True, desc=filename) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

    # Step 2: Read the gzipped CSV directly and convert to Parquet
    click.echo(f"Reading gzipped CSV file: {gz_path}")
    try:
        # Pandas automatically detects and handles gzipped files
        df = pd.read_csv(gz_path, compression="gzip")
        click.echo(f"Successfully parsed CSV. Shape: {df.shape}")
        click.echo(f"Columns: {', '.join(df.columns)}")
        # Create Parquet file
        parquet_path = output_dir_path / filename.replace(".csv.gz", ".parquet")
        click.echo(f"Converting to Parquet: {parquet_path}")
        df.to_parquet(parquet_path, index=False)
        click.echo(f"Successfully created Parquet file: {parquet_path}")
        # Display basic info about the data
        click.echo("Data sample (first 5 rows):")
        click.echo(df.head(5))
    except Exception as e:
        click.echo(f"Error processing CSV: {e}")
        raise

    click.echo("Download and conversion to Parquet completed successfully.")
    click.echo("\nTo generate a report on this data, run:")
    click.echo(f"  eridu etl report --parquet-path {parquet_path}")


@cli.group()
def etl() -> None:
    """ETL commands for data processing."""
    pass


@etl.command(name="report")
@click.option(
    "--parquet-path",
    default="./data/pairs-all.parquet",
    show_default=True,
    help="Path to the Parquet file to analyze (default is the output from 'eridu download')",
)
@click.option(
    "--truncate",
    default=20,
    show_default=True,
    help="Truncation limit for string display",
)
def etl_report(parquet_path: str, truncate: int) -> None:
    """Generate a report on entity pairs data."""
    from eridu.etl.report import generate_pairs_report

    generate_pairs_report(parquet_path, truncate)


@cli.command(name="train")
@click.option(
    "--model",
    default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    show_default=True,
    help="Base SBERT model to fine-tune",
)
@click.option(
    "--sample-fraction",
    default=0.01,
    show_default=True,
    help="Fraction of data to sample for training (1.0 = use all data)",
)
@click.option("--batch-size", default=1024, show_default=True, help="Batch size for training")
@click.option("--epochs", default=10, show_default=True, help="Number of training epochs")
@click.option(
    "--patience",
    default=2,
    show_default=True,
    help="Early stopping patience (number of evaluation steps without improvement)",
)
@click.option(
    "--resampling/--no-resampling",
    default=True,
    show_default=True,
    help="Resample training data for each epoch when sample_fraction < 1.0",
)
@click.option(
    "--fp16/--no-fp16", default=False, show_default=True, help="Use mixed precision training (fp16)"
)
@click.option(
    "--quantization/--no-quantization",
    default=False,
    show_default=True,
    help="Apply quantization to Linear layers (reduces precision to save memory)",
)
@click.option(
    "--use-gpu/--no-gpu",
    default=True,
    show_default=True,
    help="Whether to use GPU for training and inference (if available)",
)
@click.option(
    "--wandb-project",
    default="eridu",
    show_default=True,
    help="Weights & Biases project name for tracking",
)
@click.option(
    "--wandb-entity",
    default="rjurney",
    show_default=True,
    help="Weights & Biases entity (username or team name)",
)
@click.option(
    "--gradient-checkpointing/--no-gradient-checkpointing",
    default=False,
    show_default=True,
    help="Enable gradient checkpointing to save memory at the cost of computation time",
)
@click.option(
    "--weight-decay",
    default=0.01,
    show_default=True,
    help="Weight decay (L2 regularization) to prevent overfitting",
)
@click.option(
    "--random-seed",
    default=31337,
    show_default=True,
    help="Random seed for reproducibility across all frameworks",
)
@click.option(
    "--warmup-ratio",
    default=0.1,
    show_default=True,
    help="Ratio of training steps for learning rate warmup",
)
@click.option(
    "--save-strategy",
    type=click.Choice(["steps", "epoch", "no"]),
    default="steps",
    show_default=True,
    help="Strategy to save model checkpoints during training",
)
@click.option(
    "--eval-strategy",
    type=click.Choice(["steps", "epoch", "no"]),
    default="steps",
    show_default=True,
    help="Strategy to evaluate model during training",
)
@click.option(
    "--learning-rate",
    default=3e-5,
    show_default=True,
    help="Learning rate for optimizer",
)
def train(
    model: str,
    sample_fraction: float,
    batch_size: int,
    epochs: int,
    patience: int,
    resampling: bool,
    fp16: bool,
    quantization: bool,
    use_gpu: bool,
    wandb_project: str,
    wandb_entity: str,
    gradient_checkpointing: bool,
    weight_decay: float,
    random_seed: int,
    warmup_ratio: float,
    save_strategy: str,
    eval_strategy: str,
    learning_rate: float,
) -> None:
    """Fine-tune a sentence transformer (SBERT) model for entity matching."""
    # Validate that FP16 and quantization are not both enabled
    if fp16 and quantization:
        raise click.UsageError(
            "Error: Cannot use both FP16 and quantization together. Please choose only one option."
        )

    click.echo(f"Fine-tuning SBERT model: {model}")
    click.echo(f"Sample fraction: {sample_fraction}")
    click.echo(f"Batch size: {batch_size}")
    click.echo(f"Epochs: {epochs}")
    click.echo(f"Early stopping patience: {patience}")
    if sample_fraction < 1.0:
        click.echo(f"Resampling per epoch: {resampling}")
    click.echo(f"FP16: {fp16}")
    click.echo(f"Quantization: {quantization}")
    click.echo(f"Use GPU: {use_gpu}")
    click.echo(f"Gradient checkpointing: {gradient_checkpointing}")
    click.echo(f"Weight decay: {weight_decay}")
    click.echo(f"Random seed: {random_seed}")
    click.echo(f"Warmup ratio: {warmup_ratio}")
    click.echo(f"Save strategy: {save_strategy}")
    click.echo(f"Eval strategy: {eval_strategy}")
    click.echo(f"Learning rate: {learning_rate}")
    click.echo(f"W&B Project: {wandb_project}")
    click.echo(f"W&B Entity: {wandb_entity}")

    # Set environment variables based on CLI options
    os.environ["SBERT_MODEL"] = model
    os.environ["SAMPLE_FRACTION"] = str(sample_fraction)
    os.environ["BATCH_SIZE"] = str(batch_size)
    os.environ["EPOCHS"] = str(epochs)
    os.environ["PATIENCE"] = str(patience)
    os.environ["USE_RESAMPLING"] = "true" if resampling else "false"
    os.environ["WEIGHT_DECAY"] = str(weight_decay)
    os.environ["RANDOM_SEED"] = str(random_seed)
    os.environ["WARMUP_RATIO"] = str(warmup_ratio)
    os.environ["SAVE_STRATEGY"] = save_strategy
    os.environ["EVAL_STRATEGY"] = eval_strategy
    os.environ["LEARNING_RATE"] = str(learning_rate)
    os.environ["WANDB_PROJECT"] = wandb_project
    os.environ["WANDB_ENTITY"] = wandb_entity
    os.environ["USE_GPU"] = "true" if use_gpu else "false"

    # Set fp16 environment variable (default is False)
    os.environ["USE_FP16"] = "true" if fp16 else "false"

    # Set quantization environment variable (default is False)
    os.environ["USE_QUANTIZATION"] = "true" if quantization else "false"

    # Set gradient checkpointing environment variable
    os.environ["USE_GRADIENT_CHECKPOINTING"] = "true" if gradient_checkpointing else "false"

    # Import the fine_tune_sbert module here to avoid circular imports and run the module
    fine_tune_module = import_module("eridu.train.fine_tune_sbert")
    fine_tune_module.main()


@cli.command()
@click.argument("name1", type=str)
@click.argument("name2", type=str)
@click.option(
    "--model-path",
    default="data/fine-tuned-sbert-sentence-transformers-paraphrase-multilingual-MiniLM-L12-v2-original-adafactor",
    show_default=True,
    help="Path to the fine-tuned SentenceTransformer model directory",
)
@click.option(
    "--use-gpu/--no-gpu",
    default=True,
    show_default=True,
    help="Whether to use GPU acceleration for inference",
)
def compare(name1: str, name2: str, model_path: str, use_gpu: bool) -> None:
    """Compare two names using the fine-tuned SentenceTransformer model.

    Computes the similarity score between NAME1 and NAME2 using
    the specified SBERT model with optional GPU acceleration.

    Example: eridu compare "John Smith" "Jon Smith"
    """
    from eridu.etl.compare import compare_names

    similarity, success = compare_names(name1, name2, model_path, use_gpu)

    if not success:
        click.echo(f"Error: Could not load model from '{model_path}'.")
        click.echo("Please specify a valid model path with --model-path or train a model first.")
        return

    # Print the similarity score rounded to 3 decimal places
    click.echo(f"{similarity:.3f}")


if __name__ == "__main__":
    cli()
