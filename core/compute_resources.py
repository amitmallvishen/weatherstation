# Copyright 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.





#################################################################
#################################################################

## Class Name  :  compute_resource
## Description :  This class contains the core logic to calculate
##                the resouces need to estimated

#################################################################
#################################################################


from config_read import InitializationManager
from oslo_log import log as logging


LOG = logging.getLogger(__name__)



class compute_resource(object):

      config = InitializationManager()
      config.CONF( default_config_files = ['openstackconfiguration.conf'] )


      def __init__( self ):
          self.db = InitializationManager()
          self.db.CONF( default_config_files = ['openstackconfiguration.conf'] )


      def update_config_db( self ,config_dict ):

          for key in config_dict:
              if None != config_dict[key]:
                 self.db.CONF.OpenStackCapacity[key] = config_dict[key]


      def cal_num_of_instances_for_design( self ):
          capacity = self.db.CONF.OpenStackCapacity
          return (capacity.Current_number_of_instances * (( 100 + capacity.Instance_scaling_over_6_months ) /float(100) )) 

      def cal_no_of_compute_node( self ):

          capacity = self.db.CONF.OpenStackCapacity
          no_compute_node = ( capacity.Average_vCPUs_per_instance * self.cal_num_of_instances_for_design()  / \
                              ( capacity.CPUs_per_compute_node * capacity.Cores_per_CPU * capacity.Hyperthreading_Factor * capacity.CPU_Oversubscription_Factor ) )

          no_compute_node1 = capacity.Average_memory_per_instance * self.cal_num_of_instances_for_design() / float(capacity.Memory_per_compute_node)

          return round(max(no_compute_node , no_compute_node1 ) )

      def cal_total_vcpu( self ):
          capacity = self.db.CONF.OpenStackCapacity

          if True == capacity.Hyperthreading:
              total_vcpu = self.cal_no_of_compute_node() * capacity.CPUs_per_compute_node * capacity.Cores_per_CPU * capacity.Hyperthreading_Factor * capacity.CPU_Oversubscription_Factor
          else:
              total_vcpu = self. cal_no_of_compute_node() * capacity.CPUs_per_compute_node * capacity.Cores_per_CPU * capacity.CPU_Oversubscription_Factor

          return total_vcpu


      def cal_total_memory( self ):
           
          capacity = self.db.CONF.OpenStackCapacity
          total_mem = self.cal_no_of_compute_node() * capacity.Memory_per_compute_node

          return total_mem

    
      def cal_instances_based_on_vcpu( self ):
 
         return	self.cal_total_vcpu() / self.db.CONF.OpenStackCapacity.Average_vCPUs_per_instance

 
      def cal_instances_based_on_memory ( self ):
         return self.cal_total_memory() / self.db.CONF.OpenStackCapacity.Average_memory_per_instance


      def calc_os_capacity( self , config_dict = None):
          if config_dict != None:
             self.update_config_db( config_dict )

          vcpu = self.cal_instances_based_on_vcpu()
          memory = self.cal_instances_based_on_memory()

          return vcpu,memory
 
#if __name__ == "__main__":

#    res = compute_resource()
#    print "toatal no compute node",res.cal_no_of_compute_node()
#    print "total vcpu",res.cal_total_vcpu()
#    print "total memory",res. cal_total_memory()
#    print "number of instances for design", res.cal_number_of_instance_for_design()
#    print "cal_instances_based_on_vcpu",res.cal_instances_based_on_vcpu()

#    print "cal_instances_based_on_memory",res.cal_instances_based_on_memory() 

