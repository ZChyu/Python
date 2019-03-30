# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:16:24 2018

@author: Zcy
"""
import json
from flask import Flask,request,Response    
import gx_ARIMA,gx_corr,gx_Gray,gx_kmeans,gx_network,lstm,gx_network_s,gx_svm_s,gx_cnn
import gx_xgboost as xgboost
from gx_svml import gx_svmtest
app=Flask(__name__)

@app.route("/corr",methods=["GET","POST"])
def corr():
    return get_response(gx_corr.corr(request.get_json()))

@app.route("/Gray",methods=["GET","POST"])
def GrayAPI():
    return get_response(gx_Gray.model(request.get_json()))

@app.route("/ARIMA",methods=["GET","POST"])
def getPredict():
    return get_response(gx_ARIMA.predict(request.get_json()))

@app.route("/gx_kmeans",methods=["GET","POST"])
def gx_kmeans():
    return get_response(gx_kmeans.getJson(request.get_json()))

@app.route("/gx_network",methods=["GET","POST"])
def gx_getJson():
    return get_response(gx_network.getJson(request.get_json()))

@app.route("/gx_xgboost",methods=["GET","POST"])
def getXgboost():
    return get_response(xgboost.getXgboost(request.get_json()))
   
@app.route("/gx_svm",methods=["GET","POST"])
def SVM_F():
    return get_response(gx_svmtest.trainANDpredict(request.get_json()))

@app.route("/gx_lstm",methods=["GET","POST"])
def gx_lstmNetwork():
    return get_response(lstm.getLstm(request.get_json()))

@app.route("/gx_network_s",methods=["GET","POST"])
def gx_network_S():
    return get_response(gx_network_s.getNetworkSingle(request.get_json()))
    
@app.route("/gx_svm_s",methods=["GET","POST"])
def gx_svm_S():
    return get_response(gx_svm_s.getSvmSingle(request.get_json()))

@app.route("/gx_cnn",methods=["GET","POST"])
def gx_Cnn():
    return get_response(gx_cnn.getCNN(request.get_json()))

def get_response(data):
    response = Response(
                response=json.dumps(data),
                status=200,
                mimetype='application/json'
            )
    return response
if __name__ == '__main__':
  app.run(debug=False)