import torchmetrics
import config

######################################################################################
#                                       CUDA                                         #
######################################################################################
precision_metric = torchmetrics.classification.MultilabelPrecision(num_labels = config.NUM_CLASSES, 
                                                                   threshold = 0.5, 
                                                                   average = None).to(config.DEVICE)
recall_metric = torchmetrics.classification.MultilabelRecall(num_labels = config.NUM_CLASSES, 
                                                             threshold = 0.5, 
                                                             average = None).to(config.DEVICE)
accuracy_metric = torchmetrics.classification.MultilabelAccuracy(num_labels = config.NUM_CLASSES, 
                                                                 threshold = 0.5, 
                                                                 average = None).to(config.DEVICE)
f1_metric = torchmetrics.classification.MultilabelF1Score(num_labels = config.NUM_CLASSES, 
                                                          threshold = 0.5, 
                                                          average = None).to(config.DEVICE)

f1_metric_mean = torchmetrics.classification.MultilabelF1Score(num_labels = config.NUM_CLASSES, 
                                                               threshold = 0.5, 
                                                               average = 'macro').to(config.DEVICE)

######################################################################################
#                                       CPU                                          #
######################################################################################
precision_metric_cpu = torchmetrics.classification.MultilabelPrecision(num_labels = config.NUM_CLASSES, 
                                                                   threshold = 0.5, 
                                                                   average = None).to('cpu')
recall_metric_cpu = torchmetrics.classification.MultilabelRecall(num_labels = config.NUM_CLASSES, 
                                                             threshold = 0.5, 
                                                             average = None).to('cpu')
accuracy_metric_cpu = torchmetrics.classification.MultilabelAccuracy(num_labels = config.NUM_CLASSES, 
                                                                 threshold = 0.5, 
                                                                 average = None).to('cpu')
f1_metric_cpu = torchmetrics.classification.MultilabelF1Score(num_labels = config.NUM_CLASSES, 
                                                          threshold = 0.5, 
                                                          average = None).to('cpu')

f1_metric_mean_cpu = torchmetrics.classification.MultilabelF1Score(num_labels = config.NUM_CLASSES, 
                                                               threshold = 0.5, 
                                                               average = 'macro').to('cpu')

######################################################################################
#                                       FOG                                          #
#                                       CUDA                                         #
######################################################################################
fog_precision_metric = torchmetrics.classification.MulticlassPrecision(num_classes = config.NUM_CLASSES,
                                                                      average = None).to(config.DEVICE)
fog_recall_metric = torchmetrics.classification.MulticlassRecall(num_classes = config.NUM_CLASSES,
                                                                average = None).to(config.DEVICE)
fog_accuracy_metric = torchmetrics.classification.MulticlassAccuracy(num_classes = config.NUM_CLASSES,
                                                                    average = None).to(config.DEVICE)
fog_f1_metric = torchmetrics.classification.MulticlassF1Score(num_classes = config.NUM_CLASSES,
                                                             average = None).to(config.DEVICE)


############## BINARY ##############
fog_binary_precision_metric = torchmetrics.classification.BinaryPrecision().to(config.DEVICE)
fog_binary_recall_metric = torchmetrics.classification.BinaryRecall().to(config.DEVICE)
fog_binary_accuracy_metric = torchmetrics.classification.BinaryAccuracy().to(config.DEVICE)
fog_binary_f1_metric = torchmetrics.classification.BinaryF1Score().to(config.DEVICE)

