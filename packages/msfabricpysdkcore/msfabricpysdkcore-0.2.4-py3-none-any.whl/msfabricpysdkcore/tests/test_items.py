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
        self.workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'


        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.item_name = "testitem" + datetime_str
        self.item_type = "Notebook"
    
    def test_item_end_to_end(self):

        item = self.fc.create_item(display_name=self.item_name, type=self.item_type, workspace_id=self.workspace_id) 
        self.assertEqual(item.display_name, self.item_name)
        self.assertEqual(item.type, self.item_type)
        self.assertEqual(item.workspace_id, self.workspace_id)
        self.assertEqual(item.description, "")

        item = self.fc.get_item(workspace_id=self.workspace_id, item_id=item.id)
        item_ = self.fc.get_item(workspace_id=self.workspace_id,
                                  item_name=self.item_name, item_type=self.item_type)
        self.assertEqual(item.id, item_.id)
        self.assertEqual(item.display_name, self.item_name)
        self.assertEqual(item.type, self.item_type)
        self.assertEqual(item.workspace_id, self.workspace_id)
        self.assertEqual(item.description, "")

        item_list = self.fc.list_items(workspace_id=self.workspace_id)
        self.assertTrue(len(item_list) > 0)

        item_ids = [item_.id for item_ in item_list]
        self.assertIn(item.id, item_ids)

        self.fc.update_item(workspace_id=self.workspace_id, item_id=item.id, display_name=f"u{self.item_name}", return_item=True)
        item = self.fc.get_item(workspace_id=self.workspace_id, item_id=item.id)
        self.assertEqual(item.display_name, f"u{self.item_name}")

        status_code = self.fc.delete_item(workspace_id=self.workspace_id, item_id=item.id)

        self.assertAlmostEqual(status_code, 200)

    def test_item_definition(self):

        sjd = self.fc.get_item(workspace_id=self.workspace_id, item_name="helloworld", item_type="SparkJobDefinition")
        self.assertIsNotNone(sjd.definition)
        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        blubb2 = "blubb2" + datetime_str
        blubb3 = "blubb3" + datetime_str
        blubb2 = self.fc.create_item(display_name=blubb2, type="SparkJobDefinition", workspace_id=self.workspace_id,
                                   definition=sjd.definition)

        blubb3 =  self.fc.create_item(display_name=blubb3, type="SparkJobDefinition", workspace_id=self.workspace_id)

        response = self.fc.update_item_definition(workspace_id=self.workspace_id,
                                                item_id=blubb3.id, definition=sjd.definition)
        
        self.assertEqual(response.status_code, 200)
        blubb3 = self.fc.get_item(workspace_id=self.workspace_id, item_id=blubb3.id)

        self.assertIn("parts", blubb3.definition)

        self.assertEqual(len(blubb3.definition["parts"]), len(sjd.definition["parts"]))
        sjd_defintion = [part["path"] for part in sjd.definition["parts"] if part["path"] == "SparkJobDefinitionV1.json"]
        blubb3_defintion = [part["path"] for part in blubb3.definition["parts"] if part["path"] == "SparkJobDefinitionV1.json"]
        self.assertEqual(sjd_defintion, blubb3_defintion)
        
        self.assertNotEqual(blubb2.id, sjd.id)
        self.assertIn("parts", blubb2.definition)

        self.assertEqual(len(blubb2.definition["parts"]), len(sjd.definition["parts"]))
        sjd_defintion = [part["path"] for part in sjd.definition["parts"] if part["path"] == "SparkJobDefinitionV1.json"]
        blubb2_defintion = [part["path"] for part in blubb2.definition["parts"] if part["path"] == "SparkJobDefinitionV1.json"]
        self.assertEqual(sjd_defintion, blubb2_defintion)
        self.assertNotEqual(blubb2.id, blubb3.id)
        
        blubb2.delete()
        blubb3.delete()

    def test_item_connections(self):

        fc = self.fc
        connections = fc.list_item_connections(workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3', item_id = '1bcc8b76-8e1f-428d-a594-f91ce1b9b076')
        self.assertEqual(len(connections), 0)

if __name__ == "__main__":
    unittest.main()