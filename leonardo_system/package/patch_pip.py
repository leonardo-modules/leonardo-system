from __future__ import absolute_import

import contextlib
from pip.utils.logging import get_indentation, _log_state


@contextlib.contextmanager
def indent_log(num=2):
    """
    I submited PR to pip because this has raising exception for us

    https://github.com/pypa/pip/pull/3161

    .. code-block:: python

        Exception:
        Traceback (most recent call last):
          File "/srv/leonardo/sites/majklk/local/lib/python2.7/site-packages/pip/basecommand.py", line 211, in main
            status = self.run(options, args)
          File "/srv/leonardo/sites/majklk/local/lib/python2.7/site-packages/pip/commands/install.py", line 344, in run
            requirement_set.cleanup_files()
          File "/srv/leonardo/sites/majklk/local/lib/python2.7/site-packages/pip/req/req_set.py", line 589, in cleanup_files
            with indent_log():
          File "/usr/lib/python2.7/contextlib.py", line 17, in __enter__
            return self.gen.next()
          File "/srv/leonardo/sites/majklk/local/lib/python2.7/site-packages/pip/utils/logging.py", line 38, in indent_log
            _log_state.indentation -= num
        AttributeError: 'thread._local' object has no attribute 'indentation'
    """
    _log_state.indentation = get_indentation() + num
    try:
        yield
    finally:
        _log_state.indentation = get_indentation() - num
