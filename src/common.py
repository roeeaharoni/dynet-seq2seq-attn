import os
import codecs
import re

def write_results_files(hyper_params, train_inputs_path, train_outputs_path, dev_inputs_path, dev_outputs_path,
                        test_inputs_path, test_outputs_path, output_file_path, final_results, nbest=False):

    # write hyperparams
    with codecs.open(output_file_path + '.modelinfo.txt', 'w', encoding='utf8') as f:
        f.write('train inputs path = ' + str(train_inputs_path) + '\n')
        f.write('train outputs path = ' + str(train_outputs_path) + '\n')

        f.write('dev inputs path = ' + str(dev_inputs_path) + '\n')
        f.write('dev outputs path = ' + str(dev_outputs_path) + '\n')

        f.write('test inputs path = ' + str(test_inputs_path) + '\n')
        f.write('test outputs path = ' + str(test_outputs_path) + '\n')

        for param in hyper_params:
            f.write(param + ' = ' + str(hyper_params[param]) + '\n')

    # write predictions
    predictions_path = output_file_path + '.predictions'
    with codecs.open(predictions_path, 'w', encoding='utf8') as predictions:
        for i, line in enumerate(final_results):
            predictions.write(u'{}'.format(line))

    return predictions_path


def evaluate_bleu(gold, predictions):

    predictions_path = os.path.dirname(__file__) + '/predictions.tmp'
    gold_path = os.path.dirname(__file__) + '/gold.tmp'
    with codecs.open(predictions_path, 'w', encoding='utf8') as predictions_file:
        for i, line in enumerate(gold):
            predictions_file.write(u'{}'.format(line))

    with codecs.open(gold_path, 'w', encoding='utf8') as gold_file:
        for i, line in enumerate(predictions):
            l = line.decode('utf8')
            gold_file.write(l)

    bleu = evaluate_bleu_from_files(gold_path, predictions_path)
    os.remove(predictions_path)
    os.remove(gold_path)
    return bleu


def evaluate_bleu_from_files(gold_outputs_path, output_file_path):
    os.chdir(os.path.dirname(__file__))
    bleu_path = output_file_path + '.eval'
    os.system('perl multi-bleu.perl -lc {} < {} > {}'.format(gold_outputs_path, output_file_path, bleu_path))
    with codecs.open(bleu_path, encoding='utf8') as f:
        lines  = f.readlines()

    var = re.search(r'BLEU\s+=\s+(.+?),', lines[0])
    bleu = var.group(1)

    os.remove(bleu_path)

    return float(bleu)