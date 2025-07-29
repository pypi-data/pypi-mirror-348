import argparse
import sys
import multiprocessing 
import logging 
from logging.handlers import QueueHandler
import traceback
import importlib.metadata
from datetime import datetime



from .cocoremover import cocoremover



def main(): 
    
    
    # define the header of main- and sub-commands. 
    header = f'cocoremover v{importlib.metadata.metadata("cocoremover")["Version"]},\ndeveloped by Gioele Lazzari (gioele.lazzari@univr.it).'
    
    
    # create the command line arguments:
    parser = argparse.ArgumentParser(description=header, add_help=False)
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-v", "--version", action="version", version=f"v{importlib.metadata.metadata('cocoremover')['Version']}", help="Show version number and exit.")
    
    
    parser.add_argument(
        "--verbose", action='store_true', 
        help="Make stdout messages more verbose, including debug messages.")
    parser.add_argument(
        "-i", "--input", metavar='', type=str, default='-',  
        help="Path to the genome assembly file.")
    parser.add_argument(
        "-d", "--database", metavar='', type=str, default='./cocoremover.db',  
        help="Path to the database file.")
    parser.add_argument(
        "-t", "--taxid", metavar='', type=int, default=0,  
        help="Species-level NCBI taxonomy ID for the input assembly.")
    parser.add_argument(
        "-o", "--output", metavar='', type=str, default='./',  
        help="Output folder (will be created if not existing).")
    parser.add_argument(
        "-c", "--cores", metavar='', type=int, default=1, 
        help="How many parallel processes to use during the multiprocessing steps.")
    parser.add_argument(
        "--makedb", action='store_true', 
        help="Compile a fresh database with the latest type-material genomes and taxonomy available (will be overwritten if existing).")
    parser.add_argument(
        "--nocleanup", action='store_true', 
        help="Do not remove intermediate files.")
    



    # check the inputted subcommand, automatic sys.exit(1) if a bad subprogram was specied. 
    args = parser.parse_args()
    
    
    # set the multiprocessing context
    multiprocessing.set_start_method('fork') 
    
    
    # create a logging queue in a dedicated process.
    def logger_process_target(queue):
        logger = logging.getLogger('cocoremover')
        while True:
            message = queue.get() # block until a new message arrives
            if message is None: # sentinel message to exit the loop
                break
            logger.handle(message)
    queue = multiprocessing.Queue()
    logger_process = multiprocessing.Process(target=logger_process_target, args=(queue,))
    logger_process.start()
    
    
    # connect the logger for this (main) process: 
    logger = logging.getLogger('cocoremover')
    logger.addHandler(QueueHandler(queue))
    if args.verbose: logger.setLevel(logging.DEBUG) # debug (lvl 10) and up
    else: logger.setLevel(logging.INFO) # debug (lvl 20) and up
    
    
    # handy function to print without time/level (for header / trailer)
    def set_header_trailer_formatter(logger):
        formatter = logging.Formatter('%(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return handler
    
    
    # to print the main pipeline logging:
    def set_usual_formatter(logger):
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt="%H:%M:%S")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return handler
    
    
    
    # show a welcome message:
    thf_handler = set_header_trailer_formatter(logger)
    logger.info(header + '\n')
    command_line = 'cocoremover ' # print the full command line:
    for arg, value in vars(args).items():
        command_line = command_line + f"--{arg} {value} "
    logger.info('Inputted command line: "' + command_line.rstrip() + '".\n')
    logger.removeHandler(thf_handler)
    
    
    
    usual_handler = set_usual_formatter(logger)
    current_date_time = datetime.now()
    formatted_date = current_date_time.strftime("%Y-%m-%d")
    logger.info(f"Welcome to cocoremover! Launching the tool on {formatted_date}...")
    try: 
        response = cocoremover(args, logger)
            
        if response == 0:
            logger.info("cocoremover terminated without errors!")
    except: 
        # show the error stack trace for this un-handled error: 
        response = 1
        logger.error(traceback.format_exc())
    logger.removeHandler(usual_handler)


    
    # Terminate the program:
    thf_handler = set_header_trailer_formatter(logger)
    if response == 1: 
        queue.put(None) # send the sentinel message
        logger_process.join() # wait for all logs to be digested
        sys.exit(1)
    else: 
        # show a bye message
        queue.put(None) # send the sentinel message
        logger_process.join() # wait for all logs to be digested
        logger.info('\n' + header)
        sys.exit(0) # exit without errors
        
        
        
if __name__ == "__main__":
    main()