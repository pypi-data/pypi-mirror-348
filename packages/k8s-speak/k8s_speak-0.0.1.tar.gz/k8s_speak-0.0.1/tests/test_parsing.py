#!/usr/bin/env python3
"""
Tests for the EKS Speak natural language parser
"""

import sys
import os
import unittest
import json

# Add the src directory to the path so we can import our module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from k8s_speak import K8SSpeak

class TestK8SSpeak(unittest.TestCase):
    """Test cases for EKS Speak functionality"""
    
    def setUp(self):
        self.k8s_speak = K8SSpeak()
    
    def test_parse_get_pods(self):
        """Test parsing of 'get pods' command"""
        result = self.k8s_speak.parse_command("show all pods in namespace kube-system")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "pod")
        self.assertEqual(result["namespace"], "kube-system")
        self.assertIsNone(result["name"])
    
    def test_parse_describe_pod(self):
        """Test parsing of 'describe pod' command"""
        result = self.k8s_speak.parse_command("describe pod named web-server in namespace frontend")
        self.assertEqual(result["intent"], "describe")
        self.assertEqual(result["resource"], "pod")
        self.assertEqual(result["namespace"], "frontend")
        self.assertEqual(result["name"], "web-server")
    
    def test_parse_with_cluster(self):
        """Test parsing with cluster specification"""
        result = self.k8s_speak.parse_command("get services in namespace production in cluster my-eks-cluster")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "service")
        self.assertEqual(result["namespace"], "production")
        self.assertIsNone(result["name"])
        self.assertEqual(result["additional_params"]["cluster"], "my-eks-cluster")
    
    def test_generate_kubectl_command(self):
        """Test generation of kubectl command from parsed input"""
        parsed = {
            "intent": "get",
            "resource": "pod",
            "namespace": "kube-system",
            "name": None,
            "additional_params": {}
        }
        cmd = self.k8s_speak.generate_kubectl_command(parsed)
        self.assertEqual(cmd, ["kubectl", "get", "pod", "-n", "kube-system"])
        
        # With cluster context
        parsed["additional_params"]["cluster"] = "my-eks-cluster"
        cmd = self.k8s_speak.generate_kubectl_command(parsed)
        self.assertEqual(cmd, ["kubectl", "--context", "my-eks-cluster", "get", "pod", "-n", "kube-system"])
    
    def test_parse_delete_command(self):
        """Test parsing of 'delete' command"""
        result = self.k8s_speak.parse_command("delete deployment named frontend in namespace app")
        self.assertEqual(result["intent"], "delete")
        self.assertEqual(result["resource"], "deployment")
        self.assertEqual(result["namespace"], "app")
        self.assertEqual(result["name"], "frontend")
    
    def test_parse_logs_command(self):
        """Test parsing of 'logs' command"""
        result = self.k8s_speak.parse_command("get logs for pod web-server in namespace frontend")
        self.assertEqual(result["intent"], "logs")
        self.assertEqual(result["resource"], "pod")
        self.assertEqual(result["namespace"], "frontend")
        self.assertEqual(result["name"], "web-server")
    
    def test_parse_create_command(self):
        """Test parsing of 'create' command"""
        result = self.k8s_speak.parse_command("create new namespace called development")
        self.assertEqual(result["intent"], "create")
        self.assertEqual(result["resource"], "namespace")
        self.assertIsNone(result["namespace"])
        self.assertEqual(result["name"], "development")
    
    def test_parse_alternative_phrasings(self):
        """Test parsing of alternative phrasings for the same intent"""
        # Test 'list' as alternative for 'get'
        result = self.k8s_speak.parse_command("list all deployments in namespace default")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "deployment")
        
        # Test 'show me' as alternative for 'get'
        result = self.k8s_speak.parse_command("show me all configmaps in namespace kube-system")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "configmap")
        
        # Test 'give details about' as alternative for 'describe'
        result = self.k8s_speak.parse_command("give details about service called nginx-service")
        self.assertEqual(result["intent"], "describe")
        self.assertEqual(result["resource"], "service")
        self.assertEqual(result["name"], "nginx-service")
    
    def test_parse_with_abbreviations(self):
        """Test parsing with resource type abbreviations"""
        # Test 'svc' abbreviation for 'service'
        result = self.k8s_speak.parse_command("get svc in namespace default")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "service")
        
        # Test 'ns' abbreviation for 'namespace'
        result = self.k8s_speak.parse_command("get all ns")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "namespace")
        
        # Test 'cm' abbreviation for 'configmap'
        result = self.k8s_speak.parse_command("describe cm named app-config in namespace app")
        self.assertEqual(result["intent"], "describe")
        self.assertEqual(result["resource"], "configmap")
        self.assertEqual(result["name"], "app-config")
        
        # Test 'deploy' abbreviation for 'deployment'
        result = self.k8s_speak.parse_command("get deploy in namespace app")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "deployment")
    
    def test_parse_alternative_namespace_syntax(self):
        """Test parsing with alternative namespace syntax"""
        result = self.k8s_speak.parse_command("get pods in the production namespace")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "pod")
        self.assertEqual(result["namespace"], "production")
        self.assertIsNone(result["name"])
    
    def test_parse_resource_name_patterns(self):
        """Test parsing with different resource name patterns"""
        # Pattern: "resource named name"
        result = self.k8s_speak.parse_command("describe pod named web-server")
        self.assertEqual(result["name"], "web-server")
        
        # Pattern: "name resource" 
        result = self.k8s_speak.parse_command("delete frontend deployment")
        self.assertEqual(result["intent"], "delete")
        self.assertEqual(result["resource"], "deployment")
        self.assertEqual(result["name"], "frontend")
        
        # Pattern: "for resource name"
        result = self.k8s_speak.parse_command("get logs for pod api-gateway")
        self.assertEqual(result["intent"], "logs")
        self.assertEqual(result["resource"], "pod")
        self.assertEqual(result["name"], "api-gateway")
    
    def test_parse_exec_command(self):
        """Test parsing of 'exec' command"""
        result = self.k8s_speak.parse_command("execute command in pod database in namespace data")
        self.assertEqual(result["intent"], "exec")
        self.assertEqual(result["resource"], "pod")
        self.assertEqual(result["namespace"], "data")
        self.assertEqual(result["name"], "database")
    
    def test_parse_apply_command(self):
        """Test parsing of 'apply' command"""
        result = self.k8s_speak.parse_command("apply changes to deployment frontend")
        self.assertEqual(result["intent"], "apply")
        self.assertEqual(result["resource"], "deployment")
        self.assertEqual(result["name"], "frontend")
    
    def test_additional_resource_types(self):
        """Test parsing with additional resource types"""
        # Test statefulset
        result = self.k8s_speak.parse_command("get statefulset in namespace database")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "statefulset")
        
        # Test persistent volume claim
        result = self.k8s_speak.parse_command("describe pvc database-storage in namespace app")
        self.assertEqual(result["intent"], "describe")
        self.assertEqual(result["resource"], "persistentvolumeclaim")
        self.assertEqual(result["name"], "database-storage")
        
        # Test cronjob
        result = self.k8s_speak.parse_command("get all cronjobs in namespace batch")
        self.assertEqual(result["intent"], "get")
        self.assertEqual(result["resource"], "cronjob")
        self.assertEqual(result["namespace"], "batch")
    
    def test_generate_kubectl_command_with_options(self):
        """Test generation of kubectl command with different options"""
        # Test logs command
        parsed = {
            "intent": "logs",
            "resource": "pod",
            "namespace": "api",
            "name": "web-frontend",
            "additional_params": {}
        }
        cmd = self.k8s_speak.generate_kubectl_command(parsed)
        self.assertEqual(cmd, ["kubectl", "logs", "web-frontend", "-n", "api"])
        
        # Test exec command
        parsed = {
            "intent": "exec",
            "resource": "pod",
            "namespace": "database",
            "name": "postgres",
            "additional_params": {}
        }
        cmd = self.k8s_speak.generate_kubectl_command(parsed)
        self.assertEqual(cmd, ["kubectl", "exec", "postgres", "--", "/bin/bash", "-n", "database"])
        
        # Test get with format option
        parsed = {
            "intent": "get",
            "resource": "pod",
            "namespace": "default",
            "name": None,
            "additional_params": {}
        }
        cmd = self.k8s_speak.generate_kubectl_command(parsed)
        self.assertIn("-o", cmd)
        self.assertIn("wide", cmd)

if __name__ == "__main__":
    unittest.main()