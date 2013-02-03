#!/bin/bash

rename 's/ + /-/g' *
rename 's/ [a-zA-Z+-.&] /-/g' *
rename 's/ /-/g' *
rename 's/ [a-zA-Z+-.&] /-/g' */*
rename 's/ [a-zA-Z+-.&] /-/g' */*/*
rename 's/ [a-zA-Z+-.&] /-/g' */*/*/*
rename 's/ /-/g' */*
rename 's/ /-/g' */*/*
rename 's/ /-/g' */*/*/*
rename 'y/A-Z/a-z/' *
rename 'y/A-Z/a-z/' */*
rename 'y/A-Z/a-z/' */*/*
rename 's/--/-/' *
rename 's/--/-/' */*
rename 's/--/-/' */*/*
rename 's/---/-/' */*/*
rename 's/---/-/' */*
rename 's/---/-/' *
rename 's/\.-/-/g' *
rename 's/\.-/-/g' */*
rename 's/\.-/-/g' */*/*
rename 's/\.-/-/g' */*/*/*

