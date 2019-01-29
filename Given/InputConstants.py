#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 17:58:40 2019

@author: ali
"""

class Inputs:
    network_path = "../Data/"
    network_name = "nsf_14_network.json"
#    START_OF_FILE_DELIMETER = '***START OF FILE***'
#    END_OF_FILE_DELIMETER = '***END OF FILE***'
#    START_OF_NODES_DELIMETER = "***START OF NODE***"
#    END_OF_NODES_DELIMETER = "***END OF NODE***"
#    START_OF_LINK_DELIMETER = "***START OF LINK***"
#    END_OF_LINK_DELIMETER = "***END OF LINK***"
# network topology parameters
    network_topology_node_name = 0
    network_topology_node_cap = 1
    network_topology_link_dis = 1
    network_topology_link_cap = 2
# Learning parameters
    epochNum = 5000
    batchSize = 500
    trainNum=3500
    validNum=100
    node_features = 4
    learningRate = 1e-6