#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 19:24:24 2019

@author: ali
"""
#import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../Given')
import InputConstants
import json
import random as rd
# Node features class
class _Node:
    def __init__(self, name, cap, deg, bandwidth, dis, function):
        self.name = name
        self.cap = cap
        self.deg = deg
        self.ban = bandwidth
        self.dis = dis
        self.fun = {}
#        self.fun.append(function)
# Link features class
class _Link:
    def __init__(self, name, cap, bandwidth, length):
        self.cap = cap
        self.bandwidth = bandwidth
        self.length = length
        self.name = name
# Chain features class
class _Chain:
    def __init__(self, name, function, bandwidth):
        self.name = name
        self.fun = function
#        self.user = user
        self.ban = bandwidth
#        self.traf = traffic
# Grahp class contains of nodes and links features
class Graph:
    def __init__(self, path, funs):
        self.funs = funs
        self.rev_to_cost_val = 0
        self.input_cons = InputConstants.Inputs()
        link_list = []
        node_len = []
        node_ban = []
        self.reward = 0.1
        with open(path, "r") as data_file:
            self.data = json.load(data_file)
            node_name_list = [self.data['networkTopology']['nodes']
                [node_num][self.input_cons.network_topology_node_name] 
                    for node_num in range(len(self.data['networkTopology']['nodes']))]

            self.link_list = self.data['networkTopology']['links'] 
            link_list = [self.data['networkTopology']['links'][node_name]
                        for node_name in node_name_list]
# Calculation of average distance of each node from other nodes
#            for cnt_node in range(len(node_name_list)):
#                len_sum = 0
#                for cnt_link in range(len(link_list[cnt_node])):
#                    len_sum += link_list[cnt_node][cnt_link][self.input_cons.network_topology_link_dis]
#                node_len.append(len_sum / len(link_list[cnt_node]))
# Calculation of sum of incoming link bandwidth to each node
            for cnt_node in range(len(node_name_list)):
                ban_sum = 0
                for cnt_link in range(len(link_list[cnt_node])):
                    ban_sum += link_list[cnt_node][cnt_link][self.input_cons.network_topology_link_cap]
                node_ban.append(ban_sum)
#            self.data['networkTopology']['nodes'][cnt][self.input_cons.network_topology_node_cap]
            self.node_list = [_Node(node_name_list[cnt],
                              rd.randint(1, 1000),
                              len(link_list[cnt]),
                              node_ban[cnt],
                              0,
                              None) 
                              for cnt in range(len(node_name_list))]
            self.floydWarshall()
    def function_cpu_usage(self, fun):
        return(self.funs[fun])
    def function_placement(self, node, ser, fun):
        self.node_list[node].fun[ser].append(fun)
    def batch_function_placement(self, ser, node_fun_list):
#        node = node_fun[0]
#        fun = node_fun[1]
        for node_fun in node_fun_list: 
            for node, fun in node_fun:
                self.function_placement(node, ser, fun)
    def node_is_mapped(self, node_fun, chains):
#        return True
#        _sum = 0
        flag = True
        service_list = [chains[i].name for i in range(len(chains))]
        for node_1, _ in node_fun:
            _sum = 0
            for node_2, fun in node_fun:
                if node_1 == node_2:
                    _sum += self.function_cpu_usage(fun)
        #            node = _node_fun[0]
                    for s in service_list:
                        _fun = self.node_list[node_1].fun[s]
                        for _fun_ in _fun:
                           _sum += self.function_cpu_usage(_fun_)
#            print(_sum, node_1)
            if _sum > self.node_list[node_1].cap:
                        flag = False
        return flag
    def rev_to_cost(self, node_fun, ser_num, chains):
        td = 2
        
        R = self.revenue_measure(node_fun, ser_num, chains,td)
        C = self.cost_measure(node_fun, ser_num, chains, td)
        self.rev_to_cost_val = (R / C)
    def revenue_measure(self, node_fun, ser_num, chains, td):
        cpu_usage = sum([self.function_cpu_usage(node_fun[i][1])
                    for i in range(len(node_fun))])
        bandwidth_usage = chains[ser_num].ban * (len(node_fun) - 1)
        return td * (cpu_usage + bandwidth_usage)
    def cost_measure(self, node_fun, ser_num, chains, td):
        _sum = 1
        for n in range(len(node_fun)-1):
            _sum += self.hop_count(node_fun[n][0], node_fun[n+1][0])
        return chains[ser_num].ban * _sum * td
    def hop_count(self, node_1, node_2):
        return self.hop[node_1][node_2]
    def link_is_mapped(self, node_fun):
        return True
    def get_feature_matrix(self):
        self.mf_matrix = np.zeros([len(self.node_list),
                                   self.input_cons.node_features])
        for i in range(len(self.node_list)):
            self.mf_matrix[i, 0] = self.node_list[i].cap
            self.mf_matrix[i, 1] = self.node_list[i].deg
            self.mf_matrix[i, 2] = self.node_list[i].ban
            self.mf_matrix[i, 3] = self.node_list[i].dis
    def update_feature_matrix(self, node_fun):
        node = []
        for n in node_fun:
            node.append(n[0])
        node = list(dict.fromkeys(node))
#        print(node)
        if  node != []:
            for n_1 in range(len(self.node_list)):
                _sum = 0
                cnt = 0
                for n_2 in node: 
                    if n_1 != n_2:
                        _sum += self.dis_cal(n_1, n_2)
                        cnt +=1
#                print(_sum, cnt)
                if cnt != 0:
                    tmp = _sum / (cnt + 1)
                    self.node_list[n_1].dis = tmp
                    self.mf_matrix[n_1, 3] = tmp
        else:
            for n_1 in range(len(self.node_list)):
                self.node_list[n_1].dis = 0
                self.mf_matrix[n_1, 3] = 0
    
    
    def dis_cal(self, node_1, node_2):
        return self.dist[node_1][node_2]
    
        # Python Program for Floyd Warshall Algorithm 
  
# Number of vertices in the graph 
 
  
# Define infinity as the large enough value. This value will be 
# used for vertices not connected to each other 

  
# Solves all pair shortest path via Floyd Warshall Algorithm 
    def floydWarshall(self): 
#        INF  = 99999
        node_num = len(self.node_list)
        self.hop = (np.ones((node_num, node_num)) * np.inf)
        self.dist = (np.ones((node_num, node_num)) * np.inf)
        for n_1 in range(node_num): 
            node_name = self.node_list[n_1].name
            links = self.link_list[node_name]
#            print(links)
            for l in range(len(links)):
                for n_2 in range(node_num):
                    if n_1 == n_2:
                        self.hop[n_1][n_2] = 0
                        self.dist[n_1][n_2] = 0
                    elif links[l][self.input_cons.network_topology_link_name] == self.node_list[n_2].name:
                        self.hop[n_1][n_2] = 1
                        self.dist[n_1][n_2] = links[l][self.input_cons.network_topology_link_dis]
#        print(dist[0][0])  
#        dist = graph
        """ Add all vertices one by one to the set of intermediate 
         vertices. 
         ---> Before start of an iteration, we have shortest distances 
         between all pairs of vertices such that the shortest 
         distances consider only the vertices in the set  
        {0, 1, 2, .. k-1} as intermediate vertices. 
          ----> After the end of a iteration, vertex no. k is 
         added to the set of intermediate vertices and the  
        set becomes {0, 1, 2, .. k} 
        """
        for k in range(node_num): 
      
            # pick all vertices as source one by one 
            for i in range(node_num): 
      
                # Pick all vertices as destination for the 
                # above picked source 
                for j in range(node_num): 
      
                    # If vertex k is on the shortest path from  
                    # i to j, then update the value of dist[i][j] 
                    self.hop[i][j] = min(self.hop[i][j] , 
                                      self.hop[i][k]+ self.hop[k][j] 
                                    ) 
        
                    self.dist[i][j] = min(self.dist[i][j] , 
                                      self.dist[i][k]+ self.dist[k][j] 
                                    ) 
        
    
    def select_one(self, y, approach):
        if approach == 'sample':
            y_one_hot = np.zeros_like(y)
            tmp = []
            for i in range(len(self.node_list)):
                tmp.append(y[0][i])
            can = np.random.choice(y.shape[1], p=tmp)
            y_one_hot[0][can]=1
            return(y_one_hot, can)
    def make_empty_nodes(self):
        for i in range(len(self.node_list)):
                for j in range(len(self.data['chains'])):
                    self.node_list[i].fun[self.data['chains'][j]['name']] = []
        
class Chains:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
#        with open(self.path, "r") as data_file:
#            self.data = json.load(data_file)
##            service_list = [data['chains'][c]['name'] 
##            for c in range(len(data['chains']))]
##            print(service_list)
#            for i in range(len(graph.node_list)):
#                for j in range(len(self.data['chains'])):
#                    graph.node_list[i].fun[self.data['chains'][j]['name']] = []
    def read_chains(self, path, graph):
        with open(path, "r") as data_file:
            data = json.load(data_file)
#            service_list = [data['chains'][c]['name'] 
#            for c in range(len(data['chains']))]
#            print(service_list)
            for i in range(len(graph.node_list)):
                for j in range(len(data["chains"])):
                    graph.node_list[i].fun[data["chains"][j]['name']] = []
#        with open(self.path, "r") as data_file:
#            self.data = json.load(data_file)
#            for i in range(len(data['chains'])):
            return([_Chain(data["chains"][i]['name'],
                                 data["chains"][i]['functions'], 
                                 data["chains"][i]['bandwidth']) 
                                 for i in range(len(data["chains"]))])

    def read_funcions(self, path):
         with open(path, "r") as data_file:
            data = json.load(data_file)
         return(data["functions"])
    def creat_chains_functions(self, path, chain_num, fun_num, ban, cpu):
         chains = {}
         chains["chains"] = []
         chains["functions"] = {}
         for f in range(fun_num):
             chains["functions"][str(f)] = rd.randint(1, cpu)
         for c in range(chain_num):
             chain = {}
             rand_fun_num = rd.randint(1, fun_num)         
             chain['name'] = str(c)
             chain['functions'] = [str(f) 
                                for f in range(rand_fun_num)]
             chain['bandwidth'] = rd.randint(1, ban)
             chains["chains"].append(chain)
         with open(path, 'w') as outfile:  
             json.dump(chains, outfile)
#            func_list = data['chains'][0]['function']
#            print(len(data['chains']))
#            self.link_len_list = [data['networkTopology']['links'][node_name][]]
#            print(len(tmp))
#        with open(path, 'r') as data:
#            for cnt, line in enumerate(data):
#                line = line.split(',')
#                if line[0] == input_cons.START_OF_FILE_DELIMETER:
#                    start_file_line = cnt
#                elif line[0] == input_cons.END_OF_FILE_DELIMETER:
#                    end_file_line = cnt
#                elif line[0] == input_cons.START_OF_NODES_DELIMETER:
#                    start_node_line = cnt
#                elif line[0] == input_cons.END_OF_NODES_DELIMETER:
#                    end_node_line = cnt
#                elif line[0] == input_cons.START_OF_LINK_DELIMETER:
#                    start_link_line = cnt
#                elif line[0] == input_cons.END_OF_LINK_DELIMETER:
#                    end_link_line = cnt
#        if start_file_line == None:
#            print('ReadFile Error: missing "START OF FILE DELIMETER"' )
#        elif end_file_line == None:
#            print('ReadFile Error: missing "END OF FILE DELIMETER"' )
#        elif start_node_line == None:
#            print('ReadFile Error: missing "START OF NODE DELIMETER"' )
#        elif end_node_line == None:
#            print('ReadFile Error: missing "END OF NODE DELIMETER"' )
#        elif start_link_line == None:
#            print('ReadFile Error: missing "START OF LINK DELIMETER"' )
#        elif end_link_line == None:
#            print('ReadFile Error: missing "END OF LINK DELIMETER"' ) 
#        with open(path, 'r') as data:
#            for cnt, line in enumerate(data):
#                if start_node_line < cnt < end_node_line:
#                    tmp = csv.reader(line, delimiter=',')
#                    print(tmp[0])
#                    node_list.append(tmp)
#                if start_link_line < cnt < end_link_line:
#                    link_list.append(line[:])
#        for i in range(len(node_list)):
#            self.node_list.append(node(node_list[i], 2, 4, 4, 10))
#        
#        for i in range(len(link_list)):
#            self.link_list.append(link(link_list[i], 2, 2, 2))
#            

#    def makegragh(self, node):
#        node('v1' ,2, 5, 10, 50)
##        if self.end_file_line == None || self.start_file_line == None :
#            print("Error in reading file. missing delimeters")
#        while (all(data.iloc[self.start_file_num]) != input_cons.START_OF_FILE_DELIMETER):
#            self.start_file_num +=1
#            if self.start_file_num == len(data):
#                print ("Your file does not have line that contains 'START OF FILE'")
#                break
#        while (data.iloc[self.end_file_num] != input_cons.END_OF_FILE_DELIMETER):
#            self.end_file_num +=1
#        while (data.iloc[self.start_file_num + self.start_node_num] != input_cons.START_OF_NODES_DELIMETER):
#            self.start_node_num +=1
        
        
        