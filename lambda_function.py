from pdf_maker import Pdf_maker
import traceback
import logging


def lambda_handler():
    
    
    try:    


        maker = Pdf_maker()
        maker.pdfmaker()
        logging.debug('Working fine till here')
        return True , 'Done!!'

    except Exception as ex:


        tb = traceback.format_exc()
        logging.error(tb)
        return False, f"Problem with {ex}"
    
    
            


