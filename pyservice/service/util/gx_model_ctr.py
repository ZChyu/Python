# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 13:01:38 2018

@author: Lidh
"""
import os
class GMC:
	def ensure_path(self,mode,name,client_id):
		gx_base_dir='model/'+mode+'/'+name+'/'+client_id+'/'
		self.mode=mode
		self.name=name
		self.client_id=client_id
		self.base_dir=gx_base_dir+'model'
		if not os.path.exists(gx_base_dir):
			os.makedirs(gx_base_dir)
            
	def get_base_dir(self):
        
		return self.base_dir
    
	def ensure_model(self,mode,name,client_id):
		gx_base_dir='model/'+mode+'/'+name+'/'+client_id+'/'
		base_dirc=gx_base_dir
		return True if os.path.exists(base_dirc) else False,base_dirc   	        