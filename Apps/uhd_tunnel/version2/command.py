from subprocess import Popen, PIPE

def exec_command(cmd_args):
    """
    Quick wrapper around subprocess to exec shell command and pass back 
    stdout, stderr, and the return code.
 
    Required Arguments:
 
        cmd_args
            The args to pass to subprocess.
 
 
    Usage:
 
    .. code-block:: python
 
        (stdout, stderr, retcode) = exec_command(['ls', '-lah'])
 
    """
    proc = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = proc.communicate()
    proc.wait()
    return (stdout, stderr, proc.returncode)
