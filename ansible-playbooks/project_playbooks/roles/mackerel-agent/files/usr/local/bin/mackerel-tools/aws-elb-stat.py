#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from argparse import ArgumentParser
import json
import os
import sys
import simplejson
import commands
import time


def args():
    parser = ArgumentParser(description='aws_elb_stat for Mackerel.')
    parser.add_argument('--elbnames',
                        action='store',
                        nargs=1,
                        type=str,
                        required=True,
                        help='The name of ELB.')
    res = parser.parse_args()
    return res


def GraphDef():
    graphs_dic = {
        'graphs': {}
    }

    for metrics_name in metrics_list:
        if "RequestCount" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT Request/s',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "Latency" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB-STAT Latancy[s]',
                    'unit': 'float',
                    'metrics': []
                })
        elif "HealthyHostCount" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT HealthyHostCount',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "UnHealthyHostCount" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT UnHealthyHostCount',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "HTTPCode_ELB_4XX" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT HTTPCode_ELB_4XX',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "HTTPCode_ELB_5XX" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT HTTPCode_ELB_5XX',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "HTTPCode_Backend_2XX" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT HTTPCode_Backend_2XX',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "HTTPCode_Backend_3XX" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT HTTPCode_Backend_3XX',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "HTTPCode_Backend_4XX" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT HTTPCode_Backend_4XX',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "HTTPCode_Backend_5XX" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT HTTPCode_Backend_5XX',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "BackendConnectionErrors" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT BackendConnectionErrors',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "SurgeQueueLength" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT SurgeQueueLength',
                    'unit': 'integer',
                    'metrics': []
                })
        elif "SpilloverCount" in metrics_name:
            graphs_dic['graphs'].update({metrics_name: {}})
            graphs_dic['graphs'][metrics_name].update(
                {
                    'label': 'ELB_STAT SpilloverCount',
                    'unit': 'integer',
                    'metrics': []
                })

        for elb_name in elb_list:
            graphs_dic['graphs'][metrics_name]['metrics'].append(
                {'name': elb_name, 'label': elb_name}
            )

    print "# mackerel-agent-plugin"
    print simplejson.dumps(graphs_dic)


def get_metrics(elbname, metric_name, statistic):
    # for mac
    #start_time = "`date -u -v -1M +%Y-%m-%dT%TZ` "
    start_time = "`date -u -d '1 minutes ago' +%Y-%m-%dT%TZ`"

    get_metrics_cmd = "aws cloudproject get-metric-statistics" \
        " --region ap-northeast-1" \
        " --namespace AWS/ELB" \
        " --metric-name " + metric_name + \
        " --dimensions Name=LoadBalancerName,Value=" + elbname + \
        " --statistics " + statistic + \
        " --start-time " + start_time + \
        " --end-time `date -u +%Y-%m-%dT%TZ`" \
        " --period 60"
    result_get_metrics = commands.getoutput(get_metrics_cmd)
    return result_get_metrics


if __name__ == "__main__":
    options = args()
    elb_list = args().elbnames[0].split(',')

    metrics_base = "aws_elb_stat"

    metrics_child_list = [
        {"metric-name": "RequestCount", "statistic": "Sum"},
        {"metric-name": "Latency", "statistic": "Average"},
        {"metric-name": "HealthyHostCount", "statistic": "Average"},
        {"metric-name": "UnHealthyHostCount", "statistic": "Average"},
        {"metric-name": "HTTPCode_ELB_4XX", "statistic": "Sum"},
        {"metric-name": "HTTPCode_ELB_5XX", "statistic": "Sum"},
        {"metric-name": "HTTPCode_Backend_2XX", "statistic": "Sum"},
        {"metric-name": "HTTPCode_Backend_3XX", "statistic": "Sum"},
        {"metric-name": "HTTPCode_Backend_4XX", "statistic": "Sum"},
        {"metric-name": "HTTPCode_Backend_5XX", "statistic": "Sum"},
        {"metric-name": "BackendConnectionErrors", "statistic": "Sum"},
        {"metric-name": "SurgeQueueLength", "statistic": "Maximum"},
        {"metric-name": "SpilloverCount", "statistic": "Sum"}

    ]
    metrics_list = []
    for i in range(len(metrics_child_list)):
        metrics_list.append(metrics_base + "." + metrics_child_list[i]['metric-name'])
    metrics_elb_list = []
    for i in range(len(elb_list)):
        metrics_elb_list.append(metrics_base + "." + elb_list[i])

    if os.environ.get('MACKEREL_AGENT_PLUGIN_META', '') == '1':
        GraphDef()
        sys.exit(0)

    for m in metrics_child_list:
        for e in elb_list:
            metrics_sub = m['metric-name']
            metrics_statistic = m['statistic']
            metrics_name = ".".join([metrics_base, metrics_sub])
            result_metrics = get_metrics(e, metrics_sub, metrics_statistic)
            r = json.loads(result_metrics)
            if len(r['Datapoints']) == 0:
                value = 0
                epoch_time = str(int(time.time()))
            else:
                value = r['Datapoints'][0][metrics_statistic]
                t_utc = r['Datapoints'][0]['Timestamp']
                from datetime import datetime, timedelta
                t_jst = datetime.strptime(t_utc, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=9)
                epoch_time = t_jst.strftime('%s')
            result = "\t".join(
                [
                    metrics_name + "." + e,
                    str(value),
                    epoch_time
                ])
            print result



