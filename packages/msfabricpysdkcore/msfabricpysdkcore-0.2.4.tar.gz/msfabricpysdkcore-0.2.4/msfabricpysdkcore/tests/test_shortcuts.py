import unittest
from msfabricpysdkcore.coreapi import FabricClientCore
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        #load_dotenv()
        self.fc = FabricClientCore()
        self.workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'

        self.lakehouse_target = "148ef579-4a5d-4048-8a48-0a703c5e3a1a"
        self.lakehouse_shortcut = "9d1e8b07-2fea-4fc5-872c-fb586d085149"

        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.shortcutname = "shortcut" + datetime_str
        self.path_target = "Files/to_share"
        self.path_shortcut = "Files/shortcutfolder"

        self.target = {'oneLake': {'itemId': self.lakehouse_target,
                                   'path': self.path_target,        
                                   'workspaceId': self.workspace_id}}

    def test_shortcut_end_to_end(self):

        item = self.fc.create_shortcut(workspace_id=self.workspace_id,
                                       item_id=self.lakehouse_shortcut,
                                       path=self.path_shortcut,
                                       name=self.shortcutname,
                                       target=self.target)
        self.assertEqual(item.name, self.shortcutname)
        self.assertEqual(item.path, self.path_shortcut)
        self.assertIn("oneLake", item.target)

        item = self.fc.get_shortcut(workspace_id=self.workspace_id,
                                    item_id=self.lakehouse_shortcut,
                                    path=self.path_shortcut,
                                    name=self.shortcutname)
        self.assertEqual(item.name, self.shortcutname)
        self.assertEqual(item.path, self.path_shortcut)
        self.assertIn("oneLake", item.target)

        shortcuts = self.fc.list_shortcuts(workspace_id=self.workspace_id,
                                          item_id=self.lakehouse_shortcut, parent_path="Files")
        self.assertGreater(len(shortcuts), 0)


        status_code = self.fc.delete_shortcut(workspace_id=self.workspace_id,
                                             item_id=self.lakehouse_shortcut,
                                             path=self.path_shortcut,
                                             name=self.shortcutname)
        
        self.assertAlmostEqual(status_code, 200)

if __name__ == "__main__":
    unittest.main()