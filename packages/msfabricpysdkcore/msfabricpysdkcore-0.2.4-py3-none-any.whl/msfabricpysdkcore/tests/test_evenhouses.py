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

        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.item_name = "testitem" + datetime_str
        self.item_type = "Notebook"



    def test_eventhouses(self):
            
        fc = self.fc
        workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'
        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        eventhouse_name = "evh" + datetime_str
        eventhouse1 = fc.create_eventhouse(workspace_id, display_name=eventhouse_name)
        self.assertEqual(eventhouse1.display_name, eventhouse_name)
        
        eventhouses = fc.list_eventhouses(workspace_id)
        eventhouse_names = [eh.display_name for eh in eventhouses]
        self.assertGreater(len(eventhouses), 0)
        self.assertIn(eventhouse_name, eventhouse_names)

        eh = fc.get_eventhouse(workspace_id, eventhouse_name=eventhouse_name)
        self.assertIsNotNone(eh.id)
        self.assertEqual(eh.display_name, eventhouse_name)
        new_display_name = eventhouse_name + "2"
        eh2 = fc.update_eventhouse(workspace_id, eh.id, display_name=new_display_name, return_item=True)

        definition = fc.get_eventhouse_definition(workspace_id, eventhouse_id=eh.id)
       
        self.assertIn("definition", definition)
        self.assertIn("parts", definition["definition"])
        self.assertGreaterEqual(len(definition["definition"]["parts"]), 2)

        response = fc.update_eventhouse_definition(workspace_id, eventhouse_id=eh.id, definition=definition["definition"])
        self.assertIn(response.status_code, [200, 202])

        eh = fc.get_eventhouse(workspace_id, eventhouse_id=eh.id)
        self.assertEqual(eh.display_name, new_display_name)
        self.assertEqual(eh.id, eh2.id)

        status_code = fc.delete_eventhouse(workspace_id, eh.id)
        self.assertEqual(status_code, 200)