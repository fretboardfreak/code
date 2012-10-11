#!/bin/sh

#Save cwd and make sure we're in the ClassTest dir
PWD=`pwd`
cd ~/stuff/scripts/java/Intro/

#Create bytecode (*.class) files out of java code
javac *.java

#tell java to run the class "ClassTest"
java Intro

#go back to original working directory
cd $PWD

