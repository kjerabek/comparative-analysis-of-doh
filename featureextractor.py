import pandas as pd
import numpy as np


class FeatureExtractor():
    behnke_features = [
           'Duration',
           'FlowBytesSent',
           'FlowBytesReceived',
           'FlowReceivedRate',
           'PacketLengthVariance',
           'PacketLengthStandardDeviation',
           'PacketLengthMean',
           'PacketLengthMedian',
           'PacketLengthMode',
           'PacketLengthSkewFromMedian',
           'PacketLengthSkewFromMode',
           'PacketLengthCoefficientofVariation',
           'PacketTimeVariance',
           'PacketTimeStandardDeviation',
           'PacketTimeMean',
           'PacketTimeMedian',
           'PacketTimeMode',
           'PacketTimeSkewFromMedian',
           'PacketTimeCoefficientofVariation',
           'ResponseTimeTimeStandardDeviation',
           'ResponseTimeTimeMean',
           'ResponseTimeTimeMedian',
           'ResponseTimeTimeMode',
           'ResponseTimeTimeSkewFromMedian',
           'ResponseTimeTimeSkewFromMode',
           'ResponseTimeTimeCoefficientofVariation',
           'DoH']
    
    casanova_features = [
           'FlowBytesSent',
           'FlowSentRate',
           'FlowBytesReceived',
           'FlowReceivedRate',
           'PacketLengthVariance',
           'PacketLengthStandardDeviation',
           'PacketLengthMean',
           'PacketLengthMedian',
           'PacketLengthMode',
           'PacketLengthSkewFromMedian',
           'PacketLengthSkewFromMode',
           'PacketLengthCoefficientofVariation',
           'PacketTimeVariance',
           'PacketTimeStandardDeviation',
           'PacketTimeMean',
           'PacketTimeMedian',
           'PacketTimeMode',
           'PacketTimeSkewFromMedian',
           'PacketTimeSkewFromMode',
           'PacketTimeCoefficientofVariation',
           'ResponseTimeTimeVariance',
           'ResponseTimeTimeStandardDeviation',
           'ResponseTimeTimeMean',
           'ResponseTimeTimeMedian',
           'ResponseTimeTimeMode',
           'ResponseTimeTimeSkewFromMedian',
           'ResponseTimeTimeSkewFromMode',
           'ResponseTimeTimeCoefficientofVariation',
           'DoH']
    
    montazerishatoori_features = [
           'FlowBytesSent',
           'FlowSentRate',
           'FlowBytesReceived',
           'FlowReceivedRate',
           'PacketLengthVariance',
           'PacketLengthStandardDeviation',
           'PacketLengthMean',
           'PacketLengthMedian',
           'PacketLengthMode',
           'PacketLengthSkewFromMedian',
           'PacketLengthSkewFromMode',
           'PacketLengthCoefficientofVariation',
           'PacketTimeVariance',
           'PacketTimeStandardDeviation',
           'PacketTimeMean',
           'PacketTimeMedian',
           'PacketTimeMode',
           'PacketTimeSkewFromMedian',
           'PacketTimeSkewFromMode',
           'PacketTimeCoefficientofVariation',
           'ResponseTimeTimeVariance',
           'ResponseTimeTimeStandardDeviation',
           'ResponseTimeTimeMean',
           'ResponseTimeTimeMedian',
           'ResponseTimeTimeMode',
           'ResponseTimeTimeSkewFromMedian',
           'ResponseTimeTimeSkewFromMode',
           'ResponseTimeTimeCoefficientofVariation',
           'DoH']
    
    zebin_features = [
           'Duration',
           'FlowBytesSent',
           'FlowSentRate',
           'FlowBytesReceived',
           'FlowReceivedRate',
           'PacketLengthVariance',
           'PacketLengthStandardDeviation',
           'PacketLengthMean',
           'PacketLengthMedian',
           'PacketLengthMode',
           'PacketLengthSkewFromMedian',
           'PacketLengthSkewFromMode',
           'PacketLengthCoefficientofVariation',
           'PacketTimeVariance',
           'PacketTimeStandardDeviation',
           'PacketTimeMean',
           'PacketTimeMedian',
           'PacketTimeMode',
           'PacketTimeSkewFromMedian',
           'PacketTimeSkewFromMode',
           'PacketTimeCoefficientofVariation',
           'ResponseTimeTimeVariance',
           'ResponseTimeTimeStandardDeviation',
           'ResponseTimeTimeMean',
           'ResponseTimeTimeMedian',
           'ResponseTimeTimeMode',
           'ResponseTimeTimeSkewFromMedian',
           'ResponseTimeTimeSkewFromMode',
           'ResponseTimeTimeCoefficientofVariation',
           'DoH']
    
    vekshin_features = [
           'time',
           'mindelay',
           'maxdelay',
           'avgdelay',
           'var_pkt_size',
           'var_pkt_size_rev',
           'bytes_ration',
           'num_pkts_ration',
           'av_pkt_size',
           'av_pkt_size_rev',
           'median_pkt_size',
           'median_pkt_size_rev',
           'time_leap_ration',
           'bursts',
           'fizzles',
           'autocorr',
           'stSum',
           'rdSum',
           'DoH']

    jerabek_features = [
           'mean_paysize_ab',
           'mean_paysize_ba',
           'num_packets_ab_to_num_packets_ratio',
           'mean_time_between_packets_ba',
           'DoH'
        ]
    
    def extract_features(df, feature_columns):
        return df[feature_columns]
    
    def get_X(df, label_name):
        columns = df.columns.tolist()
        columns.remove(label_name)
        return df[columns].values
    
    def get_y(df, label_name):
        return df[label_name].values
