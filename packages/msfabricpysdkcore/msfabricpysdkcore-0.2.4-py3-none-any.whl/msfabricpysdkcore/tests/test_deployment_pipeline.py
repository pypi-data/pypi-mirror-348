import unittest
from msfabricpysdkcore.coreapi import FabricClientCore
from dotenv import load_dotenv

load_dotenv()


class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        self.fc = FabricClientCore()
        


    def test_spark_workspace_custom_pools(self):
        fc = self.fc

        dep_pipes = fc.list_deployment_pipelines()

        self.assertGreater(len(dep_pipes), 0)

        self.assertIn("sdkpipe", [pipe.display_name for pipe in dep_pipes])

        for pipe in dep_pipes:
            if pipe.display_name == 'sdkpipe':
                pipe_id = pipe.id
                break

        pipe = fc.get_deployment_pipeline(pipe_id)

        self.assertEqual(pipe.display_name, 'sdkpipe')
        self.assertEqual(pipe.id, pipe_id)

        stages = fc.list_deployment_pipeline_stages(pipe_id)

        self.assertGreater(len(stages), 0)
        names = [stage.display_name for stage in stages]
        self.assertIn("Development", names)
        self.assertIn("Production", names)

        dev_stage = [stage for stage in stages if stage.display_name == "Development"][0]
        prod_stage = [stage for stage in stages if stage.display_name == "Production"][0]

        items = fc.list_deployment_pipeline_stages_items(deployment_pipeline_id=pipe_id, stage_id=dev_stage.id)
        
        self.assertGreater(len(items), 0)
        self.assertIn("cicdlakehouse", [item["itemDisplayName"] for item in items])
       
        items = [item for item in dev_stage.list_items() if item["itemDisplayName"] == 'cicdlakehouse']
        item = items[0]
        item = {"sourceItemId": item["itemId"],
                "itemType": item["itemType"]}
        items = [item]

        response = fc.deploy_stage_content(deployment_pipeline_id=pipe_id, source_stage_id=dev_stage.id,target_stage_id=prod_stage.id, items=items)

        self.assertEqual(response["status"], "Succeeded")

        



