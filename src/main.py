import data_collector
import data_merger

"""
Main script for data processing.

This script initializes and starts two data processing components: data_collector and data_merger.

"""

if __name__ == '__main__':
    # Start the data collector
    data_collector.start()

    # Start the data merger
    data_merger.start()
