import logging
#
from tqdm import tqdm
#
#
#
def number_to_letter(sequence):
    result = []
    for number in sequence:
        # Adjust for the skipped 'C'
        if number >= 2:
            number += 1
        result.append(chr(number + 65))  # 65 is the ASCII code for 'A'
    return result



class TqdmLoggingHandler(tqdm):
    def __init__(self, *args, logger=None, level=logging.INFO, **kwargs):
        self.logger = logger if logger else logging.getLogger(__name__)
        self.log_level = level
        super().__init__(*args, **kwargs)

    def update(self, n=1):
        if self.logger.getEffectiveLevel() <= self.log_level:
            super().update(n)

    def close(self):
        if self.logger.getEffectiveLevel() <= self.log_level:
            super().close()