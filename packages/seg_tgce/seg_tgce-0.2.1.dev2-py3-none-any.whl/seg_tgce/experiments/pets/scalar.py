import keras_tuner as kt
from keras.optimizers import Adam
from seg_tgce.data.oxford_pet.oxford_pet import (
    fetch_models,
    get_data_multiple_annotators,
)
from seg_tgce.experiments.plot_utils import plot_training_history, print_test_metrics
from seg_tgce.loss.tgce import TcgeScalar
from seg_tgce.metrics import DiceCoefficient, JaccardCoefficient
from seg_tgce.models.ma_model import ScalarVisualizationCallback
from seg_tgce.models.unet import unet_tgce_scalar

TARGET_SHAPE = (128, 128)
GROUND_TRUTH_INDEX = 1
BATCH_SIZE = 16
NUM_CLASSES = 3
NOISE_LEVELS = [-20.0, 0.0, 10.0]
NUM_SCORERS = len(NOISE_LEVELS)
TRAIN_EPOCHS = 50
TUNER_EPOCHS = 10


def build_model(hp):
    learning_rate = hp.Float(
        "learning_rate", min_value=1e-5, max_value=1e-2, sampling="LOG"
    )
    q = hp.Float("q", min_value=0.1, max_value=0.9, step=0.1)
    noise_tolerance = hp.Float(
        "noise_tolerance", min_value=0.1, max_value=0.9, step=0.1
    )
    lambda_reg_weight = hp.Float(
        "lambda_reg_weight", min_value=0.01, max_value=0.5, step=0.01
    )
    lambda_entropy_weight = hp.Float(
        "lambda_entropy_weight", min_value=0.01, max_value=0.5, step=0.01
    )
    lambda_sum_weight = hp.Float(
        "lambda_sum_weight", min_value=0.01, max_value=0.5, step=0.01
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
        n_scorers=NUM_SCORERS,
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

    disturbance_models = fetch_models(NOISE_LEVELS)
    train, val, test = get_data_multiple_annotators(
        annotation_models=disturbance_models,
        target_shape=TARGET_SHAPE,
        batch_size=BATCH_SIZE,
        labeling_rate=0.7,
    )

    # tuner = kt.BayesianOptimization(
    # build_model,
    # objective=kt.Objective(
    # "val_segmentation_output_dice_coefficient", direction="max"
    # ),
    # max_trials=10,
    # directory="tuner_results",
    # project_name="scalar_tuning",
    # )
    #
    # print("Starting hyperparameter search...")
    # tuner.search(
    # train.take(16).cache(),
    # epochs=TUNER_EPOCHS,
    # validation_data=val.take(8).cache(),
    # )
    #
    # best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
    # print("\nBest hyperparameters:")
    # for param, value in best_hps.values.items():
    # print(f"{param}: {value}")
    #
    # model = build_model(best_hps)
    learning_rate = 0.001129163728788601
    q = 0.4
    noise_tolerance = 0.2
    lambda_reg_weight = 0.26
    lambda_entropy_weight = 0.03
    lambda_sum_weight = 0.27
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
        n_scorers=NUM_SCORERS,
        name="Unet-TGCE-Scalar-Model",
    )

    model.compile(
        loss=loss_fn,
        metrics={"segmentation_output": [dice_fn, jaccard_fn]},
        optimizer=optimizer,
    )
    model.loss_fn = loss_fn
    vis_callback = ScalarVisualizationCallback(val)

    print("\nTraining with best hyperparameters...")
    history = model.fit(
        train.take(16).cache(),
        epochs=TRAIN_EPOCHS,
        validation_data=val.take(8).cache(),
        callbacks=[vis_callback],
    )

    plot_training_history(history, "Scalar Model Training History")

    print_test_metrics(model, test, "Scalar")
