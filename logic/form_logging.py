import logging

#Initialize query logger
input_logger = logging.getLogger(__name__)

#Override default logging level
input_logger.setLevel('INFO')

#Handler/Formatter for query logs. Send to query.logs
input_handler = logging.FileHandler("query.log", mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
input_handler.setFormatter(formatter)
input_logger.addHandler(input_handler)

def log_form_data(formData):
    hpcUse = formData.get('hpc-use')
    input_logger.info("HPC Use:\n%s", hpcUse)