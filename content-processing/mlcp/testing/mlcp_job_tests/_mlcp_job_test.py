import json
import os
import tempfile


class MLCPJobTest:

    def test_run(self):
        from multiprocessing import freeze_support
        freeze_support()
        # with self.assertRaises(SystemExit) as cm:
        #     from interface_layer.application import Application
        #     Application()()
        # self.assertEqual(cm.exception.code, 0)
        self._after_application_finished()

    def _open_temporary_storage(self):
        self._tempdir = tempfile.mkdtemp()

    def _close_temporary_storage(self):
        import shutil
        shutil.rmtree(self._tempdir)

    def in_temporary_storage(self, path: str):
        return os.path.join(self._tempdir, path)

    def _set_mlcp_process_configuration(self, process_configuration: dict):
        os.environ["mlcp_process_configuration"] = json.dumps(process_configuration)

    def _set_mlcp_process_configuration_from_file(self, process_configuration_file_path: str):
        with open(process_configuration_file_path) as f:
            process_configuration = json.load(f)
        self._set_mlcp_process_configuration(process_configuration)

    def _set_stage(self, stage: str):
        os.environ['stage'] = stage

    def _after_application_finished(self):
        pass
