* website: <https://arrizza.com/python-falcon-logger.html>
* installation: see <https://arrizza.com/setup-common.html>

## Summary

This is a python module that provides a way to run a fast logger.
Peregrine Falcons are the fastest animals alive (according to Google).
They go that fast by having as minimal drag as possible.

* See [Quick Start](https://arrizza.com/user-guide-quick-start) for information on using scripts.
* See [xplat-utils submodule](https://arrizza.com/xplat-utils) for information on the submodule.

## Sample code

see sample.py for a full example

```python
from falcon_logger import FalconLogger
```

## Sample

Use doit script to run the logger and compare against other loggers.

To run the FalconLogger:

```bash
./doit falcon
./doit falcon  --numlines=100000   # saves to a file
./doit falcon2 --numlines=100000   # writes to stdout 
./doit all     --numlines=1        # prints a sample of all log line types
```

To run the others loggers:

```bash
./doit stdout  # no file, just stdout
./doit normal  # use the python logger
./doit rsyslog # use the rsyslog python module
```

## Comparing Times

The overall time is very dependent on which OS you use and the speed of your computer

```text
on MSYS2 for 100,000 lines:
stdout: total time: 3170.0 ms
falcon: total time: 3623.9 ms
normal: total time: 5722.8 ms
rsyslog fails with an exception 
```

## Example outputs

```text
# i = 2

# === showing with elapsed time delays       
# === self._log.start(f'{i}:', 'start')
# === time.sleep(0.250)
# === self._log.start(f'{i}:', 'start + 250ms')
# === time.sleep(0.123)
# === self._log.start(f'{i}:', 'start + 373ms')
00.000 ==== 2: start
00.250 ==== 2: start + 250ms
00.373 ==== 2: start + 373ms

# === the automatic DTS line when 1 hour has elapsed or at the beginning
# === self._log.start(f'{i}:', 'start')
       DTS  2025/05/11 16:21:43.170
00.000 ==== 2: start

# === self._log.line(f'{i}:', 'line')
00.000      2: line

# === self._log.highlight(f'{i}:', 'highlight')
00.000 ---> 2: highlight

# === self._log.ok(f'{i}:', 'ok')
00.000 OK   2: ok

# === self._log.err(f'{i}:', 'err')
00.000 ERR  2: err

# === self._log.warn(f'{i}:', 'warn')
00.000 WARN 2: warn

# === self._log.bug(f'{i}:', 'bug')
00.000 BUG  2: bug

# === self._log.dbg(f'{i}:', 'dbg')
00.000 DBG  2: dbg

# === self._log.raw(f'{i}', 'raw', 'line')
2 raw line

# === self._log.output(21, f'{i}:', 'output (line 21)')
00.000  -- 21] 2: output (line 21)

# === lines = [f'{i}: num_output (line 1)', f'{i}: num_output (line 2)']
# === self._log.num_output(lines)
00.000  --  1] 2: num_output (line 1)
00.000  --  2] 2: num_output (line 2)

# ===  self._log.check(True, f'{i}:', 'check true')
00.000 OK   2: check true

# === self._log.check(False, f'{i}:', 'check false')
00.000 ERR  2: check false

# === lines = [f'{i}: check_all (line 1)', f'{i}: check_all (line 2)']
# === self._log.check_all(True, 'check_all true title', lines)
00.000 OK   check_all true title: True
00.000 OK      - 2: check_all (line 1)
00.000 OK      - 2: check_all (line 2)

# === self._log.check_all(False, 'check_all false title', lines)
00.000 ERR  check_all false title: False
00.000 ERR     - 2: check_all (line 1)
00.000 ERR     - 2: check_all (line 2)

# ===  info = {
# ===         'key1': ['val1']
# ===         }
# === self._log.json(info, f'{i}:', 'json', 'list')
00.000      2: json list
00.000  >   {
00.000  >     "key1": [
00.000  >       "val1"
00.000  >     ]
00.000  >   }

# === val = '\x12\x13\x14'
# === self._log.hex(val, f'{i}:', 'hex')
00.000      2: hex
00.000          0 0x00: 12 13 14 

# === self._log.debug(f'{i}:', 'debug')
00.000 DBG  2: debug

# === self._log.info(f'{i}:', 'info')
00.000      2: info

# === self._log.warning(f'{i}:', 'warning')
00.000 WARN 2: warning

# === self._log.error(f'{i}:', 'error')
00.000 ERR  2: error

# === self._log.critical(f'{i}:', 'critical')
00.000 CRIT 2: critical

# === try:
# ===   val = 5
# ===   val = val / 0
# === except ZeroDivisionError as excp:
# ===   self._log.exception(excp)
00.000 EXCP Traceback (most recent call last):
00.000 EXCP   File "/home/arrizza/projects/web/falcon-logger/sample/main.py", line 135, in _log_all
00.000 EXCP     val = val / 0
00.000 EXCP ZeroDivisionError: division by zero

self._log.full_dts()
       DTS  2025/05/11 16:21:43.170
       
```