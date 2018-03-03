# model store, a simulation of database of models. Basic functions: get and set
# keep all the models
# responsible to send the models to RecEngine

from Models.ClusteringModel import ClusteringModel
from Models.CFmodel import CFmodel
from Models.MostPopularModel import MostPopularModel
from Models.RecentPopularModel import RecentPopularModel
from Models.KNNmodel import KNNmodel


class ModelStore(object):
    # key variables are static variables
    MP_MODEL_KEY = "mp_model_key"  # most popular
    RP_MODEL_KEY = "rp_model_key"  # recent popular
    KNN_MODEL_KEY = "knn_model_key"  # K nearest neighbor most popular model
    CF_MODEL_KEY = "cf_model_key"  # collaborative filtering
    CL_MODEL_KEY = "cl_model_key"  # clustering model, used for similarity item model because similarity is based on cluster


    def __init__(self):
        # offline models saved in a dictionary, key: static variable defined above, value: instance of class as attribute
        self.myModels = {self.MP_MODEL_KEY: MostPopularModel(), self.RP_MODEL_KEY: RecentPopularModel(),
                              self.KNN_MODEL_KEY: KNNmodel(),
                              self.CL_MODEL_KEY: ClusteringModel(),
                              self.CF_MODEL_KEY: CFmodel()}

    def setModel(self, model, key): # memberId is for online learner use ONLY
        self.myModels[key] = model #note: only for Most Popular, constructor is a "pass", no actual model is needed to recommend


    # getModel only have value if setModel was done previously
    def getModel(self, key): # get from model store, update model and then put back to modelStore(setModel)
        return self.myModels[key]

