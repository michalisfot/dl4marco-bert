import collections
import re


def load_queries(path):
    queries = []
    queries_ids = []
    with open(path) as f:
        for line in f:
            query_id, query = line.rstrip().split('\t')
            query = query.replace(' ', '%20')
            queries.append(query)
            queries_ids.append(query_id)
    return queries, queries_ids


def load_run(path):
    temp = []
    run = []
    run_id = []
    j = 0
    with open(path) as f:
        for i, line in enumerate(f):
            topic, _, doc_id, rank, score, _ = line.split(' ')
            # if topic not in run:
            #     run[topic] = []
            temp.append((doc_id, int(rank), float(score)))
            if j==99:
                run_id.append(topic)
                run.append(temp)
                temp = []
                j = -1
            j += 1
    return run_id, run


def replace(queries, queries_ids, run_id, run):
    new_run = []
    new_run_ids = []
    for i, data in enumerate(run):
        print(queries_ids[i])
        print(queries[i])
        for j, (doc_id, rank, score) in enumerate(data):
            if j > 99:
                break
            new_run_ids.append(queries_ids[i])
            new_run.append((doc_id, rank, score))
    return new_run_ids, new_run


def convert_to_trec_run(new_run_ids, car_msmarco_run, output_path):
    output = ''
    for i, (doc_id, rank, score) in enumerate(car_msmarco_run):
        # print(data[0])
        # for doc_id, rank, score in data:
        output = output + new_run_ids[i] + ' Q0 ' + doc_id + ' ' + str(rank) + ' ' + str(score) + ' BERT' '\n'
    output_file = open(output_path, "w")
    output_file.write(output)
    output_file.close()


def main():

    # queries_path = '/home/michalis/Desktop/CAsT/2020/allennlp_resolved_v5.txt'
    queries_path = '/home/michalis/Desktop/CAsT/2020/origin/2020_automatic_evaluation_topics_v1.0.json_reformed.txt'
    # original_run_path = '/home/michalis/Desktop/CAsT/2020/post_competition/I013_automatic.run'
    # car_run_path = '/home/michalis/Desktop/CAsT/2019/eval/BERT/CAR_bert_predictions_test.run'
    # msmarco_run_path = '/home/michalis/Desktop/CAsT/2019/eval/BERT/MSMARCO_bert_predictions_test.run'
    # car_msmarco_run_path = '/home/michalis/Desktop/CAsT/2019/eval/BERT/MSMARCO_CAR_bert_predictions_test_v2.run'
    car_msmarco_run_path = '/home/michalis/Desktop/CAsT/2020/post_competition/BERT/I013_automatic_BERT_predictions.run'
    final_output_path = '/home/michalis/Desktop/CAsT/2020/post_competition/BERT/reformed_I013_automatic_BERT_predictions.run'

    queries, queries_ids = load_queries(queries_path)

    # original_run = load_run(original_run_path)
    # car_run = replace(queries, load_run(car_run_path))
    # msmarco_run = replace(queries, load_run(msmarco_run_path))
    run_id, run = load_run(car_msmarco_run_path)
    new_run_ids, car_msmarco_run = replace(queries, queries_ids, run_id, run)
    convert_to_trec_run(new_run_ids, car_msmarco_run, final_output_path)

    # merge(original_run, msmarco_run, car_run, final_output_path)

    print('Done!')


if __name__ == '__main__':
    main()
