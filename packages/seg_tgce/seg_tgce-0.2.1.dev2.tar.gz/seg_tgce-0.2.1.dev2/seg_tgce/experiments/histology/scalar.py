import keras_tuner as kt
from keras.optimizers import Adam
from seg_tgce.data.crowd_seg.generator import (
    CrowdSegDataGenerator,
    DataSchema,
    Stage,
)
from seg_tgce.experiments.plot_utils import plot_training_history, print_test_metrics
from seg_tgce.loss.tgce import TcgeScalar
from seg_tgce.metrics import DiceCoefficient, JaccardCoefficient
from seg_tgce.models.ma_model import ScalarVisualizationCallback
from seg_tgce.models.unet import unet_tgce_scalar

TARGET_SHAPE = (64, 64)
BATCH_SIZE = 64
NUM_CLASSES = 6  # From CLASSES_DEFINITION in generator.py
TRAIN_EPOCHS = 50
TUNER_EPOCHS = 10
GROUND_TRUTH_INDEX = -1  # expert labeler
N_SCORERS = 24


def build_model(hp):
    learning_rate = hp.Float(
        "learning_rate", min_value=1e-5, max_value=1e-2, sampling="LOG"
    )
    q = hp.Float("q", min_value=0.1, max_value=0.9, step=0.1)
    noise_tolerance = hp.Float(
        "noise_tolerance", min_value=0.1, max_value=0.9, step=0.1
    )
    lambda_reg_weight = hp.Float(
        "lambda_reg_weight", min_value=0.01, max_value=0.2, step=0.01
    )
    lambda_entropy_weight = hp.Float(
        "lambda_entropy_weight", min_value=0.01, max_value=0.2, step=0.01
    )
    lambda_sum_weight = hp.Float(
        "lambda_sum_weight", min_value=0.01, max_value=0.2, step=0.01
    )

    optimizer = Adam(learning_rate=learning_rate)

    loss_fn = TcgeScalar(
        num_classes=NUM_CLASSES,
        q=q,
        noise_tolerance=noise_tolerance,
        lambda_reg_weight=lambda_reg_weight,
        lambda_entropy_weight=lambda_entropy_weight,
        lambda_sum_weight=lambda_sum_weight,
        name="TGCE",
    )

    dice_fn = DiceCoefficient(
        num_classes=NUM_CLASSES,
        name="dice_coefficient",
        ground_truth_index=GROUND_TRUTH_INDEX,
    )
    jaccard_fn = JaccardCoefficient(
        num_classes=NUM_CLASSES,
        name="jaccard_coefficient",
        ground_truth_index=GROUND_TRUTH_INDEX,
    )

    model = unet_tgce_scalar(
        input_shape=TARGET_SHAPE + (3,),
        n_classes=NUM_CLASSES,
        n_scorers=N_SCORERS,
        name="Unet-TGCE-Scalar-Model",
    )

    model.compile(
        loss=loss_fn,
        metrics={"segmentation_output": [dice_fn, jaccard_fn]},
        optimizer=optimizer,
    )
    model.loss_fn = loss_fn
    return model


if __name__ == "__main__":
    # Create data generators for each stage
    train_gen = CrowdSegDataGenerator(
        image_size=TARGET_SHAPE,
        batch_size=BATCH_SIZE,
        shuffle=True,
        stage=Stage.TRAIN,
        schema=DataSchema.MA_RAW,
        use_cache=True,
        cache_size=5000,
    )
    val_gen = CrowdSegDataGenerator(
        image_size=TARGET_SHAPE,
        batch_size=BATCH_SIZE,
        shuffle=False,
        stage=Stage.VAL,
        schema=DataSchema.MA_RAW,
        use_cache=True,
        cache_size=1000,
    )
    test_gen = CrowdSegDataGenerator(
        image_size=TARGET_SHAPE,
        batch_size=BATCH_SIZE,
        shuffle=False,
        stage=Stage.TEST,
        schema=DataSchema.MA_RAW,
        use_cache=True,
        cache_size=500,
    )

    # Update model's n_scorers based on the generator
    n_scorers = train_gen.n_scorers

    tuner = kt.BayesianOptimization(
        build_model,
        objective=kt.Objective(
            "val_segmentation_output_dice_coefficient", direction="max"
        ),
        max_trials=10,
        directory="tuner_results",
        project_name="histology_scalar_tuning",
    )

    print("Starting hyperparameter search...")
    tuner.search(
        train_gen.take(10),
        epochs=TUNER_EPOCHS,
        validation_data=val_gen,
    )

    best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
    print("\nBest hyperparameters:")
    for param, value in best_hps.values.items():
        print(f"{param}: {value}")

    vis_callback = ScalarVisualizationCallback(val_gen)
    model = build_model(best_hps)

    print("\nTraining with best hyperparameters...")
    history = model.fit(
        train_gen,
        epochs=TRAIN_EPOCHS,
        validation_data=val_gen,
        callbacks=[vis_callback],
    )

    plot_training_history(history, "Histology Scalar Model Training History")

    print_test_metrics(model, test_gen, "Histology Scalar")
