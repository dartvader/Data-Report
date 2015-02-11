__author__ = 'leemcdonald'

import operator
import math
from statistics import mode

def mode_lee(mode_list):

    mode_list.sort()
    mode_count = 0
    itm = 0
    word_counter = {}
    for word in mode_list:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    return max(word_counter.items(), key=operator.itemgetter(1))[0]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def median_lee(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0


def get_data():

    people_list = list()

    with open("Data/DataSet.txt") as data_set:
        for line in data_set:
            people_line = list()
            line = line.strip().split(',')
            for item in line:
                people_line.append(item)
            people_list.append(people_line)

    return people_list

def get_feature_names():
    feature_names = list()
    with open("data/featurenames.txt") as data_set:
        for line in data_set:
            feature_names.append(line.strip())
    return feature_names

def categorical_report(con_feature_dict):

    for key, value in con_feature_dict.items():
        count = 0
        missing_values = 0
        cardinality_list = list()

        first_mode_list = list()
        second_mode_list = list()

        for f in value:
            if "?" not in f:
                count += 1
                cardinality_list.append(f)
                first_mode_list.append(f)
            else:
                count += 1
                missing_values += 1

        count = count - missing_values
        missing_percentage = (missing_values / count) * 100
        cardinality = len(set(cardinality_list))
        first_mode = mode_lee(first_mode_list)
        first_mode_count = cardinality_list.count(first_mode)
        first_mode_percentage = (first_mode_count / count)*100

        for f in value:
            if f != first_mode:
                second_mode_list.append(f)
        second_mode = mode_lee(second_mode_list)
        second_mode_count = cardinality_list.count(second_mode)
        second_mode_percentage = (second_mode_count / count)*100

        cat_report_file = open("Reports/C07042060CAT.csv", 'a')

        cat_report_file.write(key + "," + str(count) + "," + str(round(missing_percentage, 2)) + ",")
        cat_report_file.write(str(round(cardinality, 2)) + "," + str(first_mode) + ",")
        cat_report_file.write(str(round(first_mode_count, 2)) + "," + str(round(first_mode_percentage, 2)) + ",")
        cat_report_file.write(str(second_mode) + "," + str(round(second_mode_count, 2)) + ",")
        cat_report_file.write(str(round(second_mode_percentage, 2)))
        cat_report_file.write("\n")
        cat_report_file.close()


def continuous_report(cat_feature_dict):

    for key, value in cat_feature_dict.items():
        median_list = list()
        cardinality_list = list()
        item_count = 0
        real_count = 0
        missing_values = 0
        total = 0.0
        square = 0
        sq_tot = 0
        for v in value:
            if v != '?':
                item_count += 1
                real_count = item_count - missing_values
                cardinality_list.append(float(v))
                median_list.append(float(v))
                total += float(v)
                square = float(v) * float(v)
                sq_tot += square
            else:
                missing_values += 1
                item_count += 1
        cardinality = len(set(cardinality_list))
        missing_percentages = (missing_values / item_count)*100
        mean = total / real_count
        median_list.sort()
        mini = min(median_list)
        maxi = max(median_list)
        median = median_lee(median_list)
        one_st_quart = median_list[int((item_count/2)/2)]
        three_rd_quart = median_list[int((item_count/2)+((item_count/2)/2))]

        # sd_mean = sq_tot / real_count
        # stand_dev = math.sqrt(sd_mean)
        stand_dev = math.sqrt((sq_tot / real_count) - (mean * mean))
        con_report_file = open("Reports/C07042060CONT.csv", 'a+')

        con_report_file.write(key + ", " + str(item_count) + ", " + str(round(missing_percentages, 2)) + ", ")
        con_report_file.write(str(round(cardinality, 2)) + ", " + str(round(mini, 2)) + ", " + str(round(one_st_quart, 2)) + ", ")
        con_report_file.write(str(round(mean, 2)) + ", " + str(round(median, 2)) + ", " + str(round(three_rd_quart, 2)) + ", ")
        con_report_file.write(str(round(maxi, 2)) + ", " + str(round(stand_dev, 2)))
        con_report_file.write("\n")
        con_report_file.close()


def main():

    con_indexes = list()
    cat_indexes = list()

    # getting the data
    data_set_list = get_data()
    feature_names_list = [i for i in get_feature_names() if i != '']
    number_of_features = len(feature_names_list)
    index_count = 0
    for line in data_set_list:
        for item in line:
            if not is_number(item):
                cat_indexes.append(index_count)
                index_count += 1
            else:
                con_indexes.append(index_count)
                index_count += 1
        break

    # Organise the Features
    # Continous Features
    con_feature_dict = {}
    # Categorical Features
    cat_feature_dict = {}
    for index in range(0, number_of_features):
        name = feature_names_list[index]
        categorical_features = list()
        continuous_features = list()
        for item in data_set_list:
            if index in cat_indexes:
                categorical_features.append(item[index])
            else:
                continuous_features.append(item[index])
        if len(categorical_features) == 0:
            con_feature_dict[name] = continuous_features
        else:
            cat_feature_dict[name] = categorical_features

    categorical_report(cat_feature_dict)
    continuous_report(con_feature_dict)


main()
