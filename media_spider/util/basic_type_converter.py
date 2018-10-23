#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import json
import traceback


def from_string_to_json(content):
    try:
        json_dict = json.loads(content)
        json_dict = normalize_dict(json_dict)
    except Exception as e:
        pass
    return json_dict


def from_json_to_string(data):
    data = normalize_dict(data)
    return json.dumps(data, ensure_ascii=False)


def normalize_dict(data):
    if type(data) == dict:
        new_data = {}
        for k in data:
            data[k] = normalize_dict(data[k])
            if type(k) == unicode:
                new_data[k.encode('utf-8')] = data[k]
            else:
                new_data[k] = data[k]
        data = new_data
    elif type(data) == list:
        for i in range(0, len(data)):
            data[i] = normalize_dict(data[i])
    elif type(data) == unicode:
        data = data.encode('utf-8')
    else:
        data = str(data)
    return data


def normalize_dict_url(data):
    call_back_data = ''
    try:
        parameter_count = 0
        for key in data:
            parameter_count += 1
            if parameter_count == 1:
                call_back_data += '?%s=%s' % (key, data[key])
            else:
                call_back_data += '&%s=%s' % (key, data[key])
    except:
        traceback.print_exc()
    return call_back_data


if __name__ == '__main__':
    # print area_name_to_id('美国', '1')
    pass
