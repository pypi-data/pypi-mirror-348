import subprocess
import threading
import sys


def exec_real_time(command, text_stdout=True, text_stderr=True):
    """
    Executes a command and prints its stdout and stderr in real time,
    handling both text and binary output.

    Args:
        command (list or str): The command to execute.
        text_stdout (bool): If True, decode stdout as text (default).
                             If False, treat stdout as raw bytes.
        text_stderr (bool): If True, decode stderr as text (default).
                             If False, treat stderr as raw bytes.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def handle_stream(stream, is_stderr, as_text):
        while True:
            chunk = stream.raw.read(4096)  # Read in chunks
            if not chunk:
                break
            if as_text:
                try:
                    text = chunk.decode(sys.stdout.encoding or "utf-8")
                    if is_stderr:
                        sys.stderr.write(f"stderr: {text}")
                    else:
                        sys.stdout.write(text)
                except UnicodeDecodeError:
                    print("binary data detected")
                    as_text = False
                    if is_stderr:
                        sys.stderr.buffer.write(chunk)
                    else:
                        sys.stdout.buffer.write(chunk)
            else:
                if is_stderr:
                    sys.stderr.buffer.write(chunk)
                else:
                    sys.stdout.buffer.write(chunk)
            sys.stdout.flush()
            sys.stderr.flush()

    stdout_thread = threading.Thread(
        target=handle_stream, args=(process.stdout, True, text_stdout)
    )
    stderr_thread = threading.Thread(
        target=handle_stream, args=(process.stderr, True, text_stderr)
    )

    stdout_thread.start()
    stderr_thread.start()

    process.wait()

    stdout_thread.join()
    stderr_thread.join()

    if process.returncode != 0:
        print(f"Command exited with code: {process.returncode}", file=sys.stderr)
