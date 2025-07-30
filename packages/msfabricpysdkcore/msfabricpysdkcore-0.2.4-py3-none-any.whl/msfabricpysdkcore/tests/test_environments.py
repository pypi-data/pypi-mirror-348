import unittest
from datetime import datetime
from dotenv import load_dotenv
from time import sleep
from msfabricpysdkcore.coreapi import FabricClientCore

load_dotenv()

class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        self.fc = FabricClientCore()

    def test_environments_crudl(self):
        fc = self.fc
        workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'
        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")

        env_name = "env" + datetime_str
        environment1 = fc.create_environment(workspace_id, display_name=env_name)
        self.assertEqual(environment1.display_name, env_name)

        environments = fc.list_environments(workspace_id)
        environment_names = [env.display_name for env in environments]
        self.assertGreater(len(environments), 0)
        self.assertIn(env_name, environment_names)

        env = fc.get_environment(workspace_id, environment_name=env_name)
        self.assertIsNotNone(env.id)
        self.assertEqual(env.display_name, env_name)
        new_name = env_name + "2"
        env2 = fc.update_environment(workspace_id, env.id, display_name=new_name, return_item=True)

        env = fc.get_environment(workspace_id, environment_id=env.id)
        self.assertEqual(env.display_name, new_name)
        self.assertEqual(env.id, env2.id)

        status_code = fc.delete_environment(workspace_id, env.id)
        self.assertEqual(status_code, 200)

    def test_environment_details(self):
        fc = FabricClientCore()
        workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'
        environment_id = '5648be67-28fa-48b6-9d1f-3c87c3704d3c'
        published_settings = fc.get_published_settings(workspace_id=workspace_id, environment_id=environment_id)
        self.assertIsNotNone(published_settings)
        self.assertIn("instancePool", published_settings)
        self.assertIn("dynamicExecutorAllocation", published_settings)
        staging_settings = fc.get_staging_settings(workspace_id=workspace_id, environment_id=environment_id)
        self.assertIsNotNone(staging_settings)
        self.assertIn("instancePool", staging_settings)
        self.assertIn("dynamicExecutorAllocation", staging_settings)
        if staging_settings["driverCores"] == 8:
            driver_cores = 4
        else:
            driver_cores = 8
        updated_settings = fc.update_staging_settings(workspace_id=workspace_id, environment_id=environment_id, driver_cores=driver_cores)
        self.assertIn("instancePool", updated_settings)
        self.assertIn("dynamicExecutorAllocation", updated_settings)
        self.assertEqual(updated_settings["driverCores"], driver_cores)
        updated_settings = fc.get_staging_settings(workspace_id=workspace_id, environment_id=environment_id)
        self.assertIn("instancePool", updated_settings)
        self.assertIn("dynamicExecutorAllocation", updated_settings)
        self.assertEqual(updated_settings["driverCores"], driver_cores)


    def test_environment_spark_libraries(self):
        fc = self.fc
        workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'
        environment_id = '5648be67-28fa-48b6-9d1f-3c87c3704d3c'

        resp = fc.get_published_libraries(workspace_id, environment_id)
        self.assertIn('customLibraries', resp)
        self.assertIn('wheelFiles', resp['customLibraries'])
        self.assertIn('msfabricpysdkcore-0.1.1-py3-none-any.whl', resp['customLibraries']['wheelFiles'])

        resp = fc.upload_staging_library(workspace_id, environment_id, 'dummy.whl')
        self.assertEqual(resp.status_code, 200)
        
        resp = fc.get_staging_libraries(workspace_id, environment_id)

        self.assertIn('customLibraries', resp)
        self.assertIn('wheelFiles', resp['customLibraries'])
        self.assertIn('dummy.whl', resp['customLibraries']['wheelFiles'])
        self.assertIn('staging.whl', resp['customLibraries']['wheelFiles'])

        
        resp = fc.publish_environment(workspace_id, environment_id)
        self.assertIn('publishDetails', resp)
        self.assertIn('state', resp['publishDetails'])
        self.assertEqual(resp['publishDetails']['state'].lower(), 'running')

        
        resp = fc.cancel_publish(workspace_id, environment_id)
        self.assertIn('publishDetails', resp)
        self.assertIn('state', resp['publishDetails'])
        self.assertEqual(resp['publishDetails']['state'].lower(), 'cancelled')

        resp = fc.delete_staging_library(workspace_id, environment_id, 'dummy.whl')
        self.assertEqual(resp.status_code, 200)

        resp = fc.get_staging_libraries(workspace_id, environment_id)

        self.assertIn('customLibraries', resp)
        self.assertIn('wheelFiles', resp['customLibraries'])
        self.assertNotIn('dummy.whl', resp['customLibraries']['wheelFiles'])
        self.assertIn('staging.whl', resp['customLibraries']['wheelFiles'])


        



