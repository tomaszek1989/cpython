"""This test checks for correct fork() behavior.
"""

import os
import time
from test.fork_wait import ForkWait
from test.support import run_unittest, reap_children, get_attribute

# Skip test if fork does not exist.
get_attribute(os, 'fork')


class ForkTest(ForkWait):
    def wait_impl(self, cpid):
        for i in range(10):
            # waitpid() shouldn't hang, but some of the buildbots seem to hang
            # in the forking tests.  This is an attempt to fix the problem.
            spid, status = os.waitpid(cpid, os.WNOHANG)
            if spid == cpid:
                break
            time.sleep(1.0)

        self.assertEqual(spid, cpid)
        self.assertEqual(status, 0, "cause = %d, exit = %d" % (status&0xff, status>>8))

def test_main():
    run_unittest(ForkTest)
    reap_children()

if __name__ == "__main__":
    test_main()
