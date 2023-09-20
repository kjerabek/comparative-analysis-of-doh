import pandas as pd
import glob
from pathlib import Path
import numpy as np
from datetime import datetime
import ipaddress
from dohpreprocessor import PreprocessorDoH



class Reader():
    DOH_CLASS = 1
    NONDOH_CLASS = 0
    
    ipfixprobe_generated_path = "/srv/data/doh_pcap/dataset_split/GeneratedData/*/data/generated/*/*/*/*_ipfixprobe.csv"
    dohlyzer_generated_path = "/srv/data/doh_pcap/dataset_split/GeneratedData/*/data/generated/*/*/*/*_dohlyzer.csv"
    netexp_generated_path = "/srv/data/doh_pcap/dataset_split/netexp/no_split/generated/*/*_netexp.csv"
    ipfixprobe_captured_path = "/srv/data/doh_pcap/dataset_split/DoH-Real-World/data/captured/pcap/*_ipfixprobe.csv"
    dohlyzer_captured_path = "/srv/data/doh_pcap/dataset_split/DoH-Real-World/data/captured/pcap/*_dohlyzer.csv"
    netexp_captured_path = "/srv/data/doh_pcap/dataset_split/netexp/no_split/generated/*/*_netexp.csv"
    doh_resolver_ip_path = "/srv/data/doh_pcap/DoH_Dataset/supplementary_files/doh_resolvers/doh_resolvers_ip.csv"
    
    dohlyzer_captured_design_path = "/srv/data/doh_pcap/dataset_split/GeneratedDataSplitValidation/*/data/generated/*/*/*/*_design_dohlyzer.csv"
    dohlyzer_captured_validation_path = "/srv/data/doh_pcap/dataset_split/GeneratedDataSplitValidation/*/data/generated/*/*/*/*_validation_dohlyzer.csv"
    ipfixprobe_captured_design_path = "/srv/data/doh_pcap/dataset_split/GeneratedDataSplitValidation/*/data/generated/*/*/*/*_design_ipfixprobe.csv"
    ipfixprobe_captured_validation_path = "/srv/data/doh_pcap/dataset_split/GeneratedDataSplitValidation/*/data/generated/*/*/*/*_validation_ipfixprobe.csv"

    
    """Read Datasets"""
    
    
    def split_PPI(x):
        if x == '[]':
            return []
        return [int(i) for i in x[1:-1].split('|')]

    def split_time(x):
        if x == '[]':
            return []
        return [datetime.strptime(i, "%Y-%m-%dT%H:%M:%S.%f") for i in x[1:-1].split('|')]

    def read_csvs(path):
        dohdf = [];
        for file in glob.glob(path):
                if Path(file).stat().st_size:
                    #print(file)
                    dohdf.append(pd.read_csv(file))

        doh = pd.concat(dohdf, ignore_index=True);
        return doh

    def remove_types_in_column_names(doh):
        colmap = dict();
        for x in doh.columns:
             colmap[x] = x.split(' ')[1]
        doh = doh.rename(columns=colmap)
        return doh
    
    def label_data(doh, src_col_name, dst_col_name, doh_resolvers_path):
        ips = list(pd.read_csv(doh_resolvers_path)['ip'])
        
        doh['DoH'] = np.where(
            np.logical_or(
                np.isin(doh[src_col_name], ips),
                np.isin(doh[dst_col_name], ips)),
            Reader.DOH_CLASS, Reader.NONDOH_CLASS)
        
        return doh

    def process_ipfixprobe_data(doh, doh_resolvers_path, nan_values=False):
        #prepare PPI arrays
        doh['PPI_PKT_LENGTHS'] = doh['PPI_PKT_LENGTHS'].apply(lambda x: Reader.split_PPI(x))
        doh['PPI_PKT_DIRECTIONS'] = doh['PPI_PKT_DIRECTIONS'].apply(lambda x: Reader.split_PPI(x))
        doh['PPI_PKT_FLAGS'] = doh['PPI_PKT_FLAGS'].apply(lambda x: Reader.split_PPI(x))
        doh['PPI_PKT_TIMES'] = doh['PPI_PKT_TIMES'].apply(lambda x: Reader.split_time(x))
        
        #filter short and UDP flows
        doh['PPI_LEN'] = doh['PPI_PKT_LENGTHS'].apply(lambda x: len(x))
        doh = doh[(doh['PROTOCOL'] == 6)].copy()
        
        #prepare features
        DoHProcessor = PreprocessorDoH()
        DoH_featureset = DoHProcessor.preprocess(doh, nan_values);

        DoH_featureset = Reader.label_data(DoH_featureset, 'SRC_IP', 'DST_IP', doh_resolvers_path)
        
        return DoH_featureset
    
    def process_dohlyzer_data(doh, doh_resolvers_path):
        doh = Reader.label_data(doh, 'SourceIP', 'DestinationIP', doh_resolvers_path)
        return doh

    def process_netexp_data_new_features(doh, doh_resolvers_path):
        doh['paysize_ba_to_paysize'] = doh['sum_paysize_ba'] / doh['sum_paysize']
        doh['num_packets_ab_to_num_packets_ratio'] = doh['num_packets_ab'] / doh['num_packets']
        doh['mean_time_between_packets_ba'] = doh['duration'] / doh['num_packets_ba']
        doh['mean_paysize_ab'] = doh['sum_paysize_ab'] / doh['num_packets_ab']
        doh['mean_paysize_ba'] = doh['sum_paysize_ba'] / doh['num_packets_ba']
        
        doh = Reader.label_data(doh, 'src_ip', 'dst_ip', doh_resolvers_path)
        
        doh = doh[[
            'src_ip',
            'dst_ip',
            'sport',
            'dport',
            'num_packets',
            'mean_paysize_ab',
            'mean_paysize_ba',
            'num_packets_ab_to_num_packets_ratio',
            'mean_time_between_packets_ba',
            'DoH'
        ]]
        
        return doh
    
    
