from lambda_src.components.masslaw_case_file_processing_pipeline_manager.lambda_templates.masslaw_step_functions_case_file_pipeline_node_handler import *
from lambda_src.components.masslaw_cases.masslaw_data_instances.masslaw_case_file_instance import *


class TextExtractionSuccess(MasslawStepFunctionCaseFilePipelineNodeHandler):

    def _execute(self):

        self.__file_instance = MasslawCaseFileInstance(self._file_id)

        self.__file_instance.set_data_property(['processing', 'stage_information', 'TextExtraction', 'status'], 'Done')
        self.__file_instance.set_data_property(['processing', 'stage_metadata', 'TextExtraction', 'valid'], 'true')

        self._set_response_attribute(['file_data'], self.__file_instance.get_data_copy())

    def _successful_execution(self):
        self.__file_instance.save_data()


handler = TextExtractionSuccess()
