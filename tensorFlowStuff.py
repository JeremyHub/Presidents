from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import pandas as pd

CSV_COLUMN_NAMES = ["role", 'isStarting', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
ROLES = ['pres', 'vp', 'va', 'ass']

train_path = open('trainData.csv')
test_path = open('evalData.csv')

train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
test = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)

train_y = train.pop('role')
test_y = test.pop('role')

def input_fn(features, labels, training=True, batch_size=256):
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle and repeat if you are in training mode.
    if training:
        dataset = dataset.shuffle(1000).repeat()

    return dataset.batch(batch_size)

my_feature_columns = []
for key in train.keys():
    my_feature_columns.append(tf.feature_column.numeric_column(key=key))
print(my_feature_columns)

classifier = tf.estimator.DNNClassifier(
    feature_columns=my_feature_columns,
    # Two hidden layers of 30 and 10 nodes respectively.
    hidden_units=[30, 10],
    # The model must choose between 4 classes.
    n_classes=4)

classifier.train(
    input_fn=lambda: input_fn(train, train_y, training=True),
    steps=5000)

eval_result = classifier.evaluate(
    input_fn=lambda: input_fn(test, test_y, training=False))

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

def input_fn(features, batch_size=256):
    # Convert the inputs to a Dataset without labels.
    return tf.data.Dataset.from_tensor_slices(dict(features)).batch(batch_size)

features = ['isStarting', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
predict = {}

for i in range(50):
    print("Please type numeric values as prompted.")
    for feature in features:
        val = input(feature + "s : ")
        predict[feature] = [float(val)]

    predictions = classifier.predict(input_fn=lambda: input_fn(predict))
    for pred_dict in predictions:
        print(pred_dict['probabilities'])
        class_id = pred_dict['class_ids']
        for id in range(len(class_id)):
            probability = 100 * pred_dict['probabilities'][class_id[id]]
            print('Prediction is "{}" ({:.1f}%)'.format(
                ROLES[class_id[id]], probability))