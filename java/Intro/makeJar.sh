#!/bin/sh

#Save cwd and make sure we're in the ClassTest dir
PWD=`pwd`
cd ~/stuff/scripts/java/Intro/

#Create bytecode (*.class) files out of java code
javac *.java

#package everything into an executable jar
#  the jar can be run with `java -jar ClassTest.jar`
jar cvfm Test.jar manifest Intro.class Messenger.class

#go back to original working directory
cd $PWD

