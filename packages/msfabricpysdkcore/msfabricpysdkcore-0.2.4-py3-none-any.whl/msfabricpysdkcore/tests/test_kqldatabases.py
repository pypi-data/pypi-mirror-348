import unittest
from datetime import datetime
from dotenv import load_dotenv
from time import sleep
from msfabricpysdkcore.coreapi import FabricClientCore

load_dotenv()

class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        #load_dotenv()
        self.fc = FabricClientCore()
    
    def test_kql_database(self):

        fc = self.fc
        workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'
        evenhouse_id = "f30ba76a-92c3-40d3-ad69-36db059c113d"

        creation_payload = {"databaseType" : "ReadWrite",
                            "parentEventhouseItemId" : evenhouse_id}

        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        kqldb_name = "kql" + datetime_str
        kqldb = fc.create_kql_database(workspace_id = workspace_id, display_name=kqldb_name,
                                    creation_payload=creation_payload)
        self.assertEqual(kqldb.display_name, kqldb_name)

        kql_databases = fc.list_kql_databases(workspace_id)
        kql_database_names = [kqldb.display_name for kqldb in kql_databases]
        self.assertGreater(len(kql_databases), 0)
        self.assertIn(kqldb_name, kql_database_names)

        kqldb = fc.get_kql_database(workspace_id, kql_database_name=kqldb_name)
        self.assertIsNotNone(kqldb.id)
        self.assertEqual(kqldb.display_name, kqldb_name)
        
        new_name = kqldb_name+"2"
        kqldb2 = fc.update_kql_database(workspace_id, kqldb.id, display_name=new_name, return_item=True)

        kqldb = fc.get_kql_database(workspace_id, kql_database_id=kqldb.id)
        self.assertEqual(kqldb.display_name, new_name)
        self.assertEqual(kqldb.id, kqldb2.id)
        
        response = fc.update_kql_database_definition(workspace_id, kqldb.id, kqldb.definition)
        self.assertIn(response.status_code, [200, 202])

        definition = fc.get_kql_database_definition(workspace_id, kql_database_id=kqldb.id)
        self.assertIn("definition", definition)
        self.assertIn("parts", definition["definition"])
        self.assertGreaterEqual(len(definition["definition"]["parts"]), 3)

        status_code = fc.delete_kql_database(workspace_id, kqldb.id)
        self.assertEqual(status_code, 200)