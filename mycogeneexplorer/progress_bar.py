"""
Contains class for creating a progress bar
"""
import time


class ProgressBar:
    """
    Class which creates a progress bar
    """

    def __init__(self, completed_symbol="\u25A0", remaining_symbol="\u25A1", total=100, divisions=None, per=10):
        """
        Create progress bar class
        :param completed_symbol: Symbol for completed progress
        :param remaining_symbol: Symbol for filling out the progress bar
        :param total: Value for full bar
        :param divisions: How many parts to divide the total into
        """
        self.complete = completed_symbol
        self.remain = remaining_symbol
        self.total = total
        self.progress = 0
        if divisions:
            self.per = total // divisions
            self.divisions = divisions
        else:
            self.per = per
            self.divisions = int(self.total / per)

    def print_bar(self, progress):
        """
        Prints the progress bar with the current progress
        :param progress: Current progress
        :return: Nothing
        """
        # Return cursor to start of line
        print("\r", end="")
        completed = int(progress / self.per)
        percent = progress / self.total
        for i in range(completed):
            print(self.complete, end="")
        for i in range(self.divisions - completed):
            print(self.remain, end="")
        print(f"{percent * 100:.2f}%", end="")
        if progress == self.total:
            print("\nFinished!")

    def inc(self):
        self.progress += 1
        self.print_bar(self.progress)


if __name__ == "__main__":
    p_bar = ProgressBar(total=35, divisions=10)
    p_bar.print_bar(20)
    print("")
    p_bar2 = ProgressBar(total=100, divisions=10)
    for i in range(100):
        time.sleep(0.1)
        p_bar2.inc()
    p_bar2.print_bar(89)
    print("")
    p_bar2.print_bar(99)
    print("")
    p_bar2.print_bar(65)
    print("")
    p = ProgressBar(total=54, per=3)
    p.print_bar(50)
    print("")
    p.print_bar(52)
    print("")
    p.print_bar(54)
    print("")
    p.print_bar(55)
    print("")