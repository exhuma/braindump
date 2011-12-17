TimeSense
=========

Project State
    Brainfart

Priority
    Low

Description
===========

TimeSense is a project for a mobile device allowing you to keep track of time
without the need to look at the clock.

The idea originates from wrist-watches which can be configured to beep every
hour.

Example
=======

You have to leave in about one hour. You head off to the shower, knowing that
you lose track of time in there. You set up timesens to notify you (f.ex. via
a beep) every 15 minutes.

Requirements Brainstorm
=======================

* Beep on absolute or relative times.

  Absolute
    When starting the timer on 11:13 and setting it up to beep each 10
    minutes, it will beep at 11:20, 11:30, 11:40, ...

  Relative
    When starting the timer on 11:13 and setting it up to beep each 10
    minutes, it will beep at 11:23, 11:33, 11:43, ...

* Optional granularity

  Notify every x seconds/minutes/hours/days

  Granularity will affect the application timer to conserve battery power (if
  that even makes sense...)

* Stop conditions

  Stop after x seconds/minuts/hours/days or after x iterations

* Optional popup-message displaying current time, passed time and iterations

* Optional screen flash, forcing screen wakeup and displaying the current
  time, the passed time since start and number of iterations. This is for
  environments too noisy to hear the beeps (f.ex.: in-game using headphones)

* Selection of built-in audible notifications. Optionally using the system
  notifications.

* Audible distinction of number of iterations (f.ex.: beep 5 times on
  iteration #5). Possibly using special sound-files if iterations become too
  large. For example, instead of beeping 20 times, beep 4 times using a
  sound-effect indicating 5-iterations.


