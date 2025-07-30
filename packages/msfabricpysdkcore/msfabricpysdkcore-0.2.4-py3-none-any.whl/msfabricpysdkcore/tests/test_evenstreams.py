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

    def test_eventstreams(self):

        fc = self.fc
        workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'

        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        es_name = "es" + datetime_str

        eventstream = fc.create_eventstream(workspace_id, display_name=es_name)
        self.assertEqual(eventstream.display_name, es_name)

        eventstreams = fc.list_eventstreams(workspace_id)
        eventstream_names = [es.display_name for es in eventstreams]
        self.assertGreater(len(eventstreams), 0)
        self.assertIn(es_name, eventstream_names)

        
        es = fc.get_eventstream(workspace_id, eventstream_name=es_name)
        self.assertIsNotNone(es.id)
        self.assertEqual(es.display_name, es_name)

        es2 = fc.update_eventstream(workspace_id, es.id, display_name=f"{es_name}2", return_item=True)

        es = fc.get_eventstream(workspace_id, eventstream_id=es.id)
        self.assertEqual(es.display_name, f"{es_name}2")
        self.assertEqual(es.id, es2.id)

        response = fc.update_eventstream_definition(workspace_id, eventstream_id=es.id, definition=es.definition)
        self.assertIn(response.status_code, [200, 202])

        definition = fc.get_eventstream_definition(workspace_id, eventstream_id=es.id)
        self.assertIn("definition", definition)
        self.assertIn("parts", definition["definition"])
        self.assertGreaterEqual(len(definition["definition"]["parts"]), 3)

        status_code = fc.delete_eventstream(workspace_id, es.id)
        self.assertEqual(status_code, 200)